# P31C-008 Runtime Scheduler Playbook Integration Report

The Runtime now has lightweight acquisition playbook jobs:

- `acquisition_playbook_plan`
- `acquisition_playbook_regression`

These jobs build lane-slot plans and regression gates. They do not create one Runtime job per source and do not depend on OpenClaw gateway or cron.
