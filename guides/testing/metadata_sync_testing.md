
# Metadata Synchronisation

Metadata synchronisation is a fundamental part of DHIS2. The ability to push and pull metadata/data between instances is key behaviour.  

This can be difficult to test, given it requires at least 2 DHIS2 instances set up. The following steps outline how to test a Metadata Synchronisation job using [Instance Manager](https://im.dhis2.org/instances).

# Steps

## Create central DHIS2 instance
This will be the central server, which remote servers try to synchronise with.

1. create new instance
2. give appropriate name e.g. `metadata-sync-central`
3. choose the image you wish to test with
4. choose the database with the name `dev/min-metadata-sync-2-39.sql.gz`  
	> **NOTE:** This Sierra Leone DB (2.39) has been modified using [these commands below](#sql-commands), in order for a Metadata Sync job to complete quickly.
5. click create (it can take a few mins to start-up)

## Create remote DHIS2 instance
This will be the remote server, which will synchronise with the central server.

1. create new instance
2. give appropriate name e.g. `metadata-sync-remote`
3. choose the image you wish to test with
4. choose the database with the name `dev/min-metadata-sync-2-39.sql.gz`  
   > **NOTE:** This Sierra Leone DB (2.39) has been modified using [these commands below](#sql-commands), in order for a Metadata Sync job to complete quickly.
5. click create (it can take a few mins to start-up)

## Setup Sync Settings on Remote Server
In order to enable synchronisation, the following steps are required on the remote server:
1. Set remote URL (insert your server names)  
   `POST` `{remote-server-url}/api/systemSettings/keyRemoteInstanceUrl?value={central-server-url}`  
2. Set remote username  
	`POST` `{remote-server-url}/api/systemSettings/keyRemoteInstanceUsername?value=system`  
3. Set remote password  
	`POST` `{remote-server-url}/api/systemSettings/keyRemoteInstancePassword?value=System123`

## Create Metadata Sync Job
Create a metadata sync job, set up to run weekly (we can still run it on-demand in a later step, this is just so we're not spamming the logs)
  
`POST` `{remote-server-url}/api/jobConfigurations` with body:
```json
{
    "name": "meta-data-sync-job",
    "jobType": "META_DATA_SYNC",
    "cronExpression": "0 0 3 ? * MON"
}
```

## Run Metadata Sync Job
First get the job id with this call:  
`GET` `{remote-server-url}/api/jobConfigurations?filter=displayName:eq:meta-data-sync-job`  
Then trigger the job to run, with this call:  
`POST` `{remote-server-url}/api/jobConfigurations/{jobUid}/execute`

## Check Job Completion
We can check if the job has run successfully by looking at a few things:
### Logs
Open the Instance Manager logs and look through them. It should look something like this:
```text
14:55:02.961  INFO [qtp733461760-23] o.h.d.s.AuthenticationLoggerListener     : Authentication event: AuthenticationSuccessEvent; username: system
14:55:11.509  INFO [qtp733461760-24] o.h.d.d.m.DefaultMetadataImportService   : (system) Import:Start
14:55:11.609  INFO [qtp733461760-24] o.h.d.p.DefaultPreheatService            : (system) Import:Preheat[REFERENCE] took 0.089778 sec.
14:55:11.646  INFO [qtp733461760-24] d.m.o.h.JobConfigurationObjectBundleHook : Validation succeeded for job configuration: 'meta-data-sync-job'
14:55:11.648  INFO [qtp733461760-24] m.o.DefaultObjectBundleValidationService : (system) Import:Validation took 0.012597 sec.
14:55:11.651  INFO [qtp733461760-24] o.h.d.d.m.o.DefaultObjectBundleService   : (system) Creating 1 object(s) of type JobConfiguration
14:55:11.661  INFO [qtp733461760-24] o.h.d.s.DefaultSchedulingManager         : Scheduling job: JobConfiguration{uid='xE0HQnOCsJM', name='meta-data-sync-job', jobType=META_DATA_SYNC, cronExpression='0 */1 * * * *', delay='null', jobParameters=org.hisp.dhis.scheduling.parameters.MetadataSyncJobParameters@7e0b36be, enabled=true, inMemoryJob=false, lastRuntimeExecution='null', userUid='null', leaderOnlyJob=false, jobStatus=SCHEDULED, nextExecutionTime=null, lastExecutedStatus=NOT_STARTED, lastExecuted=null}
14:55:11.661  INFO [qtp733461760-24] o.h.d.s.DefaultSchedulingManager         : Job xE0HQnOCsJM of type META_DATA_SYNC has been added to the schedule
14:55:11.661  INFO [qtp733461760-24] o.h.d.s.DefaultSchedulingManager         : Scheduled job: JobConfiguration{uid='xE0HQnOCsJM', name='meta-data-sync-job', jobType=META_DATA_SYNC, cronExpression='0 */1 * * * *', delay='null', jobParameters=org.hisp.dhis.scheduling.parameters.MetadataSyncJobParameters@7e0b36be, enabled=true, inMemoryJob=false, lastRuntimeExecution='null', userUid='null', leaderOnlyJob=false, jobStatus=SCHEDULED, nextExecutionTime=null, lastExecutedStatus=NOT_STARTED, lastExecuted=null}
14:55:11.669  INFO [qtp733461760-24] o.h.d.c.DefaultHibernateCacheManager     : Hibernate caches cleared
14:55:11.669  INFO [qtp733461760-24] o.h.d.d.m.DefaultMetadataImportService   : (system) Import:Commit took 0.020425 sec.
14:55:11.670  INFO [qtp733461760-24] o.h.d.d.m.DefaultMetadataImportService   : (system) Import:Done took 0.161845 sec.
14:55:21.262  INFO [qtp733461760-24] o.h.d.s.DefaultSchedulingManager         : Scheduler initiated execution of job: JobConfiguration{uid='xE0HQnOCsJM', name='meta-data-sync-job', jobType=META_DATA_SYNC, cronExpression='0 */1 * * * *', delay='null', jobParameters=org.hisp.dhis.scheduling.parameters.MetadataSyncJobParameters@664f6af, enabled=true, inMemoryJob=false, lastRuntimeExecution='null', userUid='null', leaderOnlyJob=false, jobStatus=SCHEDULED, nextExecutionTime=null, lastExecutedStatus=NOT_STARTED, lastExecuted=null}
14:55:21.280  INFO [askScheduler-13] o.h.d.d.m.j.MetadataSyncJob              : Metadata Sync cron Job started
14:55:21.281  INFO [askScheduler-13] o.h.d.d.DbmsUtils                        : Checking for an open Hibernate session
14:55:21.281  INFO [askScheduler-13] o.h.d.d.DbmsUtils                        : No open session found, caught HibernateException Could not obtain transaction-synchronized Session for current thread, opening new Hibernate session now
14:55:21.285  INFO [askScheduler-13] o.h.d.d.m.j.MetadataRetryContext         : Now trying. Current count: 1
14:55:21.290  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage started: Setting up metadata synchronisation
14:55:21.291  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage completed after 0.002s
14:55:21.292  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Process started: Starting DataValueSynchronization job
14:55:21.880  INFO [askScheduler-13] o.h.d.d.s.SyncUtils                      : Status: [Available: true, message: Authentication was successful, HTTP status: 200 OK]
14:55:21.880  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage started: Counting data values
14:55:22.245  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage completed after 0.365s: DataValues last changed before Thu Jan 01 01:00:00 IST 1970 will not be synchronized.
14:55:22.248  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage started: 1 DataValues to synchronize were found.
Remote server URL for DataValues POST sync: https://dev.im.dhis2.org/test-metadata-sync/api/dataValueSets
DataValueSynchronization job has 1 pages to sync. With page size: 10000
14:55:23.085  INFO [askScheduler-13] o.h.d.d.s.SyncUtils                      : Sync summary: ImportSummary{status=SUCCESS, description='Import process completed successfully', importCount=[imports=0, updates=0, ignores=1], conflicts={}, dataSetComplete='false', reference='null', href='null'}
14:55:23.086  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage completed after 0.838s: 1 successful and 0 failed items
14:55:23.086  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Process completed after 1.794s: SUCCESS! DataValueSynchronization job is done.
14:55:23.088  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Process started: Starting Event programs data synchronization job.
14:55:23.229  INFO [askScheduler-13] o.h.d.d.s.SyncUtils                      : Status: [Available: true, message: Authentication was successful, HTTP status: 200 OK]
14:55:23.230  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage started: Counting anonymous events ready to be synchronised.
14:55:23.230  INFO [askScheduler-13] o.h.d.d.s.EventSynchronization           : CurrentUser is null, before performing EVENT_PROGRAMS_DATA_SYNC, the remote sync user will be injected
14:55:23.410  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage completed after 0.18s: Events last changed before Thu Jan 01 01:00:00 IST 1970 will not be synchronized.
14:55:23.411  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage started: 1 anonymous Events to synchronize were found.
Remote server URL for Event programs POST synchronization: https://dev.im.dhis2.org/test-metadata-sync/api/events?strategy=SYNC
Event programs data synchronization job has 1 pages to synchronize. With page size: 60
14:55:24.081  INFO [askScheduler-13] o.h.d.d.s.SyncUtils                      : Sync summary: ImportSummaries{importSummaries=[ImportSummary{status=SUCCESS, description='null', importCount=[imports=0, updates=1, ignores=0], conflicts={}, dataSetComplete='null', reference='x6yWDMa0LP7', href='https://dev.im.dhis2.org/test-metadata-sync/api/events/x6yWDMa0LP7'}]}
14:55:24.083  INFO [askScheduler-13] o.h.d.d.s.EventSynchronization           : The lastSynchronized flag of these Events will be updated: [x6yWDMa0LP7]
14:55:24.097  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage completed after 0.686s: 1 successful and 0 failed items
14:55:24.097  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Process completed after 1.009s: SUCCESS! Event programs data sync was successfully done! It took 
14:55:24.097  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Process started: Starting Complete data set registration synchronization job.
14:55:24.249  INFO [askScheduler-13] o.h.d.d.s.SyncUtils                      : Status: [Available: true, message: Authentication was successful, HTTP status: 200 OK]
14:55:24.249  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage started: Counting complete data sets
14:55:24.301  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage completed after 0.052s: CompleteDataSetRegistrations last changed before Thu Jan 01 01:00:00 IST 1970 will not be synchronized.
14:55:24.301  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage started: 1 completed data set registrations to synchronize were found.
Remote server URL for completeness POST synchronization: https://dev.im.dhis2.org/test-metadata-sync/api/completeDataSetRegistrations
14:55:24.488  INFO [askScheduler-13] o.h.d.d.s.SyncUtils                      : Sync summary: ImportSummary{status=SUCCESS, description='Import process complete.', importCount=[imports=0, updates=1, ignores=0], conflicts={}, dataSetComplete='null', reference='null', href='null'}
14:55:24.489  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage completed after 0.188s
14:55:24.494  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Process completed after 0.397s: Complete data set registration synchronization is done.
14:55:24.494  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Process started: Starting Tracker programs data synchronization job.
14:55:24.644  INFO [askScheduler-13] o.h.d.d.s.SyncUtils                      : Status: [Available: true, message: Authentication was successful, HTTP status: 200 OK]
14:55:24.645  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage started: Counting TEIs to synchronise
14:55:24.686  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage completed after 0.041s: TrackedEntityInstances last changed before Thu Jan 01 01:00:00 IST 1970 will not be synchronized.
14:55:24.686  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage started: 1 TEIs to sync were found.
Remote server URL for Tracker programs POST synchronization: https://dev.im.dhis2.org/test-metadata-sync/api/trackedEntityInstances?strategy=SYNC
Tracker programs data synchronization job has 1 pages to synchronize. With page size: 20
14:55:24.980  INFO [askScheduler-13] o.h.d.d.s.SyncUtils                      : Sync summary: ImportSummaries{importSummaries=[ImportSummary{status=SUCCESS, description='null', importCount=[imports=0, updates=1, ignores=0], conflicts={}, dataSetComplete='null', reference='k68SkK5yDH9', href='https://dev.im.dhis2.org/test-metadata-sync/api/trackedEntityInstances/k68SkK5yDH9'}]}
14:55:24.981  INFO [askScheduler-13] o.h.d.d.s.TrackerSynchronization         : The lastSynchronized flag of these TEIs will be updated: [k68SkK5yDH9]
14:55:24.986  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage completed after 0.3s: 1 successful and 0 failed items
14:55:24.986  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Process completed after 0.492s: SUCCESS! Tracker programs data synchronization was successfully done!
14:55:24.986  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage started: Getting the current version of the system
14:55:24.991  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage completed after 0.005s: Current Metadata Version of the system: MetadataVersion{importDate=null, type=BEST_EFFORT, name='Version_3', hashCode='6cd02b2c1fe034c18ac0006bd87001ca'}
14:55:24.992  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage started: Fetching the list of remote versions
14:55:25.142  INFO [askScheduler-13] o.h.d.d.s.SyncUtils                      : Status: [Available: true, message: Authentication was successful, HTTP status: 200 OK]
14:55:25.142  INFO [askScheduler-13] o.h.d.d.m.v.MetadataVersionDelegate      : Remote server metadata version  URL: https://dev.im.dhis2.org/test-metadata-sync/api/metadata/version/history?baseline=Version_3, username: system
14:55:25.566  WARN [askScheduler-13] o.h.d.d.m.v.MetadataVersionDelegate      : Dhis http response is null
14:55:25.566  WARN [askScheduler-13] o.h.d.d.m.v.MetadataVersionDelegate      : Returning empty for the metadata versions difference
14:55:25.567  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Stage completed after 0.576s: Your instance is already using the latest version:MetadataVersion{importDate=null, type=BEST_EFFORT, name='Version_3', hashCode='6cd02b2c1fe034c18ac0006bd87001ca'}
14:55:25.567  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Process started: Synchronize metadata
14:55:25.567  INFO [askScheduler-13] o.h.d.s.ControlledJobProgress            : [META_DATA_SYNC xE0HQnOCsJM] Process completed after 0s
14:55:25.567  INFO [askScheduler-13] o.h.d.d.m.j.MetadataSyncJob              : Metadata sync cron job ended 
14:55:25.567  INFO [askScheduler-13] o.h.d.d.DbmsUtils                        : Closing Hibernate session
```

### Job Summary
Check the job summary for all stages to show as `SUCCESS`  
`GET` `{remote-server-url}/api/scheduling/completed/META_DATA_SYNC`  
It should look something like this:
```json
[
    {
        "status": "RUNNING",
        "startedTime": "2024-04-26T06:51:24.856",
        "stages": [
            {
                "status": "SUCCESS",
                "completedTime": "2024-04-26T06:51:24.873",
                "startedTime": "2024-04-26T06:51:24.856",
                "description": "Setting up metadata synchronisation",
                "totalItems": 0,
                "onFailure": "FAIL",
                "items": [],
                "duration": 17,
                "complete": true
            }
        ],
        "jobId": "Jv0MKmcTmcB",
        "duration": 18406808,
        "complete": false
    },
    {
        "summary": "Skipping synchronization, no new or updated DataValues",
        "status": "SUCCESS",
        "completedTime": "2024-04-26T06:51:25.653",
        "startedTime": "2024-04-26T06:51:24.873",
        "description": "Starting DataValueSynchronization job",
        "stages": [
            {
                "summary": "DataValues last changed before Thu Jan 01 00:00:00 UTC 1970 will not be synchronized.",
                "status": "SUCCESS",
                "completedTime": "2024-04-26T06:51:25.652",
                "startedTime": "2024-04-26T06:51:25.636",
                "description": "Counting data values",
                "totalItems": 0,
                "onFailure": "FAIL",
                "items": [],
                "duration": 16,
                "complete": true
            }
        ],
        "jobId": "Jv0MKmcTmcB",
        "duration": 780,
        "complete": true
    },
    {
        "summary": "SUCCESS! Event programs data sync was successfully done! It took ",
        "status": "SUCCESS",
        "completedTime": "2024-04-26T06:51:27.493",
        "startedTime": "2024-04-26T06:51:25.654",
        "description": "Starting Event programs data synchronization job.",
        "stages": [
            {
                "summary": "Events last changed before Thu Jan 01 00:00:00 UTC 1970 will not be synchronized.",
                "status": "SUCCESS",
                "completedTime": "2024-04-26T06:51:25.847",
                "startedTime": "2024-04-26T06:51:25.754",
                "description": "Counting anonymous events ready to be synchronised.",
                "totalItems": 0,
                "onFailure": "FAIL",
                "items": [],
                "duration": 93,
                "complete": true
            },
            {
                "summary": "1 successful and 0 failed items",
                "status": "SUCCESS",
                "completedTime": "2024-04-26T06:51:27.493",
                "startedTime": "2024-04-26T06:51:25.853",
                "description": "1 anonymous Events to synchronize were found.\nRemote server URL for Event programs POST synchronization: https://dev.im.dhis2.org/metadata-sync-central/api/events?strategy=SYNC\nEvent programs data synchronization job has 1 pages to synchronize. With page size: 60",
                "totalItems": 1,
                "onFailure": "SKIP_ITEM",
                "items": [
                    {
                        "status": "SUCCESS",
                        "completedTime": "2024-04-26T06:51:27.492",
                        "startedTime": "2024-04-26T06:51:25.855",
                        "description": "Synchronizing page 1 with page size 60",
                        "onFailure": "SKIP_ITEM",
                        "duration": 1637,
                        "complete": true
                    }
                ],
                "duration": 1640,
                "complete": true
            }
        ],
        "jobId": "Jv0MKmcTmcB",
        "duration": 1839,
        "complete": true
    },
    {
        "summary": "Complete data set registration synchronization is done.",
        "status": "SUCCESS",
        "completedTime": "2024-04-26T06:51:28.521",
        "startedTime": "2024-04-26T06:51:27.493",
        "description": "Starting Complete data set registration synchronization job.",
        "stages": [
            {
                "summary": "CompleteDataSetRegistrations last changed before Thu Jan 01 00:00:00 UTC 1970 will not be synchronized.",
                "status": "SUCCESS",
                "completedTime": "2024-04-26T06:51:27.625",
                "startedTime": "2024-04-26T06:51:27.596",
                "description": "Counting complete data sets",
                "totalItems": 0,
                "onFailure": "FAIL",
                "items": [],
                "duration": 29,
                "complete": true
            },
            {
                "status": "SUCCESS",
                "completedTime": "2024-04-26T06:51:28.515",
                "startedTime": "2024-04-26T06:51:27.626",
                "description": "1 completed data set registrations to synchronize were found.\nRemote server URL for completeness POST synchronization: https://dev.im.dhis2.org/metadata-sync-central/api/completeDataSetRegistrations",
                "totalItems": 0,
                "onFailure": "FAIL",
                "items": [],
                "duration": 889,
                "complete": true
            }
        ],
        "jobId": "Jv0MKmcTmcB",
        "duration": 1028,
        "complete": true
    },
    {
        "summary": "SUCCESS! Tracker programs data synchronization was successfully done!",
        "status": "SUCCESS",
        "completedTime": "2024-04-26T06:51:29.298",
        "startedTime": "2024-04-26T06:51:28.522",
        "description": "Starting Tracker programs data synchronization job.",
        "stages": [
            {
                "summary": "TrackedEntityInstances last changed before Thu Jan 01 00:00:00 UTC 1970 will not be synchronized.",
                "status": "SUCCESS",
                "completedTime": "2024-04-26T06:51:28.746",
                "startedTime": "2024-04-26T06:51:28.616",
                "description": "Counting TEIs to synchronise",
                "totalItems": 0,
                "onFailure": "FAIL",
                "items": [],
                "duration": 130,
                "complete": true
            },
            {
                "summary": "1 successful and 0 failed items",
                "status": "SUCCESS",
                "completedTime": "2024-04-26T06:51:29.298",
                "startedTime": "2024-04-26T06:51:28.748",
                "description": "1 TEIs to sync were found.\nRemote server URL for Tracker programs POST synchronization: https://dev.im.dhis2.org/metadata-sync-central/api/trackedEntityInstances?strategy=SYNC\nTracker programs data synchronization job has 1 pages to synchronize. With page size: 20",
                "totalItems": 1,
                "onFailure": "SKIP_ITEM",
                "items": [
                    {
                        "status": "SUCCESS",
                        "completedTime": "2024-04-26T06:51:29.298",
                        "startedTime": "2024-04-26T06:51:28.749",
                        "description": "Synchronizing page 1 with page size 20",
                        "onFailure": "SKIP_ITEM",
                        "duration": 549,
                        "complete": true
                    }
                ],
                "duration": 550,
                "complete": true
            }
        ],
        "jobId": "Jv0MKmcTmcB",
        "duration": 776,
        "complete": true
    },
    {
        "status": "RUNNING",
        "startedTime": "2024-04-26T06:51:29.299",
        "stages": [
            {
                "summary": "Current Metadata Version of the system: MetadataVersion{importDate=null, type=BEST_EFFORT, name='Version_3', hashCode='6cd02b2c1fe034c18ac0006bd87001ca'}",
                "status": "SUCCESS",
                "completedTime": "2024-04-26T06:51:29.309",
                "startedTime": "2024-04-26T06:51:29.299",
                "description": "Getting the current version of the system",
                "totalItems": 0,
                "onFailure": "FAIL",
                "items": [],
                "duration": 10,
                "complete": true
            },
            {
                "summary": "Your instance is already using the latest version:MetadataVersion{importDate=null, type=BEST_EFFORT, name='Version_3', hashCode='6cd02b2c1fe034c18ac0006bd87001ca'}",
                "status": "SUCCESS",
                "completedTime": "2024-04-26T06:51:29.829",
                "startedTime": "2024-04-26T06:51:29.310",
                "description": "Fetching the list of remote versions",
                "totalItems": 0,
                "onFailure": "FAIL",
                "items": [],
                "duration": 519,
                "complete": true
            }
        ],
        "jobId": "Jv0MKmcTmcB",
        "duration": 18402366,
        "complete": false
    },
    {
        "status": "SUCCESS",
        "completedTime": "2024-04-26T06:51:29.830",
        "startedTime": "2024-04-26T06:51:29.830",
        "description": "Synchronize metadata",
        "stages": [],
        "jobId": "Jv0MKmcTmcB",
        "duration": 0,
        "complete": true
    }
]
```

There is an easier way to check if a Metadata Sync job was successful, checking the `lastExecutedStatus` field on a `JobConfiguration`, but [this bug](https://dhis2.atlassian.net/browse/DHIS2-17292) needs to be fixed before being able to check this way.

# SQL Commands
Executing these commands leaves the database with a small amount of data to use in the Metadata sync process, namely:  
- 1 Data Value
- 1 Event Program Data Value
- 1 Complete Dataset Registration
- 1 Tracker Data Value

This enables a full Metadata synchronisation job to run quickly while ensuring that the core synchronisation functionality is working correctly, end-to-end. If data correctness is important then a different database should be used.
```sql
-- 1
DELETE FROM public.datavalue
WHERE (dataelementid, periodid, sourceid, categoryoptioncomboid) != (360543, 1499506, 260438, 360525);

-- 2
TRUNCATE TABLE public.programstageinstancecomments;

-- 3
TRUNCATE TABLE public.trackedentitydatavalueaudit;

-- 4
DELETE FROM public.programstageinstance
WHERE programstageinstanceid != 216829;

-- 5
DELETE FROM public.completedatasetregistration
WHERE datasetid != 217115;

-- 6
DELETE FROM public.trackedentityprogramowner
WHERE trackedentityinstanceid != 217202;

-- 7
DELETE FROM public.relationshipitem
WHERE trackedentityinstanceid != 217202;

-- 8
DELETE FROM public.trackedentityattributevalueaudit
WHERE trackedentityinstanceid != 217202;

-- 9
DELETE FROM public.trackedentityattributevalue
WHERE trackedentityinstanceid != 217202;

-- 10
TRUNCATE TABLE public.programinstancecomments;

-- 11
DELETE FROM public.programinstance
WHERE trackedentityinstanceid != 217202;

-- 12
DELETE FROM public.trackedentityinstance
WHERE trackedentityinstanceid != 217202;

-- 13
DELETE FROM public.programinstance
WHERE programinstanceid != 1150223;
```