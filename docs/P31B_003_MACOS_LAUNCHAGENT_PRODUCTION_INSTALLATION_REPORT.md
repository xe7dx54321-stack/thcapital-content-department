# P31B-003 macOS LaunchAgent Production Installation Report

The production LaunchAgent is installed only via explicit `--install`.

It is user-level only: `~/Library/LaunchAgents/com.thcapital.content-factory-runtime.plist`.

The plist starts `scripts/run_autonomous_runtime.py` and contains no secrets or business schedule.
