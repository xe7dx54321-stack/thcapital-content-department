# TH Capital Content Factory Dashboard

这是内容工厂的独立展示台目录，作用是把展示层从主业务仓里剥出来，单独提供：

- 固定的本地启动入口
- 独立的日志和运行状态
- 不与隔壁 VC Dashboard 抢同一个端口

## 默认入口

- 首页：`http://127.0.0.1:8780/intake`
- 今日草稿池：`http://127.0.0.1:8780/drafts`
- 今日选题池：`http://127.0.0.1:8780/top20`
- 今日锁题页：`http://127.0.0.1:8780/selection`
- 学习池：`http://127.0.0.1:8780/learning`

## 常用命令

- 启动：`./start.sh`
- 停止：`./stop.sh`
- 重启：`./restart.sh`
- 状态：`./status.sh`
- 打开浏览器：`./open.sh`

## 目录说明

- `runtime/`：当前运行状态、PID、URL
- `logs/`：服务日志

## 数据来源

真正的数据与 HTML 快照仍然来自：

- `/Users/apple/Documents/同行资本内容部门/内容生产系统`

本目录只负责把内容工厂展示台以更稳定的方式拉起来。
