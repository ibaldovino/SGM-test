from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django_filters import rest_framework as filters
from django_filters.filterset import FILTER_FOR_DBFIELD_DEFAULTS, FilterSetMetaclass

from .filters import BooleanFilter


class ImproperlyConfiguredFilter(Exception):
    pass


# Override default filter for foreign keys to our custom defined filter.
FILTER_FOR_DBFIELD_DEFAULTS[models.BooleanField]['filter_class'] = BooleanFilter

# set default lookup_expr 'icontains' for char filters
FILTER_FOR_DBFIELD_DEFAULTS[models.CharField]['extra'] = lambda f: {
    'lookup_expr': 'icontains'
}


class BaseFilter(filters.FilterSet):
    """
    Provide basic common functionality to FilterSet classes.

    * role_fields: 
       if 'role_fields' is set in the inner Meta class, the fields to be shown 
       will be the fields provided for the profile's role in 'role_fields'.

    * automatic filter ModelChoiceFilter queryset by the request's licensee:
        When a ModelChoiceFilter is used, it will automatically filter the
        queryset based on the request.licensee. This is achieved through overriding 
        the default filter for foreign keys and using the custom ByLicenseeModelChoiceFilter

    * automatic filter by licensee: 
        If the filtered model has a licensee attribute, automatically filter the resulting
        queryset by the request.licensee.

    * CharFilter: by default use 'icontains' lookup_expr

    * initial: 
        Filter fields can include the kwarg 'initial'.

    """

    FILTER_DEFAULTS = FILTER_FOR_DBFIELD_DEFAULTS

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        # request must be provided to see the user profile
        if request is None:
            raise ImproperlyConfigured(
                "Request is mandatory when instantiating FilterSet class"
            )

        # handle initial values
        if data is not None:
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get('initial')

                if not data.get(name) and initial is not None:
                    data[name] = initial

        super().__init__(data, queryset, request=request, prefix=prefix)

        role_fields = getattr(self.Meta, 'role_fields', None)
        if role_fields and self.request.profile.role in role_fields:
            role_filters = {}
            for field in role_fields[self.request.profile.role]:
                role_filters[field] = self.filters[field]
            self.filters = role_filters 

    @classmethod
    def get_role_fields(cls):
        role_fields = getattr(cls.Meta, 'role_fields', tuple())

    @classmethod
    def get_fields(cls):
        """
        Include fields declared in role_fields in Meta.fields
        """
        fields = cls._meta.fields or tuple()

        role_fields = cls.get_role_fields()
        if role_fields:
            fields = tuple(f for f in role_fields if f not in fields)

        if fields:
            cls._meta.fields = fields

        return super().get_fields()
