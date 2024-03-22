# PostgreSQL Read Replica

DHIS2 supports having Postgres read replicas. This guide will go through the steps to setup replication streaming. We will have the following components working by the end:  
- DHIS2 server
- Postgres primary DB
- Postgres replica DB

**Note:** Postgres uses the [Write-Ahead Log (WAL)](https://www.postgresql.org/docs/current/wal-intro.html) as a means to stream updates to replicas. There are many ways to set up [replication](https://www.postgresql.org/docs/current/runtime-config-replication.html), this way seems to be the simplest. You need to have postgres on your path to be able to execute the following commands. This guide is intended for local development purposes only.

Postgres version `14.7` has been used in this guide.

# Primary DB
## Create

We will set up a completely new primary DB from scratch.

`initdb -D /user/primary_db/`

where `-D` is the directory where we want our primary DB (choose a directory of your choice)

## Update

We need to update a couple of properties in `/user/primary_db/postgres.conf`  
- `listen_addresses = '*'`  
- `port = 5435`

## Start

`pg_ctl -D /user/primary_db/ start`

## Create replication user

As part of the replication process, a user with replication privileges is required. We will use `psql` to do this. Start `psql` using the primary DB port we've just set, targeting the default `postgres` DB.

`psql --port=5435 postgres`  

Now create the user `repuser` marking it with the `replication` flag.  
`create user repuser replication;`

Next we have to update the `/user/primary_db/pg_hba.conf` in order to say who is authorised to connect and stream replication from the primary DB.  
Add a new row into the existing set of values, so it includes this record:  

| Type | Database | User    | Address      | Method |
|------|----------|---------|--------------|--------|
| host | all      | repuser | 127.0.0.1/32 | trust  |

## Restart
`pg_ctl -D /user/primary_db/ restart`

# Replica DB
## Create from backup
We can create the replica DB using `pg_basebackup` to create a backup of the primary DB.

```bash
pg_basebackup -h localhost -U repuser -D /user/replica_db/ -R -C --checkpoint=fast --slot=rep_slot --port=5435
```

flags used in previous command:  
- `-h localhost` host of primary DB
- `-U repuser` user to perform back up
- `-D /user/replica_db/` directory for new replica DB
- `-R` configures replication
- `-C` recycle WAL file only after replica has consumed it
- `--slot=rep_slot` slot name for replication
- `--checkpoint=fast` start copy process instantly
- `--port=5435` port of primary DB to back up

See [pg_basebackup docs for more info](https://www.postgresql.org/docs/current/app-pgbasebackup.html)

Check the replica directory to see the newly-copied files  
`ls /user/replica_db/`

Notice the `standy.signal` file which signals it's a replica DB.

## Update
We need to update the port the replica will use so we can run both locally. Update `/user/replica_db/postgres.conf` with:  
`port = 5436`

## Start
Start the replica  
`pg_ctl -D /user/replica_db/ start`

That's it, the replica DB should now be streaming updates from the primary DB.

# Checks
We can perform a couple of checks to confirm that the WAL streaming is in place.

Check the primary DB to see if the WAL is streaming. The presence of a record here confirms it's working as expected.  
`psql postgres --port=5435`  
`select * from pg_stat_replication;`

Check the replica DB for it's corresponding streaming record.  
`psql postgres --port=5436`  
`select * from pg_stat_wal_receiver;`

We can create a test table and insert a row in the primary DB and check if it's replicated in the replica DB.  
`psql postgres --port=5435`  
`create table test (name varchar);`  
`insert into test (name) values ('data in primary DB');`  

Check in replica DB to see if changes have been streamed.  
`psql postgres --port=5436`  
`select * from test;`  

Now you can apply any scripts to the primary DB in order to set up your local dev i.e. setup SL DB with extensions etc. Any changes in the primary will also be updated in the replica.

# DHIS2 conf
In order for DHIS2 to use the read replica, the `dhis.conf` file should have the following config.  
```
# primary DB connection details
connection.url = jdbc:postgresql://localhost:5435/dhis2-SL  
connection.username = repuser  
connection.password =

# replica DB connection details
read1.connection.url = jdbc:postgresql://localhost:5436/dhis2-SL
```

If successful, read only logs will be seen at start-up:  
```
09:09:51.469  INFO [           main] o.h.d.d.ReadOnlyDataSourceManager        : Read-only data source found with connection URL key: 'read1.connection.url' and value: 'jdbc:postgresql://localhost:5436/dhis2-SL'
09:09:51.501  INFO [           main] o.h.d.d.ReadOnlyDataSourceManager        : Created read-only data source with connection URL: 'jdbc:postgresql://localhost:5436/dhis2-SL'
09:09:51.501  INFO [           main] o.h.d.d.ReadOnlyDataSourceManager        : Read only configuration initialized, read replicas found: 1
```

# Notes for local dev
When locally developing, using the read replica setup, it can be useful to see which requests are going to which DB (primary or replica). One way to do this is to tail the logs on each DB.  
Update the relevant `postgres.conf` file for each DB with the following changes:  
- `logging_collector = on`  
- `log_directory = '/user/primary_db/logs'` use the replica dir for replica DB logs  
- `log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'`    
- `log_statement = 'all'`
 

Now tail the logs of both DBs, in separate terminals and watch requests come in to each DB.  
`tail -f /user/primary_db/logs/postgresql-{data-of-newest-log}.log`  
`tail -f /user/replica_db/logs/postgresql-{data-of-newest-log}.log`