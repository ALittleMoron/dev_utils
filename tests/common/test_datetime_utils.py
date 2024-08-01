import datetime
import zoneinfo

import pytest
from freezegun import freeze_time

from dev_utils.common import datetime as datetime_utils
from tests.utils import generate_datetime_list


@pytest.mark.parametrize(
    "dt",
    generate_datetime_list(n=10, tz=zoneinfo.ZoneInfo("UTC")),
)
def test_get_utc_now(dt: datetime.datetime) -> None:
    with freeze_time(dt):
        assert datetime_utils.get_utc_now() == dt
