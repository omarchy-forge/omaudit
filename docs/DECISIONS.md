# Architecture decisions

## D-001: Static capability lint, not a security boundary

Omaudit reports observable capability and composition risk without claiming to
prove intent or safety. Scans never execute plugin code.

## D-002: Exact reviewed checkout for installation

Remote `add` installs from the temporary checkout that was actually scanned,
then verifies installed commit and capabilities before recording acceptance.
The upstream remote is restored only after verification. A mismatch is removed
through the official Omarchy command and receives no baseline.

## D-003: Explicit network operations

Normal scans are local. Only `add` and `census` fetch data after direct user
invocation. Remote Git sources are limited to HTTPS and SSH, registry responses
are HTTPS-only and bounded, and no timers or background checks are installed.
