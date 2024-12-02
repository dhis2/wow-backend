# New database table Flyway migration

This guide covers how to write a Flyway migration to introduce a new database table for metadata entities. This step is necessary when introducing new persistent entities in DHIS 2. When creating new tables, it is important to ensure data types and constraints are properly defined, and to be consistent with existing tables in the database.
[Here](https://github.com/dhis2/wow-backend/blob/master/guides/flyway_db_migration.md), you can find a general overview of how Flyway is used in DHIS2.

## Auto-generate database table

An approach to automatically generate a metadata database table is through the Hibernate `hbm2ddl` tool. To enable automatic creation of new database tables you can set the following property in `dhis.conf`:

```
connection.schema = create
```

During regular development the recommended value is:

```
connection.schema = validate
```

## Get database table definition SQL statement

A useful database administration tool which allows for generating data definition SQL statements is [dBeaver](https://dbeaver.io/), which is an open source universal database tool.

Ensure that the DHIS 2 PostgreSQL database is connected in dBeaver.

* Open the DHIS 2 database and expand schemas, select the **public** schema and expand the tables.
* Right-click the table, select **Generate SQL** and click **DDL**.

This will bring up the `CREATE TABLE` SQL statement, which can be used either directly or as a starting point for the Flyway migration. 

An exception is the usage of qualified table names, meaning including the schema name (such as `public`) before the table name, as the schema name should be omitted in DHIS 2 Flyway migrations.

## Database table definition

When creating a new database table the following applies.

* Use `create table if not exists` to create the table, as Flyway migrations should be idempotent, meaning the SQL statement should not crash nor have any effect if invoked more than once.
* Use `int8` instead of `integer` for primary key and foreign key int columns. The 8 byte int data type is more appropriate given that primary keys in many implementations have gone above the 2.1B max value for 4 byte data type.
* Include a primary key constraint on the primary key identifier column.
* Use `timestamp` instead of `timestamp without timezone` for created and last updated columns.
* Use `varchar` instead of `character varying` for limited text columns.
* Use `text` instead of `varchar` for unlimited text columns mapped to `text` in the Hibernate schema definition.
* Include foreign key constraints on all foreign key columns.
* Include unique constrains on unique columns such as `uid`, `code`, `name` and `shortname` (if appropriate).
* Ensure constraints have unique and readable names and are included in the table definition. This also helps ensure they are idempotent.
* Use lowercase table and column names. DHIS 2 uses lowercase naming of all database relations. PostgreSQL will use lowercase values for non-quoted values in any case.
* Quote column names with double quotes in case of special or reserved characters. This is optional for names without special or reserved characters but is a healthy approach in any case.
* Use lowercase for all SQL keywords such as `create table if not exists`.
* Do not include a schema reference, such as `public`, in table names. Implementations may restore the DHIS 2 database in a schema other than `public`.

## Example

The following shows an example of a proper table definition.

```sql
-- Table definition

create table if not exists indicatortype (
    indicatortypeid int8 not null,
    name varchar(230) not null,
    indicatorfactor int8 not null,
    indicatornumber bool null,
    uid varchar(11) null,
    code varchar(50) null,
    lastupdated timestamp null,
    created timestamp null,
    lastupdatedby int8 null,
    translations jsonb null,
    constraint indicatortype_code_key unique (code),
    constraint indicatortype_name_key unique (name),
    constraint indicatortype_pkey primary key (indicatortypeid),
    constraint indicatortype_uid_key unique (uid),
    constraint fk_lastupdateby_userid foreign key (lastupdatedby) references userinfo(userinfoid)
);

```

