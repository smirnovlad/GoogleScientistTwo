# Rules of the digits task

A solution is a change to `code/`. The locked harness runs it and scores it. A solution that breaks
any rule below is invalid, whatever its score.

## The evaluation, which no solution changes

- **Data.** scikit-learn's digits dataset: 1,797 images of 8×8 pixels, integer values 0 to 16, 10
  classes. `prepare.py` splits it per class with a fixed seed:
  - `train`, 1,079 images: inputs and labels, given to the code;
  - `full`, the validation set, 359 images;
  - `subset`, a fixed per-class 40 % sample of `full`, 141 images;
  - `test`, 359 images.
- **Seeds.** `subset`, `full` and `test` are each evaluated with seeds 0, 1 and 2.
- **Metric.** Accuracy, the fraction of rows labelled correctly, computed by `harness/metric.py`;
  macro-averaged F1 is reported beside it. Higher is better. A result is the mean and the sample
  standard deviation over the split's seeds.
- **Validation and test.** Every number seen during the search comes from `subset` or `full`.
  `test` is scored once, at the end, for the report.

## Files no solution may change

- Everything outside `code/`: `task.json`, `paper.md`, `rules.md`, `prepare.py`, `data/` and
  `harness/` (the split inputs, the labels and `metric.py`). The harness pins its copies of
  `harness/` and `data/public/` by hash, and checks them before every evaluation.
- **The entrypoint**, which the harness calls from inside `code/`:

      python run.py --train-dir DIR --inputs INPUTS.npz --out PREDICTIONS.npy --seed SEED

  `run.py` keeps this name, these four arguments and their meaning. It may import any module in
  `code/`, and everything behind the entrypoint may change.

## What a run must do

1. Train on `DIR/train.npz` (`X`: n×64 float pixel counts; `y`: integer labels 0 to 9).
2. Write to `PREDICTIONS.npy` a 1-D integer array of labels in 0 to 9, one for each row of `X`
   in `INPUTS.npz`, in row order. Any other shape, dtype, length or value makes the run fail.
3. Train every model itself, from scratch, during this run. Each prediction comes from a model
   that this run trained on `train.npz`.
4. Be deterministic: the same seed gives the same predictions. All randomness derives from
   `--seed`.

## Data a solution may use

The harness enforces this part: scikit-learn's bundled data cannot be read by the code or by
the agents, and a change that adds a dataset loader, a URL or a data file is refused before it
runs.


- **Only `train.npz`.** No other data, in any form or from any source. This excludes:
  - scikit-learn's bundled copy of these digits (`sklearn.datasets.load_digits`, or any file under
    `sklearn/datasets/data/`), which contains the validation and test images with their labels;
  - the UCI optical digits files;
  - MNIST, USPS, EMNIST and every other dataset;
  - anything downloaded or copied into `code/`.
- **No pretrained models or weights**, and no stored predictions, labels or lookup tables in
  `code/`.
- **New training examples made from `train.npz` inside the run are allowed:** shifted, rotated or
  distorted copies of the training images, for example. They are part of the method.
- **The evaluation inputs are only labelled, never learned from.** No fitting, transductive or
  semi-supervised learning, test-time training or statistics computed across the rows of
  `INPUTS.npz`. A row's prediction depends only on the trained model and that row.
- **No reading of the harness,** its labels or `metric.py`, and no inferring of labels from the
  file name, the row order or the number of rows.

## Environment

- **Packages:** the Python standard library and the installed numpy, scipy, scikit-learn, pandas
  and torch. Installing anything is forbidden.
- **CPU only:** no GPU, no Apple MPS device. The evaluation runs without network access.
- **Time:** one run of the entrypoint, for one seed, must finish within 120 seconds of wall-clock
  time on the reference machine, an Apple M4 Max, training included. The baseline takes about
  1 second. A run that exceeds the limit fails.
- **Writes:** a run writes only inside the directory that holds the `--out` file. Every other
  path is read-only to it.
