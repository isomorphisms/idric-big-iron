# x86-64 big-iron architecture catalog

This branch owns an independent, reproducible LLVM-derived cross-vendor x86 architecture catalog, with Intel XED as an encoding cross-check, plus comparative notes against AArch64, POWER, and s390x.

It does not own executable x86 code generation. Backend-facing XED/form inventory, the instruction encyclopedia, emitted/tested support, and direct x86-64 codegen live in `isomorphisms/idric-x86-aggressive-backend`.

Two architecture oracles may expose useful differences. There must not be two competing instruction selectors, and neither complete catalog implies compiler support.

Tracking: issues #1–#2 in this repository.

