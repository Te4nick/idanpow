import numpy as np


class NPMatrixService:
    @staticmethod
    def pow(matrix: list[list], exponent: int) -> list[list]:
        np_matrix = np.array(matrix)
        return np.linalg.matrix_power(np_matrix, exponent).tolist()

    @staticmethod
    def mult(matrix: list[list], scalar: int) -> list[list]:
        np_matrix = np.array(matrix)
        return (np_matrix * scalar).tolist()
