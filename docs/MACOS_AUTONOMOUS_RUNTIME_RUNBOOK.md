# macOS Autonomous Runtime Runbook

## Dry Run

```bash
make macos-runtime-launchd-dry-run
```

The dry run renders a user-level LaunchAgent plist into `logs/autonomous-runtime/` and does not install anything.

## Install

Only run this after reviewing the rendered plist:

```bash
python3 scripts/install_macos_runtime_launchd.py
```

The plist starts `python3 scripts/run_autonomous_runtime.py` with `RunAtLoad` and `KeepAlive`. It does not contain API keys, `.env` values, cron schedules, publishing actions, or OpenClaw gateway calls.

## Check

```bash
make macos-runtime-launchd-check
```

## Uninstall

```bash
python3 scripts/uninstall_macos_runtime_launchd.py
```

Phase 31 development performs dry-run only. Actual installation is an operator action.
