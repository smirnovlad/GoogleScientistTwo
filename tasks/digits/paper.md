# TinyMLP: A 2,410-Parameter Perceptron for Low-Resolution Handwritten Digits

## Abstract

We ask how accurate the smallest conventional neural classifier is on low-resolution handwritten
digits when its training cost is negligible. TinyMLP is a perceptron with one hidden layer of 32
rectified linear units, 2,410 parameters in total. It reads the 64 raw pixel counts of an 8×8
digit image without any preprocessing, and is trained with Adam for a fixed budget of 50 epochs.
On a stratified 60/20/20 split of the 1,797-image digits dataset distributed with scikit-learn,
TinyMLP reaches an accuracy of 0.912 ± 0.017 on the validation split and 0.909 ± 0.020 on the
test split (mean ± standard deviation over three seeds). Loading, training and prediction take
about 0.05 s on one CPU, and a complete run, from interpreter start-up to written predictions,
about one second.

## 1 Introduction

Handwritten digit recognition has long served as a test bed for learning algorithms (LeCun et
al., 1998). The optical digits data of Alpaydin and Kaynak (1998) reduce each 32×32 bitmap of a
digit to an 8×8 grid: each cell counts the set pixels in one 4×4 block, an integer from 0 to 16.
Inputs this small admit models that train in a fraction of a second, which matters wherever
memory, energy or training time is scarce.

This paper studies the simplest point in that space: a perceptron with a single small hidden
layer, trained by back-propagation (Rumelhart et al., 1986) on the raw counts, with no feature
engineering and a fixed training budget. Our contributions are:

1. TinyMLP, a 2,410-parameter classifier for 8×8 digits (Section 2);
2. a fixed evaluation protocol on a public dataset: a stratified train/validation/test split,
   and seeds (Section 3);
3. TinyMLP's measured accuracy and cost (Section 4), with the code that reproduces them.

## 2 Method

**Architecture.** TinyMLP maps the 64 pixel counts x ∈ {0, …, 16}⁶⁴ of an image, in row-major
order, through one hidden layer to a softmax over the 10 classes:

    h = max(0, W₁x + b₁),      W₁ ∈ ℝ^(32×64), b₁ ∈ ℝ^32
    p = softmax(W₂h + b₂),     W₂ ∈ ℝ^(10×32), b₂ ∈ ℝ^10

It has 64·32 + 32 + 32·10 + 10 = 2,410 parameters. The counts enter the network as they are,
without centring or scaling.

**Training.** The loss of a mini-batch of B images is the mean cross-entropy plus the L2 penalty
(α / 2B)(‖W₁‖² + ‖W₂‖²) on the weights, not the biases, with α = 10⁻⁴. We minimise it with Adam
(Kingma and Ba, 2015): learning rate 10⁻³, β₁ = 0.9, β₂ = 0.999, ε = 10⁻⁸. Mini-batches hold
B = 200 images, and the training set is reshuffled at every epoch. Training runs for a fixed
budget of 50 epochs, which is 300 updates on our training split. Weights and biases are drawn
uniformly from [−b, b] with b = √(6 / (n_in + n_out)), the normalised initialisation of Glorot and
Bengio (2010), here applied to the biases as well. The seed fixes the initialisation and the
batch order, so a run is deterministic given its seed.

**Prediction.** An image receives the class of highest probability.

**Implementation.** TinyMLP is scikit-learn's `MLPClassifier` (Pedregosa et al., 2011) with the
settings above; every other setting keeps its default. We used scikit-learn 1.7.1 and numpy 2.2.6.

## 3 Experimental setup

**Data.** We use the digits dataset distributed with scikit-learn: 1,797 images in 10 classes,
174 to 183 per class. It is a copy of the test portion of the UCI "Optical Recognition of
Handwritten Digits" data (Alpaydin and Kaynak, 1998). By the description shipped with
scikit-learn, 43 people wrote the UCI data: 30 the training portion and 13 the test portion, so
our 1,797 images come from those 13 writers.

**Splits.** We split the images per class, with a fixed seed, into a training set (60 %, 1,079
images), a validation set (20 %, 359) and a test set (20 %, 359). A fixed per-class 40 % sample of
the validation set (141 images) serves for quick checks. The splits are drawn once and shared by
every experiment. The labels of the validation and test images are used only to score
predictions.

