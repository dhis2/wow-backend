# PostgreSQL JSONB

In DHIS 2 version 2.29 we started to utilize the PostgreSQL `JSONB` data type. In later PostgreSQL versions, the support for JSONB in terms of querying, manipulation and indexing is becoming increasingly more sophisticated.

This guide aims at providing useful examples and tips for working with JSONB in SQL for DHIS 2.

## Examples

The following section lists examples of JSONB SQL queries.

### Add or update data value of an event with `jsonb_set`

```sql
update programstageinstance
set eventdatavalues = jsonb_set(
  eventdatavalues,
  '{"S33cRBsnXPo"}',
  '{
    "value":"SKJoPDgjELa", 
    "storedBy":"admin", 
    "created":"2014-11-15T00:00:00.000", 
    "lastUpdated":"2014-11-15T00:00:00.000", 
    "providedElsewhere": false
  }'::jsonb)
where uid = 'NkvkOpBjkkH';
```

### Get value of specific data element for events

```sql
select psi.eventdatavalues->'qrur9Dvnyt5'->>'value' as "Age in years"
from programstageinstance psi
where psi.programinstanceid = 1150223
and psi.eventdatavalues->'qrur9Dvnyt5' is not null
limit 100;
```

### Delete data value of event for a data element

```sql
update programstageinstance
set eventdatavalues = eventdatavalues - 'S33cRBsnXPo'
where uid = 'NkvkOpBjkkH';
```

## JSON v JSONB
Postgres supports 2 types of JSON usage
- JSON
- JSONB

At the time of writing, we currently only use JSONB in DHIS2.

Here's a table outlining some of the main differences, in order to help make informed decisions.

| Feature        | JSON                               | JSONB                           |
|----------------|------------------------------------|---------------------------------|
| Data storage   | plain string                       | binary                          |
| Write          | usually faster                     | slower due to binary conversion |
| Read           | slower, need to parse whole string | faster                          |
| White spaces   | kept                               | removed                         |
| Key order      | kept                               | not guaranteed                  |
| Partial update | no (full string replaced)          | yes (only key/field updated)    |
| Index support  | no                                 | yes                             |