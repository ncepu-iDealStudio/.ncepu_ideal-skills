"""Validation helper placeholders."""


def validate_required(value, field_name):
    if value is None or value == "":
        raise ValueError(f"{field_name} is required")
    return True
