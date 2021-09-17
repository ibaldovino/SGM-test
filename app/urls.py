# -*- encoding: utf-8 -*-
from django.conf.urls import url
from django.urls import path, re_path
from app.views import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    url(r"^user", views.UserListView.as_view(), name="page-user-list"),
    url(r'^ajax/user/delete/((?P<pk>\d+)$)?', views.ajax_del_user, name='ajax-user-delete'),
    url(r'^ajax/user/((?P<pk>\d+)$)?', views.ajax_save_user, name='ajax-user-save'),
    #re_path(r'^.*\.*', views.pages, name='pages'),
]
