# 路径硬编码审计报告

生成时间：`2026-05-22T00:33:23.977736+00:00`
扫描文件数：`40677`
命中总数：`75466`
HIGH：`77`
MEDIUM：`18800`
LOW：`56589`

## 结论摘要

发现 77 个 HIGH 风险项，P0-003 应优先处理运行脚本、控制台入口和配置文件。

## HIGH 风险项

| 文件 | 行号 | 类型 | 命中内容 | 建议 |
|---|---:|---|---|---|
| `内容工厂控制台/README.md` | 34 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容工厂控制台/open.sh` | 15 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容工厂控制台/runtime/server.json` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容工厂控制台/start.sh` | 5 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/codex_hotfix_mailbox_state.py` | 13 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/07_wechat_bridge_outbox/codex_content_hotfix` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_approved_topic_builder.py` | 26 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_content_heartbeat_queue.py` | 14 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_content_hygiene_guard.py` | 12 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_content_pack_truth.py` | 11 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_content_polish_builder.py` | 27 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_content_review_builder.py` | 12 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_daily_source_manifest.py` | 22 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_daily_source_manifest.py` | 168 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_day_mainline_briefing_builder.py` | 21 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_day_mainline_delivery_notifier.py` | 21 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_day_mainline_delivery_retry.py` | 13 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_day_mainline_selection_apply.py` | 13 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_draft_pack_builder.py` | 12 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_feishu_doc_delivery.py` | 17 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_feishu_doc_delivery.py` | 125 | `file_url` | `file://` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_frontstage_board_builder.py` | 14 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_human_publish_record.py` | 12 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_itjuzi_live_probe.py` | 21 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_lane_approved_topic_builder.py` | 25 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_learning_knowledge_builder.py` | 25 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_learning_memo_builder.py` | 14 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_learning_pool_board_builder.py` | 1565 | `file_url` | `file://{escape(sample[` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_learning_pool_board_builder.py` | 1578 | `file_url` | `file://` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_learning_pool_board_builder.py` | 1591 | `file_url` | `file://{escape(item[` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_learning_pool_board_builder.py` | 1591 | `file_url` | `file://{escape(item[` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_manual_wechat_rescue.py` | 12 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_morning_flash_autosign.py` | 11 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_morning_flash_delivery_notifier.py` | 20 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_morning_flash_gate_recovery.py` | 11 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_morning_flash_preflight.py` | 18 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_morning_flash_publish_guard.py` | 17 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_morning_flash_roundup_spec.py` | 10 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_morning_flash_source_bundle.py` | 22 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_ops_dashboard_builder.py` | 20 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_ops_dashboard_builder.py` | 198 | `file_url` | `file://{quote(path` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_pipeline_integrity_report.py` | 14 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_pipeline_reconcile.py` | 16 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_platform_lock_bridge.py` | 20 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_platform_task_sheet_to_approved.py` | 23 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_post_publish_feedback_record.py` | 12 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_public_intake_board_builder.py` | 13 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_public_intake_request_record.py` | 11 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_publish_continuity_queue.py` | 16 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_publish_queue_builder.py` | 17 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_recent_topic_guard.py` | 12 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_stage_bootstrap.py` | 12 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_stage_job_runner.py` | 19 | `mac_user_path` | `/Users/apple/.openclaw` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_top20_continuity_board_builder.py` | 14 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_top20_pack_builder.py` | 17 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_top20_pack_guard.py` | 14 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_topic_capture_round.py` | 30 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_topic_radar_brief_builder.py` | 23 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_topic_radar_execution_log_builder.py` | 11 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_wechat_bridge_enqueue.py` | 15 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_wechat_bridge_enqueue.py` | 257 | `file_url` | `file://` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_wechat_bridge_reconcile.py` | 13 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/07_wechat_bridge_outbox` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_wechat_bridge_reconcile.py` | 14 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/06_publish_queue` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_wechat_deep_capture_round.py` | 18 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_wechat_deep_capture_round.py` | 26 | `mac_user_path` | `/Users/apple/.openclaw` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_wechat_publish_submit.py` | 18 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_wechat_result_backfill.py` | 18 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_wechat_rss_refresh.py` | 17 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/market_wechat_subscription_bootstrap.py` | 20 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容生产系统/09_runbooks/scripts/test_market_day_mainline_parsers.py` | 17 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容素材库/灵感素材库/URL抓取/2026-04-12/A_night/batch1_36kr.sh` | 3 | `mac_user_path` | `/Users/apple/Documents/同行资本vc部门/VC系统开发规划/同行资本运行台/scripts/crawl4ai_capture_helper.py` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `内容素材库/灵感素材库/URL抓取/2026-04-12/A_night/batch1_36kr.sh` | 4 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容素材库/灵感素材库/URL抓取/2026-04-12/A_night` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `同行资本市场内容系统/09_runbooks/scripts/market_learning_memo_builder.py` | 11 | `mac_user_path` | `/Users/apple/Documents/同行资本市场内容系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `同行资本市场内容系统/09_runbooks/scripts/market_learning_pool_board_builder.py` | 13 | `mac_user_path` | `/Users/apple/Documents/同行资本市场内容系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `同行资本市场内容系统/09_runbooks/scripts/market_official_update_lane.py` | 12 | `mac_user_path` | `/Users/apple/Documents/同行资本市场内容系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `同行资本市场内容系统/09_runbooks/scripts/market_top20_pack_guard.py` | 26 | `mac_user_path` | `/Users/apple/Documents/同行资本市场内容系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `同行资本市场内容系统/09_runbooks/scripts/market_topic_capture_round.py` | 10 | `mac_user_path` | `/Users/apple/Documents/同行资本市场内容系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `同行资本市场内容系统/09_runbooks/scripts/market_wechat_deep_capture_round.py` | 11 | `mac_user_path` | `/Users/apple/Documents/同行资本市场内容系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |
| `同行资本市场内容系统/09_runbooks/scripts/market_wechat_rss_refresh.py` | 11 | `mac_user_path` | `/Users/apple/Documents/同行资本市场内容系统` | 优先改为环境变量、配置项或基于仓库根目录的相对路径。 |

