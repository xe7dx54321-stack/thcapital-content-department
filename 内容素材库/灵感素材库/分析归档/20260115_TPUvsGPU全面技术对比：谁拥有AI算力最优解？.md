](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247519866&idx=1&sn=179a2ec7519d8f7a1bc41958a847e7e9&scene=21#wechat_redirect)

作者：NCL

编辑：Feihong，Siqi

SemiAnalysis 最近对 Google TPU v7/v8 的深度拆解，可能是目前公开信息里少数能同时讲清硬件规格、互联拓扑与 TCO（Total Cost of Owenship，资产全生命周期总成本） 模型的系统性对比：文章中把 3D Torus + OCS 的设计哲学、以及 TPU 与 Nvidia GPU 在训练与推理中的成本结构差异拆到了可计算的层面。

但 SemiAnalysis 的结论需要打折来看：

• 文章中倾向于放大 TPU 的 MFU 优势（假设 TPU 40% vs GPU 30%），却没有充分讨论 FP8 精度下公开 MFU 数据的缺乏；

• 强调 TPU 在训练场景的 TCO 领先，却对推理场景下 GPU 凭借 FP4 算力的反超着墨不多；

• 详细介绍了 TPU 的软件优化，却淡化了这些优化本质上是在弥补 3D Torus 对不规则流量的天然劣势。

在这篇文章中，我们基于 SemiAnalysis 的数据框架，结合对训练、Prefill、Decode 三类场景做了再拆解，尝试对 TCO 效率路线进行更全面的分析对比，以下是三个关键结论：

• TCO 的真正答案是“看场景” ：训练和延迟不敏感推理选 TPU，推理 Prefill 和延迟敏感推理则 GPU 是优选；

• 3D Torus 和 Switch Fabric（NVSwitch / Fat-tree） 这两套互联体系的本质分歧不在于"谁更快"，而在于"对流量形态的假设"；

• Google 历史上靠 TPU 建立的 TCO 护城河，在 v8 这一代被显著削弱。

01 .

关键结论

1. TCO 的真正答案是"看场景"：训练和延迟不敏感推理选 TPU，推理 Prefill 和延迟敏感推理看 GPU。

SemiAnalysis 给出的 TCO（Total Cost of Ownership） 对比结论需要打折看待。 训练场景下 TPUv7 确实能带来 45-56% 的成本优势，但这一数字建立在"TPU MFU 比 GPU 高 5-10 个百分点"的假设之上——而 FP8 精度下的公开 MFU 数据并不充分，Bytedance MegaScale 在 BF16 下已将 H100 优化到与 TPU 接近的水平。更关键的是，推理场景的结论完全倒转：GB200/GB300 凭借 FP4 算力优势在 Prefill 阶段反超 TPUv7 约 35-50%，而 Decode 阶段的实际性价比差距也远没有纸面 HBM 带宽数字显示的那么大。

2. 3D Torus vs Switch Fabric（NVSwitch / Fat-tree） 两套互联体系的本质分歧不在于"谁更快"，而在于"对流量形态的假设"。

3D Torus + OCS 假设通信模式可预测、可编排，因此能在万卡规模的常规训练任务中维持高 MFU；Switch Fabric 则假设流量不确定，用全互联换取对任意通信模式的容忍度。这决定了各自的甜点区： 十万卡以上级别的训练负载，只能采取 Fat-tree；而千卡到两万卡的稳定训练负载，3D Torus 占优；几百卡以内的灵活实验、MoE 训练、以及延迟敏感的在线推理，NVSwitch 全面胜出。 当 MoE 成为主流架构、在线推理场景持续增长，TPU 面临的适配压力只会越来越大——而这正是 NVSwitch 的舒适区。

3. Google 历史上靠 TPU 建立的 TCO 护城河，在 v8 这一代被显著削弱。

TPU v8 选择 3nm + HBM3E 的保守路线，而 Nvidia Rubin 激进押注 HBM4（20TB/s vs 9.8TB/s）、FP4 算力翻倍、甚至专为 Prefill 场景推出低成本 CPX 芯片。结果是：从 GB200/TPUv7 的 1.52× 训练 TCO 差距，到 VR200/TPUv8p 仅剩 1.23×；HBM 带宽性价比差距更是从 1.32× 收窄到 1.10×。 这正是 Anthropic 需要重建 Nvidia 合作的原因：TPU 虽然在特定场景下找到了性价比甜点，但 Nvidia 的迭代速度实在太快，难以长期忽视。

02 .

TCO Comparison

衡量推理成本最直接的指标是 per-token 成本（$/M tokens） ，即在相同 setting 下（包括但不限于模型大小、 context length、首 token 延迟和 Batch size），单卡 TCO（$/h/GPU）除以在该服务目标下可长期稳定实现的 tokens per second per GPU。

以 LMSYS 的数据为例：在 NVL72 GB200 集群上，单卡可达 13,386 output tokens/s，结合约 $2.28/h/GPU 的 TCO，推理成本约为 $0.047/M tokens。

Source：  *SGLang and NVIDIA Accelerating SemiAnalysis InferenceMAX and GB200 Together*

LMSYS（Large Model Systems Organization）是一个由 UC Berkeley 主导的开源研究组织。

作为对照，H100 在相同测试设定下仅能达到 2,789 tokens/s（TCO 约 $1.42/h/GPU），对应成本约 $0.14/M tokens，约为 GB200 的 3 倍。

但 per-token 成本难以作为通用对比基准：训练场景没有统一的 token 产出定义；推理侧 TPUv7 尚未公开具体吞吐数据， SemiAnalysis 提到会在未来一两个月公布，届时我们就能更清晰地判断 TPU 在真实 token 成本上是否具备优势，不过主观上我不认为双方会拉出特别大的差距。

因此，下文退而求其次，用 TCO / Effective FLOPs 和 TCO / Bandwidth 等中间指标来近似推断性价比，为了进行这一对比，我们还需要先拆解训练和推理各阶段的实际瓶颈：

1. 在万亿参数级别的模型训练阶段，瓶颈通常会出现在算力和 Scale-out 通讯带宽上。 训练时需要计算海量梯度并通过 All-Reduce 同步到所有节点，同时前向和反向传播的矩阵运算需要极高的 FLOPs 才能在合理时间内完成。

2. 在推理的 Prefill 阶段，在合理设计并行策略（尽量增加 pipeline 并行、减少 tensor 并行同步）的前提下，瓶颈主要会转化为算力而不是通讯带宽。 原因在于 Prefill 阶段需要处理大量 token，能够触发高度并行的矩阵运算，使 GPU 长时间保持高利用率；同时，用 pipeline 并行替代大规模 tensor 并行可以显著降低跨 GPU 的同步与通讯开销，让芯片更接近算力上限地运行。

3. 在推理的 Decode 阶段，瓶颈通常会出现在内存带宽和 Scale-up 通讯带宽上。 解码时每生成一个 token 都需要从 HBM 加载全部模型参数，但其实这一过程的实际计算量很小，GPU 大部分时间在等待数据而非计算。每个 token 生成都需要不同 GPU 之间反复传输 KV Cache 和激活值，频繁的小数据传输让通信延迟成为吞吐瓶颈。

这就导致训练和不同场景下的推理需要的性能不同， 比如：

• 训练时更需要 FP8 和 Scale-out Bandwidth（TPU）；

• 而在推理 Prefill 阶段需要 FP4 和 Scale-up Bandwidth（GPU）；

• 推理 Decode 阶段需要 HBM Bandwidth 和 Scale-up Bandwidth（GPU）。

这也是 SemiAnalysis 在文章中拆开计算 GPU 和 TPU 在训练和推理场景下的性价比的原因。

接下来我们会对训练、推理 Prefill 和 Decode 三个阶段 TPU 和 GPU 的性价比进行详细对比分析。

场景 1：训练性价比

SemiAnalysis 在考虑资金成本和运营成本（包含电费、租金和技术）后计算出了 TPU 和 NVDA GPU 的 TCO。并且强调 TPU 在宣传算力时比 NVDA 和 AMD 更保守，Blackwell 系列只能做到纸面算力的 75%，MI300 甚至只能做到 50-60%。

NVDA 和 AMD 在对外宣传峰值理论算力（FLOPs）时，会用芯片在极短时间内能够跑到的最高瞬时频率来计算，即使这个频率在实际工作负载下几乎无法长时间维持。而实际情况是， NV 和 AMD 使用动态电压和频率调节（DVFS）技术，会根据功耗和温度情况不断调整芯片的频率。

SemiAnalysis 并没有提到的是， TPU 也采用类似的技术以保护芯片，所以大多时候也无法做到纸面算力的 100%，很可能也只能做到 80-90%的纸面算力。

SemiAnalysis 提到，Google 凭借 3D Torus 互联架构，以及谷歌内部人员对于训练算法软硬件优化，能够做到在 FP8 精度下的训练 MFU 高达 40%，而 GPU 仅能做到 30%。 我认为，这一观点其实是 SemiAnalysis 主观拉大了 NV 和 TPU 阵营的 MFU（Model FLOPs Utilization， 算力利用率） 差距。

目前 FP8 精度的公开资料并不够多，SemiAnalysis 的 MFU 也没有足够的证据表明是否属实。但是在之前广泛利用的 BF16 精度下，Bytedance 在 MegaScale 论文中将 H100 优化到跟谷歌 TPU 差不多的水平，只是目前在 FP8 出来的初期 Meta LLama4 在用 FP8 训练时 MFU 比较低，但是从 Llama3 的训练上看 Meta 原本的优化功底并不出众。

综合来看，通过比较下面四款芯片的 TCO / Effective FP8，可以 看出 Anthropic 通过采购 TPUv7 后能在训练成本上节省 45%，而谷歌内部能节省 56%：

场景 2：推理 Prefill 性价比

Prefill 由于可以多卡并行处理庞大的 prompt，所以更受限于单卡的算力，而 FP4 精度的优势能让 GB200/GB300 比 TPUv7 External 在 Prefill 阶段有将近 35-50% 的成本优势。

在 Prefill 阶段，若 N 个用户长度为 K 的 prompt 需要用 P 张卡进行推理，那么其中几个用户的 prompt 会作为一个 batch 传到一张卡上跑一遍整套 attention，并将得到 KV Cache 用 FP8 精度存储下来，这是在帮每个 token 看全上下文、算好“该关注谁”。

到了 MoE 阶段，Router 决定 token 去哪些 experts，这些 experts 分散在不同 GPU 且权重用 NVFP4 压缩存储，于是这些 token 被丢给对应 GPU 上的 experts 做一小段非线性计算，算完再把结果合在一起作为输出。

SGLang 通过上述这个混合精度推理的方式，充分发挥了 Blackwell 卡引入的 FP4 算力的优势，在硬件纸面 FP8 算力仅提升 2.25x 的情况下，依靠降低精度直接获得额外的 1.8x 提升，也就是 GB200 的 Prefill 效率为 H100 的 3.8x 吞吐。 这说明 GB200/GB300 在 FP4 上的算力优势，让其在 Prefill 阶段能反超 TPUv7 的成本优势。

Reference：  *Deploying DeepSeek on GB200 NVL72 with PD and Large Scale EP (Part II): 3.8x Prefill, 4.8x Decode Throughput*

（这里实际上也有 MFU 的概念，只有超长 prompt （如 100k 以上）让 MFU 接近 90-100%，而如果 prompt 比较短， Prefill 阶段也会更被 Memory Bandwidth 和 Scale-up Bandwdith 限制。)

