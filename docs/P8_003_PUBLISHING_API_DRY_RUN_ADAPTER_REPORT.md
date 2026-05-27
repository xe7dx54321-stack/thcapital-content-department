# P8-003 Publishing API Dry-run Adapter v1 Report

## 本轮目标

为微信公众号和小红书发布准备建立 dry-run adapter，只验证字段与平台包结构，不真实发布。

## 新增文件

- `src/content_system/publishing_dry_run.py`
- `scripts/run_publishing_dry_run.py`

## 核心规则

- `would_publish` 永远为 `false`。
- 必须保留 `human_confirmation_required`。
- 不调用任何真实平台 API。

## 新增命令

```bash
make publishing-dry-run
```

## 检查范围

- 微信标题、正文、证据/source、风险提示。
- 小红书标题、正文、tags、image brief。
- 人工确认门槛。

## 未做事项

- 不接微信公众号 API。
- 不接小红书 API。
- 不生成发布成功状态。
