# 阶段 0 TODO

| 优先级 | 工作项 | 状态 | 证据 |
|---|---|---|---|
| P0 | 初始化独立 Go Git 仓库、main 分支和 origin | DONE | `git remote -v`、`origin/main` |
| P0 | 固定 Go 版本并建立 Gin 空服务 | DONE | `go.mod`、`cmd/api` |
| P0 | `/api/health`、Envelope、Trace-Id、优雅停机 | DONE | `internal/httpapi`、`go test ./...` |
| P0 | 逐字节复制 Flyway V1–V9 与发布 checksum | DONE | `db/migration`、baseline verifier |
| P0 | 复制并冻结 95-operation Java OpenAPI baseline | DONE | `api/openapi/stage8-pre-spring-ai-v1.0.0-openapi.json` |
| P0 | 补齐并冻结遗漏的 RAG SSE 第 96 个操作 | DONE | `runtime-supplement.json`、supplement SHA-256 |
| P0 | 冻结 52 个核心操作清单 | DONE | `contract-manifest.json` |
| P0 | 建立 CI、gofmt、vet、test、build 门禁 | DONE | `.github/workflows/ci.yml` |
| P0 | 将阶段 0 提交推送至 GitHub origin/main | DONE | `origin/main -> 5f10d01` |

阶段 0已收尾。本周不修改 Java 仓库业务代码。