**Protocol.** Each configuration is trained from scratch on the training set with seeds 0, 1 and
2, and labels the validation and test images. We report accuracy, and the macro-averaged F1 score
as a secondary metric, as the mean ± sample standard deviation (n − 1 denominator) over the three
seeds. Every hyperparameter except the hidden width and the epoch budget is scikit-learn's
default; those two fix the model's size and its training cost. The test set was used only to
produce the test columns of Table 1. Times are wall-clock times on one Apple M4 Max CPU.

## 4 Results

**Table 1.** TinyMLP per seed: accuracy on the training set, and accuracy (correct / total) and
macro-F1 on the validation and test sets (359 images each).

| Seed | Train acc. | Validation acc. | Validation macro-F1 | Test acc. | Test macro-F1 |
|---|---|---|---|---|---|
| 0 | 0.9731 | 0.9081 (326/359) | 0.9083 | 0.9109 (327/359) | 0.9109 |
| 1 | 0.9472 | 0.8969 (322/359) | 0.8971 | 0.8886 (319/359) | 0.8883 |
| 2 | 0.9759 | 0.9304 (334/359) | 0.9310 | 0.9276 (333/359) | 0.9280 |
| **mean ± sd** | 0.9654 ± 0.0158 | **0.9118 ± 0.0170** | 0.9121 ± 0.0173 | **0.9090 ± 0.0196** | 0.9091 ± 0.0199 |

TinyMLP labels about 91 % of held-out digits correctly, and its validation and test accuracies
agree (0.9118 and 0.9090). The seed matters: the three seeds span 3.3 points on the validation
set. Over 20 seeds (0 to 19), validation accuracy is 0.9162 ± 0.0133 (range 0.8886 to 0.9359), and
accuracy on the 141-image validation sample is 0.9043 ± 0.0213 (range 0.8723 to 0.9504; seed 0
gives 0.8723). The final training loss is 0.094, 0.180 and 0.118 for seeds 0, 1 and 2; every run
used its full budget of 50 epochs.

**Cost.** Loading the data, training and prediction take 0.04 to 0.05 s per seed. A complete run,
with interpreter start-up and imports, takes 0.8 to 1.4 s (7 runs); one run's peak resident
memory was 168 MB.

## 5 Related work

LeCun et al. (1998) apply convolutional networks trained by gradient descent to handwritten
character recognition. Cortes and Vapnik (1995) introduce support-vector networks and compare
them with classical learning algorithms on a benchmark of optical character recognition. On the
optical digits data themselves, Kaynak (1995) studies methods of combining multiple classifiers.
TinyMLP belongs to the oldest family of these models, the multilayer perceptron trained by
back-propagation (Rumelhart et al., 1986), with the Adam optimiser (Kingma and Ba, 2015) and the
initialisation of Glorot and Bengio (2010) as implemented in scikit-learn (Pedregosa et al.,
2011). It differs from the models above in aiming at the smallest network and the shortest
training that still classify most digits correctly.

## 6 Conclusion

A perceptron of 2,410 parameters, trained for 50 epochs on raw pixel counts in a twentieth of a
second, labels about 91 % of held-out 8×8 handwritten digits correctly. With its fixed splits and
seeds, TinyMLP is a reproducible reference point for this dataset.

## References

- Alpaydin, E. and Kaynak, C. (1998). Optical Recognition of Handwritten Digits [Dataset]. UCI
  Machine Learning Repository. https://doi.org/10.24432/C50P49
- Cortes, C. and Vapnik, V. (1995). Support-vector networks. *Machine Learning*, 20(3), 273–297.
  https://doi.org/10.1007/BF00994018
- Glorot, X. and Bengio, Y. (2010). Understanding the difficulty of training deep feedforward
  neural networks. In *Proceedings of the Thirteenth International Conference on Artificial
  Intelligence and Statistics (AISTATS)*, PMLR 9, 249–256.
- Kaynak, C. (1995). *Methods of Combining Multiple Classifiers and Their Applications to
  Handwritten Digit Recognition.* MSc thesis, Institute of Graduate Studies in Science and
  Engineering, Bogazici University.
- Kingma, D. P. and Ba, J. (2015). Adam: A method for stochastic optimization. In *International
  Conference on Learning Representations (ICLR)*. arXiv:1412.6980.
- LeCun, Y., Bottou, L., Bengio, Y. and Haffner, P. (1998). Gradient-based learning applied to
  document recognition. *Proceedings of the IEEE*, 86(11), 2278–2324.
- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M.,
  Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher,
  M., Perrot, M. and Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of
  Machine Learning Research*, 12, 2825–2830.
- Rumelhart, D. E., Hinton, G. E. and Williams, R. J. (1986). Learning representations by
  back-propagating errors. *Nature*, 323(6088), 533–536.
