import requests
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.renderers import DatatablesRenderer

from . import filters
from . import serializers


class BaseModelViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, DatatablesFilterBackend)
    permission_classes = [IsAuthenticated]
    pagination_class = DatatablesPageNumberPagination


class UserViewSet(BaseModelViewSet):
    serializer_class = serializers.UserSerializer
    filterset_class = filters.UserFilter

    @property
    def queryset(self):
        return User.objects.all()

