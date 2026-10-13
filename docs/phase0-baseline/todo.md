# 阶段 0 TODO

| 优先级 | 工作项 | 状态 | 证据 |
|---|---|---|---|
| P0 | 初始化独立 Go Git 仓库、迁移分支和 origin | DONE | `git remote -v`、`codex/week1-baseline` |
| P0 | 固定 Go 版本并建立 Gin 空服务 | DONE | `go.mod`、`cmd/api` |
| P0 | `/api/health`、Envelope、Trace-Id、优雅停机 | DONE | `internal/httpapi`、`go test ./...` |
| P0 | 逐字节复制 Flyway V1–V9 与发布 checksum | DONE | `db/migration`、baseline verifier |
| P0 | 复制并冻结 Java OpenAPI baseline | DONE | `api/openapi` |
| P0 | 冻结 52 个核心操作清单 | DONE | `contract-manifest.json` |
| P0 | 建立 CI、gofmt、vet、test、build 门禁 | DONE | `.github/workflows/ci.yml` |
| P1 | 核对规划文本中额外的第 96 个操作 | OPEN | 进入第 2 周前完成 |
| P1 | 将阶段 0 提交推送至 GitHub origin | PENDING_REMOTE | 需要远端仓库可访问及凭据 |

本周不修改 Java 仓库；其未提交的 `README.md` 修改保留原状。