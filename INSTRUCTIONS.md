# x86-64 complete instruction inventory

Status: exhaustive source-backed encoding inventory, independent of the Idriç implementation subset.

## Architecture boundary

This branch means **64-bit AMD64 / Intel 64**, while retaining vendor-specific instruction extensions and legacy encodings that remain architecturally visible in long mode. It must not confuse one processor generation's CPUID feature set with the architecture-wide instruction catalog.

Normative semantics remain the current Intel 64/IA-32 and AMD64 architecture manuals. Because no single vendor manual is the complete union of Intel and AMD extensions, the normalized cross-vendor encoding catalog is generated from LLVM's x86 target records.

## Cross-vendor machine-readable source

Pin:

- repository: `llvm/llvm-project`
- commit: `74253d0e4f01fca3c2cc526aee9d073af3fad919`
- target root: `llvm/lib/Target/X86/X86.td` and every recursively included x86 TableGen file.

LLVM's TableGen descriptions model the concrete instruction records used by the assembler, disassembler and code generator, including legacy x86, x86-64, Intel extensions and AMD-specific facilities. TableGen multiclasses generate many real forms, so grepping source mnemonics is **not** an exhaustive inventory.

`tools/generate-instructions.sh` builds the pinned `llvm-tblgen`, evaluates the exact x86 TableGen source, and emits the complete JSON record database with `--dump-json`. The companion normalizer retains every record derived from `Instruction`, including:

- TableGen record name;
- assembler string/form;
- pseudo/real classification;
- predicates / feature requirements;
- namespace and encoding-related fields;
- the entire original TableGen JSON record so no information is lost.

Compiler-only pseudo instructions stay visible but are marked as pseudos; they are not counted as extra machine encodings. Architectural aliases are retained separately from concrete encoding records where LLVM models them separately.

## Independent Intel encoding cross-check

Pin Intel XED as an independent Intel-side oracle:

- repository: `intelxed/xed`
- commit: `0bcb6237345c5066726dcc08b3d87928df3b5b26`
- release: 2026.08.23.

XED is useful for checking Intel encoding forms and recent Intel/APX/AVX-family additions. It is **not** by itself the branch's complete AMD64/Intel-64 union because AMD-only facilities would be lost.

## Complete architectural families

The generated catalog is deliberately not reduced to "instructions a compiler normally emits". It retains records covering, where represented by the pinned architecture sources:

- scalar integer data movement, arithmetic, logic, shifts/rotates and bit manipulation;
- flags, comparisons, conditional operations and control flow;
- stack/call/return and system-call boundaries;
- x87 and MMX legacy facilities;
- SSE through AVX/AVX2/AVX-512 and later vector/mask facilities;
- FMA, BMI, population-count and byte/string-processing facilities;
- AES/SHA/GFNI/VAES/VPCLMUL and other crypto/specialized operations;
- AMX and newer accelerator-style instruction families;
- atomics, fences, cache-control and synchronization;
- virtualization/system/security instructions;
- AMD-specific families such as SVM and historical AMD extensions where still modeled;
- obsolete/compatibility encodings, explicitly distinguished from a modern long-mode emission target.

## Feature profile versus catalog

A real host such as Steam Deck gets a CPUID/OSXSAVE feature mask applied **after** generation. The catalog remains the union. An instruction does not disappear from architecture knowledge because one CPU lacks its feature bit.

## Codegen ownership and Idriç support

This branch is an architecture catalog/reference. Backend-facing XED/form inventory, the instruction encyclopedia, emitted/tested support, and executable x86-64 codegen live in `isomorphisms/idric-x86-aggressive-backend`.

The canonical x86 backend may initially target a very small SysV x86-64 scalar subset without changing this complete LLVM-derived catalog. Neither catalog implies compiler support, and disagreement between them is review evidence rather than permission to silently pick one.
