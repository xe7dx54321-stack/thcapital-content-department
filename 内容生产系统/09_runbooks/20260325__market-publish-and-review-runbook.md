# 同行资本市场内容系统｜2026-03-25｜发布队列与内容复盘

## 1. 这份 runbook 的作用

这份 runbook 用来承接已经准备好的内容，推进到：

- 可管理的发布队列
- 可持续积累的内容复盘

它解决的是：

> 内容不是“写完就结束”，而是要知道在哪个平台、由谁、什么时候发、发完效果如何、下次怎么改。

## 2. 当前 owner

- 对外唯一前台 bot：`market-editor`

当前阶段：

- `market-editor` 负责创建与维护 publish queue
- `market-editor` 负责创建 review skeleton
- 第一阶段允许“人审 + API 正式发布”，不建议继续走“后台手动发送后再补抓结果”这条难回流链路

## 3. 输入

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/{topic_key}/`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/`

## 4. 执行步骤

### A. 发布队列

1. 读取：
   - `th-publish-ops`
   - publish queue templates
   - 对应 Draft Pack

2. 先运行 queue builder：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_publish_queue_builder.py \
  --draft-pack-dir <draft_pack_dir> \
  --status queued \
  --publish-owner 老板 \
  --write
```

2.5 在日内 deadline 场景，先跑 continuity guard，避免“整包未过线但某个平台已可交付”被漏掉：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_publish_continuity_queue.py \
  --date <RUN_DATE> \
  --limit 5 \
  --preferred-platform wechat \
  --enqueue \
  --enqueue-limit 6 \
  --publish-owner 老板 \
  --planned-publish-at "<RUN_DATE> 17:30:00 CST" \
  --write
```

说明：

- 这一步会优先找 **当日已过线成品**，其次找 **当日整包 rework 但某个平台已达 publish-ready** 的对象，再次才是近期 backlog continuity。
- 当前硬要求是：**17:00 前至少要把当天可交付的公众号成品推进到草稿箱**，不能因为别的平台没过线就让全日挂零。
- `market_publish_queue_builder.py` 现在支持 **平台级 gate**：如果最新 scorecard 明确写出某个平台已达 `publish-ready`，即使整包仍在 `needs_revision`，这个平台也允许先进入 publish queue。

3. 如果准备提醒人发，再更新为：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_publish_queue_builder.py \
  --draft-pack-dir <draft_pack_dir> \
  --status waiting_human_publish \
  --write
```

4. 真实发布后，再更新为：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_publish_queue_builder.py \
  --draft-pack-dir <draft_pack_dir> \
  --status published \
  --platform wechat \
  --publish-url <published_url> \
  --write
```

4.2 如果是微信公众号，推荐生产链路不是“老板在后台点发送”，而是：

- 先让桥接把草稿送进公众号草稿箱
- 老板在草稿箱里完成人工审核
- 审核通过后，由系统调用 `freepublish/submit` 正式发布

执行命令：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_wechat_publish_submit.py \
  --queue-item <queue_item_path> \
  --write
```

说明：

- 该脚本会从 queue item 的 `publish_url=wechat-draft://...` 或 `notes.wechat_draft_media_id` 中读取草稿 `media_id`
- 调用微信官方 `freepublish/submit`
- 自动轮询 `freepublish/get`
- 成功后自动回填：
  - `status=published`
  - `actual_publish_at`
  - `publish_url`
  - `notes.wechat_publish_id / wechat_article_id`
- 这样后续 `market_wechat_result_backfill.py` 才能沿官方 API 链路继续自动追踪

