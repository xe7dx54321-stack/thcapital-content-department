# 同行资本市场内容系统｜微信公众号结果回流 Runbook

## 1. 目标

把公众号成稿从“发出去就结束”，升级成正式结果回流链路。

当前链路要解决 4 件事：

1. 让 `published` 稿件必定进入 `24h / 72h review`
2. 自动回填公众号官方结果
3. 自动挂上账号层增粉上下文
4. 允许人工补充私聊、项目线索、代表性留言等质化反馈

---

## 2. 当前正式链路

### 2.1 草稿入箱

- Mac 主机写入 queue item
- `market_wechat_bridge_enqueue.py` 生成请求包
- Windows 副机运行 `wechat_bridge_consumer.py`
- 副机把草稿推入公众号草稿箱，并写回：
  - `result.json`
  - `publish_confirmation.json`（主机确认人工已发后补回）
  - `official_metrics.json`（新）

### 2.2 发布确认

#### A. 自动正式发布（晨间快反）

- 通过 `freepublish/submit`
- 理论上可以直接拿到正式发布记录与永久链接

#### B. 人工审核后发布（日间主线 / 当前默认）

- 创始人在公众号草稿箱里手工点发送
- 发送后必须至少做以下其一：
  - 运行 `market_human_publish_record.py --queue-item ... --write`
  - 或让系统从 `human_publish_confirmed_recorded_at` 做保守推断

说明：

- 当前系统已经允许“人工发布已确认，但暂时没有最终 URL”的稿件进入正式回流。
- 不再因为缺 `publish_url` 就整条复盘链挂起。
- 同时，主机会把人工发布确认同步到 bridge 请求包，避免副机把“仅入草稿箱”的稿件误判成已发布。

---

## 3. 自动结果回流

## 3.1 主脚本

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_wechat_result_backfill.py --write
```

作用：

- 扫描 `06_publish_queue/` 中活跃的 `wechat` queue item
- 优先尝试本机官方 API
- 若本机因 VPN / 白名单等原因不可用，则自动读取 Windows 副机写回的 `official_metrics.json`
- 自动更新：
  - queue item
  - `07_performance_reviews/_wechat_metrics/*.json`
  - `07_performance_reviews/*__24h-review.md`
  - `07_performance_reviews/*__72h-review.md`
  - `11_frontstage/*__market-performance-board.md`

## 3.2 关键状态

- `waiting_publish`
- `published_time_pending`
- `waiting_t_plus_one`
- `ready`
- `article_not_found`
- `blocked_by_whitelist`
- `official_api_error`

---

## 4. Windows 副机侧官方结果抓取

当前考虑到主机可能长期挂 VPN，公众号官方 API 不能只依赖 Mac 主机。

因此 Windows 副机的 `wechat_bridge_consumer.py` 已升级为：

- 除了创建草稿
- 还会读取主机写回的 `publish_confirmation.json`
- 还会在每轮顺手执行 `official metrics sync`
- 把结果写入：

```text
07_wechat_bridge_outbox/requests/<request_id>/official_metrics.json
```

这样主机即使被白名单拦，也能继续回填真实结果。

---

## 5. 人工质化反馈录入

公众号官方接口只能给出：

- 阅读
- 分享
- 在看
- 点赞
- 评论数
- 收藏
- 完读率 / 阅读时长
- 账号层新增 / 取消关注

但下面这些必须人工补：

- 私聊数
- 项目线索数
- 商务合作线索数
- 代表性留言
- 创始人对标题 / 包装 / 选题的主观判断

录入脚本：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_post_publish_feedback_record.py \
  --queue-key <queue_key> \
  --private-message-count 2 \
  --project-lead-count 1 \
  --business-lead-count 0 \
  --notable-comment "有人问这两个 bug 会不会影响 Cursor 类产品" \
  --manual-tag 成本 \
  --manual-tag 缓存 \
  --founder-summary "这篇选题的价值在于把工程问题讲成了成本问题。" \
  --title-feedback "n/a" \
  --packaging-feedback "n/a" \
  --next-topic-hint "可以继续做 Claude Code / Cursor / Codex 成本链路对比" \
  --write
```

产物位置：

```text
/Users/apple/Documents/同行资本内容部门/内容生产系统/07_performance_reviews/_manual_feedback/<queue_key>.json
```

这些反馈会在下一轮 `market_wechat_result_backfill.py --write` 时自动并入：

- review
- performance board

### 5.1 注意区分“反馈”与“正式需求”

- 代表性留言如果只是帮助理解文章反馈，可以继续记在：
  - `07_performance_reviews/_manual_feedback/`
- 但如果留言已经构成正式业务入口，例如：
  - 想让我们写某个话题
  - 想让我们研究某个行业
  - 想让我们看看某个项目
  - 想找合作 / 推广 / 对接
- 就不要只把它埋在 feedback 里，而是另外落一条正式需求对象：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_public_intake_request_record.py \
  --source-platform wechat \
  --source-channel wechat_comment \
  --queue-key <queue_key> \
  --message-text "这里粘贴留言正文" \
  --write
```

这样后续内容工厂、VC 研究、项目评估、商务入口才能统一接得住。

---

## 6. 24h / 72h 复盘原则

当前正式只做：

- `24h review`
- `72h review`

不再追：

- `2h review`

复盘里必须同时看两层：

### 6.1 文章层

- 阅读
- 分享
- 在看
- 点赞
- 评论数
- 收藏
- 完读率 / 阅读时长

### 6.2 业务层

- 有没有私聊
- 有没有项目线索
- 有没有商务合作苗头
- 有哪些代表性留言值得转成后续选题或研究需求

---

## 7. 当前生产建议

### 7.1 日间主线

- 继续保持“草稿箱人工审核后发送”
- 发送后尽量补一条人工确认记录

### 7.2 晨间快反

- 若自动发布走 `freepublish/submit`
- 结果回流会更完整、更顺滑

### 7.3 VPN / 白名单问题

- 若 Mac 主机出口 IP 不在白名单：
  - 本机 API 会显示 `blocked_by_whitelist`
  - 系统会优先读取 Windows 副机写回的 `official_metrics.json`
- 因此公众号结果回流的长期稳定方案是：
  - `Windows 副机（不挂 VPN）负责官方 API`
  - `Mac 主机负责业务对象回填与展示`

---

## 8. 当前要看的文件

- 结果板：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/20260402__market-performance-board.md`
- review：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/07_performance_reviews/`
- 指标缓存：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/07_performance_reviews/_wechat_metrics/`
- 人工反馈：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/07_performance_reviews/_manual_feedback/`
- Windows 副机官方结果：
  - `/Users/apple/Documents/同行资本内容部门/内容生产系统/07_wechat_bridge_outbox/requests/*/official_metrics.json`

---

## 9. 下一步

这条链路稳定后，再做两件事：

1. 把 result review 里的 learnings 更正式地回写给：
   - `topic-planner`
   - `content-writer`
   - `publish-ops`
2. 把公众号留言正式升级成需求入口，而不只是评论数指标
