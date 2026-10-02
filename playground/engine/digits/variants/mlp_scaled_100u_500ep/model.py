from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
def build_model(seed):
    return make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=seed))
