# Phase37B Local Production Smoke Execution Guide

## 概述

本文档说明如何在本地 Mac mini 执行生产验证 smoke test 和 1-2 天观察。

**重要：本阶段不自动发布、不接公众号后台、不抓 RSS 外全文。**

---

## 前置条件

- [ ] Mac mini 已连接电源和网络
- [ ] Python 3.14 已安装
- [ ] Git 仓库已 clone
- [ ] `.env.rss` 已配置（见下文）
- [ ] `auto_publish` 已确认关闭
- [ ] 已阅读 `docs/LOCAL_PRODUCTION_ROLLBACK_AND_SAFETY_RUNBOOK.md`

---

## 1. 配置 .env.rss

### 1.1 复制模板

```bash
cd ~/thcapital-content-department
cp .env.rss.example .env.rss
```

### 1.2 填入 RSS URL

打开 `.env.rss`，填入 1-2 个 RSS 源的 URL：

```bash
# 最多启用 2 个源做 smoke
GEEKPARK_RSS_URL=https://geekpark.net/rss
OFFICIAL_AI_RSS_URL=https://official.ai/rss
```

### 1.3 确认未被 Git 跟踪

```bash
git status --short
# .env.rss 不应出现在列表中

cat .gitignore | grep ".env.rss"
# 应显示 .env.rss
```

---

## 2. 启用 1-2 个 RSS 源

- Smoke test 阶段最多启用 **2 个** RSS 源
- 每源最多抓取 **20 篇** 文章
- 确认 RSS URL 来自受信任来源

---

## 3. 运行各阶段 pipeline

### 3.1 Phase34A: RSS 情报层

```bash
make phase34a-daily
```

检查输出：
- `fetched_source_count` 是否等于启用的源数
- `article_count` 是否合理（每源 <= 20）
- `boundary_gate_status` 是否为 PASS

### 3.2 Phase34B: 选题多样性

```bash
make phase34b-daily
```

检查输出：
- 选题去重是否生效
- 差异化角度是否产生
- rerank 结果是否合理

### 3.3 Phase35: 编辑质量

```bash
make phase35-daily
```

检查输出：
- 标题候选数量（>= 5）
- AI 味拦截是否命中
- Draft style score 是否合理
- Version comparison gate 是否正常

### 3.4 Phase36: 生产验证

```bash
make phase36-daily
```

检查 readiness gate：
- 云端项目应为 PASS
- 本地项目应为 ACTIONABLE（初次运行）

### 3.5 Phase37A: 生产观察

```bash
make phase37a-daily
```

---

## 4. 打开 Workbench 查看生产验证面板

```bash
make wechat-workbench
```

在「系统运维 → 生产验证 / 本地观察」中查看：

- 当前模式：Local Production Validation
- RSS Smoke 状态
- Runtime 观察状态
- Production Readiness Gate
- 下一步建议

确认不显示：
- RSS secret URL
- RSS 原文全文
- raw JSON
- 运行日志全文

---

## 5. 观察 1-2 天

### 每天执行

```bash
# 每日早晨运行
make phase37a-daily
make wechat-workbench

# 记录到人工观察日志
# 打开 logs/latest_manual_observation_log.md 填写
```

### 每天检查项

1. Workbench 是否可打开
2. Runtime heartbeat 是否正常
3. 今日 final candidate 数量
4. 主选题是否重复
5. 是否有差异化角度
6. 标题是否像公众号标题
7. AI 味是否明显
8. 证据是否需要人工确认
9. 稿件是否值得人工修改
10. 是否建议发布

---

## 6. 如何记录人工观察

### 方式一：直接编辑 Markdown

打开 `同行资本市场内容系统/10_logs/latest_manual_observation_log.md`，
在对应日期的检查项中打勾，填写备注。

### 方式二：使用 JSON

编辑 `同行资本市场内容系统/10_logs/latest_manual_observation_log.json`。

---

## 7. 如何回滚

**如果遇到以下情况，立即停止并回滚：**

- RSS secret 泄漏到 Git
- auto_publish 被意外启用
- OpenClaw 被意外修改
- 系统产生大量错误

### 紧急回滚步骤

```bash
# 1. 暂停 Runtime（如果有）
python3 scripts/runtime_control.py pause

# 2. 清空 .env.rss
echo "GEEKPARK_RSS_URL=" > .env.rss
echo "OFFICIAL_AI_RSS_URL=" >> .env.rss

# 3. 检查 secret 是否泄漏
git status --short
grep -r "https://" --include="*.json" --include="*.yaml" --include="*.md" 同行资本市场内容系统/10_logs/

# 4. 删除 RSS 运行产物
rm -f 同行资本市场内容系统/10_logs/*rss-ingest*
rm -f 同行资本市场内容系统/10_logs/*rss-clean*
rm -f 同行资本市场内容系统/10_logs/*rss-intelligence*

# 5. 回到 dry-run 确认
make phase37a-daily
```

详细回滚指南：`docs/LOCAL_PRODUCTION_ROLLBACK_AND_SAFETY_RUNBOOK.md`

---

## 8. 安全边界确认

执行前确认：

- [ ] auto_publish_allowed = false
- [ ] allow_wechat_api = false
- [ ] save_fulltext_to_git = false
- [ ] 不提交 RSS 原文全文
- [ ] 不提交 .env.rss
- [ ] 不抓 RSS 外全文
- [ ] 不修改 OpenClaw
- [ ] 不调用图片模型

---

## 9. 观察期结束

观察 1-2 天后，汇总：

1. RSS smoke test 是否通过
2. Runtime 是否稳定运行
3. 人工观察记录
4. Production Readiness Gate 状态
5. 校准项建议

提交 Closeout Report 进入下一阶段。

---

**Phase37B** | Local Production Smoke Execution & 1-2 Day Observation Guide