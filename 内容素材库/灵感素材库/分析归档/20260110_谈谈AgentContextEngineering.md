## TL;DR

最近无意中看了两篇文章,一篇是 《Monadic Context Engineering》  [1]  , 另一篇是 《RECURSIVE LANGUAGE MODELS》  [2]  . 正好去年中写过一段时间Multi Agent做量化分析的小工具, 因此想展开聊一下Context Engineering.

其实这是一个挺烦人的问题, 例如模型输出的一些错误导致调用不存在的工具, 或者外部工具由于网络的稳定性等问题无法产生正确的回复. 去年在Kimi K2发布前, 很多开源模型的Agent执行能力都有各种各样的问题. 例如在    中, 有这样一个一个工作流:

当一个资产组合中标的数量增加后, 经常由于中间某一步失败而导致整个任务失败. 特别来说某些模型会在调用资产数量较多时出现无法正确的调用工具的情况, 例如函数名出错等. 或者是由于Context过长, 整个任务成本非常高(例如用Claude单次超过1美金).

因此当时在Context Engineering上做了一些优化, 大致就和这两篇论文的内容相似了.

# 1. Monadic Context Engineering

## 1.1 为什么需要Monad

在第一篇介绍MCP    的时候其实就谈到了这个话题, MCP is a Monad

在MCE论文中进一步拓展到了整个Context Engineering, 阐述了主要问题:

"命令式"指的是开发者需要明确写出每一步操作的执行顺序和控制流 (例如, 使用大量的 if/else 来处理错误, 手动传递状态对象). "ad hoc" 指的是这些解决方案通常是为特定问题量身定制的, 缺乏一个通用, 可复用的底层架构, 导致代码难以维护和扩展.带来的后果是系统像玻璃一样, 稍有预料之外的输入(如 API 失败)就可能崩溃或进入不一致的状态. 而在Agent开发过程中, 通常会遇到的核心挑战:

例如本文开头所说的对于一个资产组合的多个标的, 我们期望它能并行的执行并以最短的时间产生报告和交易决策来构建一个相对中频的量化交易策略. 但是并行执行带来的Context爆炸和错误处理是一个非常麻烦的事情. 这也是我在去年底想专门针对这个领域做一个RL后训练的原因. 实质就是一些从MCE视角上进行的转变:不再将 Agent 的工作流看作是一系列指令, 而是看作一个 在上下文中进行的计算 (computation within a context) . 正如作者所阐述的:

## 1.2 基于Monad的Agent开发

当前Agent开发的一些挑战:

构建这些 Agent 的工程师们面临着一系列反复出现的根本性挑战. 其中最重要的是 维护状态的完整性 , 这要求在可能失败的一系列操作中可靠地传播. 同时, Agent 需要错误恢复能力来优雅地处理现实世界的失败, 例如 API 超时或格式错误的模型输出, 而不让核心逻辑被防御性的代码所混淆. 此外, 开发者需要逻辑的可组合性来从独立的逻辑单元构建复杂的行为, 以便无缝地组装, 重排和替换各个步骤.

除了顺序逻辑之外, 现代 Agent 还要求强大的并发性来编排多个同时发生的动作, 而不陷入手动线程管理的复杂性. 理想情况下, 架构还应严格管理计算的副作用, 将确定性逻辑与同外部世界的非确定性交互分离开来. 最后, 随着系统的扩展, 我们必须解决 Agent 编排的问题, 管理可以为解决新问题而动态组建的专业 Agent 团队, 而不引入混乱的交互.

那么很直接的一个办法就是借鉴函数式编程. 为在上下文中组合计算提供了一种标准化的方法. 函子(Functor)允许你将一个纯函数应用到上下文中的值上. Applicative Functor对此进行了扩展, 支持将一个被包装的函数应用到一个被包装的值上, 这种结构对于并发执行独立计算至关重要. 最后, Monad 允许对依赖性操作进行排序, 其中后续的计算由前一个计算的结果决定.

然后作者再形象的解释了一下  `bind`  操作: “让我们能够为计算构建一条“铁路”. 每个逻辑步骤都扮演一个车站的角色, 而  `bind`  则铺设轨道, 确保计算过程在"成功轨道"上顺利进行. 如果任何一个步骤失败,  `bind`  会自动将整个计算分流到"失败轨道", 绕过后续的车站, 直接前往目的地. ”

# 2. AgentMonad设计

这一章是具体如何构建MCE应用于AI Agent.

## 2.1 Monad Transformer

