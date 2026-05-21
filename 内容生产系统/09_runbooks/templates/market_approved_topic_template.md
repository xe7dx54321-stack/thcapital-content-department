# Approved Topic Template

## 使用场景

这张卡用于承接创始人已明确确认的选题。

它的目标不是复述整张 `Top 8 -> Top 5` 板子，而是把已经拍板的信息整理成下游可直接执行的任务卡。

## 必备字段

- `topic_id`
- `topic_key`
- `candidate_id`
- `title`
- `approved_angle`
- `requested_platforms`
- `special_instructions`
- `approved_by`
- `approved_at`
- `status`

## 建议补充字段

- `source_board_path`
- `selected_rank`
- `selection_bucket`
- `selection_instruction`
- `restored_from_holdout`
- `platform_selection_mode`
- `platform_bundle`
- `platform_selection_reason`
- `market_potential`
- `brand_fit_judgment`
- `recommended_reason`
- `one_line_judgment`
- `source_refs`
- `risk_note`
- `draft_pack_target_dir`

## 推荐格式

```markdown
# Approved Topic Card

- `topic_id`: `topic__YYYYMMDD_HHMMSS__topic_key`
- `topic_key`: `topic_key`
- `candidate_id`: `cand__...`
- `title`: `正式选题标题`
- `approved_angle`: `最终确认角度`
- `requested_platforms`: `wechat, bilibili, baijiahao`
- `special_instructions`: `如无则写 n/a`
- `approved_by`: `老板`
- `approved_at`: `YYYY-MM-DD HH:MM:SS CST`
- `status`: `approved`

## Selection Context

- `source_board_path`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/03_topic_candidates/YYYYMMDD__daily-top8-to-top5.md`
- `selected_rank`: `2`
- `selection_bucket`: `top5`
- `selection_instruction`: `选第 2 个，做公众号、B站专栏和百家号`
- `restored_from_holdout`: `no`

## Platform Decision

- `platform_selection_mode`: `heuristic_bundle`
- `platform_bundle`: `builder_community_bundle`
- `platform_selection_reason`: `若创始人未显式指定平台，则由系统按题目属性自动推荐平台束`

## Platform Decision Notes

- `识别到 builder / workflow 信号`
- `上游 board 的平台提示提到了 wechat / zhihu`

## Carried Judgment

- `market_potential`: `高`
- `brand_fit_judgment`: `邻接高价值`
- `recommended_reason`: `...`
- `one_line_judgment`: `...`
- `risk_note`: `...`

## Source Refs

- `https://...`
- `/Users/apple/Documents/...source-packet.md`

## Next Handoff

- `draft_pack_target_dir`: `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/topic_key/`
- `next_step`: `approved -> drafting`
- `draft_scope`: `基于 approved_angle 生成 requested_platforms 对应的平台束草稿`
```
