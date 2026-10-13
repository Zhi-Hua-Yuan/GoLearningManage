#!/usr/bin/env python3
"""Verify the immutable Phase 0 migrations and OpenAPI contract."""
from __future__ import annotations
import hashlib
import json
import re
import sys
from pathlib import Path

METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def fail(message: str) -> None:
    raise SystemExit(f"baseline verification failed: {message}")

def verify_migrations(root: Path) -> None:
    manifest = root / "db" / "migration" / "published-migrations.sha256"
    if not manifest.is_file():
        fail(f"missing {manifest}")
    checked = 0
    for line_number, raw_line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 2 or not HEX64.fullmatch(parts[0]):
            fail(f"invalid migration manifest line {line_number}")
        expected, source_path = parts
        target = root / "db" / "migration" / Path(source_path).name
        if not target.is_file():
            fail(f"missing migration {target}")
        actual = sha256(target)
        if actual.lower() != expected.lower():
            fail(f"checksum mismatch for {target}: {actual} != {expected}")
        checked += 1
    if checked != 9:
        fail(f"expected 9 published migrations, found {checked}")

def verify_openapi(root: Path) -> None:
    openapi_dir = root / "api" / "openapi"
    contract = json.loads((openapi_dir / "contract-manifest.json").read_text(encoding="utf-8"))
    openapi_path = openapi_dir / contract["openapi"]["file"]
    document = json.loads(openapi_path.read_text(encoding="utf-8"))
    base_path = contract["basePath"].rstrip("/")
    operations = {(method.upper(), base_path + path) for path, item in document["paths"].items() for method in item if method.lower() in METHODS}
    expected = contract["javaBaseline"]["operations"]
    if len(operations) != expected:
        fail(f"OpenAPI operation count {len(operations)} != {expected}")
    core = {(item["method"].upper(), item["path"]) for item in contract["coreOperations"]}
    if len(core) != contract["javaBaseline"]["coreOperations"]:
        fail("core operation ledger count does not match manifest")
    missing = sorted(core - operations)
    if missing:
        fail(f"core operations missing from OpenAPI: {missing}")
    actual_hash = sha256(openapi_path).lower()
    if actual_hash != contract["openapi"]["sha256"].lower():
        fail(f"OpenAPI checksum {actual_hash} != {contract['openapi']['sha256']}")
    sidecar = openapi_dir / f"{openapi_path.name}.sha256"
    sidecar_parts = sidecar.read_text(encoding="utf-8").split()
    if len(sidecar_parts) < 2 or sidecar_parts[1] != openapi_path.name or sidecar_parts[0].lower() != actual_hash:
        fail(f"invalid OpenAPI sidecar {sidecar}")

def main() -> int:
    root = Path(__file__).resolve().parents[2]
    verify_migrations(root)
    verify_openapi(root)
    print("Phase 0 baseline verification: PASS (9 migrations, 95 OpenAPI operations, 52 core operations)")
    return 0

if __name__ == "__main__":
    sys.exit(main())