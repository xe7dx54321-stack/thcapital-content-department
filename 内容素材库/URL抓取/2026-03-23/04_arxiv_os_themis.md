# arXiv: OS-Themis - GUI代理奖励框架 - 捕获于 2026-03-22

## 元数据
- **来源**: arXiv (cs.AI)
- **URL**: https://arxiv.org/abs/2603.19191
- **发布时间**: 2026-03-19
- **作者**: Zehao Li 等14人
- **论文ID**: 2603.19191

## 摘要
OS-Themis: A Scalable Critic Framework for Generalist GUI Rewards

强化学习(RL)有潜力提高GUI代理在随机环境中的鲁棒性，但训练对奖励函数质量高度敏感。现有奖励方法难以同时实现可扩展性和性能。

**核心贡献**:
1. **OS-Themis框架**: 可扩展的多代理 critic 框架
2. **关键创新**: 将轨迹分解为可验证的里程碑，隔离关键证据
3. **OmniGUIRewardBench (OGRBench)**: 跨平台GUI结果奖励基准

**实验结果**:
- AndroidWorld上在线RL训练提升10.3%
- 自训练循环中轨迹验证和过滤提升6.9%

## 与当前优先级的关联
- **Agent Infra**: 高度相关 - GUI代理、奖励机制、代理训练
- **具身**: 中等相关 - 代理训练框架
- **量子**: 未直接涉及

## 质量评估
- **structured_accept**: true
- **reason**: 前沿研究，直接涉及代理训练基础设施
