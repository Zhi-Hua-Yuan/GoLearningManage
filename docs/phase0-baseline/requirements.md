# 阶段 0：基线冻结需求

状态：`COMPLETED`

## 目标

建立独立的 `github.com/Zhi-Hua-Yuan/GoLearningManage` Go 单体仓库，冻结 Java 当前可观察的数据库迁移和 HTTP 合同，为第 2 周兼容基座开发提供可复现输入。

## 已冻结边界

1. Go 版本固定为 `go 1.27.0`、`toolchain go1.27.2`。
2. 公开上下文路径固定为 `/api`；空服务实现 `GET /api/health`。
3. 所有成功响应使用 `{code,message,data}`，成功值为 `0/ok`。
4. 每个响应带 `X-Trace-Id`；32 位小写十六进制入站值原样传播，其他值生成新值。
5. Java V1–V9 SQL 文件逐字节复制到 `db/migration/`，原发布 checksum 清单逐字节复制到 `db/migration/published-migrations.sha256`。
6. Java 封存 OpenAPI baseline 逐字节复制到 `api/openapi/`；RAG SSE 补充契约单独冻结并纳入 CI。
7. Go 应用本周不执行 DDL、不自动运行 Flyway，不读取或写入共享 MySQL 业务数据。
8. 第 1 周不声明用户、团队、项目、里程碑、任务、周复盘或统计接口已迁移；只有健康检查由 Go 提供。

## 操作数量核对

规划文本写明完整后端为 96 个操作、核心子集为 52 个。核对结果如下：

- Java 封存 OpenAPI：95 个操作。
- Java 控制器注解清单：96 个操作。
- 缺失项：`POST /api/ai/rag/ask/stream`，来源为 `RagController.askStream`。
- 前端调用和既有 Phase 3 文档均确认该 SSE 接口存在。
- 决议：不修改历史 OpenAPI；以 `runtime-supplement.json` 补齐第 96 个操作。

因此有效运行时合同为 96 个操作，其中核心 52 个、非核心 44 个。

## 阶段 0 退出条件

- [x] 独立 Git 仓库、`main` 分支和 origin 配置完成并同步。
- [x] 空服务可构建并可运行 `/api/health`。
- [x] V1–V9 与发布 checksum 校验通过。
- [x] 95-operation OpenAPI、1-operation supplement 和 52 核心操作 ledger 校验通过。
- [x] CI 包含 baseline、gofmt、vet、test、build 门禁。
- [x] 需求、TODO、Review、Handover 文档齐备并与当前仓库事实一致。