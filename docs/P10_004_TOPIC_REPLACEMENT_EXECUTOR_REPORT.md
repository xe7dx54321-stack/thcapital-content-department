# P10-004 Topic Replacement Executor Report

## 目标

执行已批准的换题 action，从现有 high-value candidates / topic clusters 中选出替代选题。

## 已完成

- 新增 `topic_replacement_executor.py`。
- 新增 `execute_topic_replacement_actions.py`。
- 输出 `latest_topic_replacements.json` / `.md`。

## 执行策略

- 优先查 high-value candidates。
- 再查 topic clusters。
- 找不到则生成 research_more 建议。
- 不删除当前文章，不自动生成新稿。

## 当前限制

- 方向匹配仍是规则型。
