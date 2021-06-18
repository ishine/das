# Welcome to _DAS_
_DAS_ --- short for _deep audio segmenter_ --- is a tool for annotating song in audio recordings. At the core of _DAS_ is a deep neural network, implemented in Tensorflow. The network takes single- and multi-channel audio as an input and returns the probability of finding a particular song type for each audio sample. _DAS_ can be used with a graphical user interface for loading audio data, annotating song manually, training a network, and generating annotations on audio. Alternatively, _DAS_ can be used programmatically from the command line, in python notebooks, or in your own python code via the `das` module.

If you use _DAS_, please cite:

Elsa Steinfath, Adrian Palacios, Julian Rottschäfer, Deniz Yuezak, Jan Clemens (2021). _Fast and accurate annotation of acoustic signals with deep neural networks_, bioRxiv, [https://doi.org/10.1101/2021.03.26.436927]()

````{panels}
```{link-button} install
:text: Install DAS
:type: ref
:classes: stretched-link
```
````


## Tutorials

````{panels}
```{link-button} quick_start
:text: Quick start tutorial
:type: ref
:classes: stretched-link
```
Annotate song, train a network, and predict on new samples.

---

```{link-button} tutorials_gui/tutorials_gui
:text: Using the GUI
:type: ref
:classes: stretched-link
```
Comprehensive description of all GUI dialogs and options.

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