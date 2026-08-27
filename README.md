# AArch64 / NEON / SVE / SME architecture catalog

This branch owns the complete pinned A64 architecture catalog and large-system/vector comparative notes. It is inventory/research, not an executable instruction selector.

Direct generic A64 code generation is owned by `isomorphisms/idric-x86-aggressive-backend:a64-backend`. Concrete Switch, Apple, and server targets apply their own feature masks and ABI/platform profiles to the shared catalog and selector.

Complete architecture knowledge does not imply required, emitted, or tested support.

Tracking: issues #3–#4 and #9 in this repository.

