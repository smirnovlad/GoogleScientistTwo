from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
def build_model(seed):  # deterministic: the seed is unused
    return make_pipeline(StandardScaler(), SVC(kernel='rbf', C=10.0, gamma='scale'))
