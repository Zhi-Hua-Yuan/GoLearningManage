# 阶段 0 Review

## 结论

阶段 0已完成，可以进入第 2 周兼容基座开发。

## 复核要点

- `go.mod` 明确声明 `go 1.27.0` 与 `toolchain go1.27.2`。
- Gin 路由仅注册 `/api/health`，没有把未实现的核心或 Java AI 路由误注册到 Go。
- `Envelope` 的成功响应为 `code=0`、`message=ok`，健康数据为字符串 `ok`，与 Java 健康检查实际返回一致。
- Trace middleware 只接受 32 位小写 hex，并对非法或缺失值生成新的 32 位小写 hex。
- 9 个 Flyway 文件通过 Java 发布清单中的 SHA-256 校验；Go 未改写历史迁移。
- 历史 OpenAPI baseline 的 SHA-256 为 `6251fc7e067bffcdf648b2a3bc939c1bb808467debecc4dfb0e13339dae6f1b2`。
- Java 控制器共 96 个操作；其中 `POST /api/ai/rag/ask/stream` 未出现在历史 95-operation OpenAPI，因此以独立 supplement 冻结，未修改历史文件。
- 应用启动没有自动连接 MySQL 或执行 DDL，避免阶段 0 改写共享数据库。
- 本地 `main`、远端 `origin/main` 和提交 `5f10d01` 一致，工作区干净。

## 风险与后续

- 当前 shell PATH 没有自动暴露 Go 安装目录，Windows 本地命令需使用 `C:\Program Files\Go\bin\go.exe` 或刷新终端 PATH。
- 第 2 周再引入真实 MySQL readiness、JWT、BCrypt、schema version 校验和事务封装；本周不提前实现业务逻辑。