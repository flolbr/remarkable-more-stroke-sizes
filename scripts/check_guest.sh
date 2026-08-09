#!/bin/sh
set -eu

firmware=$1
build_id=$2
expected_sha256=$3
source_qmd=$4
artifact_qmd=$5

actual_build_id=$(cat /etc/version)
if [ "$actual_build_id" != "$build_id" ]; then
    echo "ERROR: guest build ID $actual_build_id does not match $build_id" >&2
    exit 1
fi

actual_sha256=$(sha256sum "$artifact_qmd" | cut -d ' ' -f 1)
if [ "$actual_sha256" != "$expected_sha256" ]; then
    echo "ERROR: guest artifact SHA-256 differs from compatibility.json" >&2
    exit 1
fi

grep -qx "VERSION $firmware" "$source_qmd"
grep -qx "VERSION $firmware" "$artifact_qmd"

source_values=$(sed -n \
    's/^[[:space:]]*thickness:[[:space:]]*\([0-9][0-9.]*\),/\1/p' \
    "$source_qmd")
artifact_values=$(sed -n \
    's/^[[:space:]]*~&[0-9][0-9]*&~:[[:space:]]*\([0-9][0-9.]*\),/\1/p' \
    "$artifact_qmd")

if [ -z "$source_values" ] || [ "$source_values" != "$artifact_values" ]; then
    echo "ERROR: readable and generated guest thickness lists differ" >&2
    exit 1
fi

echo "PASS rm2 $firmware build $build_id guest artifact load"
