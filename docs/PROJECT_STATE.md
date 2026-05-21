# 项目状态记录

## 项目定位

`thcapital-content-department` 是同行资本内容部门的内容生产与素材管理工程仓库。当前目标是逐步升级为 AI/Agent 领域内容生产 Agent 系统，覆盖多源信息采集、结构化处理、价值判断、内容生成、头部内容学习与反馈迭代。

## 当前开发原则

1. 每次只做一个小 checkpoint，避免一次性大改。
2. 每个 checkpoint 必须能说明：改了什么、为什么改、如何验收、下一步是什么。
3. 不直接重写现有业务主链路，先补工程底座、审计工具和验证工具。
4. 每轮交付采用 `changed_files/` 整包复制到 GitHub Desktop 打开的真实仓库根目录，再 commit + push。
5. 关键状态同步维护在本文件和 `docs/DEVELOPMENT_TASKS.md`。

## 已完成 checkpoint

### P0-001：项目状态与健康检查底座

状态：已完成并入库。

完成内容：

- 新增项目健康检查入口 `scripts/doctor.py`。
- 新增路径工具 `src/content_system/paths.py`。
- 新增 `Makefile` 中的 `doctor` 目标。
- 新增工程状态与任务文档。
- 验证 GitHub Desktop 提交与推送链路可用。

### P0-002：路径硬编码审计工具

状态：本轮交付。

完成内容：

- 新增 `scripts/audit_hardcoded_paths.py`。
- 新增 `make path-audit`。
- 支持扫描 `/Users/...`、`/Volumes/...`、Windows 盘符路径、`file://` 等硬编码路径。
- 支持生成 Markdown 和 JSON 审计报告。
- 输出位置：`同行资本市场内容系统/10_logs/`。

## 当前系统状态判断

系统已经具备内容工厂雏形，但后续需要继续补齐：

1. 路径配置化。
2. 信源健康监控。
3. 结构化信息入库。
4. Topic cluster 与价值评分。
5. Content brief / outline / draft / quality report 四段式内容生成链路。
6. 头部内容学习与人工反馈闭环。

## 下一步建议

下一步建议做：

`P0-003：路径配置化第一刀`

目标：根据 P0-002 审计报告，优先处理 HIGH 级硬编码路径，把运行入口中的本机绝对路径改成环境变量或基于仓库根目录的相对路径。
