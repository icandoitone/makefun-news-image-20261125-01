#!/usr/bin/env python3
"""Write the 25 November 2026 front-page image to the output directory.

The entry image is held in this repository as entry.png; this program
simply copies it to $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png
when the variable is unset), so both graded runs produce identical bytes.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> int:
    if not SOURCE.is_file():
        print(f"entry.png not found next to {__file__}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    os.chmod(target, 0o644)
    # Guard against a truncated copy: the file must still start with the
    # PNG signature and end with the IEND chunk it was written with.
    data = target.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or not data.endswith(b"IEND\xaeB`\x82"):
        print("copied entry.png failed its integrity check", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
