# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numpy as np

from .base_objective_function import ObjectiveFunction


class AckleyFunction(ObjectiveFunction):
    def __init__(self, A=20, B=2 * np.pi, metric="score", parameter_type="dictionary"):
        super().__init__(metric, parameter_type)
        self.__name__ = "ackley_function"

        self.A = A
        self.B = B

    def objective_function_dict(self, params):
        x = params["x0"]
        y = params["x1"]

        loss1 = -self.A * np.exp(-0.2 * np.sqrt(0.5 * (x * x + y * y)))
        loss2 = -np.exp(0.5 * (np.cos(self.B * x) + np.cos(self.B * y)))
        loss3 = np.exp(1)
        loss4 = self.A

        loss = loss1 + loss2 + loss3 + loss4

        return self.return_metric(loss)


class RastriginFunction(ObjectiveFunction):
    def __init__(
        self, n_dim, A=1, B=2 * np.pi, metric="score", parameter_type="dictionary"
    ):
        super().__init__(metric, parameter_type)
        self.__name__ = "rastrigin_function"

        self.n_dim = n_dim
        self.A = A
        self.B = B

    def objective_function_dict(self, params):
        loss = 0
        for dim in range(self.n_dim):
            dim_str = "x" + str(dim)
            x = params[dim_str]

            loss += self.A * self.n_dim + (x * x - self.A * np.cos(self.B * x))

        return self.return_metric(loss)


class RosenbrockFunction(ObjectiveFunction):
    def __init__(self, A=1, B=100, metric="score", parameter_type="dictionary"):
        super().__init__(metric, parameter_type)
        self.__name__ = "rosenbrock_function"

        self.A = A
        self.B = B

    def objective_function_dict(self, params):
        x = params["x0"]
        y = params["x1"]

        loss = (self.A - x) ** 2 + self.B * (y - x ** 2) ** 2

        return self.return_metric(loss)


class BealeFunction(ObjectiveFunction):
    def __init__(
        self, A=1.5, B=2.25, C=2.652, metric="score", parameter_type="dictionary"
    ):
        super().__init__(metric, parameter_type)
        self.__name__ = "beale_function"

        self.A = A
        self.B = B
        self.C = C

    def objective_function_dict(self, params):
        x = params["x0"]
        y = params["x1"]

        loss1 = (self.A - x + x * y) ** 2
        loss2 = (self.B - x + x * y ** 2) ** 2
        loss3 = (self.C - x + x * y ** 3) ** 2

        loss = loss1 + loss2 + loss3

        return self.return_metric(loss)
