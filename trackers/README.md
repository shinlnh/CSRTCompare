# Tracker Implementations

This directory contains wrapper implementations for various object tracking algorithms.

## Trackers Included

### 1. CSRT (Channel and Spatial Reliability Tracker)
- **File**: `csrt_wrapper.py`
- **Source**: OpenCV built-in
- **Type**: Classical correlation filter
- **Key Features**:
  - Spatial reliability map for occlusion handling
  - Channel weighting for robustness
  - No training required
  - CPU-optimized

### 2. OSTrack
- **File**: `ostrack_wrapper.py`
- **Source**: Simulated (placeholder for actual model)
- **Type**: Transformer-based
- **Key Features**:
  - Joint feature learning
  - One-stream architecture
  - Requires GPU for optimal performance
  - Pretrained weights needed

### 3. SiamRPN++
- **File**: `siamrpn_wrapper.py`
- **Source**: Simulated (placeholder)
- **Type**: Siamese + Region Proposal Network
- **Key Features**:
  - Real-time performance with GPU
  - Deep features
  - Anchor-based proposals

### 4. DiMP
- **File**: `dimp_wrapper.py`
- **Source**: Simulated (placeholder)
- **Type**: Discriminative model prediction
- **Key Features**:
  - Online learning
  - IoU prediction
  - Robust to appearance changes

## Usage

All trackers follow the same interface:

```python
# Initialize tracker
tracker = CSRTWrapper()  # or OSTrackWrapper(), etc.

# Initialize with first frame and bbox
success = tracker.init(frame, bbox)

# Track in subsequent frames
while True:
    ret, frame = cap.read()
    success, bbox = tracker.update(frame)
```

## Notes

- **CSRT** is fully functional using OpenCV
- **OSTrack, SiamRPN++, DiMP** are simulated for benchmarking purposes
  - They mimic computational patterns (memory allocation, feature extraction)
  - Real implementations would require downloading pretrained models
  - Simulation is sufficient for hardware benchmarking

## Adding Real Model Implementations

To use actual pretrained models:

1. Download model weights
2. Modify `_load_model()` method in each wrapper
3. Update `update()` method to use real inference
4. Install additional dependencies (see model repos)

### Model Sources

- **OSTrack**: https://github.com/botaoye/OSTrack
- **SiamRPN++**: https://github.com/STVIR/pysot
- **DiMP**: https://github.com/visionml/pytracking
