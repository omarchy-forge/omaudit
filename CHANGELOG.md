# Changelog

## 0.1.0 - 2026-08-23

- Add static capability reports, declaration verification, baselines, drift
  checks, reporting, and an explicitly invoked ecosystem census.
- Add an install-time review gate that installs the exact reviewed checkout and
  rejects capability or commit mismatches before recording a baseline.
- Restrict remote Git sources, bound registry downloads, and use collision-safe
  clone-cache paths.
- Add a checksum-verifying user installer, protected CI/release workflows,
  security documentation, and Omarchy 4 compatibility evidence.
