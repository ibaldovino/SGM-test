# -*- encoding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include  # add this
from django.views.i18n import JavaScriptCatalog
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from core import settings

urlpatterns = [
    path('admin', admin.site.urls),  # Django admin route
    path("", include("authentication.urls")),  # Auth routes - login / register
    path('api/v1/', include("api.urls")),  # API v1
    path('specz/', SpectacularAPIView.as_view(), name='specz'),  # OPENAPI
    path('swagger/', SpectacularSwaggerView.as_view(url_name='specz'), name='swagger'),  # swagger
    path("", include("app.urls")),  # UI Kits Html files
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^rosetta/', include('rosetta.urls')),
        path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),

    ]
