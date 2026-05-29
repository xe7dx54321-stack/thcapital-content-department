# P16-007 Image Generation Manual Approval Queue Report

## 本轮目标

把 image prompt 进入人工批准队列，为后续图片生成阶段做准备。

## 已完成

- 新增 `image_generation_approval_queue.py`。
- 支持 list / approve / reject / defer。
- 输出 `latest_image_generation_approval_queue.json/md`。

## 安全边界

- 即使 APPROVED，本轮也不生成图片。
- `do_not_auto_generate=true`。
- `generation_allowed=true` 只代表后续阶段可在人工确认后处理。
