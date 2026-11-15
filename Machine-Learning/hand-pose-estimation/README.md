# 2D Hand Pose Estimation

**Computer vision · Deep learning · Heatmap regression · Fall 2026**

## The problem

Given a cropped egocentric hand image, estimate the locations of **21 anatomical keypoints**. The experiment uses a subset of the Ego-Exo4D dataset and a top-down pipeline: a model predicts one heatmap per joint from a provided hand crop. Hand detection is outside the scope of this experiment.

## Mathematical formulation

For input image $I$, the convolutional network $f_\theta$ predicts heatmaps $\hat H=f_\theta(I)\in\mathbb R^{21\times112\times112}$. A joint coordinate is estimated by the heatmap maximum:

```math
\hat{\mathbf p}_j=\underset{(x,y)}{\mathrm{argmax}}\;\hat H_j(x,y).
```

The training objective compares predicted heatmaps with target heatmaps, using visibility-aware supervision. The numerical loss below is **heatmap loss**, not a distance in pixels.

## Experiment

| Measurement | Value |
|---|---:|
| Training samples | **20,998** |
| Validation samples | **5,911** |
| Test samples | **7,813** |
| Training epochs | **20** |
| Model output tensor | **1 × 21 × 112 × 112** |
| Initial validation loss | **0.99048** |
| Best validation loss | **0.66080** (epoch 12, 1-indexed) |
| Final validation loss | **0.66929** |
| Relative reduction from initial to best validation loss | **33.3%** |

![Training and validation heatmap loss across 20 epochs](assets/training-curve.svg)

The model was initialized with pretrained weights. Validation loss reached its minimum at epoch 12, then finished slightly higher at epoch 20.

### Example keypoint errors

Four visible joints on one selected test image had Euclidean errors of **1.4, 2.2, 3.0, and 1.0 pixels** (joint indices 0, 8, 12, and 16). Their mean error was **1.9 pixels**. These values describe those four joints only, rather than the full test set.

## Visual results

### Hand-pose example

![Hand-pose example](assets/handpose_cell21_0.webp)

### Ground truth and model prediction

| Ground truth | Prediction |
|---|---|
| ![Ground truth hand keypoints](assets/handpose_cell22_0.webp) | ![Predicted hand keypoints](assets/handpose_cell22_1.webp) |

These examples show predicted joint structure alongside the reference annotations.

## Evaluation and limitations

- Validation heatmap loss fell **33.3%** from its initial value to its best value. This measures the training objective, rather than a percentage gain in keypoint accuracy.
- Aggregate test-set keypoint accuracy, PCK, and normalized keypoint error have not been measured. The selected image does not establish generalization across subjects or activities.

[← Machine Learning](../README.md) · [Portfolio index](../../SHOWCASE.md)