场景 3：推理 Decode

Decode 阶段主要受制于 HBM Memory Bandwidth，但当推理追求低成本去用更大的 Batch Size 时， NVLINK Bandwidth 会逐渐成为瓶颈。所以， SemiAnalysis 认为 TPUv7 能在推理阶段靠低 40-50% TCO / HBM Bandwidth 有一定优势， 但是因为这步骤实际也和 Scale-up Bandwidth 很相关，所以实际性价比差距并没有这么大。

在 Decode 阶段，模型每次迭代为 N 个用户各生成一个新 token。每张 GPU 需要从 HBM 读取所有用户的 KV Cache（FP8 格式）和模型权重来计算 attention， 小 batch 时这个"从显存读数据"的过程主要受制于 HBM Memory Bandwidth。

但当追求低成本用更大 batch size 时，计算量上来稀释了单卡带宽压力，此时跨卡通信开始显现：attention 算完要 all-reduce 同步结果，MoE 层 Router 把 token 路由到分散在各卡的 experts（NVFP4 压缩权重）又触发 all-to-all 通信，最后再汇总回来。

大 batch 下跨卡数据交换量激增，NVLink 带宽逐渐成为新瓶颈。Decode 阶段性能瓶颈本质是随 batch size 从单卡 HBM 带宽动态迁移到多卡 NVLink 带宽。

