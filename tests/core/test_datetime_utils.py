import datetime
import zoneinfo

import pytest
from freezegun import freeze_time

from dev_utils.core import utils
from tests.utils import generate_datetime_list


@pytest.mark.parametrize(
    "dt",
    generate_datetime_list(n=10, tz=zoneinfo.ZoneInfo("UTC")),
)
def test_get_utc_now(dt: datetime.datetime) -> None:  # noqa
    with freeze_time(dt):
        assert utils.get_utc_now() == dt
