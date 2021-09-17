# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import UserOffice, UserProfile


@admin.register(UserOffice)
class UserOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'office')
    list_filter = ('user', 'office')
