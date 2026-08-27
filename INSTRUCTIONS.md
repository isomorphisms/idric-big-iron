# AArch64 / SVE complete instruction inventory

Status: exhaustive source-backed architecture inventory, independent of the Idriç implementation subset.

## Architecture pin

Pin the Arm A-profile machine-readable architecture release **2026-03**, the latest public A64 ISA release at the time of this inventory.

Normative/public machine-readable package:

`AARCHMRS_OPENSOURCE_A_profile_FAT-2026-03.tar.gz`

Arm publishes this package under its open-source machine-readable-data terms. The package contains:

- `Instructions.json` — A64, A32 and T32 instruction-set architecture data;
- `Features.json` — architecture feature/version constraints;
- `Registers.json` — AArch32/AArch64/memory-mapped system registers and system instructions;
- JSON schemas and documentation.

Arm's public A64 instruction documentation identifies **2026-03** as the latest release. A public mirror commit recording the exact package retrieval is `47b5446cf08ef6a46c86147c7deb0d56caf99d93` in Marc Zyngier's AARCHMRS mirror, with source URL:

`https://developer.arm.com/-/cdn-downloads/permalink/Exploration-Tools-OS-Machine-Readable-Data/AARCHMRS_BSD/AARCHMRS_OPENSOURCE_A_profile_FAT-2026-03.tar.gz`

## Complete branch surface

The complete inventory is every **A64** instruction/alias/encoding instance represented by the pinned `Instructions.json`, retaining its feature constraints from `Features.json`. That includes rather than filters out:

- baseline Armv8-A scalar A64;
- FP and Advanced SIMD/NEON;
- SVE and SVE2 scalable-vector/predicate instructions;
- SME/SME2 and later matrix/vector architecture represented in the release, kept feature-labelled rather than confused with SVE baseline;
- atomic/memory-ordering and synchronization instructions;
- cryptographic and specialized extensions;
- pointer authentication, memory tagging, RAS/security/control-flow facilities;
- system instructions and feature-gated newer Armv9.x operations represented in the machine data;
- aliases separated from real encoding instances.

This branch therefore carries a superset useful for comparing SVE/SVE2 and later facilities. A concrete processor profile selects feature constraints from this catalog; it does not rewrite the catalog.

## Reproducible extraction

`tools/generate-instructions.py` downloads the exact immutable 2026-03 tarball, extracts the canonical JSON files, hashes them, and emits:

- the raw `Instructions.json`, `Features.json`, and `Registers.json` untouched;
- a normalized A64-only JSON-lines index, preserving each source object and its path;
- a mnemonic/name index for navigation;
- a manifest with package/source hashes and row counts.

The raw Arm JSON is always retained. A normalizer bug therefore cannot make a partial list look complete.

## Idriç support

The initial Idriç backend can support only a tiny A64/SVE subset. That support matrix is separate. Unsupported architecture instructions remain in this complete inventory.