03 .

互联结构对比：3D Torus vs Switch Fabric

GPU 路线下的 Switch Fabric （NVSwitch / Fat-tree） 和 TPU 路线下的 3D Torus + OCS 代表了两条截然不同的 互联哲学。 同样也会对 TCO 带来影响，在这一部分我们会对这二者进行对比，在对比之前，我们会先对 Google TPU 的 3D Torus 路线进行分析。

Google TPU 的 3D Torus 路线

Google 的 OCS 路线

传统的电交换架构里，每跳一次就要做一轮 电→光→电的转换，功耗和延迟都会往上叠。 Google 用 OCS（光电路交换机）替代传统的电分组交换，核心诉求就是把功耗和成本打下来。目前 Google 主要用的是 AVGO 的 MEMS OCS，不过市面上也有其他路线，比如 Coherent 做的 DLC （数字液晶） OCS。

OCS 的直观理解是一个由上百个小镜子组成的“可调角度镜墙”。 对于一个 136x136 OCS 来说，光从输入光纤进入后，会依次打到两组 2D MEMS 微镜阵列上。每组阵列里有 136 个微小镜面，镜子都能在电信号驱动下独立倾斜。只要把每个镜子的倾角设对，交换机就能把某一束入射光精确“折”到指定的输出光纤上。这样一来，路径一旦建立，后续数据就在光域里直通，不需要每跳都做光电转换。

