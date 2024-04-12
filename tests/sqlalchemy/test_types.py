import datetime
import zoneinfo
from typing import TYPE_CHECKING, Any

import pytest
from mimesis import Datetime

from tests.utils import TableWithUTCDT, create_db_item_sync

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from tests.types import SyncFactoryFunctionProtocol


UTC = zoneinfo.ZoneInfo("UTC")


@pytest.fixture()
def table_create(
    dt_faker: Datetime,
) -> "SyncFactoryFunctionProtocol[TableWithUTCDT]":
    def _create(
        session: "Session",
        *,
        commit: bool = False,
        **kwargs: Any,  # noqa: ANN401
    ) -> TableWithUTCDT:
        params: dict[str, Any] = dict(
            dt_field=dt_faker.datetime(),
        )
        params.update(kwargs)
        return create_db_item_sync(session, TableWithUTCDT, params, commit=commit)

    return _create


@pytest.mark.parametrize(
    ("dt", "tzinfo_presents"),
    [
        (datetime.datetime.now(), False),  # noqa: DTZ005
        (datetime.datetime.now(tz=UTC), True),  # noqa: DTZ005
    ],
)
def test_dt_field(
    dt: datetime.datetime,
    tzinfo_presents: bool,
    db_sync_session: "Session",
    table_create: "SyncFactoryFunctionProtocol[TableWithUTCDT]",
) -> None:
    item = table_create(db_sync_session, dt_field=dt, commit=True)
    if tzinfo_presents:
        assert item.dt_field.tzinfo is not None
        assert item.dt_field.tzinfo == UTC
    else:
        assert item.dt_field.tzinfo is None
