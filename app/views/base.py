import json

from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db.models.constants import LOOKUP_SEP
from django.http import HttpResponse
from django.shortcuts import reverse
from django.utils.encoding import force_text
from django.views import generic


def get_field_verbose_name(model, lookup):
    """
    Get field verbose_name, following across relationships

    Usage:
    >>> get_verbose_name(WoodProduct, 'commercial_name')
    u'Nombre Comercial'
    >>> get_verbose_name(WorkOrder, 'sale_order__country__name')
    u'Nombre'

    When not found, returns the given string
    >>> get_verbose_name(WorkOrder, 'foo')
    'foo'
    """

    parts = lookup.split(LOOKUP_SEP)
    for part in parts:
        try:
            f = model._meta.get_field(part)
        except FieldDoesNotExist:
            # check if field is related
            for f in model._meta.related_objects:
                if f.get_accessor_name() == part:
                    break
            else:
                return part
        if f.is_relation and part != parts[-1]:
            model = f.related_model
            continue
        return force_text(f.verbose_name)


def get_serializer_field_verbose_name(serializer_field, serializer):
    """
    Get verbose name for fields in django rest framework serializers.

    If a label is set explicitly, take that label. Otherwise try to get
    the field verbose name and lastly, if not found, just return the label
    created automatically by drf.
    """

    def get_defined_label(field, serializer):
        label = field.label
        field_name = field.field_name
        default_label = field_name.replace('_', ' ').capitalize()

        if label != default_label:
            return label
        else:
            extra = serializer.get_extra_kwargs()
            extra_for_field = extra.get(field_name, {})
            return extra_for_field.get('label')

    defined_label = get_defined_label(serializer_field, serializer)
    if defined_label is not None:
        verbose_name = defined_label

    else:
        model = serializer.Meta.model
        try:
            model_field = model._meta.get_field(serializer_field.field_name)
            verbose_name = model_field.verbose_name
        except FieldDoesNotExist:
            if serializer_field.source != '*':
                lookup = serializer_field.source.replace('.', '__')
                verbose_name = get_field_verbose_name(model, lookup)
            else:
                verbose_name = serializer_field.label

    return force_text(verbose_name)


class BaseListView(generic.ListView):
    template_name = 'layouts/list.html'

    @property
    def filterset_class(self):
        return getattr(self.viewset_class, 'filterset_class', None)

    @property
    def serializer_class(self):
        return self.viewset_class(request=self.request).get_serializer_class()

    def get_viewset_queryset(self, request):
        """
        Use get_queryset method already defined in the viewset_class.

        If the viewset_class has associated a filterset_class, also filter the data
        by the passed in request.
        """

        qs = self.viewset_class(request=request).get_queryset()
        if self.filterset_class:
            qs = self.filterset_class(data=request.GET, request=request, queryset=qs).qs
        return qs

    def get_api_url_name(self):
        """
        Get the url name for the api endpoint to retrieve the data for the list views.
        By default use 'fronted-{model_name}-list'. Can be changed by defining an attribute
        'api_url_name'.
        """
        model_name = self.model._meta.model_name
        api_url_name = getattr(self, 'api_url_name', 'frontend-%s-list' % model_name)
        return reverse(api_url_name)

    def get_context_data(self, **kwargs):
        """
        Add the following variables to the context

        * api_url:
            The api to get the objects from. By default it build the url as
            'frontend-{model_name}-list'. Can be overridden by setting a class
            attribute 'api_url_name' that must be a valid api url name.
        * columns:
            Build datatables column definitions.
        * filter:
            FilterSet instance if 'filterset_class' class attribute was provided.
        """
        if not kwargs.get('exclude_super', False):
            context = super().get_context_data(**kwargs)
        else:
            context = {}

        context['api_url'] = self.get_api_url_name()
        context['columns'] = json.dumps(self.get_datatables_columns_definitions())

        if self.filterset_class:
            context['filter'] = self.filterset_class(request=self.request)

        return context

    def get_datatables_columns_definitions(self):
        """
        Using the fields defined in the serializer_class, build the datatables 'columns' object with
        the following defaults:
            data: 
                field_name
            orderable: 
                set fields as orderable as long as the are model fields or annotated fields
            title: 
                grab either the label defined in the field or the model's field verbose name.
        """

        serializer = self.serializer_class()
        model = serializer.Meta.model
        opts = model._meta

        # use queryset to be able to get annotated field names
        queryset = self.get_viewset_queryset(self.request)
        annotated_fields = queryset.query.annotations.keys()

        columns = []

        for field_name, serializer_field in serializer.fields.items():

            col = {
                'id': 1,
                'data': field_name,
                'title': get_serializer_field_verbose_name(serializer_field, serializer)
            }

            try:
                opts.get_field(field_name)
            except FieldDoesNotExist:
                if field_name not in annotated_fields:
                    col['orderable'] = False

            columns.append(col)

        return columns

    def get(self, *args, **kwargs):
        request = args[0]
        if 'export' in request.GET:

            queryset = self.get_viewset_queryset(request=request)

            try:
                resource_class = self.resource_class
            except AttributeError:
                raise ImproperlyConfigured(
                    'Make sure a "resource_class" was defined in "%s" for excel export functionality' %
                    self.__class__.__name__
                )
            resource = resource_class(request=request)
            dataset = resource.export(queryset=queryset)
            filename = resource.export_name

            response = HttpResponse(content_type='application/excel')
            response["Content-Disposition"] = "attachment; filename=%s" % filename
            response.write(dataset.xls)

            return response

        return super().get(*args, **kwargs)
