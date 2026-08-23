# Contributing

Use a focused branch and pull request. Keep changes deterministic, add tests,
and run:

```sh
python -m pytest -q
python -m compileall -q omaudit
python -m pip wheel . --no-deps --wheel-dir /tmp/omaudit-dist
```

Tests must use fictional fixtures and must never execute plugin QML, plugin
helpers, installers, or untrusted Git hooks. Do not add telemetry, accounts,
privileged operations, background network requests, or automatic installation.
