# P7-008 Retry / Fallback Runner Report

## 本轮目标

建立 retry / fallback plan 入口，但不重写 fetcher。

## 新增命令

```bash
make retry-fallback-runner
```

## v1 行为

- 读取 source runtime health。
- 识别 missing / error hint source。
- 根据 `config/sources.yaml` 列出 fallback methods。
- 生成 manual retry plan。

## 当前限制

- 不自动大规模补抓。
- 不改抓取主链路。
- 不新增 retry queue 数据库。
