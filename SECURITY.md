# Security policy

Omaudit is a static capability lint, not a malware detector or sandbox. A clean
report does not prove that a plugin is safe. Plugins execute unsandboxed inside
the long-running Omarchy shell with the user's permissions.

## Supported versions

Only the latest published release receives security fixes during the initial
0.x series.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting feature for this repository. Do
not include live credentials, private plugin source, or unrelated user data.

## Trust boundaries

- `scan`, `verify`, `permissions`, `badge`, and `schema` are local and do not
  execute QML or require network access.
- `add` explicitly clones one remote source, statically reviews it, asks for
  confirmation, and delegates installation to `omarchy plugin add`. The exact
  reviewed checkout is installed and rechecked before a baseline is written.
- `census` explicitly downloads the public marketplace registry and Git source.
  Remote protocols are restricted to HTTPS and SSH; Git helper transports and
  local paths are rejected.
- `check` can offer explicit destructive remediation through the official
  Omarchy removal command. It never acts without a command flag or prompt.