## MEDIUM 风险项

| 文件 | 行号 | 类型 | 命中内容 | 建议 |
|---|---:|---|---|---|
| `config/ENV_EXAMPLE.txt` | 5 | `mac_user_path` | `/Users/apple/Documents/thcapital-content-department` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `config/ENV_EXAMPLE.txt` | 8 | `mac_user_path` | `/Users/apple/Documents/thcapital-content-department/同行资本市场内容系统` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `config/ENV_EXAMPLE.txt` | 11 | `mac_user_path` | `/Users/apple/Documents/thcapital-content-department/内容生产系统` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `config/ENV_EXAMPLE.txt` | 14 | `mac_user_path` | `/Users/apple/Documents/thcapital-content-department/内容工厂控制台` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `env.example` | 5 | `mac_user_path` | `/Users/apple/Documents/thcapital-content-department` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `env.example` | 8 | `mac_user_path` | `/Users/apple/Documents/thcapital-content-department/同行资本市场内容系统` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `env.example` | 11 | `mac_user_path` | `/Users/apple/Documents/thcapital-content-department/内容生产系统` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `env.example` | 14 | `mac_user_path` | `/Users/apple/Documents/thcapital-content-department/内容工厂控制台` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260417_holdout_4_hn_frontpage_47793411_claude_opus_4_7_20260417/visual-assets/_asset-manifest.j...` | 25 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260417_holdout_4_hn_frontpage_47793411_claude_opus_4_7_20260417/visual-assets/00__c...` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260417_holdout_4_hn_frontpage_47793411_claude_opus_4_7_20260417/visual-assets/_asset-manifest.j...` | 37 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260417_holdout_4_hn_frontpage_47793411_claude_opus_4_7_20260417/visual-assets/80__s...` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260417_holdout_4_hn_frontpage_47793411_claude_opus_4_7_20260417/visual-assets/_asset-manifest.j...` | 49 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260417_holdout_4_hn_frontpage_47793411_claude_opus_4_7_20260417/visual-assets/81__s...` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260417_holdout_4_hn_frontpage_47793411_claude_opus_4_7_20260417/visual-assets/_asset-manifest.j...` | 61 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260417_holdout_4_hn_frontpage_47793411_claude_opus_4_7_20260417/visual-assets/82__s...` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/feishu-doc-delivery.json` | 4 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/feishu-doc-delivery.json` | 10 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/02__openai_...` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/feishu-doc-delivery.json` | 16 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/81__slot_2....` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/feishu-doc-delivery.json` | 22 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/83__slot_4....` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/feishu-doc-delivery.json` | 28 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/82__slot_3....` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/feishu-doc-delivery.json` | 32 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/wechat.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/feishu-doc-delivery.json` | 34 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/feishu-doc-delivery.json` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/_asset-manifest.json` | 16 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/02__openai_...` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/_asset-manifest.json` | 52 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/00__cover.p...` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/_asset-manifest.json` | 64 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/02__openai_...` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/_asset-manifest.json` | 76 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/81__slot_2....` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/_asset-manifest.json` | 88 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/82__slot_3....` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/_asset-manifest.json` | 100 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/20260429_openai_aws_joint_announcement_cloud_ai_competition/visual-assets/83__slot_4....` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_agent_ecosystem/feishu-doc-delivery.json` | 4 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_agent_ecosystem` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_agent_ecosystem/feishu-doc-delivery.json` | 7 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_agent_ecosystem/wechat.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_agent_ecosystem/feishu-doc-delivery.json` | 9 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_agent_ecosystem/feishu-doc-delivery.json` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_agent_ecosystem/visual-assets/_asset-manifest.json` | 34 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_agent_ecosystem/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_agent_ecosystem/visual-assets/_asset-manifest.json` | 46 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_agent_ecosystem/visual-assets/80__slot_1.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_agent_ecosystem/visual-assets/_asset-manifest.json` | 58 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_agent_ecosystem/visual-assets/81__slot_2.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_agent_ecosystem/visual-assets/_asset-manifest.json` | 70 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_agent_ecosystem/visual-assets/82__slot_3.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_chip_ipo_2386_usd33b/visual-assets/_asset-manifest.json` | 16 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_chip_ipo_2386_usd33b/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_chip_ipo_2386_usd33b/visual-assets/_asset-manifest.json` | 28 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_chip_ipo_2386_usd33b/visual-assets/80__slot_1.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_chip_ipo_2386_usd33b/visual-assets/_asset-manifest.json` | 40 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_chip_ipo_2386_usd33b/visual-assets/81__slot_2.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_chip_ipo_2386_usd33b/visual-assets/_asset-manifest.json` | 52 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_chip_ipo_2386_usd33b/visual-assets/82__slot_3.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 45 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/AGENTS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 53 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/SOUL.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 61 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/TOOLS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 69 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/IDENTITY.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 77 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/USER.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 85 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/HEARTBEAT.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 93 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/BOOTSTRAP.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 101 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/prompt-pack/AGENTS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 109 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/prompt-pack/TOOLS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 459 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 475 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260410` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 481 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260410/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 482 | `mac_user_path` | `/Users/apple/.openclaw/media/feishu-doc-delivery/ai_morning_brief_20260410/3209b9aa6be7d91b/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 486 | `mac_user_path` | `/Users/apple/.openclaw/media/feishu-doc-delivery/ai_morning_brief_20260410/3209b9aa6be7d91b/ai_morning_brief_20260410__feishu.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 489 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260410/feishu-doc-delivery.json` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260410/visual-assets/_asset-manifest.json` | 7 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260410/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260411/visual-assets/_asset-manifest.json` | 7 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260411/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 45 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/AGENTS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 53 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/SOUL.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 61 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/TOOLS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 69 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/IDENTITY.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 77 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/USER.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 85 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/HEARTBEAT.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 93 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/BOOTSTRAP.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 101 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/prompt-pack/AGENTS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 109 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/prompt-pack/TOOLS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 459 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 475 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260412` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 478 | `mac_user_path` | `/Users/apple/.openclaw/media/feishu-doc-delivery/ai_morning_brief_20260412/5e801c37eba879d8/ai_morning_brief_20260412__feishu.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 481 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260412/feishu-doc-delivery.json` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260412/visual-assets/_asset-manifest.json` | 7 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260412/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260413/feishu-doc-delivery.json` | 5 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260413` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260413/feishu-doc-delivery.json` | 11 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260413/visual-assets/placeholder.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260413/feishu-doc-delivery.json` | 15 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260413/wechat.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260413/feishu-doc-delivery.json` | 18 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260413/feishu-doc-delivery.json` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260413/visual-assets/_asset-manifest.json` | 7 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260413/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 45 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/AGENTS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 53 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/SOUL.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 61 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/TOOLS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 69 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/IDENTITY.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 77 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/USER.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 85 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/HEARTBEAT.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 93 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/BOOTSTRAP.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 101 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/prompt-pack/AGENTS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 109 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead/prompt-pack/TOOLS.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 459 | `mac_user_path` | `/Users/apple/.openclaw/workspace-lead` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 475 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260414` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 481 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260414/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 482 | `mac_user_path` | `/Users/apple/.openclaw/media/feishu-doc-delivery/ai_morning_brief_20260414/1b48c44d9980e6f0/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 486 | `mac_user_path` | `/Users/apple/.openclaw/media/feishu-doc-delivery/ai_morning_brief_20260414/1b48c44d9980e6f0/ai_morning_brief_20260414__feishu.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 489 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260414/feishu-doc-delivery.json` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260414/visual-assets/_asset-manifest.json` | 7 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260414/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260415/feishu-doc-delivery.json` | 5 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260415` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260415/feishu-doc-delivery.json` | 13 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260415/wechat.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260415/feishu-doc-delivery.json` | 16 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260415/feishu-doc-delivery.json` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260415/visual-assets/_asset-manifest.json` | 7 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260415/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260416/feishu-doc-delivery.json` | 5 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260416` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260416/feishu-doc-delivery.json` | 13 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260416/wechat.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260416/feishu-doc-delivery.json` | 16 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260416/feishu-doc-delivery.json` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260416/visual-assets/_asset-manifest.json` | 7 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260416/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260417/feishu-doc-delivery.json` | 5 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260417` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260417/feishu-doc-delivery.json` | 8 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260417/wechat.md` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260417/feishu-doc-delivery.json` | 11 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260417/feishu-doc-delivery.json` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |
| `内容生产系统/05_draft_packs/ai_morning_brief_20260417/visual-assets/_asset-manifest.json` | 7 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_draft_packs/ai_morning_brief_20260417/visual-assets/00__cover.png` | 确认是否参与运行；如参与运行，纳入 P0-003 配置化。 |