单个 Agent 操作可能需要与外部 API 交互, 处理可能的失败, 并更新 Agent 的内部记忆或世界模型. 试图用朴素的嵌套来管理这些关注点, 例如像  `Task<Either<State<...>>>`  这样的类型, 是行不通的. 它迫使开发者手动解开上下文的每一层, 重新引入了 Monad 旨在消除的深度嵌套的回调式代码.

一个 Monad Transformer,  `$T$`  , 是一个类型构造器, 它接受一个现有的 Monad  `$M$`  并产生一个新的, 更强大的 Monad  `$T(M)$`  , 这个新 Monad 结合了两者的行为. 至关重要的是, Transformer 提供了一个  `lift`  操作 (  `lift: M A -> T M A`  ), 它允许内部 Monad 中的任何计算能够无缝地在组合后的外部 Monad 的上下文中使用. 这使得创建一个共享单一统一接口的能力栈成为可能.

`AgentMonad`  利用这种技术创建了一个专为 Agent 工作流设计的栈:

底层是 IO 或 Task Monad, 它管理与外部世界的交互. 这将一个动作的描述与其执行分离开来, 使得行为可观察. 然后应用  `EitherT Transformer`  , 它引入了短路的错误处理逻辑. 这直接模拟了像模型上下文协议(MCP)等规范的要求, 其中工具结果必须明确指示成功或失败. 最后用  `StateT Transformer`  包装这个栈.

最终得到的类型  `StateT S (EitherT E IO)`  它确保了交互是可观察的, 错误处理是健壮的, 状态管理是函数式的, 并且工作流是可组合的. 对这个复合结构的一次  `bind`  操作就能正确地串联状态, 检查错误, 并对外部动作进行排序.

## 2.2 Level 1: AgentMonad 作为函子

最基础的操作涉及将一个纯函数应用到我们上下文中的值上, 而不改变上下文本身. 这是 Functor 及其  `map`  操作的角色.

`map`  函数 (或  `fmap`  ) 接受一个函数  和一个  `AgentMonad[S, A]`  , 返回一个  `AgentMonad[S, B]`  . 它将  `$f$`  应用于被包装的值, 同时保持状态和成功/失败状态不变. 如果流程已经失败,  `map`  不会执行任何操作.

## 2.3 Level 2: AgentMonad 作为Applicative Functor

主要用于处理一个更复杂的场景: 如果我们想要应用的函数本身也被包装在我们的上下文中呢? 这对于组合独立计算的结果特别有用.

`apply`  操作 (或  `<>`  ) 接受一个包含函数  `(A -> B)`  的  `AgentMonad`  和一个包含值  `(A)`  的  `AgentMonad`  , 返回一个包含结果  `(B)`  的新上下文. 这个机制从它们各自的上下文中提取函数和值并应用它们, 同时确保状态被传播并且失败被绕过.

## 2.4 Level 3: AgentMonad 作为 Monad

它解决了 Agent 编排的核心挑战: 对操作进行排序, 其中每个步骤的逻辑都 依赖于前一个步骤的结果 .

`bind`  操作接受一个  `AgentMonad[S, A]`  和一个函数  . 该操作从第一个上下文中解包出值和状态, 并将它们传递给  ,  会返回一个新的  `AgentMonad`  . 这允许每个步骤独立地改变状态或失败, 而状态  则由该结构隐式传递.

这种结构抽象掉了状态传递和错误检查的重复且易错的样板代码. 开发者可以完全专注于定义每个独立步骤的逻辑.

一个简单的例子如下:

```python
task = " What is a Monad ?"  
initial_state = AgentState ( task = task )  
  
# The agent logic is defined as a single , declarative , and robust chain .  
async_flow = (  
    AsyncAgentMonad.start ( initial_state )  
    .then( lambda s, _: plan_action (s, task ))  
    .then( lambda s, call : execute_tool (s, call ))  
    .then( synthesize_answer )  
    .then( format_output )  
)  
final_result_flow = await async_flow .run ()
```

或者并行调用:

```python
async def create_daily_briefing ( state : AgentState , user_query :  
    str) -> AgentMonad :  
    # 1. Define independent , asynchronous tasks  
    news_task = AsyncAgentMonad.start (state , user_query ).then(async_fetch_news)  
    weather_task = AsyncAgentMonad.start (state , user_query ).then(async_fetch_weather)  
    stocks_task = AsyncAgentMonad.start (state , user_query ).then (async_fetch_stocks)  
      
    # 2. Execute concurrently via Applicative ’gather ’  
    # The result is an AsyncAgentMonad that will resolve to a list of results  
    gathered_data_flow = AsyncAgentMonad.gather([ news_task ,weather_task , stocks_task ])  
  
    # 3. Synthesize the collected results  
    synthesis_step = await gathered_data_flow.then(async_synthesize_briefing ).run()  
    return synthesis_step
```

