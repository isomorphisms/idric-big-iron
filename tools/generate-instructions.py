#!/usr/bin/env python3
"""Snapshot every row of the pinned Go POWER instruction CSV."""

from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import urllib.request

PIN = "2549b772bfe5d4fab95e77428ecbed712cc73004"
URL = f"https://raw.githubusercontent.com/golang/arch/{PIN}/ppc64/pp64.csv"


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "instructions")
    out.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(URL) as r:
        raw = r.read()
    (out / "pp64.csv").write_bytes(raw)

    text = raw.decode("utf-8")
    data_lines = [line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    rows = list(csv.reader(io.StringIO("\n".join(data_lines))))
    if not rows or any(len(row) != 4 for row in rows):
        raise SystemExit("unexpected pp64.csv schema")

    with (out / "instructions.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, dialect="excel-tab", lineterminator="\n")
        w.writerow(["index", "instruction", "mnemonic_form", "encoding", "introduced"])
        for i, row in enumerate(rows):
            w.writerow([i, *row])

    manifest = {
        "repository": "golang/arch",
        "commit": PIN,
        "source": URL,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "rows": len(rows),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
