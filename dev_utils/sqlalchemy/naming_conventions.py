"""Module with naming conventions."""

GENERAL_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
"""Naming convention for MetaData object.

General convention, that you can find in any tutorials or in alembic documentation:

https://alembic.sqlalchemy.org/en/latest/naming.html

Usage
-----

as separate metadata:
```
from sqlalchemy import MetaData
from dev_utils.sqlalchemy.naming_conventions import GENERAL_NAMING_CONVENTION

metadata = MetaData(naming_convention=GENERAL_NAMING_CONVENTION)
```

as DeclarativeBase metadata:
```
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from dev_utils.sqlalchemy.naming_conventions import GENERAL_NAMING_CONVENTION

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=GENERAL_NAMING_CONVENTION)
```
"""
