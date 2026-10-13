# 阶段 0 Review

## 结论

实现满足空服务、不可变迁移、OpenAPI 冻结和 CI 基础要求，可以进入第 2 周兼容基座开发；在模块切流前必须解决规划 96 与事实 95 的数量差异。

## 复核要点

- `go.mod` 明确声明 `go 1.27.0` 与 `toolchain go1.27.2`。
- Gin 路由仅注册 `/api/health`，没有把未实现的核心或 Java AI 路由误注册到 Go。
- `Envelope` 的成功响应为 `code=0`、`message=ok`，健康数据为字符串 `ok`，与 Java 健康检查实际返回一致。
- Trace middleware 只接受 32 位小写 hex，并对非法或缺失值生成新的 32 位小写 hex。
- 9 个 Flyway 文件通过 Java 发布清单中的 SHA-256 校验；Go 未改写历史迁移。
- OpenAPI baseline 的 SHA-256 为 `6251fc7e067bffcdf648b2a3bc939c1bb808467debecc4dfb0e13339dae6f1b`，操作数为 95，核心 ledger 为 52。
- 应用启动没有自动连接 MySQL 或执行 DDL，避免阶段 0 改写共享数据库。

## 风险与后续

- 当前 shell PATH 没有自动暴露 Go 安装目录，Windows 本地命令需使用 `C:\Program Files\Go\bin\go.exe` 或刷新终端 PATH。
- Dockerfile 使用 `golang:1.27.2`，实际构建前需确认 Docker registry 可取得该镜像。
- CI 使用 Go 1.27.2；若 GitHub Actions runner 尚未提供该版本，应使用等价的 runner/toolchain 安装方式，不降低仓库声明的 Go 版本。
- 第 2 周再引入真实 MySQL readiness、JWT、BCrypt、schema version 校验和事务封装；本周不提前实现业务逻辑。