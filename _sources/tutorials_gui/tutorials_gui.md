# GUI tutorial

This is a tutorial walking through all steps from audio data to predictions using a recording of fly song as an example.

In the tutorial, we will use an adaptive fast training approach found in pose tracking software (LEAP, SLEAP):

1. annotate a little
2. train
3. predict
4. fix predictions
5. go back to 2. until performance is satisfactory

## Download example data

Download and open this [file](link) - it's a recording of fly song from D. Stern (link) saved as a wav file. We will use the file as an example to walk through loading, annotating, training and predicting.


## Start the GUI

Install _DeepSS_ following these [instructions](/install). Then start the GUI by opening a terminal, activating the conda environment created during install and typing `dss-gui`:
```shell
conda activate dss
dss-gui
```

In the window that opens, choose _Load audio from file_ to open the downloaded recording of fly song:

<img src="/images/xb_start.png" alt="start screen" width=450>



