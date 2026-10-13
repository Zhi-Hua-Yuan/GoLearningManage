# GoLearningManage

Go 1.27.2 migration target for `LearningManage`.

## Week 1 baseline

This repository contains the Phase 0 foundation:

- Go module `github.com/Zhi-Hua-Yuan/GoLearningManage`, pinned to `go 1.27.0` and `toolchain go1.27.2`.
- Gin HTTP server with graceful shutdown, `/api` context path, response envelope, and `X-Trace-Id` propagation.
- Runnable `GET /api/health` returning `{ "code": 0, "message": "ok", "data": "ok" }`.
- Byte-for-byte copies of Java Flyway V1–V9 and the published checksum list.
- Sealed Java OpenAPI baseline plus a 52-operation core ledger.
- CI for baseline checks, formatting, vet, tests, and build.

The sealed Java OpenAPI document currently contains 95 operations. The roadmap mentions 96; that one-operation discrepancy is explicitly recorded in `api/openapi/contract-manifest.json` and must be resolved before module cutover. No endpoint is invented to make the count appear to match.

## Local commands

On Windows, use the installed Go executable if the current shell has not yet refreshed PATH:

```powershell
& 'C:\Program Files\Go\bin\go.exe' test ./...
& 'C:\Program Files\Go\bin\go.exe' build ./cmd/api
python scripts/ci/verify_baseline.py
```

Run the service with `HTTP_ADDR=:8123` and call `GET http://localhost:8123/api/health`. Docker users can run `docker compose -f deploy/docker-compose.yml up --build`.