# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from authentication.models import UserProfile
from core.settings import ADMIN_EMAIL, ADMIN_USERNAME, ADMIN_PASSWORD

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('start')
        if User.objects.count() == 0:
            if None not in (ADMIN_EMAIL, ADMIN_USERNAME, ADMIN_PASSWORD):
                admin = User.objects.create_superuser(email=ADMIN_EMAIL,
                                                      username=ADMIN_USERNAME,
                                                      password=ADMIN_PASSWORD)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
                UserProfile(user=admin, role='full_admin').save()
                print(f'new admin {ADMIN_USERNAME} added')
            else:
                print('Your need set ADMIN_EMAIL, ADMIN_USERNAME, ADMIN_PASSWORD for use this command ')
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