到 2026 年，Google 主力用的是 300x300 OCS，其中有效可用端口是 288 个。

Coherent 走的是另一条技术路线——用 DLC 代替 MEMS 镜片。电信号让液晶分子重新排列来改变光路，整个过程没有机械运动部件。DLC 方案的好处是成本更低、驱动电压也更小，但缺点是切换速度慢很多。不过对 Google 的 AI 训练集群来说这不是问题，因为这类集群的通信拓扑大约一周才重配一次，OCS 切换速度慢一点完全可以接受。

TPUs 的 3D Torus 是如何实现的

3D Torus 是一种网络拓扑结构，每个节点在三个维度上都与相邻节点相连，并且每个维度的首尾相连形成环状。TPU Pod 采用这种拓扑来实现芯片之间的高带宽、低延迟通信。

一个 TPU pod 由 4x4x4 = 64 个 TPU 组成， 和大家普遍认为 TPU 基本采用光互连相反，实际上， TPU Pod 内部以铜缆和 PCB 互联的， 一个 Pod 有 16 个 Server，每个 Server 上的 4 个 TPU 是用 PCB 线互联，而 16 个 Server 之间则用铜缆。

TPU Pod 之间则是使用光互连，我们可以把整个 Pod 看成一个立方体，6 个面每面 4×4 共 16 颗 TPU，理论上，如果 6 个面各自独立接 OCS，需要 16×6 = 96 条光连接；但 3D Torus 允许对立的两个面共用一台 OCS，把 6 个面的需求两两合并成 3 组，实际只要 96 / 2 = 48 个 OCS 端口（或单元）就能把所有 Pod 之间的光互连铺出来。

下图是 SemiAnalysis 所给的 TPU Pod 分别需要多少 PCB 线，铜缆和光模块：

TPU Cluster Size

在这个 TPU 集群里， 最大能做到多大，本质上是被 OCS 端口总数卡住的。 以现在的 v7p 系统为例，每台 OCS 等效是一个 144×144 的交换设备，一共 288 个可用端口（144 in + 144 out）。集群里配了 48 台 OCS，所以总端口数是 48 × 288 = 13,824。之前算过，一个 4×4×4 的 TPU 立方体需要 96 个端口，那么最多能挂的立方体数量就是 13,824 ÷ 96 = 144 个，对应最大集群规模 144 × 64 = 9,216 颗 TPU。

如果未来 OCS 真正升级到 300×300 规格，每台有 576 个可用端口（其中 24 个做冗余备份），那同样是 48 台 OCS，总端口数就变成 48 × 576 = 27,648。按每个立方体仍然吃 96 个端口来算，可以支撑 27,648 ÷ 96 = 288 个 4×4×4 立方体，对应的最大集群规模直接翻倍到 288 × 64 = 18,432 颗 TPU。 也就是说，在固定 Pod 拓扑不变的前提下，单台 OCS 端口数的提升，会线性抬高整个系统可扩展到的 TPU 数量上限。

SemiAnalysis 提出， 一个 TPU Cluster 理论上可以拓展到 147,456 颗 TPU：

• 通过传统的 Fat Tree 结构扩展到用 4,608 台 64×200G 的 ToR 交换机，首先把机柜里的 TPU 数量拉上来；

• 再通过配 2,304 台 128×200G 的 leaf 交换机和 2,304 台 128×200G 的 spine 交换机，叠成一棵三层 fat-tree；

• 最上层再挂 256 台 300×400G 的 OCS。

