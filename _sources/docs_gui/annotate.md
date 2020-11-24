# Annotate song

## Initialize or edit song types
Since this is a recording without pre-existing annotations, register new song types via “Audio/Add or edit song types”. Fly song of most species contains two types of song: Pulse song, which contains trains of brief pulses and sine song, containing sustained oscillations. In _DeepSS_, two categories of song types are discriminated:
- _Events_ are defined by a single time of occurrence. The aforementioned pulse song is a song type of the event category.
- _Segments_ are song types that extend over time and are defined by a start and a stop time. The aforementioned sine song and the syllables of mouse and bird vocalizations fall into the segment category.

To annotate the fly song, create two song types: 'pulse' of category 'event' and 'sine' of category 'segment:

:::{figure} xb_make-fig
<img src="/images/xb_make.png" alt="edit annotation types" height="500px">

Create, rename or delete song types for annotation.
:::

If annotation exist for the recording you load, the song types are populated from the existing annotations. Song types can be added, deleted, and renamed in the “Audio/Add or edit song types”.

You can now activate "pulse" or "sine" for annotation using the dropdown menu on the top left of the main window. The active song type can also be changed with number keys according to the number indicated in the dropdown menu.

:::{figure} xb_types-fig
<img src="/images/xb_types.png" alt="select annotation types" height="150px">

Activate song types for annotation.
:::


## Create annotations
To annotate song in the recording, left-click on the waveform or spectrogram view. If an event-like song type is active, that’s it - you just placed the event time and a line should appear in the waveform and spectrogram view. If a segment-like song type is active, the first click should be placed at the start of the segment. The first click places one boundary of the segment and the cursor changes to a cross. A second click at the end of the segment will complete the annotation and a shaded area marking the segment should appear. Note segment annotation can also start with a click on the segment end.


:::{figure} xb_annotate-fig
<img src="/images/xb_annotate.png" alt="annotate song" height="500px">

Fully annotated fly song. Pulse (cyan) is an event-like song type and is annotated by clicking on the pulse center. Sine (red shaded area) is a segment- or syllable-like song type and is annotated by clicking on the beginning and the end of the sine syllable.
:::

## Edit annotations
Delete annotations by right-clicking on the annotation. Annotations of all song types or only the active one in the view can be deleted with `U` and `Y`, respectively, or via the _Audio_ menu. Move annotations by dragging the lines or the boundaries of the shaded area - this will change event times and segment bounds. Drag the shaded area itself to move a segment. Movement can be disabled completely or restricted to the currently selected annotation type via the _Audio_ menu.

<!--  -->

## Export and save annotations
_DeepSS_ achieves good performance even from small sets of manual annotations. Once you have completely annotated the first seconds of song - a couple of pulse trains and sine song segments - we can train a network to help with annotating the rest of the data. Export the data and the annotations for _DeepSS_ - via the `File/Export for DeepSS` to a new folder - call it `fly_first`:


:::{figure} xb_assemble-fig
<img src="/images/xb_export.png" alt="export audio and annotations" width=500>

Export audio data and annotations
:::

- _Song types to export_: Select a specific song type to export annotations for. Keep this the default of exporting all annotations. Annotations will be saved as `csv` (see a [description](/technical/data_formats) of the format).
- _Audio file format_: The format in which to export the audio data:
    - _NPZ_: Zipped numpy variables. Will store a `data` variable with the audio and a `samplerate` variable.
    - _WAV_: Wave audio file. More general but also less flexible format. For instance, floating point data is restricted to the range [-1, 1]. Audio should be scaled before saving to data loss from clipping.
    - _Recommendation_: We recommend NPZ, because it is robust and portable. WAV is more general but the format is more restricted and can lead to data loss.
- _Scale factor_: Scale the audio before export. Should be left as is. Only important when exporting to WAV, since the WAV format has range restrictions.
- _Start seconds_ & _end seconds_: Export audio and annotations only between start and end seconds. In particular relevant when exporting partially annotated data. For fast training, do not include too much silence at the before the first and after the last annotation to ensure that all parts of the exported audio contain annotated song.

To generate a larger dataset, annotate and export multiple recordings into the same folder then assemble a dataset via DeepSS/Make dataset.

We also recommend you save the full annotations next to the audio data via the file menu as a `csv` file. That way, the annotations will be loaded with the audio data for picking up annotations or for comparison with song labels inferred by a trained network.

Once data is exported, train the network.