# Sharing

- This document describes the  technical design and usage of the `Sharing` object in DHIS2.
- For more description about how to use Sharing as a DHIS2 User, please read [this document](https://docs.dhis2.org/en/use/user-guides/dhis-core-version-238/configuring-the-system/about-sharing-of-objects.html).

## What is Sharing in DHIS2
- Sharing in DHIS2 is an access control list (ACL) that specifies which users are granted or denied access to a particular object.

## How to enable Sharing for an entity
- Sharing is stored as a JsonB column in database.

```sql
alter table attribute add column if not exists sharing jsonb default '{}'::jsonb;
```

- We have defined a hibernate custom type `jsbObjectSharing` in `UserTypes.hbm.xml`
- In order to enable sharing for a entity, add this property to the entity hbm mapping file.

```
<property name="sharing" type="jsbObjectSharing"/>
```
- If the entity class extends `BaseIdentifiableObject` then it inherits the `Sharing` object. Otherwise you need to manually add this to the entity.

```java
 protected Sharing sharing = new Sharing();
```

## The format of Sharing JsonB object
- A full Sharing JSON object looks like below

```json
{
    "sharing": {
        "public": "rw------",
        "owner": "GOLswS44mh8",
        "external": false,
        "userGroups": {
            "CHkHCLtw4eX": {
                "id": "CHkHCLtw4eX",
                "access": "rwr-----"
            },
            "umOKHwu9CFL": {
                "id": "umOKHwu9CFL",
                "access": "rwrw----"
            }
        },
        "users": {
            "O2PajOxjJSa": {
                "id": "O2PajOxjJSa",
                "access": "rwrw----"
            },
            "aDy67f9ijOe": {
                "id": "aDy67f9ijOe",
                "access": "rwr-----"
            }
        }
    }
}
```

### The access String
- The basic setting of the `Sharing` object is the access setting which is a `String` with 8 characters.
- Each character can be either `-` ( no access ), `r` ( read access ) or `w` ( write access ).
- The first 2 character is for Metadata access control.
- The 3rd and 4th character is for Data access control.
- The rest are reserved characters for future use.

Example: `'rw------'`

### The Java object class defined as below, notice the `users` and `userGroups` propreties have `Map` type

```java
public class Sharing
{
    private String owner;
    private String publicAccess;
    private boolean external;
    private Map<String, UserAccess> users = new HashMap<>();
    private Map<String, UserGroupAccess> userGroups = new HashMap<>();
}
```
- ***owner***: The User UID of the User who owns of the object, has full access right. When creating a new object, if the owner is not provided then the `createdBy` User will be used.

- ***publicAccess***: give access to all logged users. The rule for generating default `publicAccess` is a combination of `Schema` and authorities settings. For example: if User has authority `F_DATASET_PUBLIC_ADD` and `Schema.defaultPrivate` is `false` then the default `publicAccess` is `rw------`.

- ***external***: if objects are shared externally, then they are visible to anyone who has access to the URL which provides the resource without any login credentials. Also note that "External access" does not give access to logged in users—to give them access, you must also allow `publicAccess`.

- ***users***: give access to specific `User`.

- ***userGroups***: give access to all members of `UserGroup`.

## Medata and Data Sharing
- Sharing in DHIS2 has two layers Metadata and Data sharing, to understand more about those sharing types, please read [this document](https://docs.dhis2.org/en/use/user-guides/dhis-core-version-238/configuring-the-system/about-sharing-of-objects.html).
- By default after adding the `sharing` column to the entity table, that entity class is enabled for Metadata Sharing.
- In order to enable Data sharing, you need to add below code the the schema descriptor of that class.
```java
public class TrackedEntityTypeSchemaDescriptor implements SchemaDescriptor
{
    @Override
    public Schema getSchema()
    {
        Schema schema = new Schema( TrackedEntityType.class, SINGULAR, PLURAL );
        schema.setDataShareable( true );
        ...
```
- The `api/schemas` endpoint can be used to find out which class has sharing enabled.

```json
{
  "klass": "org.hisp.dhis.dataset.DataSet",
  "shareable": true,
  "dataShareable": true,
  ...
}
```
## The query for checking sharing access

### We have defined some custom jsonb queries to simplify the sql query and also improve performance.

  -  `jsonb_has_user_id( sharingColumn, userId )`: return TRUE if given `sharingColumn` has given User UID.
```sql
select  $1->'users' ? $2
```
  -  `jsonb_check_user_access( sharingColumn, userId, accessString )`: return TRUE if given sharingColumn has given User UID with access `like` given `accessString`. 
```sql
select  $1->'users'->$2->>'access' like $3
```
  -  `jsonb_has_user_group_ids( sharingColumn, userGroupIds )`: return TRUE if the given `sharingColumn` contains at least one UserGroup UID from the given UserGroup UID array
```sql
SELECT   $1->'userGroups' ?| $2::text[];
```
  -  `jsonb_check_user_groups_access( sharingColumn, userGroupIds, accessString)`: return TRUE if the given `sharingColumn` contains at least one of UserGroup UID from the given UserGroup UID array and the access of UserGroup `like` given `accessString`.
```sql
SELECT exists(
         SELECT 1
         FROM  jsonb_each($1->'userGroups') je
         WHERE je.key = ANY ($3::text[])
         AND je.value->>'access' LIKE $2
     );
```


- A full SQL query condition for sharing check looks like this

```sql
( de.sharing->>'owner' is null or de.sharing->>'owner' = 'GOLswS44mh8') 

or de.sharing->>'public' like 'r%' or sharing->>'public' is null 

or ( jsonb_has_user_id ( de.sharing, 'GOLswS44mh8') = true 
    and jsonb_check_user_access( de.sharing, 'GOLswS44mh8', 'r%' ) = true ) 

or ( jsonb_has_user_group_ids( de.sharing, 'LbeIlyHEhKr') = true 
    and jsonb_check_user_groups_access ( de.sharing, '%r', 'LbeIlyHEhKr') = true )
```