4.5 如果是微信公众号，并且希望自动回填永久链接与官方表现数据，再运行：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_wechat_result_backfill.py --write
```

说明：

- 该脚本会自动读取 `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/` 中当前活跃的 wechat queue item
- 如果稿件本身就是通过 `freepublish/submit` 发布的，脚本会继续沿微信官方 API 链路回填永久链接与表现数据
- 如果稿件是“公众号后台人工发送”产生的，`freepublish/batchget` 很可能拿不到这条记录，因此不应把它当成主生产链
- 自动生成 / 更新 `24h / 72h` review 文件与 `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/` 下的表现追踪板
- Mac 本机需要存在本地凭据，优先读取环境变量 `TH_WECHAT_APPID` / `TH_WECHAT_APPSECRET`，否则读取：
  - `~/Library/Application Support/THCapital/wechat-bridge/credentials.json`
  - `~/.config/THCapital/wechat-bridge/credentials.json`

### B. 内容复盘

5. 读取：
   - `th-content-review`
   - `th-market-postmortem-optimizer`
   - review template
   - 对应 publish queue items

6. 运行 review builder：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_content_review_builder.py \
  --queue-item <queue_item_path> \
  --review-window 24h \
  --status collecting \
  --write
```

7. 当有足够真实发布信息后，可推进到：

```bash
python3 /Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_content_review_builder.py \
  --queue-item <queue_item_path> \
  --review-window 24h \
  --status ready \
  --write
```

8. 当 review 中已经有足够真实 learnings 时，再用：

```bash
# 当前阶段先由 market-editor 按 skill 手动执行 postmortem 诊断
# 不单独运行 builder，直接基于 review 卡产出优化结论
```

## 5. 标准产出

### 发布队列

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/YYYYMMDD__publish-queue-board.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue/YYYYMMDD_HHMMSS__queue_key__publish-queue-item.md`
- queue item 内现在要同时带：
  - `primary_handoff_path`
  - `supporting_asset_paths`
  - `manual_gate`
  - `human_action_required`
  - `frontstage_summary`

### 内容复盘

- `/Users/apple/Documents/同行资本内容部门/内容生产系统/07_performance_reviews/YYYYMMDD__topic_key__24h-review.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/07_performance_reviews/YYYYMMDD__weekly-review.md`
- `/Users/apple/Documents/同行资本内容部门/内容生产系统/07_performance_reviews/YYYYMMDD__monthly-review.md`

## 6. 状态纪律

- publish queue 只维护真实状态
- review 不得在未发布时装作已经有正式结论
- 浏览器自动化如需接入，只能做无 API 平台的兜底发稿 / 截图验收，不得替代主链状态

## 7. 对外回报方式

`market-editor` 对创始人的回报要尽量短，只说：

- 哪个话题已入队
- 哪个平台在等人工发
- 哪个平台已发
- 是否已开始 / 完成复盘
- 主交接文件在哪里

## 8. 关键边界

- 第一阶段不做“无人审核自动发稿”，但允许“人审通过后由 API 正式发布”
- 不得伪造 publish URL 或指标
- review 里缺数据可以写缺口，但不能硬编
- 微信官方 `datacube` 结果是 **T+1** 口径：发表后的官方表现数据需要等到 **次日 08:00 CST** 之后再拉
- 也就是说：
  - 通过 `freepublish/submit` 发布的稿件，永久链接可以自动回填
  - 正式阅读 / 点赞 / 在看 / 完读率等官方数据可以自动回填
  - 当前系统正式只做 `24h / 72h` 两个复盘窗口，不再追 2h 短窗

## 9. 微信公众号主链建议

当前已经验证过的事实是：

- “桥接入草稿箱”是通的
- “后台人工发送后，用 `freepublish/batchget` 自动回填永久链接”这条路不稳定，当前场景下拿不到已发记录
- “草稿审核后，再调用 `freepublish/submit` 正式发布”才是更适合自动结果回流的主链

因此推荐主生产链改成：

1. 系统写稿
2. Windows 桥接入公众号草稿箱
3. 老板在草稿箱审稿
4. 审稿通过后，运行 `market_wechat_publish_submit.py --queue-item ... --write`
5. 系统自动进入 `24h / 72h` 结果回流与复盘
