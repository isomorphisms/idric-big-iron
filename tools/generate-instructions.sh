#!/bin/sh
set -eu

# Generate the complete IBM z/Architecture instruction CSV from the current
# SA22-7832-14 Principles of Operation using the pinned Go architecture parser.
#
# Usage:
#   ./tools/generate-instructions.sh /path/to/SA22-7832-14.pdf [output.csv]

PDF=${1:?usage: generate-instructions.sh SA22-7832-14.pdf [output.csv]}
OUT=${2:-instructions.csv}
PIN=2549b772bfe5d4fab95e77428ecbed712cc73004

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT HUP INT TERM

git clone --filter=blob:none --no-checkout https://github.com/golang/arch "$work/arch"
git -C "$work/arch" checkout "$PIN" -- s390x/s390xspec go.mod go.sum

(
    cd "$work/arch"
    go run ./s390x/s390xspec "$PDF"
) > "$OUT"

# Refuse an extraction that silently produced nothing or malformed rows.
python3 - "$OUT" <<'PY'
import csv, pathlib, sys
p = pathlib.Path(sys.argv[1])
lines = [x for x in p.read_text(encoding='utf-8').splitlines() if x.strip() and not x.lstrip().startswith('#')]
rows = list(csv.reader(lines))
if not rows:
    raise SystemExit('no instruction rows extracted')
if any(len(r) < 3 for r in rows):
    raise SystemExit('malformed instruction row')
print(f'{len(rows)} instruction/form rows -> {p}', file=sys.stderr)
PY
