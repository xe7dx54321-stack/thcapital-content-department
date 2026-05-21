# Publish Readiness Template

## 作用

用于说明一个 Draft Pack 当前是否具备进入下一阶段的条件。

## 推荐结构

- `draft_pack_status`
- `overall_readiness`
- `platform_readiness`
- `blockers`
- `notes`
- `first_screen_ready`
- `context_bridge_ready`
- `proof_anchor_ready`
- `personality_consistency_ready`
- `cta_ready`

## 判断原则

- `ready`：可以进入下一阶段，不代表已经发布
- `needs_revision`：还有明显缺口，不能装作已经过关
- 如果首屏没有交代对象 / stakes / why now，不应标记为 `ready`
