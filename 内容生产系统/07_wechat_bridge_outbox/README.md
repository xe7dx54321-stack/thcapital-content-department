# WeChat Bridge Outbox

这个目录是 **主机（Mac）↔ 副机（Windows）** 之间的微信草稿箱桥接总线。

## 目录结构

- `tools/`：Windows 侧运行的桥接脚本
- `requests/`：主机放入的待发布请求包

每个请求包当前可能包含：

- `request.json`
- `result.json`
- `publish_confirmation.json`
- `official_metrics.json`

## 工作方式

1. 主机运行 `market_wechat_bridge_enqueue.py`，把某个 `draft pack` 的微信稿打成请求包，写入 `requests/<request_id>/`
2. Windows 副机运行 `tools/wechat_bridge_consumer.py`
3. 消费器读取 `request.json`，调用微信官方接口创建草稿
4. 消费器把草稿结果写回同目录下的 `result.json`
5. 主机一旦确认“人工已发”，会把确认信息写回 `publish_confirmation.json`
6. 消费器还会顺手抓一轮公众号官方结果，写回 `official_metrics.json`
7. 主机侧 `market_publish_queue_builder.py` 会在入队时短轮询 `result.json`，有结果就立即回填
8. 内容工厂 `market-publish-ops-check` heartbeat 会周期性运行 `market_wechat_bridge_reconcile.py --write`，把稍晚返回的草稿结果继续回填到 `publish queue item`
9. 内容工厂 `market_wechat_result_backfill.py --write` 会优先读取本机官方 API；若本机被 VPN / 白名单拦截，则自动降级读取副机写回的 `official_metrics.json`

## Mac 侧自动化说明

- 不再依赖单独的 `launchd + python3` 后台服务回填
- 原因是 macOS 会对后台进程访问 `Documents/` 中脚本施加隐私限制，导致 `Operation not permitted`
- 现在统一由内容工厂自己的 `publish-ops` 心跳负责回填，和现有业务调度链保持一致

## Windows 建议路径

- 当前副机本地路径：`D:\\THCapital\\wechat-bridge-outbox`

## 当前副机职责

- `wechat_bridge_consumer.py`
  - 创建公众号草稿
  - 上传封面与正文图片
  - 读取 `publish_confirmation.json`
  - 顺手抓取公众号官方结果并写回 `official_metrics.json`

## 安全原则

- `AppID` / `AppSecret` 不写进同步目录
- Windows 消费器优先从本机环境变量或本机本地配置文件读取密钥
