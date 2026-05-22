# P2-004 Content Quality Review v1 报告

## 本轮目标

- 对规则型草稿做规则型质量检查。
- 检查 evidence 数量、标题、正文长度、风险披露、source_id、evidence_id 和过强表述。
- 输出人工编辑前的质量状态。

## 新增文件

- `src/content_system/content_quality.py`
- `scripts/review_content_quality.py`

## 新增命令

```bash
make content-quality-review
```

## 输出产物

- `同行资本市场内容系统/05_draft_packs/YYYYMMDD__content-quality-review.json`
- `同行资本市场内容系统/05_draft_packs/YYYYMMDD__content-quality-review.md`
- `同行资本市场内容系统/05_draft_packs/latest_content_quality_review.json`
- `同行资本市场内容系统/05_draft_packs/latest_content_quality_review.md`

## 状态规则

- `READY_FOR_HUMAN_REVIEW`
- `NEEDS_LIGHT_EDIT`
- `NEEDS_MAJOR_EDIT`
- `HOLD`

## 未做事项

- 不做事实联网核查。
- 不调用 LLM 审稿。
