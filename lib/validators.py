from django.core.exceptions import ValidationError


def validate_password(password):
    if len(password) < 8:
        raise ValidationError(
            "password must be more that 8 characters", code="invalid")
