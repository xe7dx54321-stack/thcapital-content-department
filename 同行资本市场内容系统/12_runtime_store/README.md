# Runtime Store

This directory is reserved for the local SQLite runtime store.

Default database path:

```text
同行资本市场内容系统/12_runtime_store/content_system_runtime.db
```

The database is generated runtime state and must not be committed to Git. The
JSON/Markdown artifacts remain the transparent source of record; SQLite is only
a local index/query layer.
