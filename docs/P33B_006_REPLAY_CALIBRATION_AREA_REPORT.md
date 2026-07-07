# P33B-006 Replay / Calibration Area Report

## 页面定位

Phase33 的 7-day replay dashboard。

它是校准分析，不是今天正式稿件。

必须和"今日稿件"分开。

## 设计原则

- 明确标注"回放不是正式产出"
- 校准建议不会自动应用
- 每日详情默认折叠

## 页面结构

### A. 7 天总览

显示：
- 回放天数
- 选出主选题天数
- 生成候选稿天数
- 质量 PASS 天数
- 重复选题风险
- 校准建议数量

### B. 每日卡片

每一天显示：
- 日期
- 主选题
- 质量评级
- 是否值得看
- 主要问题

**默认不展示全文。**

点击后展开：
- Brief 摘要
- Outline 摘要
- Draft 摘要
- Review 摘要
- Human checklist

### C. 校准建议

显示 Phase33 proposal：
- 问题类型
- 严重程度
- 建议调整
- 目标配置
- 是否自动应用：否

明确写：
"这些建议不会自动应用，需要人工确认。"

## 数据来源

来自 `workbench_view_model.replay_dashboard`。

## 安全边界

- 不自动应用 calibration proposal
- 不修改 topic scoring / playbook / methodology
- 不覆盖历史原稿
- 不删除历史版本
