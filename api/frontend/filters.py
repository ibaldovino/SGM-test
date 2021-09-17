from django.contrib.auth.models import User

from common.filters import BaseFilter
from common.filters.filters import DateTimeFromFilter, DateTimeUntilFilter


class UserFilter(BaseFilter):
    # date_created_from = DateTimeFromFilter(field_name="created")
    # date_created_until = DateTimeUntilFilter(field_name="created")
    # process = BooleanFilter(field_name="process", reverse=True)
    last_login_from = DateTimeFromFilter(field_name="last_login", input_formats=['%d/%m/%y %H:%M'])
    last_login_until = DateTimeUntilFilter(field_name="last_login", input_formats=['%d/%m/%y %H:%M'])

    class Meta:
        model = User
        fields = ('first_name', 'email', 'last_login_from', 'last_login_until', 'id', 'is_active')
