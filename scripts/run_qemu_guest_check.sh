#!/bin/sh
set -eu

if [ "$#" -ne 6 ]; then
    echo "usage: $0 RM_DOCKER_DIR FIRMWARE BUILD_ID SHA256 SOURCE_QMD ARTIFACT_QMD" >&2
    exit 2
fi

rm_docker_dir=$1
firmware=$2
build_id=$3
expected_sha256=$4
source_qmd=$5
artifact_qmd=$6
suffix=$(printf '%s' "$firmware" | tr '.' '-')
image="rmstroke-qemu-base:$firmware"
container="rmstroke-$suffix"

cleanup() {
    docker rm -f "$container" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

docker build \
    --progress=plain \
    --target qemu-base \
    --build-arg "fw_version=$firmware" \
    --tag "$image" \
    "$rm_docker_dir"

docker run --detach --name "$container" "$image" >/dev/null

ready=false
attempt=0
while [ "$attempt" -lt 240 ]; do
    if docker exec "$container" in_vm true >/dev/null 2>&1; then
        ready=true
        break
    fi
    attempt=$((attempt + 1))
    sleep 2
done
if [ "$ready" != true ]; then
    echo "ERROR: exact-firmware QEMU guest did not reach SSH" >&2
    docker logs "$container" >&2 || true
    exit 1
fi

docker exec "$container" mkdir -p /opt/project
docker cp scripts/check_guest.sh "$container:/opt/project/check_guest.sh"
docker cp "$source_qmd" "$container:/opt/project/source.qmd"
docker cp "$artifact_qmd" "$container:/opt/project/artifact.qmd"
docker exec "$container" scp -o StrictHostKeyChecking=no \
    /opt/project/check_guest.sh \
    /opt/project/source.qmd \
    /opt/project/artifact.qmd \
    root@localhost:/tmp/
docker exec "$container" in_vm chmod 0755 /tmp/check_guest.sh
docker exec "$container" in_vm /tmp/check_guest.sh \
    "$firmware" \
    "$build_id" \
    "$expected_sha256" \
    /tmp/source.qmd \
    /tmp/artifact.qmd
