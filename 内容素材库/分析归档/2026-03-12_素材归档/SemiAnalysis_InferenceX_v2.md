# SemiAnalysis - InferenceX v2: NVIDIA Blackwell Vs AMD vs Hopper

## 2026年3月11日 抓取

### 核心要点

**InferenceX v2 (原InferenceMAX)** 是SemiAnalysis推出的开源推理基准测试工具，持续更新测试数百款芯片和热门开源框架。

#### 主要发现

1. **NVIDIA Blackwell 性能表现**
   - GB300 NVL72 达到**100x FP8 vs FP4**对比H100 disagg+wideEP基线
   - 65x FP8 vs FP8 对比H100
   - GB200 NVL72 对比H100达到**55x**性能提升
   - Blackwell Ultra平台实现**50倍/兆瓦**性能提升，35倍 token成本降低

2. **AMD MI355X 挑战**
   - FP8 disagg+wideEP SGLang与NVIDIA B200 SGLang性能相当
   - **主要问题：可组合性(composability)** - 多种优化技术组合时性能不佳
   - FP4性能在组合优化时表现不佳
   - AMD需重点改进FP4+分布式推理的可组合性

3. **软件栈进展**
   - AMD已弃用vLLM的二等分叉版本，转向上游
   - SGLang和vLLM持续优化，性能提升显著

#### 技术概念

- **吞吐量vs延迟权衡**: 吞吐量描述系统总token产出，交互性描述每个用户接收token的速度
- **预填充(Prefill)和解码(Decode)**: 预填充计算密集，解码内存带宽密集
- **解聚预填充(Disaggregated Prefill)**: 将预填充和解码分离到不同GPU池
- **张量并行(TP)、专家并行(EP)、数据并行(DP)**: 不同的模型并行策略

#### 经济性分析

- 使用InferenceX数据可以计算推理提供商单位经济性
- 例如：DeepSeek R1 0528 FP8在35 tok/s/user交互级别，B200+MTP实现最佳性能/TCO

---

Source: https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs
