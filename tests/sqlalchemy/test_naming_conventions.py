from sqlalchemy import MetaData

from dev_utils.sqlalchemy.naming_conventions import GENERAL_NAMING_CONVENTION


# FIXME: IDK, how to test this.
# NOTE: At least, I tested them with real metadata in my project.
def test_general_naming_conventions() -> None:
    metadata = MetaData(naming_convention=GENERAL_NAMING_CONVENTION)
    assert metadata.naming_convention == GENERAL_NAMING_CONVENTION
