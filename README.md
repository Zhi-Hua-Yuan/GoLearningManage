# GoLearningManage

Go 1.27.2 migration target for `LearningManage`.

## Week 1 baseline

This repository contains the Phase 0 foundation:

- Go module `github.com/Zhi-Hua-Yuan/GoLearningManage`, pinned to `go 1.27.0` and `toolchain go1.27.2`.
- Gin HTTP server with graceful shutdown, `/api` context path, response envelope, and `X-Trace-Id` propagation.
- Runnable `GET /api/health` returning `{ "code": 0, "message": "ok", "data": "ok" }`.
- Byte-for-byte copies of Java Flyway V1–V9 and the published checksum list.
- Complete 96-operation runtime contract: 95 sealed OpenAPI operations plus the omitted RAG streaming operation in `api/openapi/runtime-supplement.json`.
- CI for baseline checks, formatting, vet, tests, and build.

The sealed Java OpenAPI document remains immutable at 95 operations. The Java controller inventory and frontend streaming client identify the 96th operation, `POST /api/ai/rag/ask/stream`; it is frozen separately with its own checksum rather than altering the published baseline.

## Local commands

On Windows, use the installed Go executable if the current shell has not yet refreshed PATH:

```powershell
& 'C:\Program Files\Go\bin\go.exe' test ./...
& 'C:\Program Files\Go\bin\go.exe' build ./cmd/api
python scripts/ci/verify_baseline.py
```

Run the service with `HTTP_ADDR=:8123` and call `GET http://localhost:8123/api/health`. Docker users can run `docker compose -f deploy/docker-compose.yml up --build`.