仅展示前 100 条；完整 findings 请查看 JSON 报告。

## LOW 风险项

| 文件 | 行号 | 类型 | 命中内容 | 建议 |
|---|---:|---|---|---|
| `README.md` | 9 | `mac_user_path` | `/Users/apple/Documents/同行资本市场内容系统` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `_archive/information_旧素材库/training_guide.md` | 7 | `home_documents_path` | `~/Documents/information/raw_data/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `_archive/information_旧素材库/training_guide.md` | 8 | `home_documents_path` | `~/Documents/information/processed/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `_archive/information_旧素材库/training_guide.md` | 9 | `home_documents_path` | `~/Documents/information/logs/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `_archive/information_旧素材库/训练/obsidian知识管理系统思考.md` | 19 | `home_documents_path` | `~/Documents/information/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `_archive/information_旧素材库/训练/training_log_2026-03-03.md` | 24 | `home_documents_path` | `~/Documents/information` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `_archive/旧内容工厂控制台_Content Factory Dashboard/README.md` | 8 | `mac_user_path` | `/Users/apple/Documents/Content` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `_archive/旧内容工厂控制台_Content Factory Dashboard/README.md` | 15 | `mac_user_path` | `/Users/apple/Documents/Content` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `_archive/旧内容工厂控制台_Content Factory Dashboard/README.md` | 22 | `mac_user_path` | `/Users/apple/Documents/Content` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `_archive/旧内容工厂控制台_Content Factory Dashboard/start.sh` | 5 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `_archive/旧内容工厂控制台_Content Factory Dashboard/status.sh` | 4 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `_archive/旧内容工厂控制台_Content Factory Dashboard/stop.sh` | 4 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_业务需求与Skill映射决策表.md` | 12 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260324_同行资本市场内容系统开发计划.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_业务需求与Skill映射决策表.md` | 13 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260324_文章提及Skill分类清单.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_同行资本市场内容系统开发计划.md` | 5 | `mac_user_path` | `/Users/apple/Documents/同行资本vc部门/VC系统开发规划` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_同行资本市场内容系统开发计划.md` | 442 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 7 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260325_内容增长方法论与平台黄金标准.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 8 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260325_内容工厂5大skill对标尽调与实施方案.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 28 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260324_同行资本市场内容系统开发计划.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 72 | `mac_user_path` | `/Users/apple/.openclaw/skills/agent-reach/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 73 | `mac_user_path` | `/Users/apple/.openclaw/skills/x-reader-wechat/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 74 | `mac_user_path` | `/Users/apple/.openclaw/skills/openclaw-skills-jina-reader/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 75 | `mac_user_path` | `/Users/apple/.openclaw/skills/multi-search-engine/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 76 | `mac_user_path` | `/Users/apple/.openclaw/skills/openclaw-skills-reddit-scraper/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 77 | `mac_user_path` | `/Users/apple/.openclaw/skills/podcast-capture/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 81 | `mac_user_path` | `/Users/apple/.openclaw/workspace-analyzer-wang/skills/topdown-industry-research/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 82 | `mac_user_path` | `/Users/apple/.openclaw/workspace-analyzer-li/skills/topdown-industry-research/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 83 | `mac_user_path` | `/Users/apple/.openclaw/workspace-data/skills/topdown-signal-supply/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 84 | `mac_user_path` | `/Users/apple/.openclaw/workspace-analyzer-duo/skills/topdown-project-evaluation/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 85 | `mac_user_path` | `/Users/apple/.openclaw/workspace-work/skills/topdown-red-team/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 86 | `mac_user_path` | `/Users/apple/.openclaw/workspace-main/skills/topdown-ic-decision/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 121 | `mac_user_path` | `/Users/apple/.openclaw/skills/agent-reach/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统详细施工方案.md` | 16 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260324_同行资本市场内容系统开发计划.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统详细施工方案.md` | 17 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260324_文章提及Skill分类清单.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统详细施工方案.md` | 18 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260324_业务需求与Skill映射决策表.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_市场内容系统详细施工方案.md` | 627 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260324_目录结构规范.md` | 14 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260325_内容增长方法论与平台黄金标准.md` | 18 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260325_内容增长方法论与平台黄金标准.md` | 19 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260325_内容工厂5大skill对标尽调与实施方案.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260325_内容增长方法论与平台黄金标准.md` | 20 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260325_平台爆款内容对标与第二轮打磨建议.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260325_内容增长方法论与平台黄金标准.md` | 672 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260325_内容工厂5大skill对标尽调与实施方案.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260325_内容工厂5大skill对标尽调与实施方案.md` | 16 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260324_市场内容系统_skill方案与缺口盘点.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260325_内容工厂5大skill对标尽调与实施方案.md` | 17 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260325_内容增长方法论与平台黄金标准.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260325_内容工厂agent隔离与执行架构.md` | 18 | `mac_user_path` | `/Users/apple/.openclaw/workspace-market-editor` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260325_内容工厂agent隔离与执行架构.md` | 21 | `mac_user_path` | `/Users/apple/.openclaw/workspace-market-scout` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260325_内容工厂前台同步与展示层方案.md` | 92 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/11_frontstage/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 9 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260326_sanwan技能吸收决策总表.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 27 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260324_同行资本市场内容系统开发计划.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 28 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260324_市场内容系统详细施工方案.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 29 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260325_平台覆盖战略与分发矩阵建议.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 30 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260325_内容工厂5大skill对标尽调与实施方案.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 31 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260325_内容工厂agent隔离与执行架构.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 32 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/00_planning/20260326_sanwan技能吸收决策总表.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 36 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 37 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 38 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 39 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/05_frontstage/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 39 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/10_logs/` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 369 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-seed-refresh-and-source-scouting/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 370 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-source-capture-and-citation/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 371 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-topic-radar/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 375 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__market-topic-capture-runbook.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 376 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__market-topic-radar-runbook.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 377 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__market-asset-derivation-runbook.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 378 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__market-asset-query-resolution-runbook.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 382 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_capture_round.py` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 383 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_asset_derivation_round.py` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 384 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_asset_query_resolution_round.py` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 385 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_topic_radar_brief_builder.py` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 474 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-draft-pack/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 475 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-market-hook-title-cover/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 476 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-market-context-bridge/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 477 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-market-audience-translator/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 478 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-market-platform-renderer/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 479 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-content-polish/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 483 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__market-draft-pack-runbook.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 484 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__market-content-polish-runbook.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 488 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_draft_pack_builder.py` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 489 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_content_polish_builder.py` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 490 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_docx_export.py` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 585 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__market-frontstage-sync-runbook.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 586 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__market-topic-approval-runbook.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 587 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__market-publish-and-review-runbook.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 591 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_frontstage_board_builder.py` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 592 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_publish_queue_builder.py` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 593 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_content_review_builder.py` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 763 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-content-review/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 764 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/skills/th-market-postmortem-optimizer/SKILL.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 768 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__market-publish-and-review-runbook.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/00_planning/20260326_sanwan技能吸收正式施工路线图.md` | 772 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/scripts/market_content_review_builder.py` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/01_watchlists/20260324__watchlist-registry-board.md` | 19 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260326__source-strategy-v2-funnel-architecture.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/01_watchlists/20260324__watchlist-registry-board.md` | 20 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260325__seed-reselection-strategy.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/01_watchlists/20260324__watchlist-registry-board.md` | 21 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260325__seed-candidate-pool.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/01_watchlists/20260324__watchlist-registry-board.md` | 22 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__openai-news-and-x-stable-capture-plan.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/01_watchlists/20260324__watchlist-registry-board.md` | 23 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/09_runbooks/20260325__reddit-and-producthunt-solution-evaluation.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/01_watchlists/20260324__watchlist-registry-board.md` | 24 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260325__financing-signal-lane.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/01_watchlists/20260324__watchlist-registry-board.md` | 52 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260326__source-strategy-v2-funnel-architecture.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/01_watchlists/20260324__watchlist-registry-board.md` | 53 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260325__seed-reselection-strategy.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/01_watchlists/20260324__watchlist-registry-board.md` | 54 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/20260325__seed-candidate-pool.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |
| `内容生产系统/01_watchlists/20260324__watchlist-registry-board.md` | 55 | `mac_user_path` | `/Users/apple/Documents/同行资本内容部门/内容生产系统/01_watchlists/platform_watchlists/20260324__x-source-registry.md` | 保留历史记录即可；如会被脚本读取，再逐步清理。 |

仅展示前 100 条；完整 findings 请查看 JSON 报告。

## 下一步建议

1. P0-003 优先处理 HIGH 风险项中的运行脚本、控制台入口和配置文件。
2. 不一次性替换历史文档中的路径，避免制造无意义的大 diff。
3. 建议引入统一路径配置策略，优先使用仓库根目录相对路径和环境变量。
4. 每次路径配置化后重新运行 `make path-audit`，观察 HIGH 数量是否下降。
