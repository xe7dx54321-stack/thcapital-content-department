# P11-002 Human Accept / Reject Version Report

## 本轮目标

为候选新版本增加人工接受、拒绝、继续修改、延后决策层。

## 已完成能力

- 新增 version review board。
- 支持 `review_article_version.py --list / --accept / --reject / --revise-more / --defer`。
- 记录 `do_not_publish=true` 与 `do_not_overwrite_original=true`。

## 边界

- `ACCEPT` 只表示可作为候选最终稿参考。
- 不发布。
- 不覆盖原稿。
