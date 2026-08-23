# Project state

Last updated: 2026-08-23.

Omaudit is a zero-runtime-dependency Python 3.11+ CLI for static capability
auditing of Omarchy 4 shell plugins. It is not an Omarchy plugin and never runs
inside the shell.

## Current checkpoint

- The initial implementation covers scan, verify, declaration generation,
  baselines, installed-plugin drift checks, reports, badges, and an explicitly
  invoked ecosystem census.
- Organization-readiness hardening merged through pull request `#1` at exact
  commit `50cd612582413397cf098016845a7b55b9ca7d91`. The repository was renamed
  to use `main` and transferred from `eddieor/omaudit` to
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
  decisions, compatibility record, and `v0.1.0` release notes are shipped.
- Public release `v0.1.0` was built by successful workflow run `32632279469`.
  Independent downloads passed SHA-256 verification, isolated installation,
  version output, and a grade-A fictional scan. The release is neither draft
  nor prerelease.
- `main` requires an up-to-date pull request and the `test` status check;
  administrators are included and force pushes and deletion are disabled.
  Secret scanning, push protection, Dependabot security updates, and private
  vulnerability reporting are enabled.

## Local preservation

`builtin/`, `plugin-grok/`, `MEMORY.md`, `functionality.md`, and `handoff.md`
are pre-existing local material outside the Omaudit product tree. Preserve them
and never include them in repository commits.

## Next checkpoint

1. Extend Forge's owner catalog for CLI tools and list Omaudit from its verified
   public release.
2. Keep future capability-rule changes fixture-backed and re-run the full
   first-party static baseline before describing ecosystem results.
3. Do not publish named marketplace findings without following
   `DISCLOSURE.md`.
