# 同行资本市场内容系统｜公众号留言 / 私信正式需求入口 Runbook

## 1. 目标

把公众号留言区与后续私信入口，先搭成一套正式对象系统。

第一阶段只做 4 件事：

1. 把外部输入落成统一对象
2. 自动或半自动归类成 4 类正式需求
3. 让系统能看见这些需求有没有进来
4. 给未来微信接口 / 网页抓取 / bot 接入预留统一数据契约

明确暂不做：

- 不承诺实时自动抓微信留言
- 不承诺自动回复
- 不承诺高频自动派单

---

## 2. 当前正式分类

### 2.1 content_request

- 含义：想看某个话题的内容、希望写一篇文章、继续拆某个热点
- route: `market_content_factory`

### 2.2 research_request

- 含义：想让系统研究某个行业 / 赛道 / 方向
- route: `vc_research`

### 2.3 project_review_request

- 含义：想让系统看看某个项目、公司、BP、融资机会
- route: `vc_project_line`

### 2.4 cooperation_request

- 含义：合作 / 推广 / 对接 / 商务相关
- route: `market_business_dev`

### 2.5 unknown_request

- 含义：边界不清、语义含混、包含多个强意图
- route: `founder_triage`

---

## 3. 正式对象位置

- 需求对象目录：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/12_public_intake_requests/`
- 模板：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/templates/market_public_intake_request_template.md`
- 看板：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/YYYYMMDD__market-public-intake-board.md`

---

## 4. 手动 / 半自动录入方法

### 4.1 标准命令

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_public_intake_request_record.py \
  --source-platform wechat \
  --source-channel wechat_comment \
  --queue-key claude_code_cache_bugs_20260331 \
  --requester-handle user_a \
  --message-text "能不能继续写一篇 Claude Code 和 Codex 成本差异的拆解？" \
  --write
```

### 4.2 也支持从文件录入

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_public_intake_request_record.py \
  --source-platform wechat \
  --source-channel manual_copy \
  --message-file /absolute/path/to/message.txt \
  --write
```

### 4.3 脚本会做什么

- 自动分类为：
  - `content_request`
  - `research_request`
  - `project_review_request`
  - `cooperation_request`
  - `unknown_request`
- 自动给出：
  - `routed_department`
  - `classification_confidence`
  - `normalized_brief`
  - `next_action`

若判断不稳，默认回退到：

- `unknown_request`
- `founder_triage`

---

## 5. 看板刷新

### 5.1 标准命令

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_public_intake_board_builder.py \
  --date 2026-04-02 \
  --write
```

### 5.2 输出

- Markdown：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260402__market-public-intake-board.md`
- Snapshot JSON：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260402__market-public-intake-board.snapshot.json`

---

## 6. 后续接口契约

未来无论是：

- 微信留言抓取
- 微信私信转存
- 飞书 bot 汇报
- 网页抓取或人工复制

都尽量统一映射到同一组字段：

- `source_platform`
- `source_channel`
- `source_message_id`
- `source_article_queue_key`
- `requester_handle`
- `submitted_at`
- `normalized_request_type`
- `routed_department`
- `classification_confidence`
- `status`
- `normalized_brief`
- `next_action`

也就是说：

> 未来可以换接入方式，但不要换对象结构。

---

## 7. 当前处理纪律

- 留言入口当前是“正式需求入口”，不是互动数据仓库。
- 真正值得推进的留言，要落正式对象，不只写在人工 feedback 里。
- `market_post_publish_feedback_record.py` 仍负责记录“代表性留言”和“业务反馈”；
  - 但如果留言本身已经构成正式需求，必须另外写一条 `public intake request`。
- 第一阶段只要求“系统接得住、分得清、看得到”，不追求全自动吞吐。

---

## 8. 当前验收标准

- 可以手动 / 半自动录入一条公众号留言需求
- 系统能自动归类并落正式对象
- 系统能生成需求看板
- 后续想接微信真实留言时，不需要重新设计对象结构
