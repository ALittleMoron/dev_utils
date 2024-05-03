from fastapi import status
from fastapi.testclient import TestClient

expected_error_422_result = {
    "code": "multiple",
    "type": "multiple",
    "message": "Multiple errors ocurred. Please check list for nested_errors.",
    "attr": None,
    "location": None,
    "nested_errors": [
        {
            "code": "validation_error",
            "type": "literal_error",
            "message": "Input should be 1 or 2",
            "attr": "a",
            "location": "query",
        },
        {
            "code": "validation_error",
            "type": "missing",
            "message": "Field required",
            "attr": "b",
            "location": "query",
        },
    ],
}
base_500_result = {
    "code": "server_error",
    "type": "server_error",
    "attr": None,
    "location": None,
}
expected_error_500_result = {
    **base_500_result,
    "message": "Unexpected server error was found: test.",
}
expected_http_exception_500_result = {
    **base_500_result,
    "message": "test detail",
}


def test_all_verbose_handlers_422(test_app_all_verbose: TestClient) -> None:
    response = test_app_all_verbose.get("/?a=25")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == expected_error_422_result


def test_all_verbose_handlers_http(test_app_all_verbose: TestClient) -> None:
    response = test_app_all_verbose.get("/error")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == expected_http_exception_500_result


def test_all_verbose_handlers_http_verbose(test_app_all_verbose: TestClient) -> None:
    response = test_app_all_verbose.get("/verbose_error")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == expected_error_500_result


def test_only_verbose_handlers(test_app_only_verbose: TestClient) -> None:
    response = test_app_only_verbose.get("/")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == expected_error_500_result
