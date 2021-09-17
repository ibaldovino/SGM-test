# -*- encoding: utf-8 -*-


from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from api.frontend.viewsets import UserViewSet
from app.views.base import BaseListView
from app.views.forms import UserForm, UserProfileForm, UserFormWithoutPassword
from authentication.views import role_check


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('pages/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
@role_check(('full_admin', 'admin', 'operator'))
def ajax_save_user(request, pk=None):
    msg = {'status': _('Unexpected problem')}
    errors = None
    if request.method == "POST":

        inst = User.objects.get(id=pk) if pk is not None else None
        form = UserForm(request.POST, instance=inst) if pk is None \
            else UserFormWithoutPassword(request.POST, instance=inst)

        if form.is_valid():
            try:
                user = form.save(False)
                if pk is None:
                    validate_password(form.clean().get('password', ''))
                    user.password = make_password(form.data['password'])
                formp = UserProfileForm(request.POST)
                if formp.is_valid():
                    profile = formp.save(False)
                    user.save()
                    profile.user = user
                    profile.save()
                    msg = {'status': 'Ok'}
                else:
                    errors = [{"id": 'id_' + name, "error": ', '.join(errors)} for name, errors in formp.errors.items()]
            except ValidationError as ex:
                errors = [{"id": 'id_password', "error": ' '.join(ex.messages)}]

        else:
            errors = [{"id": 'id_' + name, "error": '. '.join(errors)} for name, errors in form.errors.items()]

    if errors is not None:
        msg = {'status': 'Form Invalid', 'errors': errors}

    return JsonResponse(msg)


@login_required(login_url="/login/")
@role_check(('full_admin', 'admin', 'operator'))
def ajax_del_user(request, pk):
    msg = {'status': _('Unexpected problem')}
    if request.method == "POST":

        inst = User.objects.get(id=pk)
        inst.is_active = False
        inst.save()
        msg = {'status': 'Ok'}

    return JsonResponse(msg)


@method_decorator(role_check(('full_admin', 'admin', 'operator')), name='dispatch')
class UserListView(BaseListView):
    model = User
    viewset_class = UserViewSet
    template_name = 'pages/user-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('User list')
        context['add_button'] = True
        context['form_add'] = [UserForm(), UserProfileForm()]
        context['form_add_url'] = ''
        return context
