# Upstream compatibility

Verified on 2026-08-23 against installed Omarchy `4.0.0-1` under
`/usr/share/omarchy`.

- `omarchy plugin add [git-url] [--enable] [--yes]` clones into a staging
  directory, runs the official validator, rejects duplicate IDs, moves the
  validated checkout into `~/.config/omarchy/plugins/<id>`, and rescans the
  shell. Omaudit delegates to this command and does not enable by default.
- `omarchy plugin remove [id] [--yes]` disables an enabled plugin before
  removing its Git checkout and rescans the shell. Omaudit delegates explicit
  removal decisions to this command.
- `omarchy plugin list --json` and `omarchy-shell shell ping` were verified;
  shell IPC returned `ok`.
- User plugins remain unsandboxed QML loaded by the long-running shell. Omaudit
  performs static reads only and does not execute QML.
- The installed official validator and current plugin-kind/entry-point contract
  were compared with `omaudit.manifest`. The optional `permissions` block is an
  Omaudit-only convention and is not enforced upstream.

Files inspected:

- `/usr/share/omarchy/bin/omarchy-plugin-add`
- `/usr/share/omarchy/bin/omarchy-plugin-remove`
- `/usr/share/omarchy/bin/omarchy-plugin-validate`
- `/usr/share/omarchy/shell/plugins/`
