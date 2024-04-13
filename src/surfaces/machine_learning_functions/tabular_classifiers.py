import numpy as np

from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import cross_val_score
from .datasets import digits_data, wine_data, iris_data

from .base_machine_learning_function import MachineLearningFunction


class KNeighborsClassifierFunction(MachineLearningFunction):
    name = "KNeighbors Classifier Function"
    _name_ = "k_neighbors_classifier"
    __name__ = "KNeighborsClassifierFunction"

    para_names = ["n_neighbors", "algorithm", "cv", "dataset"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def search_space(
        self,
        n_neighbors: list = None,
        algorithm: list = None,
        cv: list = None,
        dataset: list = None,
    ):
        search_space: dict = {}

        n_neighbors_default = list(np.arange(3, 150, 5))
        algorithm_default = ["auto", "ball_tree", "kd_tree", "brute"]
        cv_default = [2, 3, 4, 5, 8, 10]
        dataset_default = [digits_data, wine_data, iris_data]

        search_space["n_neighbors"] = (
            n_neighbors_default if n_neighbors is None else n_neighbors
        )
        search_space["algorithm"] = (
            algorithm_default if algorithm is None else algorithm
        )
        search_space["cv"] = cv_default if cv is None else cv
        search_space["dataset"] = dataset_default if dataset is None else dataset

        return search_space

    def create_objective_function(self):
        def k_neighbors_classifier(params):
            knc = KNeighborsClassifier(
                n_neighbors=params["n_neighbors"],
                algorithm=params["algorithm"],
            )
            X, y = params["dataset"]()
            scores = cross_val_score(knc, X, y, cv=params["cv"], scoring=self.metric)
            return scores.mean()

        self.pure_objective_function = k_neighbors_classifier
