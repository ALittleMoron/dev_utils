"""Module with all dev_utils project exceptions.

All exceptions depends on BaseDevError. If you work with dev_utils and don't know, what error will
be raised, use try-except with BaseDevError.
"""

# |--------------| BASE |--------------|


class BaseDevError(Exception):
    """Base dev_utils exception class."""


# |--------------| MODELS |--------------|


class NoDeclarativeModelError(BaseDevError):
    """Exception for Table object, that not mapped to DeclarativeBase model.

    Needs, because non-declarative models are not supported.
    """


class NoModelAttributeError(BaseDevError):
    """Exception for incorrect model field name: field not found in given model."""


class NoModelRelationshipError(NoModelAttributeError):
    """Exception for incorrect model relationship name: relationship not found in given model."""


# |--------------| FILTERS |--------------|


class FilterError(BaseDevError):
    """General filter error of incorrect work of FilterConverters."""


# |--------------| PROFILING |--------------|


class ProfilingError(BaseDevError):
    """General profiling error of incorrect work of profiler or profiling middlewares."""
