# P3-003 Critic Agent Review v1 Report

## 本轮目标

- 生成反方/资深审稿人视角的规则型批评意见。
- 检查证据数量、质量分、发布状态、标题、正文结构、风险披露、source/evidence 缺失和过强表述。
- 输出建设性建议与 must-fix 列表。

## 新增文件

- `src/content_system/critic_review.py`
- `scripts/build_critic_reviews.py`

## 新增命令

```bash
make critic-reviews
```

## 输出产物

- `同行资本市场内容系统/06_review_queue/*critic-reviews*.json`
- `同行资本市场内容系统/06_review_queue/*critic-reviews*.md`

## 验收方式

- `python3 -m py_compile src/content_system/critic_review.py`
- `python3 -m py_compile scripts/build_critic_reviews.py`
- `make critic-reviews`

## 注意事项

批评结果用于改稿和分流，不自动阻断业务脚本。