但由于链路层次多、带宽被一层层拆分稀释，单颗 TPU 实际能拿到的有效通信带宽比较低，也就是说绝对算力规模虽然堆上去了，但实际效率却被 Scale-up 网络带宽拖住了。

3D Torus 和 Switch Fabric(NVSwitch / Fat-tree) 对比

Switch Fabric（NVSwitch / Fat-tree） 和 3D Torus + OCS 代表了两条截然不同的互联哲学。理解它们的差异，可以从三个维度切入：互联模式假设、规模边界、优化目标。

维度 1：互联模式假设

1. Switch Fabric（NVSwitch / Fat-tree）的假设互联模式不确定

NVSwitch 在单域内（如 NVL72 的 72 张 GPU）用交换芯片实现近似全互联： 任意两点通信通常仅需 1–2 跳 ，延迟几乎恒定。因为全互联拓扑使任意 GPU 对都可以直接或通过一跳 NVSwitch 到达，无需预设固定通信路径，天然适配 All-Reduce、All-to-All、点对点等各类不确定的互联模式需求。

代价是 NVSwitch 芯片的 总交换带宽和端口数有硬天花板，单域规模被锁死在几十到百卡级别 ；一旦跨出域，就必须借助外部网络，带宽和延迟同时断崖式下降。

超过单域规模后必须要借助 Fat-tree（InfiniBand / Ethernet 的多级 spine-leaf 交换机堆叠），通过堆交换层级来堆带宽，是目前唯一能把集群推到数十万卡的方案。 代价是每多一级交换就多一跳延迟、多一份成本和功耗，且跨域带宽（典型 100 GB/s/卡）比域内 NVLink（1.8 TB/s/卡）低一个数量级。

2. 3D Torus + OCS 假设通信模式可预测、可编排。

核心不是做“任意两点直达”的通用互联，而是把训练里可预测、可编排的关键通信（梯度同步、张量切分聚合/分发、stage 间激活传递）压成路径和时序都固定的稳定数据流。关键不在于“够不够短”，而在于 路径/顺序可确定、可提前规划并与计算重叠，从而长期把链路喂满。对熟悉 LLM 结构与并行拆分的团队（如 GOOGL）来说 ，更容易把 DP/TP/PP 映 射到合适的物理维度，把需要频繁交互的分组放在物理上更“近”的区域，从而把这种“可排程”的优势放大。

这一代价是它对"流量长什么样"有强假设：一旦流量变成不规则或偏斜（典型如 MoE expert routing），某些维度的链路会被过载，且难以通过动态路由避免。单 Pod 上限约 9k 芯片，超出后跨 Pod 带宽骤 降。

维度 2：规模边界要分场景分别讨论

1. 在 LLM 训练环节：

• 百卡规模 （适合研究员个人小实验）下 NV Switch 占优，因为训练里的 TP/DP 梯度同步等关键 collectives 往往能压在单个 NVSwitch 域内，all-reduce 延迟低、带宽高，NCCL/框架并行策略也更容易稳定执行。

• 千卡到两万 卡规模（适合 Post-training  和中大型训练实验）: 3D Torus 占优——除非 MoE expert 数量较多。

训练通信大多满足"可预测可编排"条件，3D Torus + OCS 借此将单 pod 推至万卡级并维持高 MFU； GPU 同规模只能走 fat-tree，层级深、调度开销大，MFU 更易被拖累。 但 MoE 的 EP 通信本质是不规则 all-to-all： Expert 越多、负载越偏斜，通信瓶颈从"可排程的稳定流"转向"难被拓扑对齐的不规则分发与汇聚"——正好触发 3D Torus 对流量形态的强假设失效。这让万卡 TPU Pod 的扩展效率在高 Expert 数 MoE 中更早下滑，整体训练效率反而不如同规模 GPU 集群。

2. LLM 推理

LLM 推理要拆成 Prefill 和 Decode 两段看，Prefill 是算力瓶颈，Decode 是互联带宽/延迟瓶颈。

1）在推理的 Prefill 阶段，Prompt 可以被多卡并行处理，此时 GPU NVSwitch 更占优势。

因为 workload 更容易进入 compute-bound: 谁的低精度算力更猛，谁就能更接近满负载地把 token 吞下去。GB200/GB300 的 FP4 精度算力能 比 TPUv7 在 Prefill 阶段有 35-50% 的成本优势；NVL72 的 130 TB/s bisection 带宽和 1-2 跳的低延迟 fabric 可以保证多卡并行处理长 prompt 时几乎不受通信瓶颈限制。

