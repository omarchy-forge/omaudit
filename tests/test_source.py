from omaudit.source import parse_spec, safe_remote_url


def test_parse_spec_preserves_ssh_urls():
    assert parse_spec("git@github.com:owner/plugin.git") == (
        "git@github.com:owner/plugin.git", None,
    )


def test_parse_spec_accepts_only_full_commit_suffix():
    commit = "a" * 40
    assert parse_spec(f"https://github.com/owner/plugin.git@{commit}") == (
        "https://github.com/owner/plugin.git", commit,
    )
    assert parse_spec("https://example.test/repo@main") == (
        "https://example.test/repo@main", None,
    )


def test_remote_sources_reject_local_and_ext_protocols():
    assert safe_remote_url("https://github.com/owner/plugin.git")
    assert safe_remote_url("git@github.com:owner/plugin.git")
    assert safe_remote_url("ssh://git@example.test/owner/plugin.git")
    assert not safe_remote_url("/tmp/plugin")
    assert not safe_remote_url("file:///tmp/plugin")
    assert not safe_remote_url("ext::sh -c touch% /tmp/pwned")
