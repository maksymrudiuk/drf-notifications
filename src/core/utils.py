def reserved_getattr(obj, attr, rattr):
    return getattr(obj, attr, getattr(obj, rattr, None))


def get_object_or_none(model, **kwargs):

    try:
        instance = model.objects.get(**kwargs)
    except (model.DoesNotExist, model.MultipleObjectsReturned):
        return None
    else:
        return instance


# https://github.com/LPgenerator/django-db-mailer/blob/master/dbmail/__init__.py
def import_module(*args, **kwargs):

    try:
        from django.utils.importlib import import_module
    except ImportError:
        from importlib import import_module
    return import_module(*args, **kwargs)


def import_by_string(dotted_path):
    """Import class by his full module path.
    Args:
        dotted_path - string, full import path for class.
    """
    from django.utils.module_loading import import_string

    return import_string(dotted_path)
