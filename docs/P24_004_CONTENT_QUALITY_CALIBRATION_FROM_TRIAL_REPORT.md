# P24-004 Content Quality Calibration from Trial Report

## 目标

根据 stable trial 暴露的发布准备问题，校准内容质量风险，识别哪些标题、开头、核心判断、证据、逻辑、视觉问题真正拖慢发布。

## 实现

- 新增 `src/content_system/content_quality_calibration.py`。
- 新增 `scripts/build_content_quality_calibration.py`。
- 输出质量问题、publish-blocking 标记和 calibration recommendations。

## 边界

只生成校准建议，不改文章、不改方法论配置、不覆盖主线内容。
