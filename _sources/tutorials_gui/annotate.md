# Annotate song

## Initialize or edit song types
To annotate song, we first need to register the different song types we want to annotate. The example audio is a recording from a male _Drosophila melanogaster_ fly, which produces two major types of courtship song: Pulse song, which contains trains of brief pulses and sine song, containing sustained oscillations. We will register pulse and sine as song types for annotation via the _Audio/Add or edit song types_. _DeepSS_ discriminates two categories of song types:
- _Events_ are defined by a single time of occurrence. The aforementioned pulse song is a song type of the event category.
- _Segments_ are song types that extend over time and are defined by a start and a stop time. The aforementioned sine song and the syllables of mouse and bird vocalizations fall into the segment category.

 Add two new song types: 'pulse' of category 'event' and 'sine' of category 'segment:

:::{figure} xb_make-fig
<img src="/images/xb_make.png" alt="edit annotation types" height="500px">

Create, rename or delete song types for annotation.
:::

If annotations exist for the recording you loaded, the song types are populated from the existing annotations and can be added, deleted, and renamed via “Audio/Add or edit song types_.


## Create annotations

The two new song types "pulse" or "sine" can now be activated for annotation using the dropdown menu on the top left of the main window. The active song type can also be changed with number keys according to the number indicated in the dropdown menu.

:::{figure} xb_create-fig
<img src="/images/xb_create_opt.gif" alt="annotate song" width="700px">

Left clicks in waveform or spectrogram few create annotations.
:::

To annotate song in the recording, left-click on the waveform or spectrogram view. If an event-like song type is active, that’s it - you just placed the event time and a line should appear in the waveform and spectrogram view. If a segment-like song type is active, the first click should be placed at the start of the segment. The first click places one boundary of the segment and the cursor changes to a cross. A second click at the end of the segment will complete the annotation and a shaded area marking the segment should appear. Note segment annotation can also start with a click on the segment end.

## Edit annotations
Delete annotations by right-clicking on the annotation. Annotations of all song types or only the active one in the view can be deleted with `U` and `Y`, respectively, or via the _Audio_ menu. Move annotations by dragging the lines or the boundaries of the shaded area - this will change event times and segment bounds. Drag the shaded area itself to move a segment. Movement can be disabled completely or restricted to the currently selected annotation type via the _Audio_ menu.

:::{figure} xb_edit-fig
<img src="/images/xb_edit_opt.gif" alt="annotate song" width="700px">

Dragging moves, right click deletes annotations.
:::
## Export and save annotations
_DeepSS_ achieves good performance with little manual annotation. Once you have completely annotated the song between 52 and 70 seconds---a couple of pulse trains and sine song segments---you can train a network to help with annotating the rest of the data. Export the data and the annotations for _DeepSS_ - via the `File/Export for DeepSS` to a new folder - call it `fly_first`:


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
- _Start seconds_ & _end seconds_: Export audio and annotations only between start and end seconds. In particular relevant when exporting partially annotated data. For fast training, do not include too much silence at the before the first and after the last annotation to ensure that all parts of the exported audio contain annotated song. We have annotated song between x and y seconds, so set start and end seconds accordingly.

```{note}
For this tutorial, we start with a single recording. To generate a larger and more diverse dataset, annotate and export _multiple recordings into the same folder_. They can then be assembled in a single via DeepSS/Make dataset (see next page).
```

```{note}
We also recommend you save the full annotations next to the audio data via the _File/Save annotations_ as a `csv` file. That way, the annotations will be loaded the next time you load the recording.
```

Once data is exported, train the network.