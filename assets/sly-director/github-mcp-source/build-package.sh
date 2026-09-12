#!/usr/bin/env bash
set -euo pipefail

rm -rf build function.zip
mkdir -p build

python3 -m pip install \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 3.13 \
  --only-binary=:all: \
  --target build \
  -r requirements.txt

cp -R src build/src

(
  cd build
  zip -qr ../function.zip .
)

echo "Created: function.zip"
ls -lh function.zip
