# P2-007 Content Workbench Board v1 报告

## 本轮目标

- 生成每日内容工作台。
- 汇总 briefs、outlines、drafts、packages、ready for human review、needs editing 和 hold。
- 给人工编辑提供下一步动作。

## 新增文件

- `src/content_system/content_workbench.py`
- `scripts/build_content_workbench.py`

## 新增命令

```bash
make content-workbench
```

## 输出产物

- `同行资本市场内容系统/11_frontstage/YYYYMMDD__content-workbench.md`
- `同行资本市场内容系统/11_frontstage/latest_content_workbench.md`
- `同行资本市场内容系统/10_logs/YYYYMMDD__content-workbench.json`
- `同行资本市场内容系统/10_logs/latest_content_workbench.json`

## 未做事项

- 不做 review queue 状态写入。
- 不采集人工反馈。
- 不自动发布。
