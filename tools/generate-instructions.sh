#!/bin/sh
set -eu

# Evaluate the exact pinned LLVM X86 TableGen source rather than grepping .td
# files: multiclasses generate many concrete instruction records.
#
# Usage:
#   ./tools/generate-instructions.sh [output-dir]

OUT=${1:-instructions}
PIN=74253d0e4f01fca3c2cc526aee9d073af3fad919
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT HUP INT TERM
mkdir -p "$OUT"

git clone --filter=blob:none https://github.com/llvm/llvm-project "$work/llvm-project"
git -C "$work/llvm-project" checkout "$PIN"

cmake -S "$work/llvm-project/llvm" -B "$work/build" \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_TARGETS_TO_BUILD=X86 \
  -DLLVM_INCLUDE_TESTS=OFF \
  -DLLVM_INCLUDE_EXAMPLES=OFF \
  -DLLVM_INCLUDE_BENCHMARKS=OFF \
  -DLLVM_BUILD_TOOLS=OFF
cmake --build "$work/build" --target llvm-tblgen

"$work/build/bin/llvm-tblgen" --dump-json \
  -I "$work/llvm-project/llvm/include" \
  -I "$work/llvm-project/llvm/lib/Target/X86" \
  "$work/llvm-project/llvm/lib/Target/X86/X86.td" \
  > "$OUT/tablegen-records.json"

python3 - "$OUT" "$PIN" <<'PY'
import csv, hashlib, json, pathlib, sys
out = pathlib.Path(sys.argv[1])
pin = sys.argv[2]
raw = (out / 'tablegen-records.json').read_bytes()
data = json.loads(raw)

# llvm-tblgen --dump-json uses top-level record-name keys plus metadata keys.
rows = []
for name, rec in data.items():
    if name.startswith('!') or not isinstance(rec, dict):
        continue
    supers = rec.get('!superclasses', [])
    if not isinstance(supers, list) or 'Instruction' not in supers:
        continue
    asm = rec.get('AsmString', '')
    pseudo = rec.get('isPseudo', False)
    namespace = rec.get('Namespace', '')
    predicates = rec.get('Predicates', [])
    rows.append((name, asm, pseudo, namespace, json.dumps(predicates, sort_keys=True), rec))

if not rows:
    raise SystemExit('no Instruction-derived TableGen records found')

with (out / 'instructions.tsv').open('w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, dialect='excel-tab', lineterminator='\n')
    w.writerow(['record', 'asm_string', 'is_pseudo', 'namespace', 'predicates'])
    for name, asm, pseudo, namespace, predicates, _ in sorted(rows):
        w.writerow([name, asm, pseudo, namespace, predicates])

with (out / 'instruction-records.jsonl').open('w', encoding='utf-8') as f:
    for name, _, _, _, _, rec in sorted(rows):
        f.write(json.dumps({'record': name, 'data': rec}, sort_keys=True) + '\n')

manifest = {
    'repository': 'llvm/llvm-project',
    'commit': pin,
    'target': 'X86',
    'tablegen_sha256': hashlib.sha256(raw).hexdigest(),
    'instruction_records': len(rows),
    'real_records': sum(not bool(r[2]) for r in rows),
    'pseudo_records': sum(bool(r[2]) for r in rows),
}
(out / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
PY
