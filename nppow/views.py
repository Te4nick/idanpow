from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    PowerMatrixSerializer,
    MatrixSerializer,
    ValidationErrorSerializer,
)
from .services import NPMatrixService


@extend_schema(
    summary="Get power of matrix",
    request=PowerMatrixSerializer,
    responses={
        status.HTTP_200_OK: MatrixSerializer,
        status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
    },
    auth=False,
)
@api_view(["POST"])
def power_matrix(request):
    serializer = PowerMatrixSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            data=ValidationErrorSerializer({"errors": serializer.errors}).data,
        )

    result = NPMatrixService.pow(
        matrix=serializer.validated_data["matrix"],
        exponent=serializer.validated_data["exponent"],
    )

    if result is str:  # TODO: reimagine
        return Response(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            data=ValidationErrorSerializer({"errors": {"matrix": [result]}}).data,
        )

    return Response(
        status=status.HTTP_200_OK,
        data=MatrixSerializer({"matrix": result}).data,
    )
