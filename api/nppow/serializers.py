from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
import numpy as np


class SquareMatrixSerializer(serializers.Serializer):
    matrix = serializers.ListField(
        min_length=2,
        child=serializers.ListField(
            min_length=2,
            child=serializers.FloatField(),
        ),
    )
    _square_matrix: bool = True

    def validate_matrix(self, value):
        try:
            matrix = np.array(value)
            if matrix.ndim != 2:
                raise serializers.ValidationError(
                    "Matrix must be two-dimensional array"
                )
            if self._square_matrix and matrix.shape[0] != matrix.shape[1]:
                raise serializers.ValidationError("Matrix must be square matrix")
        except ValueError:
            raise serializers.ValidationError("Matrix rows must be the same length")
        return value


class PowerSquareMatrixSerializer(SquareMatrixSerializer):
    exponent = serializers.IntegerField(min_value=2, max_value=9_007_199_254_740_991)

    # def validate_exponent(self, value):
    #     if value < 1:
    #         raise serializers.ValidationError("Exponent must be a natural number")
    #     return value


class MatrixSerializer(SquareMatrixSerializer):
    _square_matrix: bool = False


class MultiplyMatrixSerializer(MatrixSerializer):
    scalar = serializers.FloatField()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Valid example 3",
            summary="Field required",
            description="Example when some required fields are missing",
            value={
                "errors": {
                    "id": ["This field is required"],
                },
            },
        ),
        OpenApiExample(
            "Valid example 4",
            summary="Matrix error",
            description="Example there is something wrong with provided matrix",
            value={
                "errors": {
                    "matrix": ["Matrix rows must be the same length"],
                },
            },
        ),
    ]
)
class ValidationErrorSerializer(serializers.Serializer):
    errors = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField())
    )


class GetOperationQuerySerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Valid example 1",
            summary="Operation Success",
            description="Operation successfully returned matrix",
            value={
                "id": "c3799cf2-6cf9-4925-916f-0736562e9930",
                "done": True,
                "result": {
                    "matrix": [[1, 2], [3, 4]],
                },
            },
            response_only=True,  # signal that example only applies to responses
        ),
        OpenApiExample(
            "Valid example 2",
            summary="Operation pending",
            description="Operation is pending for execution",
            value={
                "id": "c3799cf2-6cf9-4925-916f-0736562e9930",
                "done": False,
                "result": None,
            },
            response_only=True,  # signal that example only applies to responses
        ),
    ],
)
class OperationSerializer(GetOperationQuerySerializer):
    done = serializers.BooleanField()
    result = serializers.DictField()
