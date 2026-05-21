

↑阅读之前记得关注+星标⭐️，😄，每天才能第一时间接收到更新

直接用cc和codex写代码已经过时了，是时候搭建一个单人开发团队，实现一人公司了，今天刷到了一个开发老哥的帖子就是这么实践的，老哥已经把全套部署开源，核心是围绕OpenClaw的一个智能体架构，虽然不一定是最佳实践，但极具借鉴意义，这往后的趋势就是这样，我们暂且看看

我大概介绍一下，详细的内容大家去看老哥原文

这个老哥叫 Elvis ，开源了全套基于 OpenClaw 与 Codex 及 ClaudeCode 组合的智能体集群架构。

单人直接化身一支完整开发团队。

实测数据极具穿透力。

单日最高完成 94次代码提交。

日常平均提交量维持在 50次。

最快记录在30分钟内合并7个PR。

需求从提出到上线通常在当天完成，代码直接转化为 真实B2B SaaS的经常性收入。

跑通整套架构的月成本约 190美元 ，最低 20美元 即可起步。

传统编码大模型面临严重的上下文窗口零和博弈。

塞满代码就装不下业务逻辑，塞满客户历史记录就无法理解代码库。

剥离业务与代码的耦合成为破局关键。

OpenClaw 在这里接管全局，作为人类与底层大模型之间的核心编排层发挥作用。

编排器被命名为 Zoe 。

Zoe 直接读取存放在 Obsidian 知识库中的客户数据、会议记录和历史决策，将业务上下文精准翻译为底层提示词。

该机制与Stripe此前披露的后台智能体系统 Minions 高度同源，但完全在本地设备运行。

工作流被拆解为极度克制的自动化步骤。

需求确立后，Zoe 直接调用管理员API解除客户限制，并拉取生产数据库只读配置注入提示词。

随后系统为每个智能体分配独立的 git工作树 和 tmux会话。

```python
git worktree add ../feat-custom-templates -b feat/custom-templates origin/main  
cd ../feat-custom-templates && pnpm install  
  
tmux new-session -d -s codex-templates \  
  -c /Users/elvis/Documents/GitHub/medialyst-worktrees/feat-custom-templates \  
  $HOME/.codex-agent/run-agent.sh templates gpt-5.3-codex high
```

编码智能体在隔离环境中被唤醒。

```python
codex --model gpt-5.3-codex \  
  -c model_reasoning_effort=high \  
  --dangerously-bypass-approvals-and-sandbox \  
  Your prompt here  
  
claude --model claude-opus-4.5 \  
  --dangerously-skip-permissions \  
  -p Your prompt here
```

tmux 赋予了系统强大的中途纠偏能力。

发现方向错误时，无需杀掉进程，直接向终端发送新指令即可强行重定向。

```python
tmux send-keys -t codex-templates Stop. Focus on the API layer first, not the UI. Enter  
  
tmux send-keys -t codex-templates The schema is in src/types/template.ts. Use that. Enter
```

任务状态被实时写入 .clawdbot/active-tasks.json 注册表。

```python
{  
  id: feat-custom-templates,  
  tmuxSession: codex-templates,  
  agent: codex,  
  description: Custom email templates for agency customer,  
  repo: medialyst,  
  worktree: feat-custom-templates,  
  branch: feat/custom-templates,  
  startedAt: 1740268800000,  
  status: running,  
  notifyOnComplete: true  
}
```

任务完成后，状态文件跟手更新。

```python
{  
  status: done,  
  pr: 341,  
  completedAt: 1740275400000,  
  checks: {  
    prCreated: true,  
    ciPassed: true,  
    claudeReviewPassed: true,  
    geminiReviewPassed: true  
  },  
  note: All checks passed. Ready to merge.  
}
```

监控机制摒弃了高成本的轮询。

系统通过 cron定时任务 每10分钟执行一次确定性Shell脚本。

```python
.clawdbot/check-agents.sh
```

脚本负责检查会话存活状态、调用 gh cli 验证CI结果，并在遇到阻碍时最多自动拉起失败节点3次。

代码提交后必须通过严苛的定义标准。

除常规的 TypeScript检查、单元测试 与 Playwright端到端测试外，涉及UI层面的改动必须硬性绑定界面截图，否则CI直接阻断。

代码审查环节交由三套模型交叉验证。

Codex 兜底逻辑错误与竞态条件等核心边缘情况。

Gemini 专攻安全漏洞与架构扩展性缺陷。

Claude Code 则作为辅助验证位提供冗余审查。

这套架构在底层跑通了改良版的 拉尔夫循环 。

Zoe不再机械复用静态提示词，而是携带全局业务上下文介入失败节点进行动态调优。

它甚至具备自主寻获任务的特性。

早晨扫描 Sentry 报错日志派发修复工单，会后解析记录提取功能需求，晚间梳理 git日志 生成更新文档。

不同编码模型在此被彻底分化使用。

Codex 吞吐了 90%的复杂后端与跨文件重构任务。

Claude Code 接管前端构建与git指令操作。

Gemini则前置到UI设计环节输出规范文档。

部署方式被压缩到极致，只需将架构文档喂给 OpenClaw ，系统会在 10分钟 内全自动完成脚本生成与目录搭建。

目前的物理天花板卡在了硬件内存。

每个独立工作树和并发编译环境都在疯狂榨干本地资源。

16GB内存 的 Mac mini 在并发 4到5个智能体 时便会触发内存交换。

老哥已订购 售价3500美元、配备 128GB内存 的 M4 Max版Mac Studio 用于突破当前并发瓶颈。

技术平权正在重塑商业形态。

基于这套系统构建的公关工具 Medialyst.ai 正在落地，完全由AI编排器驱动的一人企业模式即将向传统商业巨头正面宣战。

source：

https://x.com/elvissun/status/2025920521871716562

--end--

最后记得⭐️我，每天都在更新：如果觉得文章还不错的话可以点赞转发推荐评论