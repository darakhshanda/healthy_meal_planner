from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class CustomPasswordValidator:
    """
    Custom password validator to enforce:
    - At least 8 characters
    - At least one uppercase letter
    - At least one number
    - At least one special character
    """

    def validate(self, password, user=None):
        """Validate password meets requirements"""
        errors = []

        # Check minimum length
        if len(password) < 8:
            errors.append(_("Password must be at least 8 characters long."))

        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            errors.append(
                _("Password must contain at least one uppercase letter."))

        # Check for number
        if not re.search(r'[0-9]', password):
            errors.append(_("Password must contain at least one number."))

        # Check for special character
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            errors.append(
                _("Password must contain at least one special character."))

        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        """Return help text for password requirements"""
        return _(
            "Your password must contain at least 8 characters,"
            " including one uppercase "
            "letter, one number, and one special character."
        )
