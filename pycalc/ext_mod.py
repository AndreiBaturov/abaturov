
import sys


def import_modules(_modules):

    global modules
    modules = _modules
    for module in _modules:
        try:
            globals()[module] = __import__(module)
        except ImportError:
            raise ImportError("Module not found:" + module)


def find_attr(attr_name):

    attr_name = attr_name.split('.')
    if len(attr_name) == 1:
        for module in modules:
            attr = getattr(sys.modules[module], attr_name[0], None)
            if attr is None:
                continue
            return attr
    else:
        if attr_name[0] in modules:
            attr = getattr(sys.modules[__name__], attr_name[0], None)
            for part in attr_name[1:]:
                attr = getattr(attr, part, None)
            if attr is not None:
                return attr
    raise ArithmeticError("Unknown function or constant:" + str(attr_name))
