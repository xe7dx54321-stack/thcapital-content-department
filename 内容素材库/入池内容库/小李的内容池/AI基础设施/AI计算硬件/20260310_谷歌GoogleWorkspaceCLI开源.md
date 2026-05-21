# 谷歌开源CLI：Google Workspace CLI狂揽15k Stars

> 整理日期：2026-03-10
> 标签：#谷歌 #GoogleWorkspace #CLI #OpenClaw #开源 #2026-03

---

## 背景

OpenClaw火爆的盛况持续，国内甚至出现排队在腾讯总部楼下等待安装OpenClaw的场景。

而谷歌发布了一个**CLI神器**，上传到GitHub，放在Google Workspace官方组织名下。

---

## Google Workspace CLI

### 核心功能

全新的Google Workspace CLI将Drive、Gmail、Calendar等Google Workspace云API**统一封装为一个命令行工具**，为AI智能体自动化工作流提供标准化接口，通过结构化JSON输出，**能够方便地接入包括OpenClaw在内的各类AI Agent系统**。

### 成果

**短短几天，该项目已经收获了15k的Stars**

---

## 为什么选择gws

### 1. 对人类开发者

不再需要根据REST文档手写curl请求：
- 每个资源提供--help帮助信息
- 支持使用--dry-run预览请求
- 自动处理分页

### 2. 对AI智能体

所有返回结果都是**结构化的JSON**

结合内置的Agent技能，LLM可以**在无需编写额外工具的情况下直接管理Google Workspace**。

---

## 技术架构

### 两阶段解析策略

1. **第一阶段**：读取argv[1]，识别要调用的服务（如drive）
2. **获取服务**：获取该服务的Discovery Document并进行缓存（24小时）
3. **动态构建**：根据文档中定义的资源和方法，动态构建clap::Command命令树
4. **第二阶段**：再次解析剩余命令行参数
5. **执行**：完成身份认证，构建HTTP请求并执行

---

## AI Agent Skills

### 技能库

- 内置**100多个Agent Skills**（以SKILL.md文件形式提供）
- 每个支持的API对应一个技能
- 包含常见工作流程的高层辅助技能
- **50个精选使用示例**

覆盖应用：Gmail、Drive、Docs、Calendar、Sheets等

### OpenClaw集成

两种方式可选，配置步骤简洁。

---

## 安装要求

- **Node.js 18**或更高版本
- 一个Google Cloud项目（获取OAuth凭证）
- 拥有Google Workspace访问权限的Google账号

---

## 行业意义

1. **统一接口**：将Google Workspace API变成既适合人类、也适合AI Agent调用的统一接口
2. **降低门槛**：人类不用写API请求，AI不需要写额外工具
3. **生态连接**：可以方便接入OpenClaw等AI Agent系统

---

## 参考文献

- 来源：机器之心
- 项目地址：https://github.com/googleworkspace/cli
