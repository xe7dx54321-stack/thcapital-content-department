# P12-005 Multi-day Version Analytics Report

## 本轮目标

汇总多日文章版本质量变化，判断系统是否越来越会改稿。

## 修改文件

- `src/content_system/multiday_version_analytics.py`
- `scripts/build_multiday_version_analytics.py`
- `Makefile`

## Analytics 内容

- 总版本数、accepted 数、promoted 数、final candidate 数。
- 平均 score delta。
- 最有效 action type。
- 常见风险模式。
- 用户偏好和系统质量趋势。

## 输出

- `同行资本市场内容系统/10_logs/YYYYMMDD__multiday-version-analytics.json`
- `同行资本市场内容系统/10_logs/latest_multiday_version_analytics.json`
- `同行资本市场内容系统/11_frontstage/latest_multiday_version_analytics_board.md`

## 当前限制

样本量不足时趋势会标记为 `INSUFFICIENT_DATA`，不做过度判断。
