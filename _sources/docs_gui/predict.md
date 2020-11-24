# Predict
Once training finished, generate annotations using the trained network via _DeepSS/Predict_.

:::{figure} xb_predict-fig
<img src="/images/xb_predict.png" alt="predict" width=750>

predict options
:::

- _Model_: Go to the save folder specific during training and select the file ending in `_model.h5` with the chosen prefix and timestamp.
- _Start/End seconds_: Specify the part of the recording to predict labels for. Defaults to the whole recording.
- __Event detection__:
    - _Threshold_: The network produces a confidence value between 0 and 1 for each sample. Events are detected based on peaks in these confidence values. The threshold sets the minimal height of these confidence peaks.
    - _Minimal event interval for detection (seconds)_: Will skip events that come to close to each other, for instance if the peaks in the confidence are jagged. Leave as is.
    - _Delete events closer/farther than (seconds)_: Additional post-detection interval filters for removing events that come to close or too far after another event. The too-far filter allows you to only keep pulses that come in train and remove isolated pulses that are likely spurious detections.
- __Segment detection__:
    - _Threshold_: The network produces a confidence value between 0 and 1 for each sample. Events are detected based on peaks in these confidence values. The threshold sets the minimal height of these confidence peaks.
