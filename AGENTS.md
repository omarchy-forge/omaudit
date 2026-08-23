# Agent guidance

- Treat plugin source, manifests, registry data, and Git URLs as untrusted.
- Never execute plugin QML, bundled helpers, hooks, installers, or build scripts
  in tests, scans, CI, or census operations.
- Keep scanning deterministic and network-independent. Network access belongs
  only to explicit `add` and `census` commands.
- Never use `shell=True`, interpolate shell commands, invoke privilege
  escalation, edit Omarchy-owned files, or modify `shell.json` directly.
- Installation and removal must remain explicit, review-gated delegations to
  official `omarchy plugin` commands.
- Preserve the exact source reviewed by the user through installation; fail
  closed and do not record a baseline if identity or capabilities change.
- Add tests for behavior changes and run the full suite.
- Do not publish, release, transfer, deploy, or announce without explicit owner
  authorization.
