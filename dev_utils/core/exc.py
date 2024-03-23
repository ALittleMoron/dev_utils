# |--------------| BASE |--------------|


class BaseSQLRepoError(Exception):
    """"""


# |--------------| MODELS |--------------|


class NoDeclarativeModelError(BaseSQLRepoError):
    """"""


class NoModelAttributeError(BaseSQLRepoError):
    """"""


class NoModelRelationshipError(NoModelAttributeError):
    """"""


class NoModelFieldError(NoModelAttributeError):
    """"""


# |--------------| FILTERS |--------------|


class FilterError(BaseSQLRepoError):
    """"""
