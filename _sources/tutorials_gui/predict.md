# Predict
Once training finished, generate annotations using the trained network via _DeepSS/Predict_. In contrast to training, prediction is very fast and does not require a GPU - if you trained the network remotely on a machine with a GPU, copy the generated files ending in `_model.h5` and `_params.yaml` to your local machine.

:::{figure} xb_predict-fig
<img src="/images/xb_predict.png" alt="predict" width=750>

predict options
:::

- _Model_: Go to the save folder specific during training and select the file ending in `_model.h5` with the chosen prefix and timestamp.
- _Start/End seconds_: Specify the part of the recording to predict labels for. Defaults to the whole recording. For this tutorial, predict song for the 30 seconds after you manual annotations (seconds 70-100).
- _Proof reading mode_: If True, the predictions will not yet be fully integrated but special song types ending in `_proposals` will be created. You can the fix the predictions in the view and then approve them, which will strip off the `_proposals` from them. If False, will be automatically approved and the predicted song types will be given their original names. For this tutorial, enable the proof reading mode.
- __Event detection__:
    - _Threshold_: The network produces a confidence value between 0 and 1 for each sample. Events are detected based on peaks in these confidence values. The threshold sets the minimal height of these confidence peaks.
    - _Minimal event interval for detection (seconds)_: Will skip events that come to close to each other, for instance if the peaks in the confidence are jagged. Leave as is.
    - _Delete events closer/farther than (seconds)_: Additional post-detection interval filters for removing events that come to close or too far after another event. The too-far filter allows you to only keep pulses that come in train and remove isolated pulses that are likely spurious detections.
- __Segment detection__:
    - _Threshold_: The network produces a confidence value between 0 and 1 for each sample. Events are detected based on peaks in these confidence values. The threshold sets the minimal height of these confidence peaks.
    - _Fill gaps shorter than (seconds)_: ... . Enable this!
    - _Delete segments shorter than (seconds)_: . Enable this!


## Proof reading
Since you created predictions in proof reading mode, the predictions will be assigned to two new song types, starting with the original name of the song type and ending in `_proposals`. Correct any prediction errors---add missing annotations, remove false positive annotations, adjust the timing of annotations. Once you have corrected all errors, approve annotations with `G` or `H` for approving only the active or all song types, respectively. This will rename the proposals in the view to the original names (for instance, `sine_proposals` -> `sine`).

Repeat the prediction->correction->training cycle for ever larger parts of the recording, to easily build a large dataset of annotations for training ever better networks.