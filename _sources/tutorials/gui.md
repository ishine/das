<!-- ### TODO
- update screenshots
- annotate screenshots
- Fig. 4 - screenshot with open pulldown in display and zoomed overlay
- split page into subpages under a top-level `GUI Tutorial` item in the sidebar? -->

# GUI Tutorial

Install _DeepSS_ following these [instructions](/install). Then start the GUI by opening a terminal, activating the conda environment created during install and typing `dss-gui`:
```shell
conda activate dss
dss-gui
```

In the window that opens, choose _Load audio from file_ to open your audio data:

<img src="/images/xb_start.png" alt="start screen" width=450>


## Loading audio data
This will open a dialog for selecting a file. Currently, the GUI can load audio data from a wide range of file types:

- audio files (readable by [soundfile](http://pysoundfile.readthedocs.io/), [list of supported formats](http://www.mega-nerd.com/libsndfile/#Features))
- hdfs files ([h5py](http://docs.h5py.org/)). Matlab's `.mat` [files](https://www.mathworks.com/help/matlab/ref/save.html#btox10b-1-version) also use this format.
- numpy's `npy` or `npz` files ([numpy](https://numpy.org/doc/stable/reference/routines.io.html))

```{note}
If your favorite format is not included in this list, try to convert it to a `wav` file.
```
After selecting a file, a menu allows you to adjust things before loading:

:::{figure} xb_load-fig
<img src="/images/xb_load.png" alt="loading screen">

Loading screen.
:::

- _Dataset with audio_: Select the variable in the `npz`, `mat` or `h5` file that contains the audio data. For audio (e.g. wav) and `npy` files, this field will be empty since they do not contain multiple datasets.
- _Data format_: The format for loading the file is inferred automatically but can be overridden here.
- _Audio sample rate_: The audio sample rate is obtained from the file for audio files, and from the `samplerate` variable of `npz` files (see [data formats](/technical/data_formats)). Enter the correct sample rate for formats lack that information.
- ignore_tracks (REMOVE)
- crop width and height (REMOVE)
- _File with annotations_: Load existing annotations from a `csv` file. See [here](/technical/data_formats) for a description of the expected content of that file. Will default to the name of the audio data file with the extension replaced by `csv`. You can select an alternative via the _Select file ..._ button. Will ignore the file if it does not exist or is malformed.
- _Initialize annotations_: Initialize the song types you want to annotate. “name,category;name2,category2” (category is either event or segment). After loading, you can add, delete, and rename song types via the _Audio/Add or edit annotation types_ menu.
- Sample rate events (REMOVE)
- _Minimal/Maximal spectrogram frequency_: Focus the range of frequencies in the spectrogram display on the frequencies that occur in the song you want to annotate. For instance, for fly song, we typically choose 50-1000Hz. If checking `None`, will default to the between 0 and half the audio sample rate.
- _Band-pass filter audio_: To remove noise at high or low frequencies, specify the lower and upper frequency of the pass-band. Filtering will take a while for long, multi-channel audio. Caution: If you train a network using filtered data, you need to apply the same filter to all recordings you want to apply the network to.
- Load cue points (REMOVE)

```{note}
Most of these parameters are also exposed via the command-line when starting the GUI. See [xb_cli] for details.
```

## Overview over the display and menus
Audio data from all channels (gray), with one channel being selected (white), and the spectogram of the currently selected channel below. Move forward/backward along the time axis via the `A`/`D` keys and zoom in/out the time axis with the `W`/`S` keys (See Playback/). The temporal resolution of the spectrogram can be increased at the expense of frequency resolution with the `R` and `T` keys.


:::{figure} xb_display-fig
<img src="/images/xb_display.png" alt="waveform and spectrogram display" width="100%">

Waveform (top) and spectrogram (bottom) display of a multi-channel recording.
:::

Hide the non-selected channels in the waveform view by toggling _Audio/Show all channels_. To change the channel for which the spectrogram is displayed, use the dropdown list on the upper right or switch to next/previous channel with the up/down arrow keys. The `Q` key (or _Audio/Autoselect loudest channel_) will toggle automatically selecting the loudest channel in the current view.

To listen to the waveform on display press `E`.


## Annotate song
Song types for annotation are taken from existing annotations if they were loaded. Song types for annotation can be defined upon load (see above). You can also add new or edit the names of existing song types via “Audio/Add or edit annotation types”.

:::{figure} xb_make-fig
<img src="/images/xb_make.png" alt="edit annotation types" height="500px">

Create, rename or delete song types for annotation.
:::


The dropdown many on the top left of the waveform view can be used to select which song types you want to annotate. The selected annotation type can also be changed with number keys according to the number indicated in the dropdown menu.

:::{figure} xb_types-fig
<img src="/images/xb_types.png" alt="select annotation types" height="150px">

Select annotation types.
:::

To annotate a new song, left-click on the waveform or spectrogram view. If you have selected an event-like type, that’s it - you just placed the event time and a line should appear in the waveform and spectrogram view. If you have selected a segment type, the cursor changes to a cross. You have only placed one boundary of the segment, a second click somewhere else will complete the annotation and a shaded area should appear between the time points of the first and second click.


:::{figure} xb_annotate-fig
<img src="/images/xb_annotate.png" alt="annotate song" height="500px">

Fully annotated fly song. Pulse (cyan) is an event-like song type and is annotated by clicking on the pulse center. Sine (red shaded area) is a segment- or syllable-like song type and is annotated by clicking on the beginning and the end of the sine syllable.
:::

Delete annotations by right-clicking on the annotation. You can delete all annotations or only the selected annotation with the U and Y, respectively or via the Audio menu. Move annotations by dragging the lines or the boundaries of the shaded area - this will change event times and segment bounds. Or drag the shaded area itself to move the whole segment. Movement can be disabled completely or restricted to the currently selected annotation type.

## Save annotations
Save the annotations via the file menu as a comma-separated `csv` file. See [here](data_formats.html#exported-annotations-and-audio) for a specification of the file format.
