# P32-001 Legacy Agent / Skill / Prompt Asset Audit Report

## 目标

审计当前仓库、内容素材库与 OpenClaw 只读目录中的内容生产 know-how 资产，包括 prompt、skill、recipe、rubric、template、example、failure case、agent config 与 methodology。

## 输出

- `同行资本市场内容系统/10_logs/latest_legacy_content_asset_audit.json`
- `同行资本市场内容系统/10_logs/latest_legacy_content_asset_audit.md`

## 边界

只读扫描旧目录，不修改 OpenClaw 文件；不把旧 prompt 原样迁入生产链路；含旧发布逻辑、旧状态字段或高风险依赖的资产只进入 reference / reject。
