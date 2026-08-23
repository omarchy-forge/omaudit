"""omaudit add: the install-time gate."""
import shutil
import subprocess
from pathlib import Path

import pytest

from omaudit import cli
from omaudit.cli import EXIT_MANIFEST, EXIT_OK, EXIT_USAGE, build_parser
from omaudit.report import install_summary

FIXTURES = Path(__file__).parent / "fixtures"


def _run_add(args_list):
    args = build_parser().parse_args(["add", *args_list])
    return args.func(args)


def _write_manifest(dir_: Path, plugin_id: str) -> None:
    dir_.mkdir(parents=True, exist_ok=True)
    (dir_ / "manifest.json").write_text(
        f'{{"schemaVersion": 1, "id": "{plugin_id}", "name": "{plugin_id}", '
        f'"version": "1.0.0", "kinds": ["bar-widget"], '
        f'"entryPoints": {{"barWidget": "BarWidget.qml"}}}}',
        encoding="utf-8",
    )
    (dir_ / "BarWidget.qml").write_text(
        "import QtQuick\nBarWidget { }\n", encoding="utf-8"
    )


def test_decline_writes_nothing(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "n")
    code = _run_add([str(FIXTURES / "sketchy-weather"), "--local"])
    assert code == EXIT_OK
    out = capsys.readouterr().out
    assert "aborted - nothing was written" in out
    assert not (FIXTURES / "sketchy-weather" / ".omaudit-baseline.json").exists()


def test_yes_without_omarchy_on_path(monkeypatch, capsys):
    def fake_run(*a, **k):
        raise FileNotFoundError("omarchy")
    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    code = _run_add([str(FIXTURES / "sketchy-weather"), "--local", "--yes"])
    assert code == EXIT_USAGE
    err = capsys.readouterr().err
    assert "'omarchy' not found on PATH" in err


def test_manifest_invalid_aborts_without_prompting(tmp_path, monkeypatch, capsys):
    broken = tmp_path / "broken-plugin"
    broken.mkdir()
    (broken / "manifest.json").write_text("{}", encoding="utf-8")

    # if this prompts, the test fails the moment stdin is read
    monkeypatch.setattr("builtins.input", lambda prompt: (_ for _ in ()).throw(AssertionError("should not prompt")))
    code = _run_add([str(broken), "--local"])
    assert code == EXIT_MANIFEST
    assert "manifest errors" in capsys.readouterr().out


def test_multi_plugin_source_requires_disambiguation(tmp_path, capsys):
    suite = tmp_path / "suite"
    _write_manifest(suite / "widget-a", "test.widget-a")
    _write_manifest(suite / "widget-b", "test.widget-b")

    code = _run_add([str(suite), "--local"])
    assert code == EXIT_USAGE
    err = capsys.readouterr().err
    assert "2 plugins" in err
    assert "test.widget-a" in err and "test.widget-b" in err


def test_plugin_flag_selects_one_of_several(tmp_path, monkeypatch, capsys):
    suite = tmp_path / "suite"
    _write_manifest(suite / "widget-a", "test.widget-a")
    _write_manifest(suite / "widget-b", "test.widget-b")

    monkeypatch.setattr("builtins.input", lambda prompt: "n")
    code = _run_add([str(suite), "--local", "--plugin", "test.widget-b"])
    assert code == EXIT_OK
    out = capsys.readouterr().out
    assert "test.widget-b" in out
    assert "widget-a" not in out


def test_yes_installs_and_writes_baseline(tmp_path, monkeypatch, capsys):
    fake_home = tmp_path / "home"
    install_dir = fake_home / ".config" / "omarchy" / "plugins" / "io.github.elynch303.fan-monitor"
    install_dir.mkdir(parents=True)
    for f in (FIXTURES / "real-fan-monitor").iterdir():
        if f.suffix in (".json", ".qml"):
            shutil.copy(f, install_dir / f.name)

    real_run = cli.subprocess.run
    calls = []

    def fake_run(cmd, *a, **k):
        if cmd[:1] == ["omarchy"]:
            calls.append(cmd)
            return None
        return real_run(cmd, *a, **k)

    monkeypatch.setattr(cli.Path, "home", staticmethod(lambda: fake_home))
    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    source = str(FIXTURES / "real-fan-monitor")
    code = _run_add([source, "--local", "--yes"])
    assert code == EXIT_OK
    out = capsys.readouterr().out
    assert "installed io.github.elynch303.fan-monitor" in out
    assert (install_dir / ".omaudit-baseline.json").is_file()
    # omarchy-plugin-add refuses without --yes when stdin isn't a tty
    assert calls == [["omarchy", "plugin", "add", source, "--yes"]]


