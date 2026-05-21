# PinchBench：OpenClaw专属模型评测工具

> 整理日期：2026-03-10
> 标签：#PinchBench #OpenClaw #Agent #评测 #2026-03

---

## 背景

PinchBench是来自一支做Agent基础设施的创业团队**Kilo AI**的评测工具。

### 团队背景

- 团队名：**Kilo AI**
- 投资人：GitLab前联合创始人兼CEO Sid Sijbrandij
- 曾推出爆火"氛围编程"工具**Kilo Code**
- 年初推出基于OpenClaw构建的全托管智能体平台**KiloClaw**

---

## 评测特点

### 1. 与传统Benchmark不同

传统大模型Benchmark：知识问答、数学推理

PinchBench定位：**Agent能力测试**
- 不只看模型会不会回答问题
- 而是看模型能不能完成一整件事

### 2. 测试任务

约**23个真实任务**：
- 查询并整理资料
- 写邮件或生成报告
- 调用API完成操作

### 3. 评分机制

采用**自动化检查+LLM评审**的组合方式：
- 一部分任务有明确的自动检查脚本
- 另一部分任务由LLM Judge判断结果质量

### 4. 核心指标

| 指标 | 说明 |
|------|------|
| Success Rate | 任务完成率 |
| Speed | 完成速度 |
| Cost | 推理成本 |

---

## 有趣发现

### 更大的模型并非总是制胜之道

那些偏Agent优化或推理效率更高的模型，排名反而比传统主流大模型更靠前

---

## 开源情况

PinchBench目前**完全开源**，用户可以：
- 在平台上自行运行
- 添加新任务

---

## 参考文献

- 来源：量子位
- 原文链接：https://mp.weixin.qq.com/s/9QTE6YYEkM0vOHz1E9cB5Q
