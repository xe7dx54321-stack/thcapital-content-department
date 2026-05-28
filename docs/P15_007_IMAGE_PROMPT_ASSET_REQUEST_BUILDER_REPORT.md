# P15-007 Image Prompt & Asset Request Builder Report

## 本轮目标

根据 visual plan 生成图片 prompt 和素材需求清单。

## 修改文件

- `src/content_system/image_asset_request_builder.py`
- `scripts/build_image_asset_requests.py`

## 核心能力

- 生成 `image_prompt`、`negative_prompt`、`design_brief`、`copyright_note`。
- 可标注 `recommended_tool=gpt-image-2`。

## 边界

`do_not_auto_generate=true`，不自动调用图片模型。
