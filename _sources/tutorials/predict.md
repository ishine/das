# Predict


## Command line
`dss-predict file.wav model_trunk`

## Python
- python: `dss.predict.predict('file.wav', model_save_name='model_trunk'))`
- see notebook

## Inference
events, segments = infer(x, model_name, inference_params)   # fall back sensible to defaults (all thres 0.5, no pre-processing) with warning
`events[eventname][seconds/probabilities]`
`segements[segmentname][denselabels/onset_seconds/offset_seconds/probabilities]`

for each class:
type, name, threshold=0.5, min_dist=None, min_len=None, fill_len=None

## Predict class probabilities
```python
class_probabilities = predict(x,  # array [samples, channels] or [samples, frequencies, channels]
       model_name,  # basename of the model
       )
```

## Process segments


## Process events

in a python shell/notebook
```python
import dss.predict
song = scipy.io.wavefile.read('filename')
segment_probabilities, segment_labels, event_times, event_confidence = dss.predict(song, modelfilename)
```
