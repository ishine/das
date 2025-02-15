"""General utilities"""
import tensorflow.keras as keras
import logging
import time
import numpy as np
import yaml
import h5py
from . import kapre
from . import tcn
from . import models
from typing import Dict, Callable, Any, List, Tuple


class LossHistory(keras.callbacks.Callback):
    """[summary]

    Args:
        keras ([type]): [description]
    """

    def __init__(self):
        self.min_loss = np.inf

    def on_train_begin(self, logs):
        logging.info('training started')

    def on_epoch_begin(self, epoch, logs):
        self.t0 = time.time()

    def on_epoch_end(self, epoch, logs):
        duration = time.time() - self.t0
        current_loss = logs.get('val_loss')
        current_train_loss = logs.get('loss')
        self.min_loss = np.min((current_loss, self.min_loss))
        logging.info('ep{0:>5d} ({1:1.4f} seconds): train_loss={4:1.5f} val_loss= {2:1.5f}/{3:1.5f} (current/min)'.format(epoch, duration, current_loss, self.min_loss, current_train_loss))

    def on_training_end(self, logs):
        logging.info('trained ended')


def load_model(file_trunk: str, model_dict: Dict[str, Callable],
               model_ext: str = '_model.h5',
               params_ext: str = '_params.yaml',
               compile: bool = True):
    """Load model with weights.

    First tries to load the full model directly using keras.models.load_model - this will likely fail for models with custom layers.
    Second, try to init model from parameters and then add weights...

    Args:
        file_trunk (str): [description]
        model_dict (Dict[str, Callable): [description]
        model_ext (str, optional): [description]. Defaults to '_weights.h5'.
        params_ext (str, optional): [description]. Defaults to '_params.yaml'.
        compile (bool, optional): [description]. Defaults to True.

    Returns:
        keras.Model
    """

    try:
        model_filename = _download_if_url(file_trunk + model_ext)
        model = keras.models.load_model(model_filename,
                                        custom_objects={'Spectrogram': kapre.time_frequency.Spectrogram,
                                                        'TCN': tcn.tcn_new.TCN})
    except (SystemError, ValueError, AttributeError):
        logging.debug('Failed to load model using keras, likely because it contains custom layers. Will try to init model architecture from code and load weights from `_model.h5` into it.', exc_info=False)
        logging.debug('', exc_info=True)
        model = load_model_from_params(file_trunk, model_dict, weights_ext=model_ext, params_ext=params_ext, compile=compile)
    return model


def load_model_from_params(file_trunk: str, model_dict: Dict[str, Callable],
                           weights_ext: str = '_model.h5',
                           params_ext: str = '_params.yaml',
                           compile: bool = True):
    """Init architecture from code and load model weights into it. Helps with model loading issues across TF versions.

    Args:
        file_trunk (str): [description]
        models_dict ([type]): [description]
        weights_ext (str, optional): [description]. Defaults to '_model.h5' (use weights from model file).
        params_ext (str, optional): [description]. Defaults to '_params.yaml'.
        compile (bool, optional): [description]. Defaults to True.

    Returns:
        keras.Model
    """
    params = load_params(file_trunk, params_ext=params_ext)

    model = model_dict[params['model_name']](**params)  # get the model - calls the function that generates a model with parameters
    weights_filename = _download_if_url(file_trunk + weights_ext)
    model.load_weights(weights_filename)

    if compile:
        # Compile with random standard optimizer and loss so we can use the model for prediction
        # Just re-compile the model if you want a particular optimizer and loss.
        model.compile(optimizer=keras.optimizers.Adam(amsgrad=True),
                      loss="mean_squared_error")
    return model


def save_params(params: Dict[str, Any], file_trunk: str, params_ext: str = '_params.yaml'):
    """Save model/training parameters to yaml.

    Args:
        params (Dict[str]): [description]
        file_trunk (str): [description]
        params_ext (str, optional): [description]. Defaults to '_params.yaml'.
    """
    with open(file_trunk + params_ext, 'w') as f:
        yaml.dump(params, f)


def load_params(file_trunk: str,
                params_ext: str = '_params.yaml') -> Dict[str, Any]:
    """Load model/training parameters from yaml

    Args:
        file_trunk (str): [description]
        params_ext (strs, optional): [description]. Defaults to '_params.yaml'.

    Returns:
        Dict[str, Any]: Parameter dictionary
    """
    filename = _download_if_url(file_trunk + params_ext)
    with open(filename, 'r') as f:
        try:
            params = yaml.load(f, Loader=yaml.FullLoader)
        except AttributeError:
            params = yaml.load(f)
    return params


def load_model_and_params(model_save_name, model_dict=models.model_dict) -> Tuple[keras.Model, Dict[str, Any]]:
    """[summary]

    Args:
        model_save_name ([type]): [description]
        model_dict ([type], optional): [description]. Defaults to models.model_dict.

    Returns:
        keras.Model, Dict[str, Any]: [description]
    """
    params = load_params(model_save_name)
    model = load_model(model_save_name, model_dict)
    return model, params


def _download_if_url(url: str):
    if not url.startswith('http'):
        return url
    else:
        import urllib.request
        import tempfile
        from pathlib import Path
        filename = url.split('/')[-1]  # get filename
        tmpdir = tempfile.mkdtemp()
        local_path = Path(tmpdir) / filename
        urllib.request.urlretrieve(url, local_path)
        return local_path


def load_from(filename: str, datasets: List[str]):
    """Load datasets from h5 file.

    Args:
        filename (str)
        datasets (List[str]): Names of the datasets (=keys) to load

    Returns:
        [type]: [description]
    """
    data = dict()
    with h5py.File(filename, 'r') as f:
        data = {dataset: f[dataset][:] for dataset in datasets}
    return data


class Timer:

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.start = None
        self.end = None
        self.elapsed = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start
        if self.verbose:
            print(self)

    def __str__(self):
        if self.start is None:
            s = "Timer not started yet."
        elif self.end is None:
            s = "Timer still running."
        elif self.elapsed is not None:
            s = f'Time elapsed {self.elapsed:1.2f} seconds.'
        else:
            s = "Timer in unexpected state."
        return s


class QtProgressCallback(keras.callbacks.Callback):

    def __init__(self, nb_epochs, comms):
        """Init the callback.

        Args:
            nb_epochs ([type]): number of training epochs
            comms (tuple): tuple of (multiprocessing.Queue, threading.Event)
                The queue is used to transmit progress updates to the GUI,
                the event is set in the GUI to stop training.
        """
        super().__init__()
        self.nb_epochs = nb_epochs
        self.queue = comms[0]
        self.stop_event = comms[1]

    def _check_if_stopped(self):
        try:
            if self.stop_event.is_set():
                self.model.stop_training = True
        except Exception as e:
            print(e)

    def on_train_begin(self, logs=None):
        self.queue.put((0, "Starting training."))

    def on_train_end(self, logs=None):
        self.queue.put((-1, "Finishing training."))

    def on_epoch_end(self, epoch, logs=None):
        self.queue.put((epoch, f"Epoch {epoch}/{self.nb_epochs}"))

    def on_train_batch_end(self, batch, logs=None):
        self._check_if_stopped()

    def on_test_batch_end(self, batch, logs=None):
        self._check_if_stopped()

    def on_predict_batch_end(self, batch, logs=None):
        self._check_if_stopped()