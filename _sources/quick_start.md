# Quick start tutorial
This quick start tutorial walks through all steps required to make _DAS_ work with your data, using a recording of fly song as an example. A comprehensive documentation of all menus and options can be found in the [GUI documentation](/tutorials_gui/tutorials_gui).

In the tutorial, we will train _DAS_ using an iterative and adaptive protocol that allows to quickly create a large dataset of annotations: Annotate a few song events, fast-train a network on those annotations, and then use that network to predict new annotations on a larger part of the recording. Initial, these predictions require manually correction, but correcting is typically much faster than annotating everything from scratch. This correct-train-predict cycle is then repeated with ever larger datasets until network performance is satisfactory.

## Download example data
To follow the tutorial, download and open this [audio file](https://github.com/janclemenslab/DAS/releases/download/data/Dmel_male.wav). The recording is of a _Drosophila melanogaster_ male courting a female, recorded by David Stern (Janelia, part of [this dataset](https://www.janelia.org/lab/stern-lab/tools-reagents-data)). We will walk through loading, annotating, training and predicting using this file as an example.

## Start the GUI

Install _DAS_ following these [instructions](/install). Then start the GUI by opening a terminal, activating the conda environment created during install and typing `das gui`:
```shell
conda activate das
das gui
```

The following window should open:

:::{figure} xb_start-fig
<img src="/images/xb_start.png" alt="start screen" width=450>

Loading screen.
:::

## Load audio data

Choose _Load audio from file_ and select the downloaded recording of fly song.

In the dialog that opens, leave everything as is except set _Minimal/Maximal spectrogram frequency_---the range of frequencies in the spectrogram display---to 50 and 1000 Hz. This will restrict the spectrogram view to only show the frequencies found in fly song.

:::{figure} xb_load-fig
<img src="/images/xb_quick_load.png" alt="loading screen">

Loading screen.
:::

## Waveform and spectrogram display
Loading the audio will open a window that displays the first second of audio as a waveform (top) and a spectrogram (bottom). You will see the two major modes of fly song---pulse and sine. The recording starts with sine song---a relatively soft oscillation resulting in a spectral power at ~150Hz. Pulse song starts after ~0.75 seconds, evident as trains of brief wavelets with a regular interval.

To navigate the view: Move forward/backward along the time axis via the `A`/`D` keys and zoom in/out the time axis with the `W`/`S` keys (see also the _Playback_ menu). The temporal and frequency resolution of the spectrogram can be adjusted with the `R` and `T` keys.

You can play back the waveform on display through your headphones/speakers by pressing `E`.

:::{figure} xb_display-fig
<img src="/images/xb_quick_view.png" alt="waveform and spectrogram display" width="100%">

Waveform (top) and spectrogram (bottom) display of a single-channel recording of fly song.
:::


## Initialize or edit song types
Before you can annotate song, you need to register the sine and pulse song types for annotation. _DAS_ discriminates two principal categories of song types:
- _Events_ are defined by a single time of occurrence. The aforementioned pulse song is a song type of the event category.
- _Segments_ are song types that extend over time and are defined by a start and a stop time. The aforementioned sine song and the syllables of mouse and bird vocalizations fall into the segment category.

Add two new song types for annotation via _Annotations/Add or edit song types_: 'pulse' of category 'event' and 'sine' of category 'segment':

:::{figure} xb_make-fig
<img src="/images/xb_make.png" alt="edit annotation types" height="400px">

Create two new song types for annotation.
:::


## Create annotations manually
The two new song types "pulse" or "sine" can now be activated for annotation using the dropdown menu on the top left of the main window. The active song type can also be changed with number keys indicated in the dropdown menu---in this case `1` activates pulse, `2` activates sine.

Song is annotated by left-clicking the waveform or spectrogram view. If an event-like song type is active, a single left click marks the time of an event. A segment-like song type requires two clicks---one for each boundary of the segment.

:::{figure} xb_create-fig
<img src="/images/xb_create_opt.gif" alt="annotate song" width="700px">

Left clicks in waveform or spectrogram view create annotations.
:::

## Annotate by thresholding the waveform
Annotation of events can be sped up with a "Thresholding mode”, which detects peaks in the sound energy exceeding a threshold. Activate thresholding mode via the _Annotations_ menu. This will display a draggable horizontal line - the detection threshold - and a smooth pink waveform - the energy envelope of the waveform. Adjust the threshold so that only “correct” peaks in the envelope cross the threshold and then press `I` to annotate these peaks as events.

:::{figure} xb_thres-fig
<img src="/images/xb_thres_opt.gif" alt="annotate song" width="700px">

Annotations assisted by thresholding and peak detection.
:::

## Edit annotations
In case you mis-clicked, you can edit and delete annotations. Edit event times and segment bounds by dragging the lines or the boundaries of segments. Drag the shaded area itself to move a segment without changing its duration. Movement can be disabled completely or restricted to the currently selected annotation type via the _Audio_ menu.

Delete annotations of the active song type by right-clicking on the annotation. Annotations of all song types or only the active one in the view can be deleted with `U` and `Y`, respectively, or via the _Annotations_ menu.

:::{figure} xb_edit-fig
<img src="/images/xb_edit_opt.gif" alt="annotate song" width="700px">

Dragging moves, right click deletes annotations.
:::

## Export annotations and make a dataset
_DAS_ achieves good performance with little manual annotation. Once you have completely annotated the song in the first 18 seconds of the tutorial recording---a couple of pulse trains and sine song segments---you can train a network to help with annotating the rest of the data.

Trainining requires the audio data and the annotations to be in a specific dataset format. First, export the audio data and the annotations via `File/Export for DAS` to a new folder (not the one containing the original audio)---let's call the folder `quickstart`. In the following dialog set start seconds and end seconds to the annotated time range - 0 and 18 seconds, respectively.

:::{figure} xb_export-fig
<img src="/images/xb_quick_export.png" alt="export audio and annotations" width=450>

Export audio data and annotations for the annotated range between 0 and 18 seconds.
:::

Then make a dataset, via _DAS/Make dataset for training_. In the file dialog, select the `quickstart` folder you exported your annotations into. In the next dialog, we will adjust how data is split into training, validation and testing data. For the small data set annotated in the first step of this tutorial, we will not test the model. To maximize the data available for optimizing the network (training and validation), set the test split to 0.0 (not test) and the validation split to 40:

:::{figure} xb_assemble-fig
<img src="/images/xb_quick_make_ds.png" alt="assemble dataset" width=600>

Make a dataset for training.
:::

This will create a dataset folder called `quickstart.npy` that contains the audio data and the annotations read for training.

## Fast training
Configure a network and start training via _DAS/Train_. This will ask you select the dataset folder, `quickstart.npy`. Then, a dialog allows you to configure the network. For the fast training change the following:
- Set both `Number of filters` and `Filter duration (seconds)` to 16. This will result in a smaller network with fewer parameters, which will be faster to train and requires fewer annotations to achieve adequate performance.
- Set `Number of epochs` to 10, to finish training earlier.
:::{figure} xb_train-fig
<img src="/images/xb_quick_train.png" alt="train" width=500>

Train options
:::

Then hit `Start training in GUI` - this will start training in a background process. Monitor training progress in the terminal. Training with this small dataset will finish within fewer than 10 minutes on a CPU and within 2 minutes on a GPU. For larger datasets, we highly recommend training on a machine with a discrete Nvidia GPU.

## Predict
Once training finished, generate annotations using the trained network via _DAS/Predict_. This will ask you to select a model file containing the trained. Training creates files in the `quickstart.res` folder, starting with the time stamp of training---select the file ending in `_model.h5`.

In the next dialog, predict song for 60 seconds starting after your manual annotations:
- Set `Start seconds` to 18 and `End seconds` to 78.
- Make sure that `Proof reading mode` is enabled. That way, annotations created by the network will be assigned names ending in `_proposals` - in our case `sine_proposals` and `pulse_proposals`. The proposals will be transformed into proper `sine` and `pulse` annotations during proof reading.
- Enable `Fill gaps shorter than (seconds)` and `Delete segments shorter than (seconds)` by unchecking both check boxes.

:::{figure} xb_predict-fig
<img src="/images/xb_quick_predict.png" alt="predict" width=750>

Predict in proof-reading mode on the next 60 seconds.
:::

In contrast to training, prediction is very fast, and does not require a GPU---should finish within 30 seconds. The proposed annotations should be already good --- most pulses should be correctly detected. Sine song is harder to predict and will likely be often missed or chopped up into multiple segments with gaps in between.

## Proof reading
To turn the proposals into proper annotations, fix and approve them. Correct any prediction errors---add missing annotations, remove false positive annotations, adjust the timing of annotations. Once you have corrected all errors in the view, approve annotations with `G` or `H` for approving only the active or all song types, respectively. This will rename the proposals in the view to the original names (for instance, `sine_proposals` -> `sine`).

## Go back to "Export"
Once all proposals have been approved, export all annotations (now between 0 and 78 seconds), make a new dataset, train, predict, and repeat. If prediction performance is adequate, fully train the network, this time using a completely new recording as the test set (TODO: add option to specify a file as the test set to the "Make dataset" dialog) and with a larger number of epochs.
