# Source Packet — signal:karpathy_llm_wiki

**Source ID:** x__karpathy  
**Captured:** 2026-05-09 22:xx CST  
**Type:** signal (expert observation / builder workflow)  
**Confidence:** HIGH  

## 原始入口

- Primary: Twitter @karpathy (近期推文 + GitHub gist)
- 报道源: Medium (多个来源转载 Karpathy workflow 解析)
- 关键 gist: https://karpathy.ai/ (需进一步补全 URL)

## 信号描述

Andrej Karpathy 在 2026 年初公开了他的 paradigm shift：从主要用 AI 生成代码，转向用 LLM 构建和维护个人研究 wiki ("second brain")。

**核心工作流:**
1. 用户将原始材料 (文章/论文/网页剪藏) 放入 designated "raw" folder
2. LLM agent (如 Claude Code) 被指示处理这些信息
3. LLM 读取原始数据，总结，并在 wiki 中创建新的互链文章
4. 用户很少直接编辑 wiki；LLM 充当 librarian
5. 界面层使用 Obsidian 存储 markdown 文件

**与 RAG 的区别:**
- 不使用复杂的 RAG pipeline 或向量数据库
- 结构化 markdown 文件本身构成知识库
- LLM 直接读取和推理

**同期发声:** "90% of what AI twitter tells you to learn will be dead in 6 months"

## 一跳派生

- GitHub gist (Karpathy 原版 workflow 描述): 待补
- Obsidian 官方: https://obsidian.md/
- 相关教程: 各 Medium 站点的 follow-up 教程

## 结构化评分

| 维度 | 评分 | 备注 |
|---|---|---|
| 一手性 | 9/10 | 直接来自 Karpathy本人 |
| 传播性 | 9/10 | 开发者圈 viral，multiple 教程跟进 |
| 破圈性 | 7/10 | 从开发者圈向更广泛知识工作者扩散中 |
| 数据硬度 | 6/10 | Workflow 描述性强，数字指标少 |
| 视觉素材 | 7/10 | Obsidian 截图 + 流程图 |

## 可执行下一步

- [ ] 补全 Karpathy GitHub gist 原始链接
- [ ] 获取实际 Obsidian + LLM 搭建教程链接
- [ ] 抓取 Twitter 上"90% dead in 6 months"那条推文原文
- [ ] 确认 copy.fail HTML exploit explanation 的 HTML 输出效果截图