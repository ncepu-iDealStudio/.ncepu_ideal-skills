"""Common helper utilities."""


def put_remove_none(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}
