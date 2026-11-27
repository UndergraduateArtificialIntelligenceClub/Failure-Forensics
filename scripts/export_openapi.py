"""Export or verify the committed OpenAPI v1 document."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.mock_server import app

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "openapi" / "openapi-v1.json"


def rendered_contract() -> str:
    return json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the committed contract does not match the FastAPI models",
    )
    args = parser.parse_args()
    rendered = rendered_contract()

    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text() != rendered:
            raise SystemExit(
                "openapi/openapi-v1.json is stale; run scripts/export_openapi.py"
            )
        return

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(rendered)
    print(f"wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
