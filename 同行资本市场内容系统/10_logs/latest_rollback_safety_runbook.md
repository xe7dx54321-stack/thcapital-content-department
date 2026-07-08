# Local Production Rollback & Safety Runbook

## 概述

- **生成时间**: 2026-07-08T02:48:14.189764
- **状态**: runbook_generated
- **章节总数**: 8

---

## pause_runtime. 如何暂停 Runtime

暂停 Mac mini Runtime 定时任务

**命令**:

```bash
python3 scripts/runtime_control.py pause
# 确认状态
python3 scripts/runtime_control.py status
```

**备注**: 暂停后 Runtime 不执行定时任务，但可手动运行

---

## resume_runtime. 如何恢复 Runtime

恢复 Mac mini Runtime 定时任务

**命令**:

```bash
python3 scripts/runtime_control.py resume
# 确认状态
python3 scripts/runtime_control.py status
```

**备注**: 恢复后 Runtime 恢复定时任务执行

---

## disable_rss. 如何停用真实 RSS 源

停用本地真实 RSS 源配置

**命令**:

```bash
# 清空 .env.rss
echo 'GEEKPARK_RSS_URL=' > .env.rss
echo 'OFFICIAL_AI_RSS_URL=' >> .env.rss
# 确认未启用
cat .env.rss
```

**备注**: 停用后 RSS ingest 将使用 mock 数据或 dry-run

---

## delete_outputs. 如何删除本地 RSS 运行产物

删除本地 RSS 运行产生的日志和输出

**命令**:

```bash
rm -f 同行资本市场内容系统/10_logs/*rss-ingest*
rm -f 同行资本市场内容系统/10_logs/*rss-clean*
rm -f 同行资本市场内容系统/10_logs/*rss-intelligence*
# 确认删除
ls 同行资本市场内容系统/10_logs/*rss* 2>/dev/null || echo '已删除'
```

**备注**: 不删除源码和配置文件

---

## check_secret. 如何确认没有 secret 入库

检查 Git 中是否包含 RSS secret

**命令**:

```bash
git status --short
# 搜索可能泄漏的 URL
grep -r 'https://' --include='*.json' --include='*.yaml' --include='*.md' 同行资本市场内容系统/10_logs/
# 检查 .env.rss 是否被忽略
cat .gitignore | grep '.env.rss'
```

**备注**: 如有泄漏，立即删除并从 Git 历史中移除

---

## dry_run. 如何回到 dry-run

恢复到云端 dry-run 模式

**命令**:

```bash
# 确认 .env.rss 已清空
cat .env.rss
# 运行 dry-run pipeline
make phase36-daily
make phase35-daily
make phase34a-daily
make wechat-workbench
```

**备注**: Dry-run 不依赖真实 RSS 和 Runtime

---

## rollback_commit. 如何回滚到上一个 commit

Git 回滚操作

**命令**:

```bash
# 查看最近 commit
git log --oneline -5
# 回滚到上一个 commit（保留改动）
git reset --soft HEAD~1
# 或回滚到指定 commit
git reset --hard <commit-hash>
# 强制推送到远程（谨慎）
git push --force origin main
```

**备注**: 谨慎使用 --force，仅在必要时执行

---

## stop_observation. 什么情况必须停止观察

需要立即停止观察的情况

**命令**:

```bash
# 立即暂停 Runtime
python3 scripts/runtime_control.py pause
# 清空 RSS 配置
echo '' > .env.rss
# 检查泄漏
git status --short
```

**备注**: 
以下情况必须立即停止：
- RSS secret 泄漏到 Git
- auto_publish 被意外启用
- OpenClaw 被意外修改
- 系统产生大量错误或异常输出
- 发现安全漏洞或合规问题


---


## 安全检查清单

执行回滚后，确认以下检查：

- [ ] Runtime 已暂停
- [ ] .env.rss 已清空
- [ ] RSS 运行产物已删除
- [ ] Git 中无 secret 泄漏
- [ ] .env.rss 在 .gitignore 中
- [ ] auto_publish 已禁用
- [ ] OpenClaw 未修改

---

**Phase36** | Local Production Rollback & Safety Runbook
