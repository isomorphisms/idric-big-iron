#!/usr/bin/env python3
"""Snapshot the complete Arm AARCHMRS 2026-03 data and isolate A64.

The raw Arm JSON files are the completeness oracle.  The normalized A64 subtree
is a convenience view and generation fails rather than guessing if the schema
no longer exposes one unambiguous A64 instruction-set node.
"""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import urllib.request

URL = "https://developer.arm.com/-/cdn-downloads/permalink/Exploration-Tools-OS-Machine-Readable-Data/AARCHMRS_BSD/AARCHMRS_OPENSOURCE_A_profile_FAT-2026-03.tar.gz"
FILES = ("Instructions.json", "Features.json", "Registers.json")


def walk(value, path=()):
    yield path, value
    if isinstance(value, dict):
        for k, v in value.items():
            yield from walk(v, path + (str(k),))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from walk(v, path + (str(i),))


def scalar_name(obj):
    if not isinstance(obj, dict):
        return None
    for key in ("name", "id", "title", "instruction_set", "instructionSet"):
        value = obj.get(key)
        if isinstance(value, str):
            return value
    return None


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "instructions")
    out.mkdir(parents=True, exist_ok=True)

    with urllib.request.urlopen(URL) as r:
        package = r.read()
    (out / "AARCHMRS_OPENSOURCE_A_profile_FAT-2026-03.tar.gz").write_bytes(package)

    extracted = {}
    with tarfile.open(fileobj=io.BytesIO(package), mode="r:gz") as tf:
        for member in tf.getmembers():
            base = Path(member.name).name
            if base not in FILES or not member.isfile():
                continue
            f = tf.extractfile(member)
            if f is None:
                continue
            data = f.read()
            extracted[base] = data
            (out / base).write_bytes(data)

    missing = sorted(set(FILES) - set(extracted))
    if missing:
        raise SystemExit(f"missing expected AARCHMRS files: {missing}")

    instructions = json.loads(extracted["Instructions.json"])
    candidates = []
    for path, value in walk(instructions):
        name = scalar_name(value)
        if name and name.strip().upper() == "A64":
            candidates.append((path, value))

    # Prefer the largest matching A64 node: the instruction-set container rather
    # than a nested cross-reference. Require it to be uniquely largest.
    sized = sorted(((len(json.dumps(v, sort_keys=True)), p, v) for p, v in candidates), reverse=True)
    if not sized:
        raise SystemExit("could not find an A64 node in Instructions.json")
    if len(sized) > 1 and sized[0][0] == sized[1][0]:
        raise SystemExit("ambiguous A64 nodes in Instructions.json")
    _, a64_path, a64 = sized[0]
    (out / "A64.json").write_text(json.dumps(a64, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    names = set()
    for _, value in walk(a64):
        if isinstance(value, dict):
            for key in ("mnemonic", "name", "title"):
                v = value.get(key)
                if isinstance(v, str) and v.strip():
                    names.add(v.strip())
    (out / "A64-names.txt").write_text("\n".join(sorted(names)) + "\n", encoding="utf-8")

    manifest = {
        "source": URL,
        "package_sha256": hashlib.sha256(package).hexdigest(),
        "a64_json_path": list(a64_path),
        "files": {
            name: {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            for name, data in sorted(extracted.items())
        },
        "a64_indexed_names": len(names),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
