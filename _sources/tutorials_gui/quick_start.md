# Quick start tutorial
This quick start tutorial walks through steps required to go from audio data to automated annotations, using a recording of fly song as an example. A comprehensive documentation of all menus and options is in the [GUI documentation]().

The tutorial will demonstrate an iterative and adaptive training approach to quickly create a large dataset of annotations for training a _DeepSS_ network: Annotate a few song events, fast-train a network on those annotations, and then use that network to predict new annotations on a short stretch of recording. Given the small dataset used for training, these predictions require manually correction, but correcting is typically much faster than annotating everything from scratch. This correct-train-predict cycle is then repeated until network performance is satisfactory.

```
TODO:
- annotate dialogs with what is supposed to be changed and how
```

## Download example data
To follow the tutorial, download and open this [file](link) - it's a recording of fly song from a male _Drosophila melanogaster_ courthing a females, recorded by D. Stern (link) saved as a wav file. We will use the file as an example to walk through loading, annotating, training and predicting.

## Start the GUI

Install _DeepSS_ following these [instructions](/install). Then start the GUI by opening a terminal, activating the conda environment created during install and typing `dss-gui`:
```shell
conda activate dss
dss-gui
```

<img src="/images/xb_start.png" alt="start screen" width=450>

## Load audio data

In the window that opens, choose _Load audio from file_ and select the downloaded recording of fly song.

In the dialog that opens, leave everything as is except set _Minimal/Maximal spectrogram frequency_ - the range of frequencies in the spectrogram display - to 50 and 1000 Hz, which is the frequency range of fly song.

:::{figure} xb_load-fig
<img src="/images/xb_load.png" alt="loading screen">

Loading screen.
:::

This will open a window that displays the first seconds of audio as a waveform (top) and a spectrogram (bottom).

Navigation...


:::{figure} xb_display-fig
<img src="/images/xb_display.png" alt="waveform and spectrogram display" width="100%">

Waveform (top) and spectrogram (bottom) display of a multi-channel recording.
:::


## Initialize or edit song types
Before you can annotate song, you need to register the different song types for annotation. The example audio is a recording from a male _Drosophila melanogaster_ fly, which produces two major types of courtship song: Pulse song, which contains trains of brief pulses and sine song, containing sustained oscillations. _DeepSS_ discriminates two categories of song types:
- _Events_ are defined by a single time of occurrence. The aforementioned pulse song is a song type of the event category.
- _Segments_ are song types that extend over time and are defined by a start and a stop time. The aforementioned sine song and the syllables of mouse and bird vocalizations fall into the segment category.

Add two new song types for annotation via _Annotations/Add or edit song types_: 'pulse' of category 'event' and 'sine' of category 'segment:

:::{figure} xb_make-fig
<img src="/images/xb_make.png" alt="edit annotation types" height="500px">

Create, rename or delete song types for annotation.
:::

## Create and edit Annotations


## Export


## Make dataset
For the small data set annotated in the first step of this tutorial, we will not test the model - maximize the data available during training by setting the test split to 0.0 and the validation split to 40.

## Fast training
```
set nb_filters to 16 and kernel_size to 16 - fewer parameters work better with little data.
train for 10 epochs
will increase to bigger model and more epochs with more data.
```
For this tutorial, leave all parameters as they are - these parameters are a good starting point for your creating a good network. Training can be performed directly in the GUI in a background process. Monitor the terminal for information on training progress. Training with a small dataset on a CPU should finish after much less than 10 minutes. For larger datasets, we highly recommend training on a machine with a discrete Nvidia GPU.


## Predict

For this tutorial, predict song for 60 seconds starting after your manual annotations (18-78 seconds).
## Proof-read

Repeat the prediction->correction->training cycle for ever larger parts of the recording, to easily build a large dataset of annotations for training ever better networks.
