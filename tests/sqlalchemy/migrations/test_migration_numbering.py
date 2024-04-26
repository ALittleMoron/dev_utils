from alembic.operations.ops import DowngradeOps, MigrationScript, UpgradeOps
from freezegun import freeze_time

from dev_utils.alembic.migration_numbering import process_revision_directives_datetime_order
from dev_utils.core.utils.datetime import get_utc_now


# FIXME: IDK, how to test my process_revision_directives functions.
# NOTE: At least, I tested them with real alembic.
def test_process_revision_directives_datetime_order() -> None:
    migrations = [MigrationScript(None, UpgradeOps(), DowngradeOps()) for _ in range(10)]
    now = get_utc_now()
    with freeze_time(now):
        process_revision_directives_datetime_order(None, None, migrations)  # type: ignore
    for migration in migrations:
        assert migration.rev_id == now.strftime("%Y%m%d%H%M%S")
