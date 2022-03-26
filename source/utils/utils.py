"""
Implements functions, classes, methods for another services and providers
"""


def clear_from_ellipsis(
    **kwargs: dict[any, any]
) -> dict[any, any]:
    """
    Clears passed kwargs from ellipsis(...) and
    returns dict that not contains ellipsis as value.
    And in addition it works recursively
    """
    cleared_kwargs = {}
    for key, value in kwargs.items():
        if value is ...:
            continue

        cleared_kwargs[key] = value

        if type(value) is dict:
            cleared_kwargs[key] = clear_from_ellipsis(**value)

    return cleared_kwargs
