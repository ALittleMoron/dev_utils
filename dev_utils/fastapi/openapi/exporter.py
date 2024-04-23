import argparse
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml
from uvicorn.importer import import_from_string

from dev_utils.core.logging import logger

if TYPE_CHECKING:
    from fastapi import FastAPI


def get_openapi_specs_from_string(
    app: str = "mail:app",
    app_dir: str | None = None,
) -> dict[str, Any]:
    """Get OpenAPI specifications for given FastAPI app."""
    if app_dir is not None:
        logger.info("adding %s to sys.path", app_dir)
        sys.path.insert(0, app_dir)
    logger.info("importing app from %s", app)
    fastapi_instance: "FastAPI" = import_from_string(app)
    openapi = fastapi_instance.openapi()
    return openapi


def export_openapi_file(
    app: str = "mail:app",
    app_dir: str | None = None,
    out: str = "openapi.yaml",
) -> None:
    """Export OpenAPI schema to file."""
    openapi = get_openapi_specs_from_string(app, app_dir)
    version = openapi.get("openapi", "unknown version")
    logger.info("writing openapi spec v%s", version)
    with Path(out).open("w", encoding="utf8") as f:
        if out.endswith(".json"):
            json.dump(openapi, f, indent=2, ensure_ascii=False)
        else:
            yaml.dump(openapi, f, sort_keys=False, allow_unicode=True)
    logger.info("spec written to %s", version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="exporter.py")
    parser.add_argument(
        "app",
        help='App import string. Eg. "main:app"',
        default="mail:app",
    )
    parser.add_argument(
        "--app-dir",
        help="Directory containing the app",
        default=None,
    )
    parser.add_argument(
        "--out",
        help="Output file ending in .json or .yaml",
        default="openapi.yaml",
    )
    args = parser.parse_args()
    export_openapi_file(app=args.app, app_dir=args.app_dir, out=args.out)