其实在前端框架上也出现过类似的情况, 早期的Node.js框架Express开始导致的大量的Callback Hell, 然后逐渐演进到Koa2 这样的框架. 而现在的Google ADK其实也有点类似于Koa2这样的洋葱式的模型. 但后期我可能更习惯于React/Redux这样偏函数式编程的前端, 把一些复杂的状态都在web端处理, 尽量把后端的接口做的简单一点. 所以也期待Agent框架上会有一些变化, 虽然学习曲线有点陡峭, 但是写起来真方便.

# 3. 沙箱Monad

其实另一个问题是在模型训练和推理中, 涉及沙箱执行的环境, 特别是一系列复杂的多步的操作, 例如Browser Use/Mobile Use/ Computer Use的场景, 如何构建这些沙箱的状态记录和回滚, 进一步降低副作用的影响. 这是一个值得去展开考虑的话题. 例如VM/容器级别的快照, 网页类应用前端来适配这样的Monad ?

# 4. RECURSIVE LANGUAGE MODELS

然后是第二篇论文, 《Recursive Language Models》提出了一种新颖, 强大且通用的推理框架, 用于解决大型语言模型的长上下文处理瓶颈. 通过将长提示外部化到 REPL 环境中, 并允许模型通过代码和递归调用与之交互, RLM 成功地将输入长度扩展了数个数量级, 并在各种复杂度的任务上显著优于现有方法.

实质是构建了一个REPL环境, 对长上下文的处理采用了  `分治`  和  `递归`  的算法, 实际上就是把Context当成一个栈来使用.

去年我在构建一个量化交易算法的Agent时, 也采用了类似的逻辑, 不过分治和递归都是手工写的一些代码. 另外在阅读很多论文的时候, 也有一个小的Agent分章节进行一些翻译/总结/分析, 并让模型产生一些辩证的观点. 然后当时也有一些想法做一些后训练, 把这些能力直接做进模型里. 另一方面还蛮期待支持Sparse Attention的模型出现, 这样就可以更好的将Context的需求降低.

## 4.1 长上下文的问题

现有方法存在一些局限性:

1. 上下文压缩/精简 (Context Condensation/Compaction): 这是一种流行的推理时方法, 当上下文超过阈值时, 反复对其进行总结. 这种方法的根本缺陷在于它是有损的. 它假设提示早期的某些细节可以被安全地遗忘, 以便为新内容腾出空间. 对于需要密集访问提示多个部分的任务, 这种方法表现不佳.
2. 任务分解 (Task Decomposition): 许多先前工作专注于任务的递归分解, 但它们的输入仍然无法超越底层 LLM 的上下文窗口.

## 4.2 RLM的观点

RLM 的观点是: 长提示不应直接被送入神经网络, 而应被视为 LLM 可以进行符号化交互的外部环境.

其工作机制如下:

1. 给定一个任意长度的Prompt

    , RLM 初始化一个REPL的编程环境 (本文中使用 Python REPL).
2. 被加载为 REPL 环境中的一个变量 (例如, 一个巨大的字符串或字符串列表).
3. RLM 向 LLM 提供关于 REPL 环境的元信息 (例如, 变量  的长度), 并允许 LLM 编写代码来:

- 窥视 (peek into) : 查看变量  的片段.
- 分解 (decompose) : 将  切分成小块.
- 递归调用 (invoke itself recursively) : 对  的片段构建子任务, 并 递归地调用自身 (或一个子 LLM) 来处理这些子任务.

4. 迭代与反馈: LLM 可以迭代地观察代码执行的副作用, 并根据结果调整下一步行动.

## 4.3 Token as instruction

设计上, 通过REPL让大模型分治和递归来处理复杂任务从体系结构的视角来看就是: Token as instruction.赋予了大模型本身一个栈的结构, 在    中也有相应阐述:

就像前段时间说的, 本文就是在试图通过大模型架构构造一个自己能够产生代码运行的通用计算机架构, token as instruction. 当脑子里补出这图的时候, 就豁然开朗了. 大模型从自回归可能真的要走向自生成Instruction的路了.... 那么构造一个大模型的冯诺伊曼架构大概就如下了.

这条路可以做一些有趣的RL, 应该也有一些收益, 例如RLM举的例子:

从技术上来看, 配合block based sparse attention是一个挺有趣的视角.

参考资料

[1]

Monadic Context Engineering:  *https://arxiv.org/pdf/2512.22431*

[2]

RECURSIVE LANGUAGE MODELS:  *https://arxiv.org/pdf/2512.24601*