2）在推理的 Decode 阶段，瓶颈通常出现在 HBM 带宽和 Scale-up 互联上。更具体来看：

• 对于延迟不敏感的离线大 batch 推理，TPU + 3D Torus 有性价比优势。 当 batch 足够大时，通信与调度开销更容易被吞吐摊薄，torus 的带宽也能被利用起来， 这时 TPU 有比 GPU 便宜 30-50% 的内存带宽成本（TCO / HBM Bandwidth）。

• 对于延迟敏感的在线小 batch 推理，GPU + NVSwitch 优势放大。 由于这时请求更碎、更随机时，torus 的固定 6 方向链路更容易出现热点和延迟抖动；而 NVSwitch 能让任意两张 GPU 互相传数据都基本是一跳直达 ，延迟更稳定可预测。 由于这时瓶颈变成了 Scale-up 互联了，而 GPU 的互联性价比（TCO / Scale-up Bandwidth） 和 TPU 相差不大，所以这时 GPU 能靠更好的用户体验胜出。

• 对于多 Experts 的 MoE 推理，GPU + NVSwitch 优势更明显。MoE 的 expert routing 本质上是不规则的 all-to-all，token 会被 gating 分发到分散在不同芯片上的 expert，流量模式和 torus 的 6 邻居固定拓扑天然不匹配。结果往往是热门 expert 所在的芯片会在某一个 torus 维度上形成持续热点，带来排队和尾延迟抖动。相对地，NVSwitch  能把“任意 GPU 到任意 GPU”的传输基本压成一跳直达，把 dispatch → compute → gather 的通信开销压到亚毫秒级，延迟更稳定、可预测。 因此，Expert 越多、负载越偏斜、路由越不规则，NVSwitch 的延迟确定性和体验优势就越大。

维度 3：TPU 软件优化

SemiAnalysis 花了不少篇幅介绍 TPU 为推理场景进行的算法优化，本质上是谷歌在在软件/编译器层面试图缩小 TPU 与 GPU 的差距， 把 TPU 原本不擅长处理的"不规则/动态"访存与通信，重新包装成“可预测、可流水”的稳定数据流， 从而让 3D Torus 的带宽被充分利用起来。

1. TPU KV Cache Management

GPU 用 paged attention 把 KV cache 当虚拟内存来管，按需从分散的地址把数据块抓出来再拼起来（scatter/gather）。这会带来大量随机地址访问和不连续读写，但 GPU 的高带宽显存加上强大的随机访存单元能容忍这类不规则操作。

TPU 的随机访存能力较弱，硬件更偏向批量、连续、可预测的数据搬运；一旦访存模式变成"动态地址 + 随机抓取"，延迟和吞吐都会恶化。

为此，Google 改用"预取 + pipeline": 提前把下一条序列需要的数据块搬进芯片，用矩阵计算把搬运延迟盖住，让内存访问重新变成时序可预测的稳定数据流。

但对应的代价是灵活性不如 GPU： 一批请求的结构必须提前确定，对请求随机到达、长度高度不一的在线场景适配成本更高。

2. TPU All-fused MoE Kernel

GPU 跑 MoE 模型的传统流程是先把 token 按目标专家排序，再分发到对应专家。排序本身是 GPU 擅长的并行操作，且 NVSwitch 能让传数据和做计算同时进行、互不干扰，所以这套流程在 GPU 上跑得很顺。

TPU 上的情况完全不同 ：它排序慢，而且很难一边搬数据一边算。如果按传统流程走，"先 排好队再一起发出去"这一步就会卡住整个流水线。 Google 的解法是干脆不排队——改成"轮到哪个专家就处理哪个专家"，一个一个来，把排序这个麻烦事直接跳过；同时趁着某个专家在算的时候，后台悄悄把下一个专家要用的数据搬过来，让搬运和计算交替进行、互不等待。

但这只能缓解单集群内的调度开销，无法改变 3D Torus 对流量形态的强假设：一旦专家数量多、负载偏斜、路由不规则，某些方向的链路仍会被过载，延迟难以被软件优化消除。

3. SparseCore

GPU + NVSwitch 天然支持任意两个 GPU 一跳直达，分发和汇聚的通信开销被压到毫秒级，通信与计算分开跑是互联层面的默认能力。这在面对 MoE 稀疏激活带来的动态 all-to-all 路由时尤为关键，确保 token-to-expert 分发不受拓扑限制。

