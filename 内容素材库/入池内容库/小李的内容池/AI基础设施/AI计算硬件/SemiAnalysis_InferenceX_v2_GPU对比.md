# SemiAnalysis - InferenceX v2: NVIDIA Blackwell Vs AMD vs Hopper

> 整理日期：2026-03-12
> 标签：#AI基础设施 #GPU #NVIDIA #AMD #半导体 #2026-03

---

## 核心内容

### 1. InferenceX v2基准测试工具
"InferenceX v2 (原InferenceMAX)是SemiAnalysis推出的开源推理基准测试工具，持续更新测试数百款芯片和热门开源框架。"

作为业界领先的推理性能评测工具，InferenceX v2为评估不同AI硬件平台的推理能力提供了标准化参考。

### 2. NVIDIA Blackwell性能表现

#### GB300 NVL72
"GB300 NVL72达到100x FP8 vs FP4对比H100 disagg+wideEP基线，65x FP8 vs FP8对比H100。"

Blackwell架构在推理性能上展现出惊人的提升，相比上一代Hopper架构实现了数倍乃至数十倍的性能飞跃。

#### GB200 NVL72
"GB200 NVL72对比H100达到55x性能提升。"

GB200作为Blackwell系列的另一款产品，同样展现出强大的推理性能优势。

#### Blackwell Ultra
"Blackwell Ultra平台实现50倍/兆瓦性能提升，35倍token成本降低。"

除了绝对性能提升，Blackwell Ultra在能效比方面也有显著改善，这对于大规模AI部署至关重要。

### 3. AMD MI355X挑战

#### 性能表现
"FP8 disagg+wideEP SGLang与NVIDIA B200 SGLang性能相当。"

AMD在FP8精度下的推理性能已经接近NVIDIA的最新产品，这对于NVIDIA的市场地位构成一定威胁。

#### 主要问题：可组合性
"主要问题：可组合性(composability)——多种优化技术组合时性能不佳。FP4性能在组合优化时表现不佳。"

尽管单精度性能接近NVIDIA，但AMD在多种优化技术组合使用时表现不佳，这是AMD需要重点改进的方向。

### 4. 软件栈进展
"AMD已弃用vLLM的二等分叉版本，转向上游。SGLang和vLLM持续优化，性能提升显著。"

AMD正在改善其软件生态，与主流开源推理框架的整合日益紧密。

### 5. 核心技术概念

#### 吞吐量vs延迟
"吞吐量描述系统总token产出，交互性描述每个用户接收token的速度。"

这是评估AI推理系统的两个关键维度，不同应用场景对这两者的侧重点不同。

#### 预填充和解码
"预填充计算密集，解码内存带宽密集。"

理解这两个阶段的差异对于优化推理系统至关重要。

#### 解聚预填充
"将预填充和解码分离到不同GPU池。"

这是提升推理效率的重要架构创新，可以更好地平衡计算和内存资源。

### 6. 经济性分析
"使用InferenceX数据可以计算推理提供商单位经济性。例如：DeepSeek R1 0528 FP8在35 tok/s/user交互级别，B200+MTP实现最佳性能/TCO。"

通过基准测试数据，可以准确评估不同硬件配置的成本效益比，为AI服务提供商提供采购决策依据。

---

### 市场影响

NVIDIA通过Blackwell系列进一步巩固了其在AI推理市场的领先地位，但AMD的追赶态势不容忽视。两者在性能、价格和生态方面的竞争将持续推动AI硬件行业发展。

---

*来源：SemiAnalysis*
