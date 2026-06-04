# P17-006 Human Final Visual Review Report

## 本轮目标

建立每张图片的最终人工视觉审查流程。

## 已完成能力

- 新增 `final_visual_review`。
- 支持 `review_visual_asset.py --list / --approve / --reject / --needs-revision / --defer`。
- 记录 relevance、clarity、information density、wechat readability、aesthetic fit、copyright safety。

## 边界

- approve 只代表图片视觉审查通过。
- 不自动发布。
- 不自动生成图片。
