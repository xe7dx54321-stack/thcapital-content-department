# P14-004 Methodology-based Topic Scoring Report

## 本轮目标

在原 value scoring 之外，新增 methodology-based topic scoring，判断信息是否真的适合成文。

## 修改文件

- `src/content_system/methodology_topic_scoring.py`
- `scripts/score_topics_with_methodology.py`

## 输出

- `同行资本市场内容系统/03_topic_candidates/latest_methodology_topic_scores.json`
- `同行资本市场内容系统/03_topic_candidates/latest_methodology_topic_scores.md`

## 核心能力

- 对 high-value candidates / topic clusters 重新打方法论分。
- 标记 WRITE / WATCH / HOLD / REJECT。
- 推荐 content strategy recipe。
- 识别“信息有价值但不适合成文”和“适合成文但需要补证据”的情况。

## 边界

不替换原 value scoring，不自动改变候选池，只生成辅助评分。
