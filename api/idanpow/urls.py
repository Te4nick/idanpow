"""
URL configuration for idanpow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.urls import path
from nppow.views import NPMatrixViewSet

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path(
        "matrix/power",
        NPMatrixViewSet.as_view(
            {
                "get": "get_pow_matrix_status",
                "post": "post_pow_matrix",
            },
        ),
        name="matrix_power",
    ),
    path(
        "matrix/multiplication/scalar",
        NPMatrixViewSet.as_view(
            {
                "get": "get_mult_matrix_status",
                "post": "post_mult_matrix",
            },
        ),
        name="matrix_power",
    ),
]
