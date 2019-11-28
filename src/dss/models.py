"""Defines the network architectures."""
import tensorflow.keras as keras
import tensorflow.keras.layers as kl
from typing import List
from . import tcn as tcn_layer
from .kapre.time_frequency import Spectrogram
from .kapre.utils import AmplitudeToDB


model_dict = dict()


def _register_as_model(func):
    """Adds func to model_dict Dict[modelname: modelfunc]. For selecting models by string."""
    model_dict[func.__name__] = func
    return func


@_register_as_model
def cnn(nb_freq, nb_classes, nb_channels=1, nb_hist=1, nb_filters=16,
        nb_stacks=2, kernel_size=3, nb_conv=3, loss="categorical_crossentropy",
        batch_norm=False, return_sequences=False, sample_weight_mode: str = None,
        learning_rate: float = 0.0001,
        **kwignored):
    """CNN for single-frequency and multi-channel data - uses 1D convolutions.

    Args:
        nb_freq ([type]): [description]
        nb_classes ([type]): [description]
        nb_channels (int, optional): [description]. Defaults to 1.
        nb_hist (int, optional): [description]. Defaults to 1.
        nb_filters (int, optional): [description]. Defaults to 16.
        nb_stacks (int, optional): [description]. Defaults to 2.
        kernel_size (int, optional): [description]. Defaults to 3.
        nb_conv (int, optional): [description]. Defaults to 3.
        loss (str, optional): [description]. Defaults to "categorical_crossentropy".
        batch_norm (bool, optional): [description]. Defaults to False.
        return_sequences (bool, optional): [description]. Defaults to False.
        kwignored (Dict, optional): additional kw args in the param dict used for calling m(**params) to be ingonred

    Raises:
        ValueError: When trying to init model with return_sequences.
                    The cnn only does instance classificaton, not regression (sequence prediction).

    Returns:
        [type]: [description]
    """
    if return_sequences:
        raise ValueError('Cannot perform regression with CNN.')
    inp = kl.Input(shape=(nb_hist, nb_channels))
    out = inp
    for conv in range(nb_conv):
        for _ in range(nb_stacks):
            out = kl.Conv1D(nb_filters * (2 ** conv), kernel_size, padding='same', activation='relu')(out)
            out = kl.BatchNormalization()(out) if batch_norm else out
        out = kl.MaxPooling1D(min(int(out.shape[1]), 2))(out)

    out = kl.Flatten()(out)
    out = kl.Dense(nb_classes * 4, activation='relu')(out)
    out = kl.Dense(nb_classes * 2, activation='relu')(out)
    out = kl.Dense(nb_classes, activation='relu')(out)
    out = kl.Activation("softmax")(out)

    model = keras.models.Model(inp, out, name='FCN')
    model.compile(optimizer=keras.optimizers.Adam(lr=learning_rate, amsgrad=True),
                  loss=loss, sample_weight_mode=sample_weight_mode)
    return model


