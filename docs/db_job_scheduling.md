## State Diagram

```mermaid
stateDiagram-v2
direction LR
state ONCE_ASAP {
  [*] --> Prepared: `create` (programmatically)
  Done --> [*]: `deleteFinishedJobs` (heartbeat task)
}
Prepared --> Ready/Scheduled: `executeNow`
Ready/Scheduled --> Ready/Scheduled: `executeNow` (run manually in app)
Ready/Scheduled --> Running: `start`
Ready/Scheduled --> [*]: delete (in app)
Running --> Done: `finish`
Running --> Running: `updateProgress`
Running --> Ready/Scheduled: `rescheduleStaleJobs`
Running --> Ready/Scheduled: `finish`
Running --> Ready/Scheduled: `skip`
Running --> Cancelled: `cancel` (user request)
Cancelled --> Done
Cancelled --> Ready/Scheduled
Disabled --> Ready/Scheduled: enable (in app)
Ready/Scheduled --> Disabled: disable (in app)
[*] --> Ready/Scheduled: create (in app)
note right of Cancelled: still running but flagged
note left of Ready/Scheduled: scheduler loop picks up here
```
OBS! 
* transition to disable and delete can apply in any state but is only shown from `Ready/Scheduled`
* `Cancelled` is identical to `Running` except it cannot transition to `Cancelled` any more (not all transtions are shown for simplicity)


| State | `jobState` | `schedulingType` | Other conditions |
|--|--|--|--|
| `Prepared` | `NOT_STARTED` | `ONCE_ASAP` | |
| `Ready/Scheduled` | `SCHEDULED` | * | |
| `Running` | `RUNNING` | * | |
| `Cancelled` | `RUNNING` | * | `cancel = true` |
| `Done` | `DISABLED` | `ONCE_ASAP` | `lastFinished != null` |
| `Disabled` | * | * | `enabled = false` |
