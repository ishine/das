# Make datasets with custom data

You can also use existing annotations,
0. (simplest, least flexible) Export to data and annotations to formats readable by the GUI.
1. (simplest, least flexible) Folder with the data and annotations in a specific format (wav and csv files). Allows you to use GUI for editing annotations and making a dataset.
2. (intermediate simplicity and flexibility) Folder with the data and annotations in a custom format - requires providing custom functions for loading both data types.
3. (complex, maximally flexible) Bring your own mappable.

### 0. Export to a format readable by _dss-gui_
Can read many audio formats (see [GUI tutorial](/tutorials_gui/load))
Requires annotations in a specific, simple format: DESCRIBE

If audio and annotations are "perfect" and require not editing or cutting, put npz and wav files into a single folder. Can then use GUI.



### 1. Make a folder with wav/npz and csv
`data` folder with `*.wav` files with the recording and matching `*.csv` files with the annotations - recordings and annotations will be matched according to the file base name:
```shell
data\
    file01.wav
    file01.csv
    another_file.wav
    another_file.csv
    yaf.wav
    yaf.csv
```
Save your annotations as csv.
Make audio readable - many different formats supported. If unsupported, convert.

Then follow instructions from GUI tutorial (load with data and use gui to make edit annotation, export, make dataset, train).

Export audio as npz or wav and annotations as csv into one folder - make dataset straight away.


### 2. Use notebook with custom loaders to directly read recordings and annotations
Same general data structure as above but with custom data formats. If your recordings and annotations are not in the format expected by the standard loaders used above (`scipy.io.wavefile.read` for the recordings, `pd.read_csv` with name/start_seconds/stop_seconds for annotations), or if it's hard to convert your data into these standard formats, you can provide your own loaders as long as they conform to the following interface:

- _data loaders_: `samplerate, data = data_loader(filename)`, accepts a single string argument - the path to the data file and returns two things: the samplerate of the data and a numpy array with the recording data [time, channels]. Note: `scipy.io.wavefile.read` returns `[time,]` arrays - you need to add a new axis to make it 2d!
- _annotation loaders_: `df = annotation_loader(filename)`, accepts a single string argument with the file path and returns a pandas DataFrame with these three columns: `name`, `start_seconds`, `stop_seconds` (see 1).

ref notebook



## 3. Bring your own mappable
Lastly, you directly create a dataset from you own data.

DeepSS expects a simple dictionary-like data structure (see [dataset structure](/technical/data_formats) doc):
```
data
  ├── ['train']
  │   ├── ['x']         (the audio data - samples x channels)
  │   ├── ['y']        (annotations - samples x song types, first one is noise, needs to add to )
  │   ├── ['y_suffix1'] (optional, multiple allowed)
  ├── ['val']
  │   ├── ['x']
  │   ├── ['y']
  │   ├── ['y_suffix1']
  ├── ['test']
  │   ├── ['x']
  │   ├── ['y']
  │   ├── ['y_suffix1']
  └── attrs
        └── ['samplerate'] (of x and y in Hz)
              ['class_names']
              ['class_types'] (event or segment)
              ['class_names_suffix1']
              ['class_types_suffix1'] (event or segment)
```

Data is accessed via keys, for instance `data['train']['x']`. `attrs` is a dictionary accessed via `.` notation: `data.attrs['samplerate']`.

This structure can be implemented via python's builtin [dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries), [hdf5](https://www.h5py.org), [xarray](http://xarray.pydata.org'), [zarr](https://zarr.readthedocs.io), or anything else that implements a key-value interface (called a Mapping in python).

We provide a alternative storage backend - `npy_dir` ([source](../src/dss/npy_dir.py)) - that mirrors the data structure in directory hierarchy with [numpy's npy](https://numpy.org/doc/stable/reference/generated/numpy.load.html) files (inspired by Cyrille Rossant's series of blog posts ([1](https://cyrille.rossant.net/moving-away-hdf5/), [2](https://cyrille.rossant.net/should-you-use-hdf5/)), [jbof](https://github.com/bastibe/jbof) and [exdir](https://exdir.readthedocs.io/)). For instance, `data['train']['x']` is stored in `dirname/train/x.npy`. `attrs` is stored as a `yaml` file in the top directory.

This provides structured access to data via npy files. npy files have the advantage of providing a fast memory-mapping mechanism for out-of-memory access if your data set does not fit in memory. While zarr, h5py, and xarray provide mechanisms for out-of-memory access, they tend to be generally slower or require fine tuning to reach the performance reached with memmapped npy files.

_Notes_

- that the annotations correspond to probabilities - they should sum to 1.0 for each sample. The first "song" type, should be noise or no song, `p(no song)`
- y_suffix...