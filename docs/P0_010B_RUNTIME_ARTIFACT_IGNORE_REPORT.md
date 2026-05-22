# P0-010b Runtime Artifact Ignore 修复报告

## 背景

P0-010 验证时，`make official-lane-with-manifest` 成功运行并生成 official lane runtime manifest，但 `git status --short --branch` 显示若干运行产物仍为 untracked 文件。

这些文件包括：

- `同行资本市场内容系统/02_topic_radar/raw/official_YYYYMMDD/`
- `同行资本市场内容系统/02_topic_radar/source_packets/YYYYMMDD__official_lane/`
- `同行资本市场内容系统/03_topic_candidates/YYYYMMDD__official-top20.md`
- `同行资本市场内容系统/10_logs/YYYYMMDD__official-source-manifest.md`
- `同行资本市场内容系统/10_logs/latest_official_runtime_manifest.json`
- `同行资本市场内容系统/10_logs/latest_source_runtime_health.json`
- `同行资本市场内容系统/10_logs/latest_source_runtime_health.md`

这些属于运行生成产物，不应进入 Git。

## 本轮修复

本轮只更新 `.gitignore`，补齐以下忽略范围：

1. 活跃市场系统的 raw/source_packets 运行产物。
2. official lane 生成的 top20 和 source manifest。
3. runtime manifest 文件的 hyphen/underscore 两种命名形式。
4. source health / source runtime health 文件的 hyphen/underscore 两种命名形式。
5. latest official runtime manifest。

## 不做事项

本轮不修改 P0-010 的 wrapper 功能，不修改 official lane 主脚本，不改 fetcher，不做 retry/fallback，不新增数据库。

## 验收方式

运行：

```bash
git status --short --branch
```

预期：P0-010 验证产生的 raw、source_packets、official-top20、official-source-manifest、latest runtime/source-runtime-health 文件不再作为 untracked 文件出现。

如需复验：

```bash
make official-lane-with-manifest
make source-runtime-health
git status --short --branch
```

生成产物仍应被 `.gitignore` 忽略。

## 下一步

P0-010 主体功能已验证成功。P0-010b 清理 generated artifact ignore 规则后，可以继续进入 P0-011：Official Lane Runtime Manifest Direct Writer v1，或先继续观察 wrapper 运行结果。