@_register_as_model
def cnn2D(nb_freq, nb_classes, nb_channels=1, nb_hist=1, nb_filters=16,
          nb_stacks=2, kernel_size=3, nb_conv=3, loss="categorical_crossentropy",
          batch_norm=False, return_sequences=False, sample_weight_mode: str = None,
          learning_rate: float = 0.0001,
          **kwignored):
    """CNN for multi-frequency and multi-channel data - uses 2D convolutions.

    Args:
        nb_freq ([type]): [description]
        nb_classes ([type]): [description]
        nb_channels (int, optional): [description]. Defaults to 1.
        nb_hist (int, optional): [description]. Defaults to 1.
        nb_filters (int, optional): [description]. Defaults to 16.
        nb_stacks (int, optional): [description]. Defaults to 2.
        kernel_size (int, optional): [description]. Defaults to 3.
        nb_conv (int, optional): [description]. Defaults to 3.
        loss (str, optional): [description]. Defaults to "categorical_crossentropy".
        batch_norm (bool, optional): [description]. Defaults to False.
        return_sequences (bool, optional): [description]. Defaults to False.
        kwignored (Dict, optional): additional kw args in the param dict used for calling m(**params) to be ingonred

    Raises:
        ValueError: When trying to init model with return_sequences.
                    The cnn only does instance classificaton, not regression (sequence prediction).

    Returns:
        [type]: [description]
    """
    inp = kl.Input(shape=(nb_hist, nb_freq, nb_channels))
    out = inp
    for conv in range(nb_conv):
        for stack in range(nb_stacks):
            out = kl.Conv2D(nb_filters * (2 ** conv), (max(1, int(out.shape[1])), kernel_size), padding='same', activation='relu')(out)
            out = kl.BatchNormalization()(out) if batch_norm else out

        out = kl.MaxPooling2D((min(int(out.shape[1]), 2), 2))(out)
    out = kl.Flatten()(out)
    out = kl.Dense(int(nb_classes * 8 * nb_filters), activation='relu')(out)
    out = kl.Dropout(0.1)(out)
    out = kl.Dense(int(nb_classes * 4 * nb_filters), activation='relu')(out)
    out = kl.Dropout(0.1)(out)
    out = kl.Dense(int(nb_classes * 2 * nb_filters), activation='relu')(out)
    out = kl.Dropout(0.1)(out)
    out = kl.Dense(nb_classes, activation='relu')(out)
    out = kl.Activation("softmax")(out)

    model = keras.models.Model(inp, out, name='CNN2D')
    model.compile(optimizer=keras.optimizers.Adam(lr=learning_rate, amsgrad=True),
                  loss=loss, sample_weight_mode=sample_weight_mode)
    return model


@_register_as_model
def fcn(nb_freq, nb_classes, nb_channels=1, nb_hist=1, nb_filters=16,
        nb_stacks=2, kernel_size=3, nb_conv=3, loss="categorical_crossentropy",
        batch_norm=False, return_sequences=True, sample_weight_mode: str = None,
        learning_rate: float = 0.0001,
        **kwignored):
    """[summary]

    Args:
        nb_freq ([type]): [description]
        nb_classes ([type]): [description]
        nb_channels (int, optional): [description]. Defaults to 1.
        nb_hist (int, optional): [description]. Defaults to 1.
        nb_filters (int, optional): [description]. Defaults to 16.
        nb_stacks (int, optional): [description]. Defaults to 2.
        kernel_size (int, optional): [description]. Defaults to 3.
        nb_conv (int, optional): [description]. Defaults to 3.
        loss (str, optional): [description]. Defaults to "categorical_crossentropy".
        batch_norm (bool, optional): [description]. Defaults to False.
        return_sequences (bool, optional): [description]. Defaults to True.
        kwignored (Dict, optional): additional kw args in the param dict used for calling m(**params) to be ingonred

    Returns:
        [type]: [description]
    """
    inp = kl.Input(shape=(nb_hist, nb_channels))
    out = inp
    for conv in range(nb_conv):
        for _ in range(nb_stacks):
            out = kl.Conv1D(nb_filters * (2 ** conv), kernel_size,
                            padding='same', activation='relu')(out)
            out = kl.BatchNormalization()(out) if batch_norm else out
        out = kl.MaxPooling1D(min(int(out.shape[1]), 2))(out)

    for conv in range(nb_conv, 0, -1):
        out = kl.UpSampling1D(size=2)(out)
        out = kl.Conv1D(nb_filters * (2 ** conv), kernel_size,
                        padding='same', activation='relu')(out)

    if not return_sequences:
        out = kl.Flatten()(out)
    out = kl.Dense(nb_classes)(out)
    out = kl.Activation("softmax")(out)

    model = keras.models.Model(inp, out, name='FCN')
    model.compile(optimizer=keras.optimizers.Adam(lr=learning_rate, amsgrad=True),
                  loss=loss, sample_weight_mode=sample_weight_mode)
    return model


