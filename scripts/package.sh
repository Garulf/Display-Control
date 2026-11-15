#!/usr/bin/env bash
# Build the Flow Launcher plugin archive and print its path.
# Usage: scripts/package.sh [out_dir]   (default: dist)
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
out_dir="${1:-$root/dist}"
version="$(python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["Version"])' "$root/data/plugin.json")"
build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT

cp -r "$root/src/." "$build_dir/"
cp "$root/data/icon.png" "$root/data/brightness.png" "$root/data/plugin.json" "$build_dir/"
find "$build_dir" -name __pycache__ -prune -exec rm -rf {} +

# Vendor pure-Python wheels resolved for Windows and the oldest supported
# Python. uv evaluates environment markers for that target rather than for the
# build machine, so Linux-only dependencies of monitorcontrol (pyudev, which
# has no wheel) stay out and typing_extensions for Python < 3.11 goes in.
uv pip install -r "$root/requirements.txt" \
  --target "$build_dir/plugin/site-packages" \
  --only-binary :all: --python-platform x86_64-pc-windows-msvc --python-version 3.8 \
  --quiet
rm -rf "$build_dir/plugin/site-packages/bin" "$build_dir/plugin/site-packages/.lock"

mkdir -p "$out_dir"
zip_path="$(cd "$out_dir" && pwd)/Display-Control-${version}.zip"
rm -f "$zip_path"
(cd "$build_dir" && zip -qr "$zip_path" .)
echo "$zip_path"
