# IBM z/Architecture complete instruction inventory

Status: exhaustive source-backed architecture inventory, independent of the Idriç Linux user-mode subset.

## Architecture pin

Normative source: **IBM z/Architecture Principles of Operation, SA22-7832-14**, fifteenth edition (April 2025). IBM's current systems library lists this as the current Principles of Operation publication for z17-era systems.

The complete architecture includes problem-state and privileged/control facilities, decimal and floating-point families, vector generations, string/character operations, cryptographic/specialized assists and I/O/system instructions. Linux `s390x` is only an execution environment/profile layered on that architecture.

## Reproducible machine extraction

Pin the existing open-source architecture extractor at:

- repository: `golang/arch`
- commit: `2549b772bfe5d4fab95e77428ecbed712cc73004`
- generator: `s390x/s390xspec/spec.go`

The generator reads the IBM Principles of Operation PDF directly, locates **Instructions Arranged by Name**, follows the manual's complete instruction outline, and emits instruction heading, mnemonic/form, binary encoding and flags in CSV form.

The same pinned repository contains `s390x/s390x.csv` (blob `a53942d853bbe3f794ec133107e57849ea6bbff3`), generated from the preceding SA22-7832-13 edition. It is retained as a reproducible baseline, not mislabeled as the current -14 inventory.

`tools/generate-instructions.sh` builds that exact extractor and runs it against a caller-supplied SA22-7832-14 PDF. The generated CSV is the complete normalized inventory for this branch. This deliberately avoids manually copying hundreds of z instructions.

## Required fields

Every generated row preserves:

- IBM instruction heading;
- assembler mnemonic and operand form;
- instruction-format/encoding bit layout;
- facility/flags information emitted by the extractor.

A later normalization layer may add facility-level names from the -14 manual, but it must not drop rows from the raw extraction.

## Included surface

No instruction family is filtered out merely because Linux user code is unlikely to use it. The complete source-backed result includes:

- fixed-point loads/stores, arithmetic, logical, shifts and bit operations;
- condition-code and branch/control-flow instructions;
- memory/string/character and translate/search families;
- packed/zoned decimal and conversion operations;
- hexadecimal, binary and decimal floating point;
- vector support, integer, string, floating and decimal instructions;
- atomics, serialization and synchronization;
- crypto, compression, transactional-execution and specialized assists;
- privileged/control/I/O instructions present in the architecture.

## Future codegen gate

This branch is inventory/research and claims no executable Idriç s390x backend. Open an emitted/tested support matrix only after an explicit reproducible assembler/linker/execution gate and a tiny exact Linux problem-state oracle. A future scalar subset remains separate from this catalog and may never erase unsupported z instructions.
