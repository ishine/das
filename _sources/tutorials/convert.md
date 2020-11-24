# Convert your own annotations and audio data
If you start from scratch---with non-annotated audio recording---you can use the GUI. Start from scratch - non-annotated data - using the GUI. See the [GUI tutorial](/tutorials_gui/tutorials_gui) for a description of all steps - from loading data, annotating song, making a dataset, training a network and generating annotations after training...

However, often annotations exist, from old manual annotations or produced by other tools. _DeepSS_ can be used with existing annotations, by converting the existing annotations into the dss format.

If audio data is in a format supported by dss (see [here]()), open in GUI and export to folder. For processing large sets of recordings, use the [notebook]().

## Annotation format
csv file with three columns:
- `name`: name of the song element for instance 'pulse' or 'sine' or 'syllable A'
- `start_seconds`: *start* of the song element in seconds rel. to the start of the recording
- `stop_seconds`: *end* of the song element in seconds rel. to the start of the recording

There are two types of song elements:
- `events` have not extent in time, `start_seconds=stop_seconds`, and are best used for brief, pulsatile signals like fly pulse song
- `segments` extend in time, `start_seconds>stop_seconds`, and should be used for normal syllables or fly sine song

### Examples of transforming custom annotation formats
Build DataFrame from segment on- and offsets and event times loaded from a custom format:

Use `xb.annot` to generate a csv file from lists of event names and start and stop seconds:

```python
from xarray_behave.annot import Events  # require install with gui

# define three annotations
names = ['bip', 'bop', 'bip']
start_seconds = [1.34, 5.67, 9.13]
stop_seconds = [1.34, 5.85, 9.13]

# save to csv file
evt = Events.from_lists(names, start_seconds, stop_seconds)
df = evt.to_df()
print(df)
df.to_csv(filename)
```

Do it yourself:

```python
import numpy as np
import pandas as pd

# create empty DataFrame with the required columns
df = pd.DataFrame(columns=['name', 'start_seconds', 'stop_seconds'])

# append a segment
onset = 1.33 # seconds
offset = 1.42  # seconds
segment_bounds = [onset, offset]
segment_name = 'sine_song'

new_row = pd.DataFrame(np.array([segment_name, *segment_bounds])[np.newaxis,:],
                        columns=df.columns)
df = df.append(new_row, ignore_index=True)

# append an event
event_time = 2.15 # seconds
event_name = 'pulse'

new_row = pd.DataFrame(np.array([event_name, event_time, event_time])[np.newaxis,:],
                        columns=df.columns)
df = df.append(new_row, ignore_index=True)
```

## Convert audio data
Can read many formats, but for making a dataset, two formats are supported:

Supported formats:

Load your data and save as wav:
```python
scipy.io.wavfile.write(...)
```

```matlab
wavwrite(...)
```

```{warning}
Caution when saving wav - clipping.
```

Or npz file. (NPZ format)
```python
np.savez(filename, data=audio, samplerate=samplerate)
```

