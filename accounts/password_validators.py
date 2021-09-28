from django.core.exceptions import ValidationError
import re
from django.utils.translation import gettext as _


class LowerCasePasswordValidator():
    def validate(self, password, user=None):
        if not re.search("[a-z]", password):
            raise ValidationError(
                _("password must have a lowercase word"),
                code="lower_case",
            )

    def get_help_text(self):
        return _('password must have a lowercase word')


class UpperCasePasswordValidator():
    def validate(self, password, user=None):
        if not re.search("[A-Z]", password):
            raise ValidationError(
                _("password must have a uppercase word"),
                code="lower_case",
            )

    def get_help_text(self):
        return _('password must have a uppercase word')
