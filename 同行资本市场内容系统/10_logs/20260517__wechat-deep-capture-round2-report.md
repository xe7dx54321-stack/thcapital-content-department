# 微信全文深抓补轮报告 | 2026-05-17 18:49

> cron触发：18:05 CST  |  补轮原因：原脚本批量SIGTERM全部失败  |  本轮直接逐条web_fetch
> 目标：下午新增条目补全文，保留原始导出与清洗正文，供晚上选题复盘用

## 抓取统计
- 总计：14条  |  成功：7条  |  失败：7条（其中4条为hub.baai.ac.cn无正文，2条qbitai.com 403，1条URL跳转）

## 成功条目（7条）

🟢 **[HIGH]** 36氪 — 大模型清场前夜（Kimi+阶跃+DeepSeek三天70亿美元）
   > 来源：版面之外/画画 | 核心：模型商品化、三天抢窗口、四小龙剧本、三条路
   > → deep_articles/2026-05-17/20260517__36kr__da_moxing_qing_chang_qian_ye.md

🟢 **[HIGH]** 36氪 — 豆包推出收费：纯免费的大模型越来越少了
   > 来源：首席商业评论/做镜观天 | 核心：68/200/500元三档订阅、推理成本不降反升、3.5亿月活达天花板
   > → deep_articles/2026-05-17/20260517__36kr__dou_ban_shou_fei.md

🟢 **[HIGH]** 36氪 — 48小时打款，估值6万亿（Anthropic 500亿美元新融资）
   > 来源：投中网/刘燕秋 | 核心：ARR 440亿美元、推理毛利率70%、亚马逊250亿+谷歌400亿算力协议、48小时锁定份额
   > → deep_articles/2026-05-17/20260517__36kr__anthropic_500yi_6wanyi.md

🟢 **[HIGH]** 智东西 — 阶跃星辰完成约170亿人民币融资
   > 来源：智东西/杨京丽 | 核心：华勤龙旗豪威中兴产业链资本集中入场、HKIC背书、6月底港股交表、红筹已拆
   > → deep_articles/2026-05-17/20260517__zhidx__jieyue_170yi.md

🟢 **[MEDIUM]** 极客公园 — 无屏手环被AI重新激活
   > 来源：极客公园/张勇毅 | 核心：WHOOP 101亿估值/Oura 110亿估值/Google Fitbit Air入局、硬件只是入口AI才是产品、四种商业模式
   > → deep_articles/2026-05-17/20260517__geekpark__wu_ping_shou_huan_ai.md

🟢 **[MEDIUM]** 爱范儿/APPSO — 苹果带摄像头AirPods H90被迫暂停
   > 来源：凤凰网/APPSO | 核心：H90产线解散、欧盟GDPR合规风险、即时告知义务无法实现、N50眼镜同困境、2027爆发
   > → deep_articles/2026-05-17/20260517__appsso__apple_airpods_h90_pause.md

🟢 **[MEDIUM]** 新浪财经 — xAI关停并入SpaceX，史上最大独角兽消名
   > 来源：IPO上市实务/吕敬之 | 核心：xAI 2500亿美元估值三个月归零、联创12人全部出走、Colossus 1租给Anthropic、SpaceX 6月8日路演目标1.75-2万亿美元IPO
   > → deep_articles/2026-05-17/20260517__sina__xai_guandting_spacex_ipo.md

## 失败条目（7条）

🔴 **[HIGH]** 量子位 — NCB评估指标（浙大×爱丁堡）
   > https://hub.baai.ac.cn/view/54568 — 返回仅标题，无正文内容

🔴 **[HIGH]** 量子位 — Google AI Co-Mathematician
   > https://hub.baai.ac.cn/view/54560 — 返回仅标题，无正文内容

🔴 **[HIGH]** 新智元 — 中国移动Token运营体系
   > https://hub.baai.ac.cn/view/54565 — 返回仅标题，无正文内容

🔴 **[HIGH]** 机器之心 — DeepSeek正在进行73亿美元融资
   > https://finance.sina.com.cn/stock/t/2026-05-09/doc-inhximsz3242168.shtml — URL跳转至"科博会脑机接口"文章，内容不符

🔴 **[MEDIUM]** 量子位 — xAI解散但Grok仍在训练
   > https://hub.baai.ac.cn/view/54540 — 返回仅标题，无正文内容

🔴 **[MEDIUM]** 量子位 — 百度文心大模型5.1发布
   > https://www.qbitai.com/2026/05/415019.html — 403 Forbidden

🔴 **[MEDIUM]** 量子位 — 两项AI政策同时发布
   > https://www.qbitai.com/2026/05/414496.html — 403 Forbidden

## 失败原因分析

| 来源 | 失败数 | 原因 |
|---|---|---|
| hub.baai.ac.cn（智源社区） | 3条 | 防火墙/反爬，仅返回meta标题，正文未解锁 |
| qbitai.com（量子位） | 2条 | 403 Forbidden，需User-Agent或登录cookie |
| sina.com.cn | 1条 | 原始URL已失效/跳转至其他文章 |

## 输出产物

清洗正文已写入：
`/Users/apple/Documents/同行资本市场内容系统/02_topic_radar/deep_articles/2026-05-17/`

7篇成功文章学习素材，供晚上选题复盘、内容拆解和学习池沉淀使用。

*market-scout runtime | 微信全文深抓补轮 | 不构成投资结论*