@_register_as_model
def fcn2D(nb_freq, nb_classes, nb_channels=1, nb_hist=1, nb_filters=16,
          nb_stacks=2, kernel_size=3, nb_conv=3, loss="categorical_crossentropy",
          batch_norm=False, return_sequences=True, sample_weight_mode: str = None,
          learning_rate: float = 0.0005,
          **kwignored):
    """[summary]

    Args:
        nb_freq ([type]): [description]
        nb_classes ([type]): [description]
        nb_channels (int, optional): [description]. Defaults to 1.
        nb_hist (int, optional): [description]. Defaults to 1.
        nb_filters (int, optional): [description]. Defaults to 16.
        nb_stacks (int, optional): [description]. Defaults to 2.
        kernel_size (int, optional): [description]. Defaults to 3.
        nb_conv (int, optional): [description]. Defaults to 3.
        loss (str, optional): [description]. Defaults to "categorical_crossentropy".
        batch_norm (bool, optional): [description]. Defaults to False.
        return_sequences (bool, optional): [description]. Defaults to True.
        kwignored (Dict, optional): additional kw args in the param dict used for calling m(**params) to be ingonred

    Returns:
        [type]: [description]
    """
    inp = kl.Input(shape=(nb_hist, nb_freq, nb_channels))
    out = inp
    for conv in range(nb_conv):
        for stack in range(nb_stacks):
            out = kl.Conv2D(nb_filters * (2 ** conv), (max(1, int(out.shape[1])), kernel_size), padding='same', activation='relu')(out)
            out = kl.BatchNormalization()(out) if batch_norm else out
        out = kl.MaxPooling2D((min(int(out.shape[1]), 2), 2))(out)
    for conv in range(nb_conv, 0, -1):
        out = kl.Conv2D(int(nb_filters * (conv / 2)), (max(1, int(out.shape[1])), kernel_size), padding='same', activation='relu')(out)
        out = kl.BatchNormalization()(out) if batch_norm else out

    out = kl.Flatten()(out)
    out = kl.Dense(nb_classes, activation='relu')(out)
    out = kl.Activation("softmax")(out)

    model = keras.models.Model(inp, out, name='CNN')
    model.compile(optimizer=keras.optimizers.Adam(lr=learning_rate, amsgrad=True), loss=loss)
    return model


@_register_as_model
def tcn_seq(nb_freq: int, nb_classes: int, nb_hist: int = 1, nb_filters: int = 16, kernel_size: int = 3,
            nb_conv: int = 1, loss: str = "categorical_crossentropy",
            dilations: List[int] = [1, 2, 4, 8, 16], activation: str = 'norm_relu',
            use_skip_connections: bool = True, return_sequences: bool = True,
            dropout_rate: float = 0.00, padding: str = 'same', sample_weight_mode: str = None,
            nb_pre_conv: int = 0, learning_rate: float = 0.0001,
            **kwignored):
    """Create TCN network.

    Args:
        nb_freq (int): [description]
        nb_classes (int): [description]
        nb_hist (int, optional): [description]. Defaults to 1.
        nb_filters (int, optional): [description]. Defaults to 16.
        kernel_size (int, optional): [description]. Defaults to 3.
        nb_conv (int, optional): [description]. Defaults to 1.
        loss (str, optional): [description]. Defaults to "categorical_crossentropy".
        dilations (List[int], optional): [description]. Defaults to [1, 2, 4, 8, 16].
        activation (str, optional): [description]. Defaults to 'norm_relu'.
        use_skip_connections (bool, optional): [description]. Defaults to True.
        return_sequences (bool, optional): [description]. Defaults to True.
        dropout_rate (float, optional): [description]. Defaults to 0.00.
        padding (str, optional): [description]. Defaults to 'same'.
        nb_pre_conv (int, optional): number of conv-relu-batchnorm-maxpool2 blocks before the TCN - useful for reducing the sample rate. Defaults to 0
        kwignored (Dict, optional): additional kw args in the param dict used for calling m(**params) to be ingonred

    Returns:
        [keras.models.Model]: Compiled TCN network model.
    """
    input_layer = kl.Input(shape=(nb_hist, nb_freq))
    out = input_layer
    for conv in range(nb_pre_conv):
        out = kl.Conv1D(nb_filters * (2 ** conv), kernel_size, padding='same', activation='relu')(out)
        out = kl.BatchNormalization()(out)
        out = kl.MaxPooling1D(min(int(out.shape[1]), 2))(out)

    x = tcn_layer.TCN(nb_filters=nb_filters, kernel_size=kernel_size, nb_stacks=nb_conv, dilations=dilations, activation=activation,
                      use_skip_connections=use_skip_connections, padding=padding, dropout_rate=dropout_rate, return_sequences=return_sequences)(out)
    x = kl.Dense(nb_classes)(x)
    x = kl.Activation('softmax')(x)
    if nb_pre_conv > 0:
        x = kl.UpSampling1D(size=2**nb_pre_conv)(x)
    output_layer = x
    model = keras.models.Model(input_layer, output_layer, name='TCN')
    model.compile(optimizer=keras.optimizers.Adam(lr=learning_rate, amsgrad=True, clipnorm=1.),
                  loss=loss, sample_weight_mode=sample_weight_mode)
    return model


