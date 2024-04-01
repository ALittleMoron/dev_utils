from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_middlewares_correct_install(
    test_sync_app: 'TestClient',
) -> None:
    result = test_sync_app.get('/')  # type: ignore
    jsn = result.json()  # type: ignore
    assert isinstance(jsn, list)
    assert len(jsn) == 10  # type: ignore
