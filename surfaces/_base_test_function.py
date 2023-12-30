# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import time
import numpy as np
import pandas as pd
from functools import reduce

from hyperactive import Hyperactive
from hyperactive.optimizers import GridSearchOptimizer

from ..machine_learning.data_collector import SurfacesDataCollector


class ObjectiveFunction:
    explanation = """ """

    dimensions = " "
    formula = r" "
    global_minimum = r" "

    def __init__(self, metric="score", input_type="dictionary", sleep=0):
        self.metric = metric
        self.input_type = input_type
        self.sleep = sleep

        self.sql_data = SurfacesDataCollector()

    def search_space(self, min=-5, max=5, step=0.1, value_typ="array"):
        search_space_ = {}

        for dim in range(self.n_dim):
            dim_str = "x" + str(dim)

            values = np.arange(min, max, step)
            if value_typ == "list":
                values = list(values)
            search_space_[dim_str] = values

        return search_space_

    def collect_data(self, if_exists="append"):
        para_names = list(self.search_space().keys())
        search_data_cols = para_names + ["score"]
        search_data = pd.DataFrame([], columns=search_data_cols)
        search_data_length = 0

        dim_sizes_list = [len(array) for array in self.search_space().values()]
        search_space_size = reduce((lambda x, y: x * y), dim_sizes_list)

        while search_data_length < search_space_size:
            hyper = Hyperactive(verbosity=["progress_bar"])
            hyper.add_search(
                self.objective_function_dict,
                self.search_space(value_typ="list"),
                initialize={},
                n_iter=search_space_size,
                optimizer=GridSearchOptimizer(direction="orthogonal"),
                memory_warm_start=search_data,
            )
            hyper.run()

            search_data = pd.concat(
                [search_data, hyper.search_data(self.objective_function_dict)],
                ignore_index=True,
            )

            search_data = search_data.drop_duplicates(subset=para_names)
            search_data_length = len(search_data)

        self.sql_data.save(self.__name__, search_data, if_exists)

    def load_search_data(self):
        try:
            dataframe = self.sql_data.load(self.__name__)
        except:
            print("Path 2 database: ", self.sql_data.path)
        return dataframe

    def return_metric(self, loss):
        if self.metric == "score":
            return -loss
        elif self.metric == "loss":
            return loss

    def objective_function_np(self, *args):
        para = {}
        for i, arg in enumerate(args):
            dim_str = "x" + str(i)
            para[dim_str] = arg

        return self.objective_function_dict(para)

    def __call__(self, *input):
        time.sleep(self.sleep)

        if self.input_type == "dictionary":
            return self.objective_function_dict(*input)
        elif self.input_type == "arrays":
            return self.objective_function_np(*input)
