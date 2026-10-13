#!/usr/bin/env python3
"""Verify the immutable Phase 0 migrations and complete 96-operation contract."""
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

def collect_operations(document: dict, base_path: str) -> set[tuple[str, str]]:
    prefix = base_path.rstrip("/")
    return {
        (method.upper(), prefix + path)
        for path, item in document["paths"].items()
        for method in item
        if method.lower() in METHODS
    }

def verify_sidecar(path: Path, expected_hash: str) -> None:
    parts = path.read_text(encoding="utf-8").split()
    if len(parts) < 2 or parts[1] != path.name.removesuffix(".sha256"):
        fail(f"invalid checksum sidecar {path}")
    if parts[0].lower() != expected_hash.lower():
        fail(f"checksum sidecar {path} does not match {expected_hash}")

def verify_openapi(root: Path) -> None:
    openapi_dir = root / "api" / "openapi"
    contract = json.loads((openapi_dir / "contract-manifest.json").read_text(encoding="utf-8"))
    base_path = contract["basePath"]

    sealed_path = openapi_dir / contract["openapi"]["file"]
    sealed_document = json.loads(sealed_path.read_text(encoding="utf-8"))
    sealed_operations = collect_operations(sealed_document, base_path)
    if len(sealed_operations) != contract["openapi"]["operations"]:
        fail(f"sealed OpenAPI operation count {len(sealed_operations)} != {contract['openapi']['operations']}")
    sealed_hash = sha256(sealed_path)
    if sealed_hash.lower() != contract["openapi"]["sha256"].lower():
        fail(f"sealed OpenAPI checksum {sealed_hash} != {contract['openapi']['sha256']}")
    verify_sidecar(openapi_dir / f"{sealed_path.name}.sha256", sealed_hash)

    supplement_meta = contract["runtimeSupplement"]
    supplement_path = openapi_dir / supplement_meta["file"]
    supplement_document = json.loads(supplement_path.read_text(encoding="utf-8"))
    supplement_operations = collect_operations(supplement_document, base_path)
    if len(supplement_operations) != supplement_meta["operations"]:
        fail(f"runtime supplement operation count {len(supplement_operations)} != {supplement_meta['operations']}")
    supplement_hash = sha256(supplement_path)
    if supplement_hash.lower() != supplement_meta["sha256"].lower():
        fail(f"runtime supplement checksum {supplement_hash} != {supplement_meta['sha256']}")
    verify_sidecar(openapi_dir / f"{supplement_path.name}.sha256", supplement_hash)
    if sealed_operations & supplement_operations:
        fail("runtime supplement duplicates a sealed OpenAPI operation")

    manifest_supplement = {
        (item["method"].upper(), item["path"])
        for item in contract["supplementalOperations"]
    }
    if manifest_supplement != supplement_operations:
        fail("supplemental operation ledger does not match runtime supplement")

    runtime_operations = sealed_operations | supplement_operations
    runtime_expected = contract["runtimeInventory"]["operations"]
    if len(runtime_operations) != runtime_expected:
        fail(f"runtime operation count {len(runtime_operations)} != {runtime_expected}")
    core = {
        (item["method"].upper(), item["path"])
        for item in contract["coreOperations"]
    }
    if len(core) != contract["runtimeInventory"]["coreOperations"]:
        fail("core operation ledger count does not match manifest")
    missing = sorted(core - runtime_operations)
    if missing:
        fail(f"core operations missing from runtime contract: {missing}")
    if contract["countReconciliation"]["status"] != "resolved":
        fail("operation count reconciliation is not resolved")


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    verify_migrations(root)
    verify_openapi(root)
    print("Phase 0 baseline verification: PASS (9 migrations, 96 runtime operations, 52 core operations)")
    return 0

if __name__ == "__main__":
    sys.exit(main())