# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

ROLE_TYPES = [('full_admin', _('Full administrator')),
              ('admin', _('Administrator')),
              ('read_only_admin', _('Read only administrator')),
              ('operator', _('operator')),
              ('driver', _('Driver')),
              ('passenger', _('Passenger')),
              ('read_only_passenger', _('Read only passenger')),
              ]


class UserOffice(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Office'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('User office')
        verbose_name_plural = _('User offices')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    role = models.CharField(max_length=100, verbose_name=_('Role'), choices=ROLE_TYPES)
    office = models.ForeignKey(UserOffice, models.SET_NULL, verbose_name=_("Office"), related_name='users', default=None, null=True)

    def to_edit_form(self):
        return {'id_first_name': self.user.first_name,
                'id_last_name': self.user.last_name,
                'id_email': self.user.email,
                'id_username': self.user.username,
                'id_role': self.role,
                'id_office': self.office,
                'id_id': self.user.id
                }


    class Meta:
        verbose_name = _('User profile')
        verbose_name_plural = _('User profiles')
