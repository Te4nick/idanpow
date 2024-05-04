from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from uuid import UUID
from .serializers import (
    PowerSquareMatrixSerializer,
    ValidationErrorSerializer,
    OperationSerializer,
    GetOperationQuerySerializer,
    MultiplyMatrixSerializer,
)
from .services import NPMatrixService
from .services.operation_service import OperationService


class NPMatrixViewSet(ViewSet):
    ops_service = OperationService()

    @extend_schema(
        summary="Post matrix and exponent to execute power operation",
        request=PowerSquareMatrixSerializer,
        responses={
            status.HTTP_200_OK: OperationSerializer,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: None,
        },
        auth=False,
    )
    @action(detail=False, methods=["POST"])
    def post_pow_matrix(self, request):
        try:
            serializer = PowerSquareMatrixSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data=ValidationErrorSerializer({"errors": serializer.errors}).data,
                )

            op_id = self.ops_service.execute_operation(
                func=NPMatrixService.pow,
                args=(
                    serializer.validated_data["matrix"],
                    serializer.validated_data["exponent"],
                ),
            )
            op = self.ops_service.get_operation(op_id)
            return Response(
                status=status.HTTP_200_OK,
                data=OperationSerializer(op).data,
            )
        except:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Get matrix power operation details",
        parameters=[GetOperationQuerySerializer],
        responses={
            status.HTTP_200_OK: OperationSerializer,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: None,
        },
        auth=False,
    )
    @action(detail=False, methods=["GET"])
    def get_pow_matrix_status(self, request):
        try:
            query_ser = GetOperationQuerySerializer(data=request.query_params)
            if not query_ser.is_valid():
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data=ValidationErrorSerializer({"errors": query_ser.errors}).data,
                )

            op = self.ops_service.get_operation(UUID(query_ser.data.get("id")))
            if op is None:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                status=status.HTTP_200_OK,
                data=OperationSerializer(
                    {
                        "id": op.id,
                        "done": op.done,
                        "result": {
                            "matrix": op.result,
                        },
                    }
                ).data,
            )
        except:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Post matrix and scalar to execute scalar multiplication operation",
        request=MultiplyMatrixSerializer,
        responses={
            status.HTTP_200_OK: OperationSerializer,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: None,
        },
        auth=False,
    )
    @action(detail=False, methods=["POST"])
    def post_mult_matrix(self, request):
        try:
            serializer = MultiplyMatrixSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data=ValidationErrorSerializer({"errors": serializer.errors}).data,
                )

            op_id = self.ops_service.execute_operation(
                func=NPMatrixService.mult,
                args=(
                    serializer.validated_data["matrix"],
                    serializer.validated_data["scalar"],
                ),
            )
            op = self.ops_service.get_operation(op_id)
            return Response(
                status=status.HTTP_200_OK,
                data=OperationSerializer(op).data,
            )
        except:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Get matrix scalar multiplication operation details",
        parameters=[GetOperationQuerySerializer],
        responses={
            status.HTTP_200_OK: OperationSerializer,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: None,
        },
        auth=False,
    )
    @action(detail=False, methods=["GET"])
    def get_mult_matrix_status(self, request):
        try:
            query_ser = GetOperationQuerySerializer(data=request.query_params)
            if not query_ser.is_valid():
                return Response(
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    data=ValidationErrorSerializer({"errors": query_ser.errors}).data,
                )

            op = self.ops_service.get_operation(UUID(query_ser.data.get("id")))
            if op is None:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                status=status.HTTP_200_OK,
                data=OperationSerializer(
                    {
                        "id": op.id,
                        "done": op.done,
                        "result": {
                            "matrix": op.result,
                        },
                    }
                ).data,
            )
        except:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
