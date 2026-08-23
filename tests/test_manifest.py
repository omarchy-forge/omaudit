import json

from omaudit.manifest import load


def _plugin(tmp_path, **changes):
    data = {
        "schemaVersion": 1,
        "id": "io.example.plugin",
        "name": "Plugin",
        "version": "1.0.0",
        "kinds": ["bar-widget"],
        "entryPoints": {"barWidget": "BarWidget.qml"},
    }
    data.update(changes)
    (tmp_path / "manifest.json").write_text(json.dumps(data), encoding="utf-8")
    (tmp_path / "BarWidget.qml").write_text("Item {}\n", encoding="utf-8")
    return load(tmp_path)


def test_matches_official_id_and_entrypoint_safety(tmp_path):
    assert not _plugin(tmp_path, id="bad..id").ok
    assert not _plugin(tmp_path, entryPoints={"barWidget": "dir/../BarWidget.qml"}).ok


def test_matches_official_default_section_validation(tmp_path):
    assert not _plugin(tmp_path, barWidget={"defaultSection": "somewhere"}).ok


def test_unknown_kind_is_not_rejected_beyond_official_validator(tmp_path):
    manifest = _plugin(tmp_path, kinds=["future-kind"], entryPoints={})
    assert manifest.ok
    assert any("unknown plugin kind" in warning for warning in manifest.warnings)
