from django.conf.urls import include, url

# from .rest.router import urlpatterns as rest_urls
from .frontend.router import urlpatterns as frontend_urls

urlpatterns = [
    # url(r'^rest/', include(rest_urls)),
    url(r'^frontend/', include(frontend_urls))
]
