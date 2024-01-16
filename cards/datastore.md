
# Datastore Cheat Sheet

<table width="100%" >
<tr>
<td width="50%" valign="top">

> [!NOTE]
> ### API `/api/dataStore/`
> Query `GET`
> * list namespaces: `/api/dataStore/`
> * list keys: `/api/dataStore/{ns}`
> * list entries: `/api/dataStore/{ns}?fields=...`;
>  [parameters](https://github.com/dhis2/dhis2-core/blob/master/dhis-2/dhis-api/src/main/java/org/hisp/dhis/datastore/DatastoreParams.java):
> `page`, `pageSize`, `paging`, `headless`, `rootJunction`, `order`, `filter`, `fields`*
> * read entry: `api/dataStore/{ns}/{key}`
>
> Create `POST`
> 
> Update `PUT`
> * `/api/dataStore`; parameters: `path`, `roll`
  

> [!TIP]
> ### Good To Know
> * use `fields=.` to extract the root

</td>      
<td width="50%">

> [!TIP]
> ### Ideas
> * this
> * that
> * other

> [!CAUTION]
> ### Pitfalls
> * advanced search requires `fields`

> [!IMPORTANT]
> ### Improvments
> * [x] partial and rolling collection update dhis2/dhis2-core#15881 

</td>
</tr>
</table>


