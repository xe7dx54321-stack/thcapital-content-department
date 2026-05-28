# P13-006 Performance-to-Learning Feedback Loop Report

## 本轮目标

把真实发布后的人工表现数据转成学习反馈，反哺选题、标题、开头、结构、证据和 Agent 策略。

## 修改文件

- `src/content_system/performance_learning_feedback.py`
- `scripts/build_performance_learning_feedback.py`
- `Makefile`

## 已完成能力

- 读取 content performance memory、multi-day analytics、action effectiveness、prompt/rule regression 和 pattern 学习产物。
- 输出 topic/title/opening/evidence/agent feedback。
- 所有 recommendations 均为 `auto_apply=false`。
- 新增 `make performance-learning-feedback`。

## 安全边界

- 只生成建议。
- 不自动改 prompt。
- 不自动改 scoring rules。
- 不自动改 pattern adapters。

## 当前限制

反馈质量依赖人工 metrics 的持续录入。