@_register_as_model
def tcn(*args, **kwargs):
    """Synonym for tcn_seq."""
    return tcn_seq(*args, **kwargs)


@_register_as_model
def tcn_tcn(nb_freq: int, nb_classes: int, nb_hist: int = 1, nb_filters: int = 16, kernel_size: int = 3,
            nb_conv: int = 1, loss: str = "categorical_crossentropy",
            dilations: List[int] = [1, 2, 4, 8, 16], activation: str = 'norm_relu',
            use_skip_connections: bool = True, return_sequences: bool = True,
            dropout_rate: float = 0.00, padding: str = 'same', sample_weight_mode: str = None,
            nb_pre_conv: int = 0, learning_rate: float = 0.0005, upsample: bool = True,
            **kwignored):
    """Create TCN network with TCN layer as pre-processing and downsampling frontend.

    Args:
        nb_freq (int): [description]
        nb_classes (int): [description]
        nb_hist (int, optional): [description]. Defaults to 1.
        nb_filters (int, optional): [description]. Defaults to 16.
        kernel_size (int, optional): [description]. Defaults to 3.
        nb_conv (int, optional): [description]. Defaults to 1.
        loss (str, optional): [description]. Defaults to "categorical_crossentropy".
        dilations (List[int], optional): [description]. Defaults to [1, 2, 4, 8, 16].
        activation (str, optional): [description]. Defaults to 'norm_relu'.
        use_skip_connections (bool, optional): [description]. Defaults to True.
        return_sequences (bool, optional): [description]. Defaults to True.
        dropout_rate (float, optional): [description]. Defaults to 0.00.
        padding (str, optional): [description]. Defaults to 'same'.
        nb_pre_conv (int, optional): If >0 adds a single TCN layer with a final maxpooling layer
                                     with block size of `2**nb_pre_conv` before the TCN.
                                     Useful for speeding up training by reducing the sample rate early in the network.
                                     Defaults to 0 (no downsampling)
        learning_rate (float, optional) Defaults to 0.0005
        upsample (bool, optional): whether or not to restore the model output to the input samplerate.
                                   Should generally be True during training and evaluation but my speed up inference .
                                   Defaults to True.
        kwignored (Dict, optional): additional kw args in the param dict used for calling m(**params) to be ingonred

    Returns:
        [keras.models.Model]: Compiled TCN network model.
    """
    input_layer = kl.Input(shape=(nb_hist, nb_freq))
    out = input_layer
    if nb_pre_conv > 0:
        out = tcn_layer.TCN(nb_filters=nb_filters, kernel_size=kernel_size, nb_stacks=nb_pre_conv, dilations=dilations,
                            activation=activation, use_skip_connections=use_skip_connections, padding=padding,
                            dropout_rate=dropout_rate, return_sequences=return_sequences, name='frontend')(out)
        out = kl.MaxPooling1D(pool_size=2**nb_pre_conv, strides=2**nb_pre_conv)(out)  # or avg pooling?

    x = tcn_layer.TCN(nb_filters=nb_filters, kernel_size=kernel_size, nb_stacks=nb_conv, dilations=dilations,
                      activation=activation, use_skip_connections=use_skip_connections, padding=padding,
                      dropout_rate=dropout_rate, return_sequences=return_sequences)(out)
    x = kl.Dense(nb_classes)(x)
    x = kl.Activation('softmax')(x)
    if nb_pre_conv > 0 and upsample:
        x = kl.UpSampling1D(size=2**nb_pre_conv)(x)
    output_layer = x
    model = keras.models.Model(input_layer, output_layer, name='TCN')
    model.compile(optimizer=keras.optimizers.Adam(lr=learning_rate, amsgrad=True, clipnorm=1.),
                  loss=loss, sample_weight_mode=sample_weight_mode)
    return model


