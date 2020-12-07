# Train
To train a network involves two steps:
- First, make a dataset from exported annotations.
- Then, configure and train a network.

## Make a dataset from exported annotations
Training expects data in a specific format in which the data is split into different parts for use during training ( and validation) and after training for evaluating network performance. For details, see [here](data_formats.html#dataset-for-training). The GUI automates the generation of these datasets from audio annotated using the GUI. Alternatively, you can also [use your existing annotations](/tutorials/convert) or [make a dataset yourself](/tutorials/make_ds_notebook).

If using the GUI, start the process of making a dataset via _DeepSS/Make dataset for training_. This will first ask you to select a data folder that contains the exported audio and annotations, and then present a dialog with options for customizing the dataset:

:::{figure} xb_assemble-fig
<img src="/images/xb_assemble.png" alt="assemble dataset" width=650>

Dialog for customizing a dataset for training.
:::

- _Data folder_ & _Store folder_: The data folder contains your exported annotations (annotations as `_annotations.csv`, audio as `npz` or `wav`). A dataset will be created from these annotations and save in the store folder. By default, the store folder is the data folder with an `.npy` appended. _Important: You can change the name of the store folder but the data folder should end in `.npy` for DeepSS to robustly recognize the dataset._
- _Make individual training targets_: By default, the dataset will contain targets for a single network that recognizes all annotated song types --- in our case sine and pulse. To train a network for specific song types, enable this option. We found that training individual networks improves performance for multi-channel audio, but not for single audio.
- _Width of events (seconds)_: Events are defined by a single time point --- to make training more robust, events should be represented by gaussian with specified width (standard deviation).
- _Gap between segments (seconds)_: To simplify post processing of segments, in particular for birdsong with its many syllable types, we found that introducing brief gaps helps with post-processing the inferred annotations.
- _Train/validation/test splits_: The data is split into three parts, which are used during different phases of training:
    - _train_: optimize the network parameters
    - _validation_: monitor network performance during training and steer training (stop early or adjust learning rate)
    - _test_: independent data to assess network performance after training. This can be omitted when training on very little data.
    - Splits can be generated using a mixture of two strategies:
        - _Split by files_: Use a fraction of files in the data folder for the specific split. The full files will be used for the split. Only works if you have multiple annotated files
        - _Split by samples_: Select a fraction of data from each file in the data folder.
    - _Recommendation_: If you have enough files, split train and validation by samples and split test by files that come from different individuals. That way your test set assesses how well the network generalizes to new individuals.If you have too few files or the specific song types do not appear in all files, split by samples.

```{note}
The dataset can be inspected using the [inspect_dataset notebook](/tutorials/inspect_dataset) if you are curious or if training fails.
```


## Train DeepSS using the GUI
Configure a network and start training via _DeepSS/Train_. This will ask you select the dataset folder ending in `.npy` that you just created. with the dataset, which song type to train the network for (will train network for all song types by default), and network and training parameters (see [DeepSS]() for details). Training can be started locally in a separate process or a script can be generated that can be execute to train elsewhere, for instance on a cluster.

:::{figure} xb_train-fig
<img src="/images/xb_train.png" alt="train" width=600>

Train options
:::

Options are grouped into three sections:

__Data set__:
- _Data folder_: Folder with the assembled annotations. Name must end in `.npy`
- _Save folder_: Folder for saving the files generated during training (network model and parameters, test results). Defaults to data folder with `.npy` replaced by `.res`.
- _Prefix for save files_: Files generated during training are named based on the time the training started (`YYYYMMDD_hhmmss`). You can add an informative prefix, for instance `pulsesine`. An underscore will be interleaved between the prefix and the timestamp. The resulting files will then start with something like `pulsesine_20201012_125534`.
- _Song type_: Select song type you want the network to recognize. Defaults to blank (all annotated song types). Will be populated with training targets if you select _Make individual training targets_ during dataset assembly.
- _Data fraction_ & _Seed_: Use a random subset of the data from the training and validation splits. The gives you reproducibility. This does not affect the test set. That way you can train a network on different subsets of your data and test on the same dataset.

__Network parameters__:
- _Downsampling frontend_: Trainable frontend initialized with STFT filters. Improves performance and speeds up training and inference for signals with high carrier frequencies relative to the amplitude or frequency modulation spectra - for instance ultrasonic vocalizations or bird song. Only works with single-channel, not with multi-channel audio.
    - _Number of filters_: Number of filters per layer in the frontend.
    - _Filter duration (samples)_: Duration of the filters in the frontend.
    - _Downsample factor_: The output of the STFT will be downsampled by that factor(only every Nth sample will be taken) before being fed into the main TCN.
- _Chunk duration (samples)_: Number of samples processed at once. Defines an upper bound to the context available to the network.
- _Number of filters_: Number of filters in each layer of the network. Vary between 16 and 32. Fewer typically decrease performance, more rarely help.
- _Filter duration (samples)_: Duration of each filter in samples. Should correspond to the duration of the lowest level song feature (e.g. the carrier if training on raw audio without a downsampling frontend).
- _Number of TCN blocks_: Number of TCN blocks in the network. Deeper networks (more TCNs) allow extracting more derived sound features. We found values between 2 and 6 blocks to work well.
- _Separable TCN blocks_: Useful only for multi-channel audio. Whether the convolutions in individual TCN blocks should be time-channel separable: Each audio channel is first filtered with a common set of filters and then the filtered channels are combined with a second set of filters. Allows sharing filters across channels - the idea is that some filtering operations should be applied to each channel equally. The first one or two TCN blocks can be set to use separable convolutions for multi-channel audio. Should be a space-separated sequence of `True` or `False` with the same length as the number of TCN blocks. For instance, a 5-block network with the first two blocks set to use separable convolutions would be: `True True False False False`.

__Training parameters__:
- _Learning rate_: Determines how by how much training parameters are updated in every step. Too small, and performance will take very long to improve, too large and performance will decrease. Depends on the network and data size. Values between 0.1 and 0.0001 typically work.
- _Reduce learning rate patience_: The learning rate can be reduced if the performance does not decrease for the specified number of epochs. We did not find this to improve or speed up training much.
- _Number of epochs_: Maximum number of training epochs. For training with the small data set used on this tutorial, 10 epochs are sufficient. For training on larger datasets leave as is. Training will stop early if the validation loss did not decrease in the last 20 epochs.
- _Create tensorboard logs_: Create tensorboard logs for monitoring training.

### Recommended configurations
- add table with optimal architectures from paper
- settings fast training
- when to use frontend

### Train from the command line
Note that the data set is portable---you can copy the folder with the data to another computer with a GPU and run training from the GUI there. If that machine cannot be used with a GUI---for instance if it's a linux server, the network configuration can be exported as a command line script and executed via a terminal. For instance:
```shell
dss train --data-dir /Users/deepss/tutorial/gui_demo.npy --save-dir /Users/deepss/tutorial/gui_demo.res --nb-hist 256 --ignore-boundaries True --nb-filters 32 --kernel-size 32 --nb-conv 3 --use-separable False False False --learning-rate 0.0001 --nb-epoch 400 --model-name tcn --no-reduce-lr  --no-tensorboard
```

The script uses the command-line interface `dss train` for training _DeepSS_---see [cli](/technical/cli)) for details. The script will likely require some edits:
- `--data-dir` needs to point to the dataset folder ending in `.npy` on the remote machine
- `--save-dir` needs to point to a valid, writable paths
- add a line to activate a specific conda environment before running `dss train`. For instance, `conda activate dss`
- activate linux modules, for instance to enable CUDA; or specify parameters for you job scheduler.

## Files generated during training
The following files will be created in the _save folder_:
- model (arch + weights in one file but sth fails to load across versions)
- params (info on data formats etc.)
- results - test results (not required for inference)

The `_model.h5` and `_params.yaml` are required for using the network for predictions and need to be copied to your local machine if you train remotely.