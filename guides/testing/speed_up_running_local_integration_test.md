# Problem 
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

# Cut start-up time in half
As applying the migrations seems to cause most of the start-up time, we can avoid these by generating a new base schema after the migrations have already been applied. 
This optional setup allows running a Postgres integration test in half this time (`~25 seconds`). To do this we need: 
1. a new base schema, generated from:
   1. extensions 
   2. original base schema
   3. all migrations 
4. Updated test config in file `postgresTestDhis.conf`, with the following property:
   1. `flyway.skip_migration = true`

## How to create a new base schema 
To generate a new base schema follow these steps.

### 1 - Create empty DB with required extensions
```shell
#!/bin/bash

echo "drop database dhis2";
sudo -u dhis dropdb dhis2 --if-exists

echo "create database dhis2";
sudo -u dhis createdb -O dhis dhis2

echo "create extensions";
sudo -u dhis psql -c "create extension postgis;" dhis2
sudo -u dhis psql -c "create extension pg_trgm;" dhis2
sudo -u dhis psql -c "create extension btree_gin;" dhis2
```

### 2 - Start the DHIS2 core server 
From latest master branch, start the DHIS2 core server locally, using the newly-created DB. 
The app will apply all the base schema & all migrations. This brings us up to the latest point in time for the full DB schema. 

### 3 - Create a new base schema 
After the app was started, the DB is now in a state where we would like a new snapshot of the current schema. This new base schema will include: 
1. extensions
2. original base schema
3. all migrations 

To generate the new schema, use the command: 
```shell
pg_dump --schema-only --no-owner dhis2 > ~/Documents/scripts/init-db.sql
```

## Use new schema in integration test 
With the new schema generated, copy/move it to the directory: 
```text
dhis2-core/dhis-2/dhis-support/dhis-support-test/src/main/resources/db
```

This directory will be checked during Postgres container creation, to see if the file `init-db.sql` is present. 
If it is present, the Postgres container will use that script to initialize the DB. 
If it is not present, the Postgres container will start up as normal & all migrations will be applied to the base schema (original setup). 

# Points of note 
The generation of a new base schema will need to be kept up to date to include newer migrations. This could be easily automated, chaining a few commands. 

The file `dhis2-core/dhis-2/dhis-support/dhis-support-test/src/main/resources/db/init-db.sql` is included in the `.gitignore` file as it should never be added. 

Revert the test property when finished.