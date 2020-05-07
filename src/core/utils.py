def reserved_getattr(obj, attr, rattr):
    return getattr(obj, attr, getattr(obj, rattr, None))


def get_object_or_none(model, **kwargs):

    try:
        instance = model.objects.get(**kwargs)
    except (model.DoesNotExist, model.MultipleObjectsReturned):
        return None
    else:
        return instance
