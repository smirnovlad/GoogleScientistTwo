from sklearn.neural_network import MLPClassifier
def build_model(seed):  # TinyMLP exactly, unscaled, but 200 epochs instead of 50
    return MLPClassifier(hidden_layer_sizes=(32,), max_iter=200, batch_size=200, random_state=seed)
