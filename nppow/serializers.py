from rest_framework import serializers
import numpy as np


class MatrixSerializer(serializers.Serializer):
    matrix = serializers.ListField(
        min_length=2,
        child=serializers.ListField(
            min_length=2,
            child=serializers.FloatField(),
        ),
    )

    def validate_matrix(self, value):
        matrix = np.array(value)
        if matrix.ndim != 2:
            raise serializers.ValidationError("Matrix must be two-dimensional array")
        if matrix.shape[0] != matrix.shape[1]:
            raise serializers.ValidationError("Matrix must be square matrix")
        return value


class PowerMatrixSerializer(MatrixSerializer):
    exponent = serializers.IntegerField(min_value=2)  # TODO: max_value=?

    # def validate_exponent(self, value):
    #     if value < 1:
    #         raise serializers.ValidationError("Exponent must be a natural number")
    #     return value


class ValidationErrorSerializer(serializers.Serializer):
    errors = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField())
    )
