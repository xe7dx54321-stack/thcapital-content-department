# Operator Acceptance Checklist

## Daily Acceptance

The system is acceptable for daily use when:

- `make stable-daily-ops` runs without crashing.
- The workbench opens at `同行资本市场内容系统/11_frontstage/latest_wechat_workbench.html`.
- Today's operator actions are visible.
- The content queue and publishing readiness are visible.
- Quality issues and blockers are explicit.
- No automatic publishing, WeChat API, image generation, or config mutation is enabled.

## Manual Review

Manual review is always required before any real publishing action. The system can be ready for daily ops while content remains not ready to publish.

## Stop Conditions

Stop and repair first when:

- A safety boundary fails.
- A blocker is present.
- Publishing checklist regression fails.
- Workbench generation fails.
- The queue has no explanation for non-ready content.
