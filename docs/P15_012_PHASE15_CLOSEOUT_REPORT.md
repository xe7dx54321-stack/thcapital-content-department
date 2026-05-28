# P15-012 Phase 15 Closeout Report

## Phase 15 v1 目标

让系统从“按方法论评价内容”升级为“按方法论生成 brief / outline / draft / rewrite，并能为公众号文章规划图片和生成图片需求”。

## Methodology-aware Brief Builder

新增 methodology brief，回答核心问题、核心判断、why now、预期差、证据计划、反方、风险和视觉机会。

## Methodology-aware Outline Builder

新增 recipe-aware outline，每节包含问题、判断、证据和 visual slot。

## Methodology-aware Draft Writer

新增规则型方法论草稿，强调先判断后材料、证据服务判断、风险平衡和结尾框架。

## Methodology-aware Rewrite Executor

新增方法论改稿 executor，只生成新版本，不覆盖原稿。

## Article Visual Strategy Methodology

新增 8 类 visual type、10 个图片评价标准和 4 条图片获取/生成策略。

## Visual Plan Builder

为文章生成图片规划，说明每张图的位置、信息功能和 source strategy。

## Image Prompt & Asset Request Builder

生成 image prompt、negative prompt、design brief 和 copyright note。

## Methodology Regression Test Set

新增方法论回归测试样例。

## Human Methodology Calibration Board

新增人工校准看板。

## Workbench Generation & Visual Panel

工作台展示 generation / visual panel，并支持复制 image prompt / design brief。

## Daily Pipeline

新增 `make phase15-daily`。

## 当前限制

- 不自动生成图片。
- 不自动调用图片模型。
- 不自动发布。
- 不自动改 config/prompt/rules。
- 图片生成和图片使用需要人工确认。

## 下一阶段建议

Phase 16：Methodology-driven Live Agent Generation Pilot v1

- P16-001：Live Methodology Brief Agent Pilot
- P16-002：Live Methodology Draft Agent Pilot
- P16-003：Live Visual Prompt Agent Pilot
- P16-004：Human Calibration Feedback Apply v1
- P16-005：Image Generation Manual Approval Flow v1
