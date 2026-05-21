

当 AI Agent 逐渐走出对话框，真正的难点不再是 “回答得多聪明”，而是 能否 像人一样完成任务闭环 ：看懂屏幕、点击按钮、填写表单、整理文件、生成交付物，并把结果同步回团队协作系统。

我们开源的 Open Cowork ，正是一次面向 “桌面端虚拟同事” 的实践：一键安装、无需写代码，让模型在安全沙箱里操作你的工作空间，既能产出 PPT/Word/Excel/PDF 等专业成果，也能通过 GUI 直接操作电脑完成更复杂更通用的跨应用流程。

- 代码链接：https://github.com/OpenCoworkAI/open-cowork

![]()
已关注
关注
重播
分享

赞

关闭
观看更多

更多

*退出全屏*

 *切换到竖屏全屏*  *退出全屏*  机器之心  已关注  分享视频  ，时长 00:37 

0 / 0

00:00
/
00:37
切换到横屏模式

继续播放

进度条，百分之0

00:00
/
00:37
00:37

*全屏*
倍速播放中

](https://mpvideo.qpic.cn/0bc3fmbkgaaci4acqenaxbuvek6dumvqfiya.f10002.mp4?dis_k=92eb31315b648182149e9443e2b92a95&dis_t=1772744504&play_scene=10120&auth_info=JLTR554GH3lIl4+5wmxjHEgIFSUpYFgwS1lkDnEibkQfL2FAYS0END98QG8XBm48XAI=&auth_key=d41ff31dc20b76cc38516884aaae8a88&vid=wxv_4406836652829048837&format_id=10002&support_redirect=0&mmversion=false)

继续观看

支持远程操控和通用GUI操作，开源版桌面虚拟同事Open Cowork来了！

观看更多
转载
,
支持远程操控和通用GUI操作，开源版桌面虚拟同事Open Cowork来了！
机器之心
已关注

分享

点赞

在看

已同步到看一看

GUI操作

![]()
已关注
关注
重播
分享

赞

关闭
观看更多

更多

*退出全屏*

 *切换到竖屏全屏*  *退出全屏*  机器之心  已关注  分享视频  ，时长 00:25 

0 / 0

00:00
/
00:25
切换到横屏模式

继续播放

进度条，百分之0

00:00
/
00:25
00:25

*全屏*
倍速播放中

](https://mpvideo.qpic.cn/0bc3raaaaaaabeaesn5b7vuvbcgdaceaaaaa.f10002.mp4?dis_k=40bba2538e183238a7e2a5aaf8ca52d7&dis_t=1772744504&play_scene=10120&auth_info=XbOTxQAUKEaR2rmTPGIYTlJGICliUjFCDGoOendvFht7OxoyeQ9lMXoVb0ZWbzhaWA==&auth_key=bd0c451482a9e0dc279f7ba60f72c0ff&vid=wxv_4405454023768784901&format_id=10002&support_redirect=0&mmversion=false)

继续观看

支持远程操控和通用GUI操作，开源版桌面虚拟同事Open Cowork来了！

观看更多
转载
,
支持远程操控和通用GUI操作，开源版桌面虚拟同事Open Cowork来了！
机器之心
已关注

分享

点赞

在看

已同步到看一看

PPT生成

![]()
已关注
关注
重播
分享

赞

关闭
观看更多

更多

*退出全屏*

 *切换到竖屏全屏*  *退出全屏*  机器之心  已关注  分享视频  ，时长 00:39 

0 / 0

00:00
/
00:39
切换到横屏模式

继续播放

进度条，百分之0

00:00
/
00:39
00:39

*全屏*
倍速播放中

](https://mpvideo.qpic.cn/0bc3cqcjwaaeraanfsffzzuvifgdtmkajgya.f10002.mp4?dis_k=11b7fe00bfa444013cbf063852ed3d11&dis_t=1772744504&play_scene=10120&auth_info=dJu/0JQEF31AlIjslzhgHR8MQiUlZVAzSQ4/DXggaU9PL2YdYCgMMDd/RzpCUm09CwY=&auth_key=997afcc579f4b2bc5a6e828accd7ab52&vid=wxv_4405454476619366408&format_id=10002&support_redirect=0&mmversion=false)

继续观看

支持远程操控和通用GUI操作，开源版桌面虚拟同事Open Cowork来了！

观看更多
转载
,
支持远程操控和通用GUI操作，开源版桌面虚拟同事Open Cowork来了！
机器之心
已关注

分享

点赞

在看

已同步到看一看

飞书操控

一、为什么要做「能用电脑」的 AI？

过去两年，大模型的推理与生成能力突飞猛进，但在真实办公场景中，高频任务往往卡在 执行层面 ：

- 应用孤岛 ： 网页、桌面应用、企业系统之间缺乏统一 API。
- 流程割裂 ： 数据分散在浏览器、文档、IM 和本地文件中。
- 人工瓶颈 ： 用户仍需充当 “搬运工”，在不同窗口间复制粘贴。

我们认为，Agent 不应只止步于 “对话建议”。Open Cowork 的目标是将这些碎片化动作自动化： 像人一样操作电脑，跑完流程，并以可交付的形式（文档、表格、PPT）落地，最终通过飞书等工具进入团队协作流。

二、Open Cowork 是什么？

Open Cowork 是 Claude Cowork 理念的 开源增强实现 。 它提供 Windows 与 macOS 的一键安装包，核心是一个 “沙箱化工作区”：模型被授权在指定 Workspace 内读写文件、调用工具，并通过内置 Skills 系统将数据加工成专业交付物。

此外，Open Cowork 不仅仅是 Claude Cowork 的开源复刻，我们还实现了近期热门的 OpenClaw 的核心远程控制功能（例如通过飞书远程发送指令并收到回复），以及支持了对电脑端 APP 的通用 GUI 操作（例如可以支持模型操作 Cursor APP 来进行代码的迭代改进与交互测试），这对于没有实现 MCP 接口的桌面 APP 尤为重要。

能力对比一览：

|  |  |  |  |
| --- | --- | --- | --- |
|  | MCP & Skills | Remote Control  ( 远程协作 ) | GUI Operation  ( 屏幕操作 ) |
| Claude Cowork | ✅ | ❌ | ❌ |
| OpenClaw | ✅ | ✅ | ❌ |
| Open Cowork | ✅ | ✅ | ✅ |

三、三大能力组合：

Skills × GUI × Remote

1）Skills：面向交付的 “工作流技能库”

Agent 的价值不应止步于 Chat 窗口。Open Cowork 内置了标准化的 Skills 系统（支持自定义与扩展），核心目标只有一个： 产出可用的文件 。

- 覆盖主流格式 ： 支持 PPTX、DOCX、XLSX、PDF 的原生生成与编辑。
- 结构化输出 ： 无论是将非结构化文本转为 Excel 报表，还是根据大纲自动生成演示文稿，我们让模型直接交付 “半成品” 甚至 “成品”，而非中间态的文字。

PPT 制作视频：从本地文件 / 大纲自动生成可编辑的 PPTX

2）GUI：让模型像人一样操作电脑，把能做的事情变多

API 总有覆盖不到的地方，但 UI 界面是通用的。GUI 模块让模型具备了 “人类操作” 的能力，将 Agent 的可用性扩展到 OS 层面。

- Screen-to-Action ： 通过截图理解当前 UI 状态，规划并执行鼠标点击、拖拽、文本输入等动作。
- 跨应用自动化 ： 能够处理复杂的跨软件链路（例如：从 ERP 抓数据 -> 填入 Excel -> 导出 PDF）。

在产品体验上，我们强调的是 “能做更多事、像人一样动手”。对于 GUI 理解与操作任务，建议选择更强的多模态模型以获得更稳的步骤执行。

GUI 操作视频：利用 GUI 界面操作 cursor 写小程序并迭代改进

3）Remote：接入飞书，把它变成真正的 “虚拟同事”

如果 GUI 让它 “会做事”，Remote 则让它 “懂协作”。Open Cowork 拒绝做一个孤独的桌面程序，通过接入飞书（Lark）等协作平台，它打通了 本地执行与团队协同的壁垒 。

- 闭环工作流 ： AI 在你电脑上跑完数据（GUI/Skills），转头就能把做好的报表扔进部门群（Remote），或者同步到在线文档。
- 真正的虚拟同事 ： 它既有本地环境的执行权限，又有团队系统的沟通权限。产出不再停留在你的硬盘里，而是直接流动到团队的业务流中。

远程操控视频：利用飞书远程操控 Open Cowork

四、安全性：让 “能动手” 尽量可控

桌面端 Agent 的能力越强，安全边界越重要。Open Cowork 的基本原则是：默认把所有操作限制在你选定的 workspace 内。同时，我们提供更强的 VM 级隔离选项：Windows 侧优先使用 WSL2，macOS 侧可使用 Lima，将命令执行放入隔离环境中运行，以降低对宿主机的影响。

桌面端 Agent 的能力越强，赋予 Agent “系统级操作权限” 越要严格地风控。Open Cowork 坚持 “默认安全” 的设计原则：

- Workspace 限制 ： 文件读写权限被严格圈定在用户授权的目录下，防止全盘扫描。
- 环境隔离（Sandbox） ： 提供基于虚拟化的强隔离方案。

￮ Windows ： 推荐使用 WSL2 子系统运行核心逻辑。

￮ macOS ： 适配 Lima 虚拟机环境。 通过将命令执行放入隔离沙箱，最大程度降低对宿主机的误操作风险。

五、如何快速上手（3 分钟）

1）下载并安装：Windows 使用 .exe，macOS（Apple Silicon）使用 .dmg。

2）配置模型：在设置页填写 API Key、Base URL 与模型名（支持多家 OpenAI-compatible/Anthropic-compatible 提供方）。

3）选择工作区：授权一个你希望 AI 操作的文件夹作为 workspace。

4）开始协作：例如 “读取这个文件夹里的 financial\_report.csv，生成 5 页 PPT 总结，并把结果发到飞书群里。”

六、开源与共建

Open Cowork 以 MIT License 开源，欢迎开发者贡献新的 Skills、MCP Connector、Remote 集成与 GUI 操作优化。我们希望和更多社区伙伴一起，把 “桌面虚拟同事” 从 demo 变成可持续迭代的基础设施。

作者简介：

Open Cowork Team：由多位清华大学在读的博士生 / 本科生组成，关注桌面端 AI Agent、MCP 生态与安全沙箱。我们希望把 AI 从 “会聊天” 推进到 “会动手”，打造可安装、可扩展、可共建的虚拟同事工作台。

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com