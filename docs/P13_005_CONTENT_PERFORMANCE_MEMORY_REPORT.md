# P13-005 Content Performance Memory Report

## 本轮目标

把人工录入的发布表现沉淀为长期内容表现记忆，关联 final candidate、version、title pattern 和 lessons。

## 修改文件

- `src/content_system/content_performance_memory.py`
- `scripts/update_content_performance_memory.py`
- `Makefile`

## 已完成能力

- 生成 `content_performance_memory.json/md`。
- 生成 frontstage performance memory board。
- 记录 views、likes、wows、shares、comments、new followers。
- 提取 title/opening pattern 和初步 lessons。

## 安全边界

- 只记录和总结，不自动改规则。
- 不自动发布，不自动抓取数据。

## 当前限制

样本少时 lessons 只作为弱信号，不能视为绝对结论。
