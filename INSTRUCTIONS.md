# POWER complete instruction inventory

Status: exhaustive source-backed architecture inventory, independent of the Idriç implementation subset.

## Architecture pin

Primary architecture: **Power ISA Version 3.1C**, released 2024-05-26 by the OpenPOWER Foundation.

The OpenPOWER publication describes 3.1C as a **data cleanup** revision after 3.1B. Books I–III remain the architecture boundary: user instructions, virtual-environment/storage instructions, and operating-environment/supervisor instructions all belong to the architecture inventory even when Idriç initially emits only Linux user-mode scalar code.

## Machine-readable instruction table

Pin:

- repository: `golang/arch`
- commit: `2549b772bfe5d4fab95e77428ecbed712cc73004`
- file: `ppc64/pp64.csv`
- blob: `b2aa6b37edbf5dad8bb6f46125b685b7524313d4`

That CSV is generated from the Power ISA manual and contains one row per documented instruction description/form with four fields:

1. instruction headline;
2. assembler mnemonic/form;
3. complete instruction encoding field layout;
4. ISA version in which the instruction was introduced.

The checked source identifies itself as the POWER ISA 3.1B instruction description. Because OpenPOWER labels 3.1C as a data-cleanup revision, this is the normalized encoding table used here for the 3.1C branch boundary; the 3.1C publication remains the normative semantic source. If a future audit finds any 3.1C instruction-table delta, the generated inventory must be amended rather than silently treating 3.1B metadata as newer than it is.

## Included architectural surface

The complete generated table includes, without filtering for likely compiler use:

- scalar integer data movement, arithmetic, logical, rotate/mask, shifts and bit operations;
- condition-register production/manipulation;
- LR/CTR branches, calls, returns and indirect control flow;
- fixed-point loads/stores and endian-sensitive forms;
- floating-point instructions;
- VMX/AltiVec vector instructions;
- VSX scalar/vector instructions;
- decimal and conversion facilities;
- atomics/reservation instructions, barriers and cache/memory-control operations;
- prefixed instructions introduced in modern POWER;
- MMA and other architected matrix/vector facilities represented by the pinned table;
- privileged/system/hypervisor instructions present in the architecture data;
- compatibility/specialized instructions that an initial Idriç backend will never emit.

Assembler aliases are not allowed to create fictional extra encodings; each generated row preserves the manual headline, mnemonic/form and encoding together.

## Reproducible output

`tools/generate-instructions.py` downloads only the immutable CSV above, preserves every non-comment row in source order, verifies the four-column schema, and writes both the raw canonical CSV and a normalized TSV/JSON manifest with hashes and row counts.

The raw canonical CSV is always retained beside normalized output so a parser bug cannot silently erase instructions while still claiming completeness.

## Future codegen gate

This branch is inventory/research and claims no executable Idriç POWER backend. Open an emitted/tested support matrix only after an explicit reproducible assembler/linker/execution gate and a tiny exact source oracle. Complete architecture inventory does **not** mean a future backend implements VMX, VSX, MMA, privileged operations, or every legacy facility.
