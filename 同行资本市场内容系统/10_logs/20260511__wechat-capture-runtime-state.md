# market-scout runtime state | 2026-05-11 14:45 CST

## 本轮执行记录

- **触发来源：** cron 11:52/13:52/21:52 wechat lane
- **执行时间：** 2026-05-11 14:45 CST
- **执行脚本（顶位）：** `market_wechat_deep_capture_round.py`
- **注：** `market_topic_capture_round.py` 不存在，已用 deep_capture 顶位
- **深抓结果：** 6/14 成功（43%），HIGH 3/8，M 中 3/6

## 成功条目

| 优先级 | 来源 | 标题 |
|--------|------|------|
| HIGH | 36氪 | 大模型清场前夜 Kimi+阶跃+DeepSeek |
| HIGH | 36氪 | 字节豆包付费订阅测试 |
| MEDIUM | 极客公园 | 无屏手环被AI重新激活 |
| MEDIUM | 爱范儿 | 苹果带摄像头AirPods H90 |
| MEDIUM | 新智元 | Anthropic Claude新功能Orbit泄露 |
| MEDIUM | 量子位 | xAI解散但Grok仍在训练 |

## 失败条目（待后续补证）

| 优先级 | 来源 | 标题 | 失败原因 |
|--------|------|------|---------|
| HIGH | 量子位 | NCB评估指标（浙大×爱丁堡） | hub.baai.ac.cn curl 0 bytes |
| HIGH | 量子位 | Google AI Co-Mathematician | hub.baai.ac.cn curl 0 bytes |
| HIGH | 新智元 | 中国移动Token运营体系 | hub.baai.ac.cn curl 0 bytes |
| HIGH | 36氪 | Anthropic推进500亿美元新融资 | 36kr.com curl 0 bytes |
| HIGH | 机器之心 | DeepSeek正在进行73亿美元融资 | sina.com.cn curl 0 bytes |
| HIGH | 智东西 | 阶跃星辰完成约170亿人民币融资 | zhidx.com curl 0 bytes |
| MEDIUM | 量子位 | 百度文心大模型5.1发布 | qbitai.com curl 0 bytes |
| MEDIUM | 量子位 | 两项AI政策同日发布 | qbitai.com curl 0 bytes |

## 已知失败模式

- **hub.baai.ac.cn** 全线失败（4/4）：jina reader curl 模式对该域名持续返回空
- **36kr/zhidx/qbitai/sina** 偶发失败：网络超时或反爬拦截

## 今日 source packet 状态

- `02_topic_radar/source_packets/2026-05-11/__wechat__public_accounts__2026-05-11.md` ✅ 已存在，内容完整
- Deep Articles 已落盘：`02_topic_radar/deep_articles/2026-05-11/`（14 条，含 __raw.md）
- Learning Memo：`11_frontstage/20260511__head-media-learning-memo.md` ✅
- 报告：`10_logs/20260511__wechat-deep-capture-report.md` ✅
- 日志：`10_logs/20260511__wechat-deep-capture.log` ✅

## 待补事项

- [ ] `market_topic_capture_round.py` 需重建，对应 runbook `20260325__market-topic-capture-runbook.md` 缺失
- [ ] hub.baai.ac.cn 域名在 jina reader 模式下需要替代方案（如直接 target URL 或换用 web_fetch 工具）
- [ ] 今天失败条目（DeepSeek/阶跃/Kimi 融资信号 + 百度文心5.1 + 两项AI政策）内容已存在于 source packet 搜索合成段，无需降级

## 交付物

- 本 runtime state：`10_logs/20260511__wechat-capture-runtime-state.md`
- 今日 Top20 初筛包：见 `03_topic_candidates/20260511__top20-screening-pack.md`（若已生成）

*market-scout runtime | 只做 intake，不写入虚拟vc运行台*
