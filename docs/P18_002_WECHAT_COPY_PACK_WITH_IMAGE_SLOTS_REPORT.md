# P18-002 WeChat Copy Pack with Image Slots Report

## 目标

生成可人工复制到微信公众号后台的图文发布包，并把图片槽位、插入说明、caption、alt text 和版权提示放进同一份 pack。

## 已完成

- 新增 `wechat_copy_pack_with_images.py`。
- 输出 `wechat-copy-pack-with-images` JSON/Markdown sidecar。
- 正文生成 `[[IMAGE_SLOT_X]]` markers，便于人工插图后删除。

## 边界

- 不调用公众号 API。
- 不生成草稿箱。
- 不发布。
