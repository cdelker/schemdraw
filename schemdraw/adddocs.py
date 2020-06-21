''' Decorator function for appending class docstrings '''

def adddocs(original):
    def wrapper(target):
        target.__doc__ += '\n\n' + original.__doc__
        return target
    return wrapper