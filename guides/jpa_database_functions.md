# Using database function in JPA

#### 1. Intro
- PostgreSQL has built-in functions for JSONB data type as described [here](https://www.postgresql.org/docs/9.5/functions-json.html). However they are not supported by JPA Creteria API, or HQL/JPQL. We can only call those JSONB functions in Java by using native SQL queries.  
- One solution is to created a custom database function which uses JSONB operators inside. Then register that function with `PostgisPG95Dialect`. By that, we can call the registered function with JPA Criteria API.
- This solution can be applied to other cases where you just want to call a database function in JPA. 

#### 2. Code example
2.1 Create database function and put it in a flyway script.
```sql
CREATE or replace FUNCTION jsonb_has_user_id(jsonb, text )
RETURNS bool
AS $$
select  $1->'users' ? $2
$$
LANGUAGE SQL IMMUTABLE PARALLEL SAFE;
```

2.2 Register database function in `DhisPostgresDialect`
```java
public class DhisPostgresDialect
    extends PostgisPG95Dialect
{
      public static final String HAS_USER_ID = "jsonb_has_user_id" ;

    public DhisPostgresDialect()
    {
        registerFunction( JsonbFunctions.HAS_USER_ID, new StandardSQLFunction( JsonbFunctions.HAS_USER_ID, StandardBasicTypes.BOOLEAN ) );

    }
}
```
2.3 Call registered database function with JPA `CriteriaBuilder`

```java
builder.function(  
                    JsonbFunctions.HAS_USER_ID, // function name
                    Boolean.class, // return type
                    root.get( "sharing" ), // first argument
                    builder.literal( userUid ) // second argument
                )
```
2.4 Call registered database function with HQL query
```java
String sql = "select dataelement from dataelement where function('jsonb_has_user_id', sharing, 'y2pwrlq0RAa') = true";
```