TPU + 3D Torus 在处理 MoE 的不规则通信时，分发和汇聚容易卡住。Google 的应对是在芯片内加一个独立的稀疏计算单元（SparseCore），专门跑 MoE 的分发汇聚，和矩阵计算硬件级并行。 这在本质上是在硬件层承认 TPU 需要“类 NVSwitch 的通信-计算解耦能力”。

如果 Mosaic 编译器成熟、SparseCore 落地，能把 TPU 的 MoE 上限抬高、更接近 GPU 的灵活性。但这也会让 TPU 会浪费一些片上面积在 SparseCore，影响 Tensor 算力提升。

可以看到， TPU 的在推理场景的优化方向始终是“让不规则变规则”，而 GPU + NVSwitch 的设计哲学是“从一开始就容忍不规则”。 前者需要持续投入工程资源去适配每一种新的工作负载，后者则提供了一个更通用的底座。

当 MoE 成为主流架构、在线推理场景持续增长，TPU 面临的适配压 力 只会越来越大 ，而这正是 NVSwitch 的舒适区。

04 .

产品侧对比：NVDA Rubin vs Google TPU 8

Google TPU v8：双轨策略与成本结构重塑

Google 在 TPU v8 上采取“双供应商”策略，本质是降低 ASIC 的利润抽成。 TPU v8 分为两个 SKU，这两个 SKU 分别和不同的供应商合作：

• TPU 8AX（代号 Sunfish）：与 Broadcom 合作，沿用 N3E 制程，2 compute die + 1 I/O chiplet + 8 stack HBM3E 12-high，内存带宽为 9.8 TB/s， 相比 v7 提升 ～30%（9.6Gbps pin speed）。

• TPU 8X（代号 Zebrafish）：与 Medi aTek 合作，N3P 制程，1 compute die + 1 I/O die + 6 stack HBM3E 12-high，采用 MediaTek 自研 224G SerDes。

Google 选择 MediaTek 的核心逻辑是“Customer Owned Tooling”模式。

Broadcom 对整个 SiP 封装（包括 HBM）叠加了可观的利润率，尽管 Google 几乎全权负责计算单元的前后端设计，Broadcom 只贡献 PHY 和控制器。而 MediaTek 更灵活——Google 可以 直接从 SK Hynix 采购 HBM ，绕过设计公司的 margin 堆叠。 考虑到 HBM 占封装级 BOM 的最大头，这个设计成本影响巨大。

然而这个选择的代价是 工程资源被分散、tape-out 周期拉长 。没有 Broadcom 手把手带，TPU v8X 的流片时间远超预期，直到本季度才完成。

Nvidia Rubin：激进提速、推理专项优化

Nvidia 在竞争压力下临时加码了 Rubin 规格。

• 原计划：1800W 功耗，13T B/s HBM 带宽。

• 最终规格：2300W 功耗，20 TB/s HBM4 带宽（10Gbps pin speed）。

这不是常规迭代，而是 Nvidia 对 AMD MI400 和 Google TPU 双重威胁的应激反应。

Rubin 代际最主要的更新是显著倾向于优化推理的性能和 TCO，甚至新推出了针对 Prefill 场景的 CPX。

1. FP4 算力翻倍

GB300→VR200（Rubin）在"同为 3nm 级、还是两块大 die"的前提下把 FP4 FLOPS 拉到近乎翻倍 。本质不是制程奇迹，而是把 原本给互联/IO 的面积和功耗预算统统挪去堆 Tensor/SM ，再叠加更高 TDP 和频率上限一起堆出来的结果。

具体来说，Rubin 仍采用两块 3nm 计算 die，但在两侧加上独立 I/O tile，把 NVLink、PCIe、NVLink-C2C 这类 SerDes 大头搬出去， 大约释放出 20–30% 的逻辑面积配给更多 Tensor Core 和 SM， 同时从 Blackwell 世代的 4NP 切到 3NP（Nvidia 定制 3NP 或标准 N3P）带来逻辑密度提升，使得在“同工艺、同 die 数”下可以塞进显著更多做 FP4 矩阵乘的阵列单元。

在此基础上，Rubin 整卡 TDP 被推到约 2300W，既有利于时钟略微抬升，又支撑了更大的 Tensor Core systolic array——从 Blackwell 的 64×64 到 Rubin 的 128×128。

2. HBM4 带宽要求反复上调

