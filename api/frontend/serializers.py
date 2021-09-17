from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class ChoiceDisplayField(serializers.ChoiceField):

    def to_representation(self, obj):
        if (obj == '' and self.allow_blank) or obj not in self._choices:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class UserSerializer(serializers.ModelSerializer):
    actions = serializers.SerializerMethodField()

    def get_actions(self, obj: User):
        if not hasattr(obj, 'profile'):
            return ''

        html = f"""<button type="button" class="btn btn-icon btn-rounded btn-warning" 
                    onclick="modal_add_object({obj.profile.to_edit_form()})"

                    data-toggle="tooltip" data-original-title="{_('Edit')}">
                        <i class="feather icon-edit"></i>
                    </button>

                    <button type="button" class="btn btn-icon btn-rounded btn-danger" 
                    onclick="modal_del_object({obj.id})" 
                    data-toggle="tooltip" data-original-title="{_('Delete')}">
                        <i class="feather icon-trash-2"></i>
                    </button>
                """
        return html

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'last_login', 'is_active', 'actions')
