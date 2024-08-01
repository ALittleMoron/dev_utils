"""Module with objects core utils.

Contains functions to inspect objects or extract information from them
"""

import inspect


def get_object_class_absolute_name(obj: object) -> str:
    """Get any object class absolute name.

    Absolute name is name with all modules, which this object is contains in. For example,
    we have package ``my_package`` with module ``my_module`` with class ``MyClass``. This Function
    will return ``my_package.my_module.MyClass``
    """
    class_ = obj if inspect.isclass(obj) else obj.__class__
    module = class_.__module__
    if module == "builtins":
        return class_.__qualname__
    return module + "." + class_.__qualname__
