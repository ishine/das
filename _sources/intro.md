# Welcome to _DeepSS_
_DeepSS_ --- short for _DeepSongSegmenter_ --- is a tool for annotating song in audio recordings. At the core of _DeepSS_ is a deep neural network, implemented in Tensorflow. The network takes single- and multi-channel audio as an input and returns the probability of finding a particular song type for each audio sample. _DeepSS_ can be used with a graphical user interface for loading audio data, annotating song manually, training a network, and generating annotations on new samples and recordings. _DeepSS_ can also be used programmatically from the command line, in python notebooks, or in your own python code via the _dss_ module.



If you use _DeepSS_, please cite: REF_GOES_HERE

````{panels}
```{link-button} install
:text: Install
:type: ref
:classes: stretched-link
```
````


## Tutorials

````{panels}
```{link-button} tutorials_gui/tutorials_gui
:text: Using the GUI
:type: ref
:classes: stretched-link
```
Annotate song, train a network, and predict on new samples

---

```{link-button} tutorials/notebook
:text: Use in notebooks
:type: ref
:classes: stretched-link
```
Train a network using your own annotations, and predict on new samples

---

```{link-button} tutorials/cli
:text: Use command line interface
:type: ref
:classes: stretched-link
```
Train and predict using the command line

---

```{link-button} unsupervised/unsupervised
:text: Classify
:type: ref
:classes: stretched-link
```
Cluster existing annotations in song types.

````


## Documentation

````{panels}

```{link-button} annotate
:text: Annotate song manually
:type: ref
:classes: stretched-link
```

---

```{link-button} train
:text: Train
:type: ref
:classes: stretched-link
```

---

```{link-button} predict
:text: Predict song labels
:type: ref
:classes: stretched-link
```

````