为显著增强推理 Decode 阶段，Nvidia 在过去几个季度里多次上调 VR200 HBM4 的性能规格，从早期的 8Gbps 到现在的 10 Gbps，HBM4 bandwidth 从 16.4TB/s 来到了 20TB/s。 而同期的 TPU v8 虽然也略有上调，但最终版本还是停在 9.6Gbps 的 HBM3E，对应 9.8TB/s。 这让 Nvidia 阵营在内存带宽这条推理 Decode 的关键瓶颈上巩固优势。

3. CPX 推理专用芯片

为了进一步提升推理 TCO，Nvidia 在 VR200 NVL144 里引入 Rubin CPX，本质是在系统层面把“推理的 Prefill 计算型工作负载”从“需要高 HBM 容量 + 高 NVLink 带宽的通用 GPU 路径”里拆出来，做成一条更便宜、但更贴合 Prefill 瓶颈的专用算力芯片。

CPX 在仅相当于 R200/VR200 的 1/5–1/4 BOM 成本下，仍能实现 60% 的 FP4 算力，从而进一步巩固了其在推理 Prefill 环节的 TCO 优势。

Nvidia 通过 CPX 主动降低单位算力的内存与互联 BOM，把同等预算更多地押在“有效 Prefill 吞吐”上，从而在 TTFT（Time-to-First-Token） 这条关键体验指标上，继续拉开和其它体系（例如更强调 torus/内存带宽性价比的路线）之间的差距，形成“Prefill 阶段优势 = 更高吞吐 + 更低 TCO”的护城河。

R200 NVL144 CPX 机架进一步放大了这一优势：每个 compute tray 同时搭载 4 张 Rubin GPGPU （2 die + 288GB HBM + NVLink）和 8 张 Rubin CPX （1 die + 128GB GDDR7 + PCIe），实现了 Prefill 与 Decode 的物理解耦。

高性价比的 CPX 卡专门消化 Prefill 负载，GPU 卡则保留 NVSwitch 全连接拓扑来服务 Decode 和 MoE 路由，避免两阶段混跑时的相互干扰，从而在 Prefill 阶段的 TCO/Token 上拉开与竞品的差距。

TCO 变革

Google 历史上靠 TPU 建立的 TCO 护城河，在 v8 这一代被显著削弱。 原因有三：

1. 制程保守：TPU v8 仍在 3nm + HBM3E，Nvidia 上 3nm + HBM4，AMD 同期瞄准 2nm + HBM4。

2. 内存带宽落后：HBM 3E（9.8TB/s）vs HBM4（20TB/s），差距约 50%。

3. SerDes 节奏慢：尽管为 Broadcom SerDes 付 出高昂成本，Google 直到 2027 年才迁移到 224G。

Google 的问题不只是设计选择保守，还包括供应链效率。 从芯片制造到组装成机架再到跑起负载，Google 的周期比竞争对手更长。

如果 Nvidia 按计划执行 VR200 和 VR300：

• 外部客户：TPU v8 从"有竞争力"变成"不占优"。

• 内部负载：Rubin + Kyber rack 的 TCO 可能 追平甚至超过 TPU v8 ，即使是 Google 自己的训练任务。

这正是 Anthropic 需要重建 Nvidia 合作的原因： TPU（以及 Trainium）虽然在特定场景下穿针引线找到了性价比甜点，但 Nvidia 的迭代速度实在太快，难以长期忽视。从全球 FLOPs 出货量看，Nvidia 仍是绝对主导。

排版：傅一诺

延伸阅读

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247520518&idx=1&sn=2387449e94ca14114f7acc199d36959b&scene=21#wechat_redirect)

当 AI 接管钱包：Agentic Commerce 如何重构互联网经济？

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247520510&idx=1&sn=ffb241930b5b6fe38203e2c4dbefd129&scene=21#wechat_redirect)

深度解读 AGI-Next 2026：分化、新范式、Agent 与全球 AI 竞赛的 40 条重要判断

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247520443&idx=1&sn=e025ef2b59fd69c56e294d5f163beda6&scene=21#wechat_redirect)

拾象 2026 AI Best Ideas：20 大关键预测

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247520406&idx=1&sn=8e95b0b7825e3ddfa4c1bcca44b51755&scene=21#wechat_redirect)

Benchmark 新合伙人 Everett Randle: 忘掉 SaaS 逻辑与毛利率，AI 时代估值看单客价值

](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247520371&idx=1&sn=e92361c3d521d0bb77c5b7cc95d84978&scene=21#wechat_redirect)

AI 医疗全景更新：为什么硅谷 healthcare 领域出现了最多的 AI 独角兽？

