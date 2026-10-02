"""TinyMLP: a single-hidden-layer perceptron for 8x8 handwritten digits.

The network reads the 64 raw pixel counts of an 8x8 digit image (integers
0..16, no preprocessing) and predicts one of the 10 digit classes:

    64 inputs -> 32 ReLU units -> 10 softmax outputs   (2,410 parameters)

It is trained with Adam on the cross-entropy loss plus an L2 weight penalty,
for a fixed budget of 50 epochs of mini-batches of 200 images.
"""
from sklearn.neural_network import MLPClassifier

# Hyperparameters, as reported in the paper (Section 2).
HIDDEN_UNITS = 32
EPOCHS = 50
BATCH_SIZE = 200
LEARNING_RATE = 1e-3
L2_PENALTY = 1e-4


def build_model(seed):
    """An untrained TinyMLP; its initial weights and batch order depend only on `seed`."""
    return MLPClassifier(
        hidden_layer_sizes=(HIDDEN_UNITS,),
        activation="relu",
        solver="adam",
        learning_rate_init=LEARNING_RATE,
        batch_size=BATCH_SIZE,
        alpha=L2_PENALTY,
        max_iter=EPOCHS,
        shuffle=True,
        random_state=seed,
    )
