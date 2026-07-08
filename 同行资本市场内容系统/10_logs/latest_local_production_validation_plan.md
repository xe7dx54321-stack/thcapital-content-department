# Cloud-to-Local Production Validation Plan

## 概述

- **生成时间**: 2026-07-08T03:14:53.939307
- **当前模式**: cloud_development
- **状态**: generated

## 云端已完成能力

- Phase33B: Workbench 运营控制台
- Phase34A: WeChat RSS 全文情报层工程能力
- Phase34B: 选题去重、差异化角度、主选题 rerank
- Phase35: 编辑风格手册、叙事框架、标题生成、AI 味拦截

## 需要本地真实 RSS 验证的能力

- RSS ingest 稳定性
- 正文清洗效果
- 情报抽取准确性
- 竞品覆盖价值

## 需要 Mac mini Runtime 验证的能力

- LaunchAgent 定时运行
- Heartbeat 监控
- Retry queue 处理
- Missed-run catch-up

## 仅需 dry-run 的能力

- 编辑风格手册验证
- 叙事框架选择
- 标题生成规则
- AI 味拦截
- Draft style score
- Version comparison gate

## 验证顺序

| Step | 名称 | 描述 | 必须 | 本地执行 | 云端安全 |
|------|------|------|------|----------|----------|
| cloud_regression | 云端回归验证 | 验证所有 Phase35/34B/34A/33B pipeline 在云端通过 | True | False | True |
| rss_smoke_test | RSS Smoke Test | 本地启用 1-2 个 RSS 源进行小规模验证 | False | True | False |
| runtime_observation | Runtime 观察 | Mac mini Runtime/LaunchAgent 观察 1-2 天 | False | True | False |
| data_calibration | 真实数据校准 | 记录真实数据校准结果 | False | True | False |
| workbench_panel | Workbench 生产验证面板 | Workbench 显示生产验证状态 | True | False | True |
| readiness_gate | Production Readiness Gate | 评估是否可以进入真实观察 | True | False | True |

## 通过标准

- ✅ 所有云端 pipeline 通过
- ✅ Usage boundary gate 通过
- ✅ 无 secret 入 Git
- ✅ 无 OpenClaw 修改
- ✅ auto_publish 已禁用

## 警告标准

- ⚠️ RSS smoke test 待本地执行
- ⚠️ Runtime 观察待本地执行
- ⚠️ 真实数据校准待执行

## 阻断标准

- ❌ 云端 pipeline 失败
- ❌ Secret 泄漏检测
- ❌ auto_publish 已启用
- ❌ OpenClaw 被修改

## 统计

- **检查项总数**: 6
- **本地执行项**: 3
- **云端安全项**: 3

---

**Phase36** | Cloud-to-Local Production Validation Plan
