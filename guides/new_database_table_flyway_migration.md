# New database table Flyway migration

This guide covers how to write a Flyway migration to introduce a new database table for metadata entities. This step is necessary when introducing new persistent entities in DHIS 2. When creating new tables, it is important to ensure data types and constraints are properly defined, and to be consistent with existing tables in the database.

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

* Use `CREATE TABLE IF NOT EXISTS` to create the table, as Flyway migrations should be idempotent, meaning the SQL statement should not crash nor have any effect if invoked more than once.
* Use `int8` instead of `integer` for primary key and foreign key int columns. The 8 byte int data type is more appropriate given that primary keys in many implementations have gone above the 2.1B max value for 4 byte data type.
* Include a primary key constraint on the primary key identifier column.
* Use `timestamp` instead of `timestamp without timezone` for created and last updated columns.
* Use `varchar` instead of `character varying` for limited text columns.
* Use `text` instead of `varchar` for unlimited text columns mapped to `text` in the Hibernate schema definition.
* Include foreign key constraints on all foreign key columns.
* Include unique constrains on unique columns such as `uid`, `code`, `name` and `shortname` (if appropriate).
* Ensure constraints have unique and readable names.
* Use lowercase table and column names. DHIS 2 uses lowercase naming of all database relations. PostgreSQL will use lowercase values for non-quoted values in any case.
* Quote column names with double quotes in case of special or reserved characters. This is optional for names without special or reserved characters but is a healthy approach in any case.
* Use uppercase for all SQL keywords such as `CREATE TABLE IF NOT EXISTS`.
* Do not include a schema reference, such as `public`, in table names. Implementations may restore the DHIS 2 database in a schema other than `public`.

## Example

The following shows an example of a proper table definition.

```sql
-- Table definition

CREATE TABLE IF NOT EXISTS indicatortype (
    indicatortypeid int8 NOT NULL,
    name varchar(230) NOT NULL,
    indicatorfactor int8 NOT NULL,
    indicatornumber bool NULL,
    uid varchar(11) NULL,
    code varchar(50) NULL,
    lastupdated timestamp NULL,
    created timestamp NULL,
    lastupdatedby int8 NULL,
    translations jsonb NULL,
    CONSTRAINT indicatortype_code_key UNIQUE (code),
    CONSTRAINT indicatortype_name_key UNIQUE (name),
    CONSTRAINT indicatortype_pkey PRIMARY KEY (indicatortypeid),
    CONSTRAINT indicatortype_uid_key UNIQUE (uid)
);

-- Constraints

ALTER TABLE indicatortype ADD CONSTRAINT fk_lastupdateby_userid FOREIGN KEY (lastupdatedby) REFERENCES userinfo(userinfoid);
```

