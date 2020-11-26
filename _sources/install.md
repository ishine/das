# Install

## Pre-requisites


__Anaconda__: _DeepSS_ is installed using an anaconda environment. For that, you first have to [install anaconda](https://docs.anaconda.com/anaconda/install/) (or use [miniconda](https://docs.conda.io/en/latest/miniconda.html)).

__CUDA libraries for using the GPU__: While _DeepSS_ works well for annotating song using CPUs, GPUs will greatly improve annotation speed and are in particular recommended for training a _DeepSS_ network. The network is implement in the deep-learning framework Tensorflow. To make sure that Tensorflow can utilize the GPU, make sure you have the required CUDA libraries installed: [https://www.tensorflow.org/install/gpu]().

__Libsoundfile on linux__: The graphical user interface (GUI) reads audio data using [soundfile](http://pysoundfile.readthedocs.io/), which relies on `libsndfile`. `libsndfile` will be automatically installed on Windows and macOS but needs to be installed separately with: `sudo apt-get install libsndfile1`. Alternatively, _DeepSS_ can be installed and used w/o the GUI (see below).

## Install _DeepSS_ with or without the GUI
Create an anaconda environment called `deepss` that contains all the required packages, including the GUI:
```shell
conda env create -f https://raw.githubusercontent.com/janclemenslab/deepsongsegmenter/master/env/deepss_gui.yml -n dss
```

If you do not need the `xb` GUI (for instance, for training _DeepSS_ on a server), install the plain version:

```shell
conda env create -f https://raw.githubusercontent.com/janclemenslab/deepsongsegmenter/master/env/deepss_plain.yml -n dss
```

## Test the installation
To test the installation, activate the conda environment and run these three commands in the terminal:
```shell
conda activate dss
dss-train --help
dss-predict --help
dss-gui
```
The first two should display the command line arguments for `dss-train` and `dss-predict`. The last command, `dss-gui` will start the graphical user interface - this will *not* work with the plain install.

## Next steps
If all is working, train _DeepSS_ to annotate song in your own recordings. Either [annotate some song manually using the GUI](annotate) or, if you already have annotations, use them to [make a dataset for training](make_dataset) _DeepSS_.
