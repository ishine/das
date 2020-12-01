# GUI tutorial

This is a tutorial walking through all steps from audio data to predictions using a recording of fly song as an example.

In the tutorial, we will use an adaptive fast training approach found in pose tracking software (LEAP, SLEAP):

1. annotate a little
2. train
3. predict
4. fix predictions
5. go back to 2. until performance is satisfactory


## Download example data

Download and open this [file](link) - it's a recording of fly song from a male _Drosophila melanogaster_ courthing a females, recorded by D. Stern (link) saved as a wav file. We will use the file as an example to walk through loading, annotating, training and predicting.


## Start the GUI

Install _DeepSS_ following these [instructions](/install). Then start the GUI by opening a terminal, activating the conda environment created during install and typing `dss-gui`:
```shell
conda activate dss
dss-gui
```

<img src="/images/xb_start.png" alt="start screen" width=450>

## Load audio data


In the window that opens, choose _Load audio from file_ and select the downloaded recording of fly song. Alternatively, use the menu  _File/New from file_.

### Supported formats

Currently, the GUI can load audio data from a wide range of file types:

- audio files like `wav` etc. (read with [soundfile](http://pysoundfile.readthedocs.io/), [list of supported formats](http://www.mega-nerd.com/libsndfile/#Features))
- hdfs files typically ending in`h5` (read with [h5py](http://docs.h5py.org/)). `mat` files save with recent versions of Matlab also use this format (see [matlab docs](https://www.mathworks.com/help/matlab/ref/save.html#btox10b-1-version)).
- numpy's `npy` or `npz` files ([numpy](https://numpy.org/doc/stable/reference/routines.io.html))

The example recording is an audio file in `wav` format.

```{note}
If your favorite format is not included in this list, [convert it to a supported format](/tutorials/convert).
```

### Customizing loading
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

For the purpose of this tutorial, keep the defaults and hit the `Load data` button.

## Overview over the display and menus
Audio data from all channels (gray), with one channel being selected (white), and the spectogram of the currently selected channel below. The example recording is single channel so only one white audio trace will be displayed.

To navigate the view: Move forward/backward along the time axis via the `A`/`D` keys and zoom in/out the time axis with the `W`/`S` keys (See Playback/). The temporal resolution of the spectrogram can be increased at the expense of frequency resolution with the `R` and `T` keys.

You can play back the waveform on display through your computer speakers by pressing `E`.



:::{figure} xb_display-fig
<img src="/images/xb_display.png" alt="waveform and spectrogram display" width="100%">

Waveform (top) and spectrogram (bottom) display of a multi-channel recording.
:::

The waveform view can be adjusted further for multi-channel recordings: Hide the non-selected channels in the waveform view by toggling _Audio/Show all channels_. To change the channel for which the spectrogram is displayed, use the dropdown list on the upper right or switch to next/previous channel with the up/down arrow keys. The `Q` key (or _Audio/Autoselect loudest channel_) will toggle automatically selecting the loudest channel in the current view.