@_register_as_model
def tcn_stft(nb_freq: int, nb_classes: int, nb_hist: int = 1, nb_filters: int = 16, kernel_size: int = 3,
             nb_conv: int = 1, loss: str = "categorical_crossentropy",
             dilations: List[int] = [1, 2, 4, 8, 16], activation: str = 'norm_relu',
             use_skip_connections: bool = True, return_sequences: bool = True,
             dropout_rate: float = 0.00, padding: str = 'same', sample_weight_mode: str = None,
             nb_pre_conv: int = 0, learning_rate: float = 0.0005, upsample: bool = True,
             **kwignored):
    """Create TCN network with trainable STFT layer as pre-processing and downsampling frontend.

    Args:
        nb_freq (int): [description]
        nb_classes (int): [description]
        nb_hist (int, optional): [description]. Defaults to 1.
        nb_filters (int, optional): [description]. Defaults to 16.
        kernel_size (int, optional): [description]. Defaults to 3.
        nb_conv (int, optional): [description]. Defaults to 1.
        loss (str, optional): [description]. Defaults to "categorical_crossentropy".
        dilations (List[int], optional): [description]. Defaults to [1, 2, 4, 8, 16].
        activation (str, optional): [description]. Defaults to 'norm_relu'.
        use_skip_connections (bool, optional): [description]. Defaults to True.
        return_sequences (bool, optional): [description]. Defaults to True.
        dropout_rate (float, optional): [description]. Defaults to 0.00.
        padding (str, optional): [description]. Defaults to 'same'.
        nb_pre_conv (int, optional): If >0 adds a single STFT layer with a hop size of 2**nb_pre_conv before the TCN.
                                     Useful for speeding up training by reducing the sample rate early in the network.
                                     Defaults to 0 (no downsampling)
        learning_rate (float, optional) Defaults to 0.0005
        upsample (bool, optional): whether or not to restore the model output to the input samplerate.
                                   Should generally be True during training and evaluation but my speed up inference.
                                   Defaults to True.
        kwignored (Dict, optional): additional kw args in the param dict used for calling m(**params) to be ingonred

    Returns:
        [keras.models.Model]: Compiled TCN network model.
    """
    if nb_freq > 1:
        raise ValueError(f'This model only works with single channel data but last dim of inputs has len {nb_freq} (should be 1).')
    input_layer = kl.Input(shape=(nb_hist, nb_freq))
    out = input_layer
    if nb_pre_conv > 0:
        out = Spectrogram(n_dft=64, n_hop=2**nb_pre_conv,
                          return_decibel_spectrogram=True, power_spectrogram=1.0,
                          trainable_kernel=True, name='trainable_stft', image_data_format='channels_last')(out)
        # out = AmplitudeToDB()(out)
        out = kl.Reshape((out.shape[1], out.shape[2] * out.shape[3]))(out)

    x = tcn_layer.TCN(nb_filters=nb_filters, kernel_size=kernel_size, nb_stacks=nb_conv, dilations=dilations,
                      activation=activation, use_skip_connections=use_skip_connections, padding=padding,
                      dropout_rate=dropout_rate, return_sequences=return_sequences)(out)
    x = kl.Dense(nb_classes)(x)
    x = kl.Activation('softmax')(x)
    if nb_pre_conv > 0 and uspample:
        x = kl.UpSampling1D(size=2**nb_pre_conv)(x)
    output_layer = x
    model = keras.models.Model(input_layer, output_layer, name='TCN')
    model.compile(optimizer=keras.optimizers.Adam(lr=learning_rate, amsgrad=True, clipnorm=1.),
                  loss=loss, sample_weight_mode=sample_weight_mode)
    return model
