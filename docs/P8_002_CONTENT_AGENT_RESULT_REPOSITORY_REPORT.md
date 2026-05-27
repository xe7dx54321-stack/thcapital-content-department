# P8-002 Content / Agent Result Repository v1 Report

## 本轮目标

在 SQLite runtime store 之上提供统一 repository API，减少后续代码直接散落读取文件或 SQL 查询。

## 新增文件

- `src/content_system/artifact_repository.py`
- `scripts/sync_artifact_repository.py`

## Repository 能力

- `list_recent_artifacts`
- `get_artifact_by_id`
- `list_recent_agent_runs`
- `list_publishing_candidates`
- `list_human_feedback`
- `search_artifacts_by_title`

## 新增命令

```bash
make artifact-repository-sync
```

## 输出产物

- `同行资本市场内容系统/10_logs/*artifact-repository-summary*.json`
- `同行资本市场内容系统/10_logs/*artifact-repository-summary*.md`

## 未做事项

- 不建立 Web API。
- 不替换现有文件产物。
