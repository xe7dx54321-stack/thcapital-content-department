# Phase 33B Closeout Report

## 任务名称

Phase 33B：Workbench UX Information Architecture Cleanup v1

## 目标达成

将 Workbench 从"工程调试面板堆叠"重构成"内容工厂运营控制台"。

用户每天打开页面后，可在 30 秒内看懂：
1. 系统是否正常
2. 今天是否有最终候选稿
3. 这篇稿子是否值得审阅
4. 如果有问题，下一步该做什么

## 新信息架构

### 五个主导航（中文）

1. **今日总览** - 默认首页，只看结论
2. **今日稿件** - 读稿和审稿
3. **质量检查** - 内容质量和证据质量
4. **历史回放** - Phase33 7-day replay & calibration
5. **系统运维** - Runtime / LaunchAgent / OpenClaw / 调试

## 核心改动

### 新增文件

- `src/content_system/workbench_view_model.py` - 统一视图模型
- `scripts/build_workbench_view_model.py` - View Model 构建脚本
- `tests/test_workbench_view_model.py`
- `tests/test_workbench_information_architecture.py`
- `tests/test_workbench_today_overview.py`
- `tests/test_workbench_article_workspace.py`
- `tests/test_workbench_quality_check.py`
- `tests/test_workbench_replay_dashboard.py`
- `tests/test_workbench_system_ops.py`
- `tests/workbench_vm_fixture.py`

### 重构文件

- `src/content_system/wechat_workbench_frontend.py` - 五区域模块化渲染
- `src/content_system/wechat_workbench_data.py` - 集成 view model 生成
- `src/content_system/workbench_ui_server.py` - 服务端适配
- `scripts/serve_workbench_ui.py` - 启动脚本
- `Makefile` - 新增 `workbench-view-model` / `phase33b-workbench` 命令

## View Model Schema

```
schema_version: v1
├── today_overview      (结论优先，无调试字段)
├── today_article       (内容-only，无系统状态)
├── quality_check       (内容质量 + 证据质量)
├── replay_dashboard    (历史回放，不污染今日)
└── system_ops          (Runtime / LaunchAgent / OpenClaw / debug)
```

## 测试结果

```
Ran 15 tests in 0.003s
OK
```

覆盖：
- today_overview 只包含结论字段
- today_article 不含 Runtime PID / OpenClaw / path-audit
- quality_check 不含 LaunchAgent / heartbeat
- replay_dashboard 不污染 today_article
- system_ops 包含 Runtime / LaunchAgent / OpenClaw
- debug_actions 只出现在 system_ops
- 没有 final candidate 时首页显示 NO_CANDIDATE
- Runtime 异常时首页显示 SYSTEM_ISSUE
- 有 final candidate 且 quality PASS 时首页显示 READY_TO_REVIEW

## 浏览器验收

14 项全部通过：
- ✅ 默认首页是"今日总览"
- ✅ 首页 30 秒内能看懂今日状态
- ✅ 今日总览不出现 Runtime PID
- ✅ 今日总览不出现 path-audit
- ✅ 今日总览不出现 raw JSON
- ✅ 今日稿件页能直接看到最终候选稿
- ✅ 今日稿件页不出现 LaunchAgent / OpenClaw
- ✅ 质量检查页只显示内容质量和证据质量
- ✅ 历史回放页与今日稿件明显区分
- ✅ 系统运维页集中展示 Runtime / LaunchAgent / OpenClaw
- ✅ Agent 详细审稿默认折叠
- ✅ Replay 每日详情默认折叠
- ✅ console error = 0
- ✅ 页面整体干净、不拥挤

## 安全边界确认

✅ 不自动发布公众号
✅ 不接微信公众号 API
✅ 不进入公众号草稿箱
✅ 不抓取公众号后台数据
✅ 不抓全文
✅ 不自动生成图片
✅ 不调用图片模型
✅ 不修改 OpenClaw jobs.json
✅ 不接 OpenClaw gateway
✅ 不修改 OpenClaw cron
✅ 不停用 OpenClaw jobs
✅ 不关当前 Mac mini Runtime / LaunchAgent
✅ 不改写核心采集、选题、写稿逻辑
✅ 不自动应用 Phase33 calibration proposal
✅ 不修改 topic scoring / playbook / methodology
✅ 不覆盖历史原稿
✅ 不删除历史版本
✅ 不提交运行产物
✅ 不提交 API key 或 .env

## 下一阶段

Phase 34A：WeChat RSS Full-text Intelligence & Competitive Coverage v1
