#!/usr/bin/env python3
"""Validate compatibility metadata and derive tests from readable QMD sources."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "compatibility.json"
VERSION_RE = re.compile(r"^VERSION\s+(\S+)$", re.MULTILINE)
THICKNESS_RE = re.compile(r"^\s*thickness:\s*([0-9]+(?:\.[0-9]+)?),", re.MULTILINE)
HASHED_VALUE_RE = re.compile(r"~&\d+&~:\s*([0-9]+(?:\.[0-9]+)?),")
HASH_TOKEN_RE = re.compile(r"~&\d+&~")


def fail(message: str) -> None:
    raise ValueError(message)


def read_manifest() -> dict:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema") != 1:
        fail("compatibility.json: unsupported schema")
    targets = data.get("targets")
    if not isinstance(targets, list) or not targets:
        fail("compatibility.json: targets must be a non-empty list")
    return data


def version(text: str, path: Path) -> str:
    versions = VERSION_RE.findall(text)
    if len(versions) != 1:
        fail(f"{path}: expected exactly one VERSION")
    return versions[0]


def thicknesses(text: str, path: Path) -> list[str]:
    values = THICKNESS_RE.findall(text)
    if not values:
        fail(f"{path}: no thickness entries found")
    numeric = [float(value) for value in values]
    if numeric != sorted(set(numeric)):
        fail(f"{path}: thicknesses must be unique and ascending")
    return values


def artifact_thicknesses(text: str, path: Path) -> list[str]:
    iterable = re.search(r"\biterable\s*=\s*\[(.*?)\n\s*\];", text, re.DOTALL)
    if not iterable:
        fail(f"{path}: generated iterable not found")
    values = HASHED_VALUE_RE.findall(iterable.group(1))
    if not values:
        fail(f"{path}: no generated thickness entries found")
    return values


def quoted_lines(block: str, path: Path) -> list[str]:
    values: list[str] = []
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("//"):
            continue
        if not line.endswith(","):
            fail(f"{path}: malformed label line: {line}")
        try:
            value = ast.literal_eval(line[:-1])
        except (SyntaxError, ValueError) as exc:
            fail(f"{path}: invalid label literal: {line}: {exc}")
        if not isinstance(value, str) or not value:
            fail(f"{path}: labels must be non-empty strings")
        values.append(value)
    return values


def validate_labels(text: str, values: list[str], path: Path) -> None:
    table_match = re.search(
        r"const labelsByLanguage\s*=\s*\{(?P<body>.*?)^\s*\};",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if table_match:
        tables = re.findall(
            r"^\s*([a-z]{2}):\s*\[(.*?)^\s*\],",
            table_match.group("body"),
            re.MULTILINE | re.DOTALL,
        )
        if not tables:
            fail(f"{path}: labelsByLanguage contains no language tables")
        expected_suffixes = [f"({value})" for value in values]
        for language, block in tables:
            labels = quoted_lines(block, path)
            if len(labels) != len(values):
                fail(f"{path}: {language} label count does not match thickness count")
            for label, suffix in zip(labels, expected_suffixes, strict=True):
                if not label.endswith(suffix):
                    fail(f"{path}: {language} label {label!r} must end with {suffix!r}")
        return

    labels = re.findall(r"^\s*displayName:\s*(['\"])(.*?)\1,", text, re.MULTILINE)
    if len(labels) != len(values):
        fail(f"{path}: displayName count does not match thickness count")
    if any(not label for _, label in labels):
        fail(f"{path}: labels must be non-empty")


def validate_target(target: dict) -> dict:
    required = {
        "firmware",
        "build_id",
        "hardware",
        "source",
        "artifact",
        "sha256",
        "evidence",
    }
    missing = required - target.keys()
    if missing:
        fail(f"compatibility.json: target missing {sorted(missing)}")

    firmware = target["firmware"]
    if not re.fullmatch(r"\d{14}", target["build_id"]):
        fail(f"{firmware}: build_id must contain 14 digits")
    source = ROOT / target["source"]
    artifact = ROOT / target["artifact"]
    if not source.is_file() or not artifact.is_file():
        fail(f"{firmware}: source or artifact is missing")

    source_text = source.read_text(encoding="utf-8")
    artifact_text = artifact.read_text(encoding="utf-8")
    if version(source_text, source) != firmware or version(artifact_text, artifact) != firmware:
        fail(f"{firmware}: directory, manifest, and QMD VERSION must agree")
    if HASH_TOKEN_RE.search(source_text):
        fail(f"{source}: readable source contains hashed identifiers")
    if not HASH_TOKEN_RE.search(artifact_text):
        fail(f"{artifact}: generated artifact contains no hashed identifiers")

    source_values = thicknesses(source_text, source)
    artifact_values = artifact_thicknesses(artifact_text, artifact)
    if source_values != artifact_values:
        fail(f"{firmware}: generated artifact thicknesses differ from readable source")
    validate_labels(source_text, source_values, source)

    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if digest != target["sha256"]:
        fail(f"{firmware}: artifact SHA-256 differs from compatibility.json")

    evidence = target["evidence"]
    if set(evidence) != {"hash", "ci_load", "qemu_ui", "hardware"}:
        fail(f"{firmware}: evidence keys must be hash, ci_load, qemu_ui, hardware")
    if not all(isinstance(value, bool) for value in evidence.values()):
        fail(f"{firmware}: evidence values must be booleans")

    return {
        "firmware": firmware,
        "build_id": target["build_id"],
        "hardware": target["hardware"],
        "source": target["source"],
        "artifact": target["artifact"],
        "sha256": target["sha256"],
        "thicknesses": [float(value) for value in source_values],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", action="store_true", help="emit a GitHub Actions matrix")
    parser.add_argument(
        "--exclude-canary",
        action="store_true",
        help="omit the manifest canary from matrix output",
    )
    parser.add_argument(
        "--only-canary",
        action="store_true",
        help="include only the manifest canary in matrix output",
    )
    parser.add_argument("--firmware", help="validate only one manifest target")
    args = parser.parse_args()

    try:
        manifest = read_manifest()
        targets = manifest["targets"]
        firmwares = {target.get("firmware") for target in targets}
        if manifest.get("canary") not in firmwares:
            fail("compatibility.json: canary must identify a target")
        if args.firmware:
            targets = [target for target in targets if target["firmware"] == args.firmware]
            if not targets:
                fail(f"unknown firmware: {args.firmware}")
        elif args.exclude_canary:
            targets = [target for target in targets if target["firmware"] != manifest["canary"]]
        elif args.only_canary:
            targets = [target for target in targets if target["firmware"] == manifest["canary"]]
        results = [validate_target(target) for target in targets]
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.matrix:
        print(json.dumps({"include": [
            {
                "firmware": item["firmware"],
                "build_id": item["build_id"],
                "hardware": item["hardware"],
                "source": item["source"],
                "artifact": item["artifact"],
                "sha256": item["sha256"],
            }
            for item in results
        ]}, separators=(",", ":")))
    else:
        for item in results:
            rendered = ", ".join(f"{value:g}" for value in item["thicknesses"])
            print(f"PASS {item['hardware']} {item['firmware']}: {rendered}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
