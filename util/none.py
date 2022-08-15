
def has_none(*args, **kwargs):
    if args:
        return None in args
    if kwargs:
        return None in kwargs.values()


