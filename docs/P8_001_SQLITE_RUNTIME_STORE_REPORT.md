# P8-001 SQLite Runtime Store v1 Report

## 本轮目标

建立本地 SQLite runtime store，用于索引 pipeline run、agent run、source health、content artifacts、publishing candidates 和 human feedback。

## 新增文件

- `src/content_system/runtime_store_schema.py`
- `src/content_system/runtime_store.py`
- `scripts/init_runtime_store.py`
- `scripts/sync_runtime_store.py`
- `scripts/build_runtime_store_summary.py`
- `同行资本市场内容系统/12_runtime_store/README.md`

## 存储策略

SQLite 只做本地索引和查询层，不替换 JSON/Markdown 产物。数据库文件写入 `同行资本市场内容系统/12_runtime_store/content_system_runtime.db`，并由 `.gitignore` 忽略。

## 新增命令

```bash
make runtime-store-init
make runtime-store-sync
make runtime-store-summary
```

## 验收命令

```bash
make runtime-store-init
make runtime-store-sync
make runtime-store-summary
```

## 未做事项

- 不提交数据库文件。
- 不引入远程数据库。
- 不改变现有 JSON/Markdown 产物格式。
