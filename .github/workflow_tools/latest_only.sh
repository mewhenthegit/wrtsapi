#!/bin/sh

# This shell script should only be used by github workflows
# The intended purpose of this script is to delete every distribution but the latest

VERSION=$(cat pyproject.toml | egrep -o [0-9]+\.[0-9]+\.[0-9]+ | head -n 1)
echo $VERSION
mkdir tmp
mv dist/wrts-$VERSION.tar.gz tmp/
mv dist/wrts-$VERSION-py3-none-any.whl tmp/
rm dist/*
mv tmp/wrts-$VERSION.tar.gz dist/
mv tmp/wrts-$VERSION-py3-none-any.whl dist/
rm -d tmp

echo "Removed every distrobution except for version $VERSION"