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

```{link-button} tutorials/tutorials
:text: Use in python and from the terminal
:type: ref
:classes: stretched-link
```
Convert your own data, train and evaluate a network, predict on new samples in realtime.

---

```{link-button} unsupervised/unsupervised
:text: Classify
:type: ref
:classes: stretched-link
```
Discover song types in annotated syllables.

````