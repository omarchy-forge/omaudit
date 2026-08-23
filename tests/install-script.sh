#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
release="$work/release"
fakebin="$work/bin"
mkdir -p "$release" "$fakebin"

python3 -m pip wheel "$repo" --no-deps --wheel-dir "$release" >/dev/null
(
  cd "$release"
  sha256sum omaudit-0.1.0-py3-none-any.whl > checksums.txt
)

cat > "$fakebin/curl" <<'CURL'
#!/usr/bin/env bash
set -euo pipefail
url=${!#}
cp "$OMAUDIT_TEST_RELEASE_DIR/${url##*/}" .
CURL
chmod +x "$fakebin/curl"

export OMAUDIT_TEST_RELEASE_DIR="$release"
export PATH="$fakebin:$PATH"
export HOME="$work/home"

bash "$repo/install.sh" --version v0.1.0
test "$("$HOME/.local/bin/omaudit" version)" = "omaudit 0.1.0"
first_target=$(readlink "$HOME/.local/bin/omaudit")
bash "$repo/install.sh" --version v0.1.0 | grep -q "already installed"
test "$(readlink "$HOME/.local/bin/omaudit")" = "$first_target"

sed -i 's/^[0-9a-f]\{64\}/ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff/' "$release/checksums.txt"
export HOME="$work/bad-home"
if bash "$repo/install.sh" --version v0.1.0 >/dev/null 2>&1; then
  echo "installer accepted a bad checksum" >&2
  exit 1
fi
test ! -e "$HOME/.local/bin/omaudit"

echo "install script checks passed"
