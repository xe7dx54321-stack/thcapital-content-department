# One-week Trial Run Protocol

Phase 20 的一周试运行只做人工运营演练，不自动发布、不接公众号 API、不进入草稿箱。

## Daily Routine

1. 运行 `make phase20-daily`。
2. 打开工作台审稿模式，先看“今日运营”。
3. 判断 TODAY / THIS_WEEK 内容是否真的可发。
4. 对缺图、缺证据、需重写、需推迟的内容记录人工动作。
5. 如人工发布，先创建 publish session，再手动复制到公众号后台。
6. 发布后人工录入 metrics 和视觉表现。
7. 收盘前查看 content ops closeout 和 failure handling。

## Do Not Publish When

- 缺一手证据或证据链不足。
- 图片资产缺失或视觉 checklist 未通过。
- copy pack 仍有 image slot marker 未处理。
- 标题/开头仍明显空泛。
- pipeline 出现 BLOCKER 且未人工排查。

## Exit Criteria

- 连续 5 个工作日 pipeline 不崩。
- operator 能清楚判断今日是否可发。
- 发布、图片、metrics 全部保持人工确认。
- failure handling 和 checklist regression 能解释主要风险。
