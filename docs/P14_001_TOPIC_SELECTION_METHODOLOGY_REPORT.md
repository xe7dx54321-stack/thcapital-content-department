# P14-001 Topic Selection Methodology Report

## 本轮目标

建立统一的选题方法论，用 8 个维度判断“什么题值得写”，并明确一票否决项与进入写作链路前必须回答的问题。

## 修改文件

- `config/topic_selection_methodology.json`
- `docs/CONTENT_TOPIC_SELECTION_METHOD.md`
- `src/content_system/topic_selection_methodology.py`
- `scripts/validate_topic_selection_methodology.py`

## 核心能力

- 定义变化强度、预期差、产业链影响、证据强度、叙事张力、窗口期、独立判断潜力、读者收益。
- 保留 reject rules，避免只有标题党、PR、弱证据或无法形成判断的选题进入写作链路。
- 提供 validate 命令，确保配置可审阅、可复用。

## 边界

方法论只提供判断标准，不自动改写现有 scoring rules，也不替代人工判断。
