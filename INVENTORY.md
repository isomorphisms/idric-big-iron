# Architecture inventory invariant

Every architecture branch in this repository must preserve **complete architecture knowledge separately from the Idriç subset that happens to be implemented**.

A branch is not considered inventoried merely because it links a manual or names instruction families.

## Required artifacts

Each `arch/*` branch must carry an exhaustive, reproducible inventory containing at least:

- the exact ISA/specification revision being described;
- every architectural instruction mnemonic in that pinned scope;
- instruction/encoding variants when the architecture gives them distinct encodings or semantics;
- operand forms and programmer-visible effects needed to distinguish those variants;
- extension/facility/version membership;
- user/problem-state versus privileged/system classification where the ISA distinguishes them;
- aliases/pseudoinstructions clearly separated from real encodings;
- provenance for the primary specification or permissively licensed machine-readable instruction database used to generate the inventory;
- a separate table for what Idriç currently emits.

For very large ISAs, the checked-in inventory should be generated from a pinned machine-readable source rather than maintained manually. The generator and source revision are part of the architecture record.

## Current branches

| Branch | Architecture boundary |
| --- | --- |
| `arch/x86-64` | AMD64 / Intel 64 common long-mode architecture, with vendor-specific extensions kept distinguishable |
| `arch/aarch64-sve` | AArch64 A64 plus Advanced SIMD, SVE/SVE2, with later SME kept separately versioned |
| `arch/power` | POWER ISA 3.1c, including scalar, VMX/AltiVec, VSX and architected MMA/prefixed facilities |
| `arch/s390x` | IBM z/Architecture as pinned by the branch, including problem-state and system facilities with facility-level membership |

The explanatory `docs/*.md` architecture tours requested by existing issues remain useful, but they do not substitute for the exhaustive inventory.
