import numpy as np


class NPMatrixService:
    @staticmethod
    def pow(matrix: list[list], exponent: int) -> list[list] | str:
        np_matrix = np.array(matrix)
        try:
            return np.linalg.matrix_power(np_matrix, exponent).tolist()
        except np.linalg.LinAlgError as e:
            return e.args[0]
