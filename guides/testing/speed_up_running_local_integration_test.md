# Pain Point 
It currently takes `~50 seconds` for a Postgres integration test to start-up locally, before executing any tests. (Different machines may have different results. Data taken from Mac M2 pro 16GB) 

This is not ideal for local development and is painful.
Looking into why it takes so long, revealed this info:

| seconds | info                            |
|---------|---------------------------------|
| 15      | for test container to come up   |
| 7       | for PostgreSQL base schema init |
| 20      | for migrations to complete      |
| 7       | for App to come up              |
| 49      | total, before test execution    |

# Remedy - Cut start-up almost completely using local dhis conf
A new integration test config `use.local.dhis.conf` has been added to the `postgresTestDhis.conf` file. If the value is set to `yes` or `true` then the integration test will use your local `dhis.conf` file for all config. This includes which database to use for the test, bypassing the need for docker.

The intended use of this setting is for scenarios where you might be developing a new feature or debugging and will be running the same test(s) multiple times.

It is not intended to run the entire integration test suite, as some tests require custom dhis config.

Requirements:  
- have an empty DB with all required extensions running (see script below)
- update `postgresTestDhis.conf` with config `use.local.dhis.conf=yes`
- ensure your local `dhis.conf` file points to the correct DB and includes the following config `hibernate.cache.use_second_level_cache=false`  

Watch out for other properties in `postgresTestDhis.conf` that may be required in your local `dhis.conf`.

## Empty DHIS2 DB script
```text
#!/bin/bash

echo "drop database dhis2";
sudo -u <your_postgres_user> dropdb dhis2 --if-exists

echo "create database dhis2";
sudo -u <your_postgres_user> createdb -O dhis dhis2

echo "create extensions";
sudo -u <your_postgres_user> psql -c "create extension postgis;" dhis2
sudo -u <your_postgres_user> psql -c "create extension pg_trgm;" dhis2
sudo -u <your_postgres_user> psql -c "create extension btree_gin;" dhis2
```