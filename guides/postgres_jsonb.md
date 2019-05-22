# PostgreSQL JSONB

In DHIS 2 version 2.29 we started to utilize the PostgreSQL JSONB data type. In later PostgreSQL versions, the support for JSONB in terms of querying, manipulation and indexing has been increasingly more sophisticated.

This guide aims at providing useful examples and tips for working with JSONB in SQL for DHIS 2.

## Examples

The following section lists examples of JSONB SQL queries.

### Add data value to an event with `jsonb_insert`

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
    "providedElsewhere": false}'::jsonb)
where uid = 'NkvkOpBjkkH';
```
