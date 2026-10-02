from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
def build_model(seed):  # TinyMLP exactly (32 units, 50 epochs, batch 200), plus input standardisation
    return make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(32,), max_iter=50, batch_size=200, random_state=seed))
