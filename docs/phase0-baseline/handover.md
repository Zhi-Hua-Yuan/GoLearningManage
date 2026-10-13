# 阶段 0 Handover

## 已交付

- 仓库：`D:\ajavacode\GoLearningManage`
- 分支：`main`
- origin：`https://github.com/Zhi-Hua-Yuan/GoLearningManage.git`
- 已同步提交：`5f10d01`
- 启动入口：`cmd/api/main.go`
- 健康检查：`GET /api/health`
- 数据库基线：`db/migration/V1__...` 至 `V9__...`
- HTTP 基线：`api/openapi/stage8-pre-spring-ai-v1.0.0-openapi.json`
- 运行时补充：`api/openapi/runtime-supplement.json`，补齐 `POST /api/ai/rag/ask/stream`
- 阶段门禁：`python scripts/ci/verify_baseline.py`、`.github/workflows/ci.yml`

## 验收命令

```powershell
$go = 'C:\Program Files\Go\bin\go.exe'
& $go version
& $go fmt ./...
& $go test ./...
& $go vet ./...
& $go build ./cmd/api
python scripts/ci/verify_baseline.py
```

运行服务后：

```powershell
Invoke-RestMethod http://localhost:8123/api/health -Headers @{ 'X-Trace-Id' = '0123456789abcdef0123456789abcdef' }
```

预期响应为 `code=0`、`message=ok`、`data=ok`，并返回相同的 `X-Trace-Id`。

## 交接注意事项

1. 不要修改 V1–V9、历史 OpenAPI 或其 checksum；后续 V10+ 只能追加兼容迁移，并通过独立 Flyway CLI/容器执行。
2. `runtime-supplement.json` 是第 96 个运行时操作的契约来源，修改时必须同步 SHA-256 和 verifier。
3. 不要在 Go 尚未完成差分验证前接管任何核心写路由。
4. 下一周优先完成配置校验、MySQL pool/transaction、统一错误、ID/时间、JWT 与 BCrypt，并为双向 Java/Go 兼容测试准备 fixture。