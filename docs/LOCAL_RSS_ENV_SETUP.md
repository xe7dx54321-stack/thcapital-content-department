# 本地 RSS 环境配置指南

## 概述

本文档说明如何在本地 Mac mini 生产环境中配置 RSS 源，进行小规模 smoke test 验证。

## 重要安全规则

1. **永远不要提交真实 RSS URL 到 Git**
2. **使用 `.env.rss` 文件存储 RSS URL，该文件已被 `.gitignore` 忽略**
3. **`.env.rss.example` 只包含占位符，可以提交**
4. **不要在云端开发模式下启用真实 RSS**

## 配置步骤

### 1. 复制环境变量模板

```bash
cp .env.rss.example .env.rss
```

### 2. 编辑 `.env.rss` 文件

打开 `.env.rss` 文件，填入你的真实 RSS URL：

```bash
GEEKPARK_RSS_URL=https://geekpark.net/rss
OFFICIAL_AI_RSS_URL=https://official.ai/rss
```

### 3. 确认 `.env.rss` 不会被提交

```bash
git status --short
# .env.rss 应不在列表中

cat .gitignore | grep ".env.rss"
# 应显示 ".env.rss"
```

### 4. 加载环境变量

在运行 RSS 相关脚本前，加载环境变量：

```bash
source .env.rss
# 或
export $(cat .env.rss | xargs)
```

### 5. Smoke Test 配置

在 `config/rss_live_smoke_test.example.yaml` 中：

- `max_count: 2` - 最多启用 2 个 RSS 源
- `articles_per_source: 20` - 每个源最多 20 篇文章

### 6. 运行 Smoke Test

```bash
# 验证 RSS 源配置
make wechat-rss-sources-validate

# 抓取 RSS 文章
make wechat-rss-ingest

# 清洗去重
make wechat-rss-clean

# 提取情报
make wechat-article-intelligence

# 竞品覆盖分析
make competitive-coverage-analysis

# 使用边界检查
make wechat-rss-usage-boundary-gate

# 查看 Workbench
make wechat-workbench
```

## Smoke Test 验收字段

运行完成后，检查以下字段：

| 字段 | 说明 |
|------|------|
| `fetched_source_count` | 抓取的 RSS 源数量 |
| `article_count` | 抓取的文章总数 |
| `cleaned_count` | 清洗后的文章数 |
| `duplicate_count` | 去重的文章数 |
| `intelligence_article_count` | 提取情报的文章数 |
| `coverage_count` | 竞品覆盖分析数 |
| `style_pattern_count` | 风格 pattern 数 |
| `boundary_gate_status` | 使用边界 gate 状态 |
| `workbench_panel_visible` | Workbench 面板是否可见 |

## 如何恢复 Disabled 状态

如果需要停用真实 RSS：

### 1. 清空 `.env.rss`

```bash
echo "GEEKPARK_RSS_URL=" > .env.rss
echo "OFFICIAL_AI_RSS_URL=" >> .env.rss
```

### 2. 删除 RSS 运行产物

```bash
rm -f 同行资本市场内容系统/10_logs/*rss-ingest*
rm -f 同行资本市场内容系统/10_logs/*rss-clean*
rm -f 同行资本市场内容系统/10_logs/*rss-intelligence*
```

### 3. 确认 secret 没有入库

```bash
git status --short
grep -r "https://" --include="*.json" --include="*.yaml" --include="*.md" 同行资本市场内容系统/10_logs/
# 应无真实 URL 出现
```

### 4. 回到 dry-run 模式

```bash
make phase36-daily
# 应正常运行，不依赖真实 RSS
```

## 故障排查

### 问题：`.env.rss` 被意外提交

**解决**：

```bash
git reset HEAD -- .env.rss
git checkout -- .env.rss
rm .env.rss
# 重新从 .env.rss.example 复制
```

### 问题：RSS URL 泄漏到日志

**解决**：

检查日志文件，删除包含真实 URL 的文件：

```bash
grep -l "https://geekpark" 同行资本市场内容系统/10_logs/*.json
# 如有命中，删除对应文件
```

## 安全检查清单

- [ ] `.env.rss` 在 `.gitignore` 中
- [ ] `.env.rss.example` 只包含空占位符
- [ ] 真实 RSS URL 只在 `.env.rss` 中
- [ ] `.env.rss` 不在 `git status` 中
- [ ] 日志文件无真实 URL
- [ ] `auto_publish_allowed: false`

## 下一步

完成 Smoke Test 后，进入 Runtime 观察：

```bash
make runtime-observation-plan
make phase36-daily
```

---

**Phase36** | Cloud-to-Local Production Validation