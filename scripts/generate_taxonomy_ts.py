import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.detection.taxonomy import FailureCategory, FailureFamily

OUTPUT = ROOT / "frontend/src/lib/taxonomy.ts"


def generate_enum(name, values):
    lines = [f"export enum {name} {{"]

    for item in values:
        lines.append(f'  {item.name} = "{item.value}",')

    lines.append("}")
    return "\n".join(lines)


content = (
    "// Auto-generated from backend/app/detection/taxonomy.py\n"
    "// Do not edit manually.\n\n"
    + generate_enum("FailureFamily", FailureFamily)
    + "\n\n"
    + generate_enum("FailureCategory", FailureCategory)
    + "\n"
)

if "--check" in sys.argv:
    if not OUTPUT.exists() or OUTPUT.read_text() != content:
        print("FAIL: TypeScript taxonomy is out of sync.")
        sys.exit(1)
    print("PASS: TypeScript taxonomy is synchronized.")
else:
    OUTPUT.write_text(content)
    print("Generated frontend/src/lib/taxonomy.ts")
