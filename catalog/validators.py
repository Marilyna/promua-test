from wtforms import ValidationError

from catalog.models import User


class EmailUnique(object):
    """
    Validates that email was not used before. This validator will stop
    the validation chain on error.

    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(email=field.data)
        if user:
            if self.message is None:
                message = field.gettext('This email is already registered')
            else:
                message = self.message

            raise ValidationError(message)
