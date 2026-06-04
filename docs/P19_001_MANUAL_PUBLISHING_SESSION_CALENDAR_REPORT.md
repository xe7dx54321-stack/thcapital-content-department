# P19-001 Manual Publishing Session Calendar Report

## 目标

把 manual publish session 升级为 7 天日历视图，并把 copy pack、visual checklist 和 final candidate readiness 合并到每个发布 slot。

## 已完成

- 新增 `publishing_session_calendar.py`。
- 新增 `build_publishing_session_calendar.py`。
- 输出 publishing session calendar JSON/Markdown 和 frontstage board。

## 边界

- 不自动创建 publish session。
- 不自动发布。
- 不调用公众号 API。
