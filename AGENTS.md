# Agent Instructions

## Scheduled Reminders

Before scheduling reminders, check available skills and follow skill guidance first.
Use the built-in `cron` tool to create/list/remove jobs (do not call `nanobot cron` via `exec`).
Get USER_ID and CHANNEL from the current session (e.g., `8281248569` and `telegram` from `telegram:8281248569`).

**Do NOT just write reminders to MEMORY.md** — that won't trigger actual notifications.
**Do NOT use cron to monitor or drive batch/subagent task progress** — that is handled by the built-in heartbeat watchdog and subagent announce mechanism.

## Heartbeat Watchdog

`HEARTBEAT.md` is checked every 30 minutes by the heartbeat watchdog.
The watchdog evaluates **wake conditions** defined in the file against the current runtime state.

Use `edit_file` to manage HEARTBEAT.md:
- **Add tasks**: append under "Active Tasks"
- **Set wake conditions**: write rules under "Wake Conditions"
- **Mark complete**: change `[ ]` to `[x]` or move to "Completed"

When you spawn subagents for long-running tasks, write appropriate wake conditions so the watchdog can detect if you become stalled.

**Do NOT create cron jobs to check batch task progress.** The heartbeat watchdog already monitors wake conditions every 30 minutes. Cron jobs run as independent sessions without access to main session state — they cannot accurately assess subagent progress and will produce false alarms and duplicate work.