def test_install_mismatch_is_removed_without_baseline(tmp_path, monkeypatch, capsys):
    fake_home = tmp_path / "home"
    plugin_id = "io.github.elynch303.fan-monitor"
    install_dir = fake_home / ".config" / "omarchy" / "plugins" / plugin_id
    install_dir.mkdir(parents=True)
    for f in (FIXTURES / "real-fan-monitor").iterdir():
        if f.suffix in (".json", ".qml"):
            shutil.copy(f, install_dir / f.name)
    (install_dir / "BarWidget.qml").write_text(
        'Process { command: ["curl", "https://unexpected.example"] }\n',
        encoding="utf-8",
    )

    calls = []
    monkeypatch.setattr(cli.Path, "home", staticmethod(lambda: fake_home))
    monkeypatch.setattr(cli, "current_commit", lambda _path: None)
    monkeypatch.setattr(cli.subprocess, "run", lambda cmd, **k: calls.append(cmd) or _Ok())

    reviewed = cli._audit(FIXTURES / "real-fan-monitor")
    expected = {key for key, info in reviewed["capabilities"].items() if info["observed"]}
    code = cli._install(
        str(FIXTURES / "real-fan-monitor"), reviewed,
        expected_capabilities=expected,
    )
    assert code == cli.EXIT_FINDINGS
    assert not (install_dir / ".omaudit-baseline.json").exists()
    assert ["omarchy", "plugin", "remove", plugin_id, "--yes"] in calls
    assert "does not match" in capsys.readouterr().err


def test_install_uses_reviewed_checkout_and_restores_remote(tmp_path, monkeypatch):
    reviewed_repo = tmp_path / "reviewed"
    _write_manifest(reviewed_repo, "test.reviewed")
    subprocess.run(["git", "init", "-q", str(reviewed_repo)], check=True)
    subprocess.run(["git", "-C", str(reviewed_repo), "add", "."], check=True)
    subprocess.run([
        "git", "-C", str(reviewed_repo), "-c", "user.name=Test",
        "-c", "user.email=test@example.test", "commit", "-qm", "fixture",
    ], check=True)

    fake_home = tmp_path / "home"
    install_dir = fake_home / ".config" / "omarchy" / "plugins" / "test.reviewed"
    real_run = subprocess.run

    def fake_run(cmd, **kwargs):
        if cmd[:4] == ["omarchy", "plugin", "add", str(reviewed_repo)]:
            install_dir.parent.mkdir(parents=True)
            return real_run(["git", "clone", "-q", str(reviewed_repo), str(install_dir)], check=True)
        return real_run(cmd, **kwargs)

    monkeypatch.setattr(cli.Path, "home", staticmethod(lambda: fake_home))
    monkeypatch.setattr(cli.subprocess, "run", fake_run)
    doc = cli._audit(reviewed_repo)
    expected = {key for key, info in doc["capabilities"].items() if info["observed"]}
    commit = real_run(
        ["git", "-C", str(reviewed_repo), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()

    assert cli._install(
        str(reviewed_repo), doc,
        original_source="https://github.com/example/reviewed.git",
        expected_commit=commit,
        expected_capabilities=expected,
    ) == cli.EXIT_OK
    assert (install_dir / ".omaudit-baseline.json").is_file()
    remote = real_run(
        ["git", "-C", str(install_dir), "remote", "get-url", "origin"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    assert remote == "https://github.com/example/reviewed.git"


class _Ok:
    returncode = 0


def test_install_summary_splits_plain_and_flagged_lines():
    from omaudit.cli import _audit
    doc = _audit(FIXTURES / "real-omarqui")
    text = install_summary(doc)
    assert "grade D - know what you're doing" in text
    assert "reads files" in text
    assert "talks to internet" in text
    assert "! reads credentials and can send them off-box" in text
    # fs.sensitive is a flagged capability - it should not also get a plain line
    assert "touches credentials" not in text


def test_install_summary_no_capabilities():
    from omaudit.cli import _audit
    doc = _audit(FIXTURES / "good-clock")
    text = install_summary(doc)
    assert "no capabilities detected" in text


def test_install_summary_declared_vs_undeclared_wording():
    from omaudit.cli import _audit
    doc = _audit(FIXTURES / "sketchy-weather")
    text = install_summary(doc)
    assert "the author declared: talks to internet" in text
    assert "everything else is undeclared" in text
