## Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

### Problem
1-2 paragraphs on what is slow and how slow (one number), linking it to key place or entry point in the code

### Solution
1-2 paragraphs summarizing the change and the result, with numbers before and after

**Changes/Caveats/...** (optional bullet list of changes for larger PRs)
* behaviour stays the same
* not measured: X

1 indicator line on AI disclaimer/use


## Example 1 (based on dhis2/dhis2-core#26191)

### Problem
`/api/tracker/relationships?trackedEntity=` finds relationships with `exists (from item) or exists (to item)`.
Postgres cannot use an index for this `or`, so it reads all relationships in the database.
On Perf Land MNCH (69,548 relationships) one lookup takes about 20 ms.
The time grows with the database, not with the relationships of the entity.

### Solution
The query starts from the items of the entity and joins their relationships.
Postgres uses the unique indexes on `from_relationshipitemid` and `to_relationshipitemid`.

**Caveats**
- The query does not use `relationshipitem.relationshipid`. This column is nullable, and only the importer sets it.

Changes made by AI 🤖


## Example 2 (based on dhis2/dhis2-core#26257)

### Problem
Predictor runs become quadratically slower with the number of org units that have data.
`PredictionDataConsolidator.orgUnitsRemaining` is an `ArrayDeque`, and its `remove(Object)` is linear.

### Solution
Change it to a `LinkedHashSet`.
The iteration order stays the same, and removal takes constant time.
The behaviour does not change.

AI Assisted 🤖


## Example 3 (based on dhis2/dhis2-core#25983)

### Problem
A data value export with `limit`/`offset` and no `order` sorts by `pe.startdate, pe.enddate, dv.created, deid`.
The sort costs time on large exports.
It also does not make pages stable, because it is not a total order.
One bulk import gives many rows the same `created`.

### Solution
Without an explicit `order`, the export has no `ORDER BY`.

**Caveats**
- Not checked: parallel plans and writes during paging.
- A client that needs stable pages must set `order`.

No AI used
