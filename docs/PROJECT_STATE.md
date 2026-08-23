# Project state

Last updated: 2026-08-23.

Omaudit is a zero-runtime-dependency Python 3.11+ CLI for static capability
auditing of Omarchy 4 shell plugins. It is not an Omarchy plugin and never runs
inside the shell.

## Current checkpoint

- The initial implementation covers scan, verify, declaration generation,
  baselines, installed-plugin drift checks, reports, badges, and an explicitly
  invoked ecosystem census.
- Organization-readiness hardening is in progress on
  `harden/organization-readiness` before transfer from `eddieor/omaudit` to
  `omarchy-forge/omaudit`.
- Remote source protocols are restricted; clone-cache paths are deterministic
  and collision-safe; registry responses are HTTPS-only and bounded.
- `omaudit add` installs the exact checkout shown to the user, verifies the
  installed commit and capability set, restores the upstream update remote, and
  refuses to record a baseline if anything differs.
- Omarchy `4.0.0-1` add/remove/list behavior and healthy shell IPC were verified
  against the installed `/usr/share/omarchy` implementation without changing
  Omarchy-owned files or executing plugin QML.
- The release installer, pinned CI, tag release workflow, security policy,
  decisions, compatibility record, and `v0.1.0` release notes are present but
  are not shipped until their pull request, transfer, and release complete.

## Local preservation

`builtin/`, `plugin-grok/`, `MEMORY.md`, `functionality.md`, and `handoff.md`
are pre-existing local material outside the Omaudit product tree. Preserve them
and never include them in repository commits.

## Next checkpoint

1. Pass the complete test, package, installer, history, and official-validator
   baseline.
2. Merge the hardening pull request, rename the default branch to `main`, and
   transfer the repository with explicit owner authorization.
3. Apply organization governance and publish verified `v0.1.0` assets.
4. Extend Forge's owner catalog for CLI tools and list Omaudit only after its
   release is live.
