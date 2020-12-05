# Install

## Pre-requisites


__Anaconda__: _DeepSS_ is installed using an anaconda environment. For that, first install the [anaconda python distribution](https://docs.anaconda.com/anaconda/install/) (or [miniconda](https://docs.conda.io/en/latest/miniconda.html)).

<!-- ```shell
curl https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
sh miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
``` -->

__CUDA libraries for using the GPU__: While _DeepSS_ works well for annotating song using CPUs, GPUs will greatly improve annotation speed and are in particular recommended for training a _DeepSS_ network. The network is implement in the deep-learning framework Tensorflow. To make sure that Tensorflow can utilize the GPU, the required CUDA libraries need to be installed. See the [tensorflow docs](https://www.tensorflow.org/install/gpu) for details.

__Libsoundfile on linux__: The graphical user interface (GUI) reads audio data using [soundfile](http://pysoundfile.readthedocs.io/), which relies on `libsndfile`. `libsndfile` will be automatically installed on Windows and macOS. On Linux, the library needs to be installed manually with: `sudo apt-get install libsndfile1`. Note that _DeepSS_ will work w/o `libsndfile` but will only be able to load more unusual audio file formats.

## Install _DeepSS_ with or without the GUI
Create an anaconda environment called `deepss` that contains all the required packages, including the GUI:
```shell
conda env create -f https://raw.githubusercontent.com/janclemenslab/deepsongsegmenter/master/env/deepss_gui.yml -n dss
```

If you do not need require the graphical user interface `dss gui` (for instance, for training _DeepSS_ on a server), install the non-GUI version:
```shell
conda env create -f https://raw.githubusercontent.com/janclemenslab/deepsongsegmenter/master/env/deepss_plain.yml -n dss
```

## Test the installation
To quickly test the installation, activate the conda environment and run these two commands in the terminal:
```shell
conda activate dss
dss train --help
dss gui
```
The first one should display the command line arguments for `dss train`. The second command, `dss gui` will start the graphical user interface - this will *not* work with the non-GUI install.

## Next steps
If all is working, you can now use _DeepSS_ to annotate song. To get started, you will first need to train a network on your own data. For that you need manual annotations - either create new annotations [using the GUI](tutorials_gui) or convert existing annotations [using python scripts](tutorials).
