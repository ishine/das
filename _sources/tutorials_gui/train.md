# Train
To train a network, you need to make a dataset from exported annotations and configure and train a network.


## Assemble exported annotations
Training expects data in a specific format with splits and metadata (see [specification](data_formats.html#dataset-for-training)). The GUI automates the generation of these datasets from audio annotated using the GUI. You can also do it yourself (see notebook tutorial) but also present sample code for using your own data formats.

Select the folder with the exported audio and annotations via `DeepSS/Make dataset for training`. This will open a

:::{figure} xb_assemble-fig
<img src="/images/xb_assemble.png" alt="assemble dataset" width=650>

Make dataset options
:::

- _Data folder_ & _Store folder_: The data folder contains your exported annotations. A dataset will be created from these annotations and save in the store folder. By default, the store folder is the data folder with an `.npy` appended. _Important: You can change the name of the store folder but the `.npy` should be kept for DeepSS to robustly recognize the dataset._
- _Make individual training targets_: By default, the dataset will contain targets for a single network that recognizes all annotated song types --- in our case sine and pulse. To train a network for specific song types, enable this option. In our example, this will create additional separate targets for training a network to connect pulse song or sine song only. We found that training individual networks improves performance for multi-channel audio, but not for single audio.
- _Width of events (seconds)_: Events are defined by a single time point --- to make training more robust, events should be represented by gaussian with specified width (standard deviation).
- _Gap between segments (seconds)_: To simplify post processing of segments, in particular for birdsong with its many syllable types, we found that introducing brief gaps helps with post-processing the inferred annotations.
- _Train/validation/test splits_: The data is split into three parts, which are used during different phases of training:
    - _train_: optimize the network parameters
    - _validation_: monitor network performance during training and steer training (stop early or adjust learning rate)
    - _test_: independent data to assess network performance after training. This can be omitted when training on very little data.
    - Splits can be generated using a mixture of two strategies:
        - _Split by files_: Use a fraction of files in the data folder for the specific split. The full files will be used for the split. Only works if you have multiple annotated files
        - _Split by samples_: Select a fraction of data from each file in the data folder.
    - _Recommendation_: If you have enough files, split train and validation by samples and split test by files that come from different individuals. That way your test set assesses how well the network generalizes to new individuals.If you have too few files or the specific song types do not appear in all files, split by samples. For the sake of this tutorial, we will not test the model - so set the test split to 0.0.

Once the dataset is assembled, you can inspect the dataset with the [1_inspect_data.ipynb]() notebook if you are curious or if training fails.

## Train DeepSS using the GUI
Configure a network and start training via _DeepSS/Train_. This will ask you select the dataset folder ending in `.npy` that you just created. with the dataset, which song type to train the network for (will train network for all song types by default), and network and training parameters (see [DeepSS]() for details). Training can be started locally in a separate process or a script can be generated that can be execute to train elsewhere, for instance on a cluster.

edit script to fix paths, add cluster config commands or activate conda env.

:::{figure} xb_train-fig
<img src="/images/xb_train.png" alt="train" width=600>

Train options
:::

Options are grouped into three sections:

### Data set
- _Data folder_: Folder with the assembled annotations. Name must end in `.npy`
- _Save folder_: Folder for saving the files generated during training (network model and parameters, test results). Defaults to data folder with `.npy` replaced by `.res`.
- _Prefix for save files_: Files generated during training are named based on the time the training started (`YYYYMMDD_hhmmss`). You can add an informative prefix, for instance `pulsesine`. An underscore will be interleaved between the prefix and the timestamp. The resulting files will then start with something like `pulsesine_20201012_125534`.
- _Song type_: Select song type you want the network to recognize. Defaults to blank (all annotated song types). Will be populated with training targets if you select _Make individual training targets_ during dataset assembly.
- _Data fraction_ & _Seed_: Use a random subset of the data from the training and validation splits. The gives you reproducibility. This does not affect the test set. That way you can train a network on different subsets of your data and test on the same dataset.

### Network parameters
- _Downsampling frontend_: Does not work with multi-channel audio.
    - _Frontend type_: stft (short term Fourier transform) or TCN (REMOVE OPTION AND FIX TO STFT)
    - _Number of filters_: per layer
    - _Filter duration (samples)_:
    - _Downsample factor_:
- _Chunk duration (samples)_:
- _Number of filters_: Number of filters in each layer of the network. Vary between 16 and 32. Fewer typically decrease performance, more rarely help.
- _Filter duration (samples)_: Duration of each filter in samples. Should correspond to the duration of the lowest level song feature (e.g. the carrier if training on raw audio without a downsampling frontend).
- _Number of TCN blocks_: Number of TCN blocks in the network. Deeper networks (more TCNs) allow extracting more derived sound features. We found values between 2 and 6 blocks to work well.
- _Separable TCN blocks_: Useful only for multi-channel audio. Whether the convolutions in individual TCN blocks should be time-channel separable: Each audio channel is first filtered with a common set of filters and then the filtered channels are combined with a second set of filters. Allows sharing filters across channels - the idea is that some filtering operations should be applied to each channel equally. The first one or two TCN blocks can be set to use separable convolutions for multi-channel audio. Should be a space-separate sequence, the same length as the number of TCN blocks, with either `True` or `False`. For instance, a 5-block network with the first two blocks set to separable would be: `True True False False False`.


### Training parameters
- _Learning rate_: Determines how by how much training parameters are updated in every step. Too small, and performance will take very long to improve, too large and performance will decrease. Depends on the network and data size. Values between 0.1 and 0.0001 typically work.
- _Reduce learning rate patience_: The learning rate can be reduced if the performance does not decrease for the specified number of epochs. We did not find this to improve or speed up training much.
- _Number of epochs_: Maximum number of training epochs. For training with the small data set used on this tutorial, 10 epochs are sufficient. For training on larger datasets leave as is. Training will stop early if the validation loss did not decrease in the last 20 epochs.
- _Create tensorboard logs_: Ignore.

## Train
For this tutorial, leave all parameters as they are - these parameters are a good starting point for your creating a good network. Training can be performed directly in the GUI in a background process. Monitor the terminal for information on training progress. We highly recommend training on a machine with a discrete Nvidia GPU.

Note that the data set is portable---you can copy the folder with the data to another computer with a GPU and run training from the GUI there. If that machine cannot be used with a GUI---for instance if it's a linux server, the network configuration can be exported as a command line script and executed via a terminal. For instance:
```shell
python3 -m dss.train --data-dir /Users/deepss/tutorial/gui_demo.npy --save-dir /Users/deepss/tutorial/gui_demo.res --nb-hist 256 --ignore-boundaries True --nb-filters 32 --kernel-size 32 --nb-conv 3 --use-separable False False False --learning-rate 0.0001 --nb-epoch 400 --model-name tcn --no-reduce-lr  --no-tensorboard
```
The script uses the command-line interface `dss-train` for training _DeepSS_---see [cli](/technical/cli)) for details. The script will likely require some edits:
- `--data-dir` needs to point to the dataset folder ending in `.npy` on the remote machine
- `--save-dir` needs to point to a valid, writable paths
- add a line to activate a specific conda environment before running `dss-train`. For instance, `conda activate dss-server`
- activate linux modules, for instance to enable CUDA; or specify parameters for you job scheduler.

## Files generated during training
The following files will be created in the _save folder_:
- model (arch + weights in one file but sth fails to load across versions)
- params (info on data formats etc.)
- results - test results (not required for inference)

The `_model.h5` and `_params.yaml` are required for using the network for predictions and need to be copied to you local machine if you train remotely.