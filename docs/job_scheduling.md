# Job Scheduling

This document describes the job and scheduling solution in DHIS2.

## Jobs
### Fundamentals
In DHIS2 the term job refers to a potentially long-running background task with
a scheduled execution time.

Each job has a `JobType`. While there can be multiple `JobConfiguration`s 
for a type only one of these can run at a time.
This is an essential intentional restriction that is crucial to understand.

The `JobConfiguration` is linked to its `Job` implementation by the 
`JobType`. For each type there is one class implementing the `Job` interface.

### In-Memory vs Database Jobs
A job configuration can be flagged as an "in memory job". This means the 
change of (primarily) `JobStatus` is only applied to the `JobConfiguration` 
object but never persisted in the database. 
These configurations are often ad-hoc created and not persisted but in 
theory even a persisted configuration could be an "in memory job".

The `JobStatus` of `JobConfiguration`s that aren't "in memory jobs" is 
updated in the database whenever their `JobStatus` changes. This also 
affects last execution status and time as well as the next execution time.

### Leader Only Jobs
When jobs are flagged as "leader only" this means only the leader node in a 
cluster should run these jobs in the scheduler. The intention is to only 
perform database work once independent of the number of DHIS2 nodes 
connected to the same database.

### Job Parameters
Most `Job`s have job specific execution parameters that are part of a 
`JobConfiguration`. These are represented as subtypes of `JobParameters` and 
stored as JSON in the database.


## Scheduling
### How Jobs are started
Jobs are meant to be executed asynchronously started by a scheduler based on
the configuration. A job is executed either based on a CRON expression or
runs regularly based on a fixed time delay between executions.

Jobs are automatically (re)scheduled when the configuration is created or
updated. When a scheduled job is due to run it will attempt to stop any
running job of the same type assuming that this is a "phantom" that did not
finish cleanly. For scheduled configurations the `nextExecutionTime` 
contains the instant when the job should run again.

A job configuration can also be run manually. In that case the
part of configuration controlling the point in time the job should run is
ignored and the job is started right away. However, this is only possible
when a job of the same type is not already running.

### How Job execution is coordinated
Coordination of job execution is done to prevent running more than one job 
of the same type at a time. It does not matter if they were scheduled or run 
manually.

Scheduled execution is done using the DHIS2 wide `TaskScheduler`.
Manual execution is done using springs `AsyncTaskExecutor`.
These two are coordinated in the `DefaultSchedulingManager` using maps of 
`Future`s per `JobType` to remember scheduled and manually executed jobs.

### How Jobs are stopped (forced quit)
The internal `Future`s represent either a job being scheduled or a job 
currently running. If a job should be stopped the `Future` representing it 
is cancelled as an attempt to stop the execution. This means the thread 
running the task will get interrupted and hopefully terminate in a controlled 
way. 

Stopping a job can sometimes be ineffective due to error handling within the 
process.

### How Jobs are cancelled (request to give up)
`Job` implementations that make use of the `JobProgress` tracking and 
control can be asked to cooperatively give up running at the next "safe point".

When cancelled a job completes the item or step they are processing currently. 
Once the item is done they check if cancellation was requested and if so skip 
further execution to the end. 

A cancelled job does not roll back any changes done so far. A job might have 
specific routines to clean up a cancelled run but generally no such cleanup 
is done. Usually a cancelled job exists with a `CancellationException` and 
will have `JobStatus#FAILED`. However, this depends on how exactly a job 
handles the cancellation. Sometimes cancellation can be considered as a 
successful run. 


## Progress
### Fundamental of Progress Tracking
When `Job` implementations are executed it progress **can** be tracked. 
A `JobProgress` instance is created by the scheduler and passed to the 
execution method.

Tracking is an optional feature to allow an implementation to inform the 
scheduling in a generic way about the progress that is made for the background 
task the job is performing. 

The progress is divided into three levels

1. **Process**: a bracket around the overall background task
2. **Stage**: a technical or logical step within the process (task)
3. **Work Item**: a single "uninterruptible" unit of work within a stage

Both process and stage are strictly sequential and cannot fork-join parallel 
processing. The item level is meant for either sequential or parallel 
processing of work items. 

What process, stages and items will be occurring during the execution is 
unknown up-front. This information is "discovered" and collected into a tree 
structure as the execution progresses. Stages do however often provide a 
`totalItems` count when they start looping over a certain number of work items.
This allows to get a rough understanding of how much of the work of a stage 
has been completed already.

When a new process, stage or item node is collected and added to the 
execution three it's status is `RUNNING`. Once it is completed successful it 
changes to `SUCCESS`. Should an item fail the status becomes `ERROR`. 
Depending on the error handling this can further fail the stage and the overall 
process.

When a job is cancelled the process changes to status `CANCELLED` immediately.
The currently running item is completed as usual but the current stage might 
then also end with status `CANCELLED`.

### Using Progress Tracking
To use progress tracking in the implementation of a `Job`'s execution code 
the code "informs" the `JobProgress` object about the progress made by 
calling its methods. 

Each level consists of a start marker where a new node is announced.
For each node stated a corresponding call to _complete_ (execution is 
considered successful) or _failed_ should occur. These calls are added on 
top of (or in-between) the code that does perform the work.

For example, a simple sequence of calls would look as follows:

1. `startingProcess`
2. (maybe some loading of items)
3. `startingStage`
4. `statingItem`
5. (do the work for the item)
6. `completedItem`
7. `statingItem`
8. (do the work for the item)
9. `completedItem`
10. `completedStage`
11. (again, maybe some loading)
12. `startingStage`
13. `statingItem`
14. (assuming doing the work failed)
15. `failedItem`
16. `failedStage`
17. `failedProcess`

What kind of processing is represented as a process, stage or item is 
specific to the job and chosen as the author sees fit.

As this decoration of the essential processing code with the additional 
calls to the progress tracker clutters the code quite a bit there are helper 
methods `runStage` and `runStageInParalellel` in the `JobProgress` interface 
that can be used to do the bulk of the decoration. 

A typical stage can look like this:

```java
List<Item> items = loadItems();
progress.startingStage("Now doing step X", items.size());
progress.runStage(items, this::describeItem, this::processItem );
```
The `processItem` method passed as lambda is doing the work for one `Item` 
object. The `describeItem` method provides a readable description for the 
item which is used in the tree.
