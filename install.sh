#!/usr/bin/env bash
set -euo pipefail

repository="omarchy-forge/omaudit"
requested=""

fail() { printf 'omaudit installer: %s\n' "$*" >&2; exit 1; }

while (( $# > 0 )); do
  case "$1" in
    --version) (( $# >= 2 )) || fail "--version requires vX.Y.Z"; requested="$2"; shift 2 ;;
    -h|--help) printf 'Usage: install.sh [--version vX.Y.Z]\n'; exit 0 ;;
    *) fail "unknown option: $1" ;;
  esac
done

command -v curl >/dev/null || fail "curl is required"
command -v python3 >/dev/null || fail "Python 3.11 or newer is required"
python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 11))' || fail "Python 3.11 or newer is required"
command -v sha256sum >/dev/null || fail "sha256sum is required"

if [[ -z $requested ]]; then
  release_url=$(curl -fsSIL -o /dev/null -w '%{url_effective}' "https://github.com/$repository/releases/latest")
  requested=${release_url##*/}
fi
[[ $requested =~ ^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$ ]] || fail "invalid release version: $requested"
version=${requested#v}

install_root="${XDG_DATA_HOME:-$HOME/.local/share}/omaudit"
bin_dir="${XDG_BIN_HOME:-$HOME/.local/bin}"
version_root="$install_root/$version"
current=""
if [[ -x $bin_dir/omaudit ]]; then
  current=$($bin_dir/omaudit version 2>/dev/null | awk '{print $2}') || true
fi
if [[ $current == "$version" ]]; then
  printf 'omaudit %s is already installed.\n' "$version"
  exit 0
fi

(
  work=$(mktemp -d)
  trap 'rm -rf -- "$work"' EXIT
  cd "$work"
  base="https://github.com/$repository/releases/download/$requested"
  wheel="omaudit-${version}-py3-none-any.whl"
  curl -fLO "$base/$wheel"
  curl -fLO "$base/checksums.txt"
  grep "  $wheel\$" checksums.txt | sha256sum --check --status - || fail "wheel checksum verification failed"
  mkdir -p "$install_root" "$bin_dir"
  rm -rf -- "$version_root"
  python3 -m venv "$version_root"
  trap 'rm -rf -- "$work"; if [[ ! -x "$version_root/bin/omaudit" ]]; then rm -rf -- "$version_root"; fi' EXIT
  "$version_root/bin/pip" install --no-deps --disable-pip-version-check "$wheel"
  test "$("$version_root/bin/omaudit" version)" = "omaudit $version" || fail "installed version did not match"
  ln -sfn "$version_root/bin/omaudit" "$bin_dir/omaudit"
)

printf 'Installed omaudit %s at %s/omaudit\n' "$version" "$bin_dir"
