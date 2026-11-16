import subprocess
import sys
from pathlib import Path

from app.detection.taxonomy import FailureCategory, FailureFamily

ROOT = Path(__file__).resolve().parents[2]


def test_taxonomy_matches_architecture():
    architecture = (ROOT / "docs/design/architecture.md").read_text()

    expected_categories = set()

    for line in architecture.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]

        if len(cells) == 2 and cells[0] in FailureFamily.__members__:
            expected_categories.update(cells[1].split(", "))

    assert len(FailureFamily) == 6
    assert len(FailureCategory) == 31
    assert {c.value for c in FailureCategory} == expected_categories
    assert "PROPAGATION_ERROR" not in FailureCategory.__members__


def test_generated_typescript_is_synchronized():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/generate_taxonomy_ts.py"),
            "--check",
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
