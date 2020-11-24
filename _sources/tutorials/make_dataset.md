# Make datasets with custom data
If your data is readable by the GUI, you only need to convert annotations. You can then load both into the GUI and export to data and annotations for DeepSS.

Three alternatives:

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

Simplest way - no need of having to deal with specific of the data structure required by DeepSS for training - simply hit _DeepSS/Make dataset for training_ and select the folder.

### 2. Use notebook with custom loaders to directly read recordings and annotations
Intermediate simplicity and flexibility) Folder with the data and annotations in a custom format - provide custom functions for loading audio data and annotations. This is illustrated in a notebook (ADD NOTEBOOK AND LINK)

### 3. DIY dataset
Complex, maximally flexible) Bring your own mappable (for experts): Generate the data structure yourself. The description of the [dataset structure](/technical/data_formats) has information on how to do that.
