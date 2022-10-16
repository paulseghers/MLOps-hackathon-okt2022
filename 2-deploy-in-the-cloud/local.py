import pandas as pd
import seaborn as sns
from sklearn.svm import SVC
import pickle
from google.cloud import storage

FEATURES = "sepal_length  sepal_width  petal_length  petal_width".split()


def build_dataset():
    iris: pd.DataFrame = sns.load_dataset("iris")
    # print(iris)
    iris.to_csv("iris.csv", index=False)


def train_model():
    iris = pd.read_csv("iris.csv")
    X = iris[FEATURES]
    y = iris["species"]
    clf = SVC().fit(X, y)
    return clf


def save_model(clf):
    with open("model.pkl", "wb") as fp:
        pickle.dump(clf, fp)
    # clf_bytes = pickle.dumps(clf)
    # storage.Client().bucket("mybuck").blob("myblob").upload_from_string(clf_bytes)


def load_model():
    with open("model.pkl", "rb") as fp:
        clf = pickle.load(fp)
    # clf_bytes = storage.Client().bucket("mybuck").get_blob("myblob").download_as_bytes()
    # clf = pickle.loads(clf_bytes)
    return clf


def test_model(clf):
    sample = dict(zip(FEATURES, range(len(FEATURES))))
    preds = clf.predict(pd.DataFrame([sample]))
    print(list(preds))


if __name__ == "__main__":
    build_dataset()
    clf = train_model()
    save_model(clf)
    clf = load_model()
    test_model(clf)
