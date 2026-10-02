# TinyMLP

Code for the paper *TinyMLP: A 2,410-Parameter Perceptron for Low-Resolution Handwritten Digits*.

TinyMLP labels 8×8 images of handwritten digits, each given as 64 pixel counts from 0 to 16. It is
a perceptron with one hidden layer, 64 → 32 ReLU → 10 softmax (2,410 parameters), trained with
Adam for 50 epochs on the raw counts.

## Usage

    python run.py --train-dir DIR --inputs INPUTS.npz --out PREDICTIONS.npy --seed SEED

| Argument | Content |
|---|---|
| `DIR/train.npz` | `X`, n×64 pixel counts (float); `y`, labels 0 to 9 (int) |
| `INPUTS.npz` | `X`, m×64 pixel counts: the images to label |
| `PREDICTIONS.npy` | written by the script: m labels (int64), in the row order of `INPUTS.npz` |
| `SEED` | fixes the initialisation and the batch order: the same seed gives the same predictions |

The script prints one line: the seed, the training-set size, the epochs run, the final training
loss, the training accuracy, the number of predictions and the time taken.

## Files

- `model.py`: the model and its hyperparameters.
- `run.py`: loading, training, prediction.
- `requirements.txt`: the versions we used, with Python 3.13.5. CPU only.

## Expected results

Accuracy on the paper's validation set (359 images) and on its fixed 141-image sample, on an
Apple M4 Max with numpy 2.2.6 and scikit-learn 1.7.1:

| Seed | Validation (359) | Validation sample (141) |
|---|---|---|
| 0 | 0.9081 | 0.8723 |
| 1 | 0.8969 | 0.9007 |
| 2 | 0.9304 | 0.9149 |
| mean ± sd | 0.9118 ± 0.0170 | 0.8960 ± 0.0217 |

On that platform and those versions, every number above is reproduced exactly. Where another
platform or version changes them, compare with the spread over 20 seeds (0 to 19): validation
accuracy 0.9162 ± 0.0133. A three-seed mean within two standard errors of it, 0.9008 to 0.9316,
is consistent with this code.

## Warnings

- scikit-learn's `ConvergenceWarning` at the end of training means that the optimiser stopped at
  its fixed budget of 50 epochs.
- On Apple M4 machines with numpy older than 2.3.1, matrix products raise spurious floating-point
  warnings ("overflow encountered in matmul") although their results are exact. `run.py` silences
  them, and stops if the trained weights are not finite.
