import django_filters as filters
from django import forms
from django.utils.translation import gettext as _

BOOLEAN_CHOICES = (
    (True, _('Yes')),
    (False, _('No')),
)

NULL_BOOLEAN_CHOICES = ((None, ''),) + BOOLEAN_CHOICES


def get_date_widget():
    return forms.DateInput(attrs={'class': 'datepicker'})


def get_datetime_widget():
    return forms.DateInput(attrs={'class': 'datetimepicker'})


class DateFromFilter(filters.DateTimeFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'Fecha inicial')
        kwargs.setdefault('lookup_expr', 'gte')
        kwargs.setdefault('widget', get_date_widget())
        super().__init__(*args, **kwargs)


class DateUntilFilter(filters.DateTimeFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'Fecha final')
        kwargs.setdefault('lookup_expr', 'lte')
        kwargs.setdefault('widget', get_date_widget())
        super().__init__(*args, **kwargs)


class DateTimeFromFilter(filters.DateTimeFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'Fecha inicial')
        kwargs.setdefault('lookup_expr', 'gte')
        kwargs.setdefault('widget', get_datetime_widget())
        super().__init__(*args, **kwargs)


class DateTimeUntilFilter(filters.DateTimeFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'Fecha final')
        kwargs.setdefault('lookup_expr', 'lte')
        kwargs.setdefault('widget', get_datetime_widget())
        super().__init__(*args, **kwargs)


class BooleanFilter(filters.BooleanFilter):
    def __init__(self, reverse=False, *args, **kwargs):
        c = BOOLEAN_CHOICES
        if reverse:
            c = list(c)
            c.reverse()
            c = tuple(c)
        widget = forms.Select(choices=c, attrs={"class": "select2"})
        kwargs.setdefault('widget', widget)
        super().__init__(*args, **kwargs)


class NullBooleanFilter(filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        widget = forms.Select(choices=NULL_BOOLEAN_CHOICES)
        kwargs.setdefault('widget', widget)
        super().__init__(*args, **kwargs)


class ModelChoiceFilter(filters.ModelChoiceFilter):
    def __init__(self, *args, **kwargs):
        widget = forms.Select(attrs={"class": "select2"})
        kwargs.setdefault('widget', widget)
        super().__init__(*args, **kwargs)


class ChoiceFilter(filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        widget = forms.Select(attrs={"class": "select2"})
        kwargs.setdefault('widget', widget)
        super().__init__(*args, **kwargs)
