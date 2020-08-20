

# PostgreSQL setup

This guide provides useful PostgreSQL commands for a development environment on Ubuntu/Debian.

## Install PostgreSQL 12

```bash
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
sudo apt update
sudo apt -y install postgresql-12 postgresql-client-12
```

## Start and stop

```bash
sudo service postgresql start
sudo service postgresql stop
```

## Allow connections from localhost

Open authentication config file:

```bash
sudo nano /etc/postgresql/12/main/pg_hba.conf
```

Comment out this line:

```
# "local" is for Unix domain socket connections only
# local   all             all                                     peer
```

Add these lines to the end of the file:

```
# Allow local connections without authentication
local   all             all                                     trust
host    all             all             0.0.0.0/0               trust
```

Restart to make changes take effect:

```bash
sudo service postgresql restart
```

## Performance tuning

Create file `pg_custom.conf` with the following content:

```properties
# Resource specific settings

max_connections = 300
shared_buffers = 2000MB
work_mem = 64MB
maintenance_work_mem = 2048MB
effective_cache_size = 6000MB

max_wal_size = 2GB
checkpoint_timeout = 15min

# SSD settings

random_page_cost = 1.1

# Generic settings

synchronous_commit = off
wal_writer_delay = 10000ms
checkpoint_completion_target = 0.9
max_locks_per_transaction = 96

# Log settings

log_lock_waits = on
log_duration = on
log_statement = 'all'
log_min_duration_statement = 10

# Include postgis schema in search path

search_path = '"$user", public, postgis'

# Extension pg_stat_statements settings

# shared_preload_libraries = 'pg_stat_statements'
# track_activity_query_size = 2048
# pg_stat_statements.track = all
```

Set ownership of the file and move it the config directory:

```bash
sudo chown postgres:postgres pg_custom.conf
sudo mv pg_custom.conf /etc/postgresql/12/main/
```


Open the main config file:

```
sudo nano /etc/postgresql/12/main/postgresql.conf
```

Include the custom config by including this line at the end of the file:

```properties
include 'pg_custom.conf'
```

Restart to make changes take effect:

```bash
sudo service postgresql restart
```

