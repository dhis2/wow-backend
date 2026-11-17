# Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

**Jira**: [full link to the Jira]

## Problem
1-3 sentences on what is slow, linking it to key place or entry point in the code

## Solution
1-3 sentences summarizing the change and the result

## Data/proof it works
1-3 sentences or a small table with the most important performance metrics/numbers, totals etc.
Keep it compressed and compact, only the most important numbers.



# Example 1 (based on dhis2/dhis2-core#26191)

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-22457

## Problem
`/api/tracker/relationships?trackedEntity=` finds relationships with `exists (from item) or exists (to item)`.
Postgres cannot use an index for this `or`, so it reads all relationships in the database.
On Perf Land MNCH, the p95 of one lookup is 29 ms.

## Solution
The query starts from the items of the entity and joins their relationships.
Postgres uses the unique indexes on `from_relationshipitemid` and `to_relationshipitemid`.
The p95 of the two relationship requests goes down by 62% and 72%.

## Data/proof it works
Gatling load test on Perf Land MNCH, p95:

| Request | Before | After |
|---|---:|---:|
| Relationships of a tracked entity | 29 ms | 11 ms |
| Relationships of an event | 18 ms | 5 ms |

The other requests stay within 8 ms of the baseline.


# Example 2 (based on dhis2/dhis2-core#26257)

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-22494

## Problem
Predictor runs become quadratically slower with the number of org units that have data.
`PredictionDataConsolidator.orgUnitsRemaining` is an `ArrayDeque`, and its `remove(Object)` is linear.
One large predictor run takes 50.8 s.

## Solution
Change it to a `LinkedHashSet`.
The iteration order stays the same, and removal takes constant time.
The run time goes from 50.8 s to 28.4 s.

## Data/proof it works
A Yearly predictor on a copy of a national database: 265,734 org units, 188,211 predictions.
`PredictionDataConsolidator.getData` goes from about 21 s to 1.5 s.

AI Assisted


# Example 3 (based on dhis2/dhis2-core#25983)

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-22125

## Problem
A data value export with `limit`/`offset` and no `order` sorts by `pe.startdate, pe.enddate, dv.created, deid`.
The sort costs time on large exports.
It also does not make pages stable, because it is not a total order.
In one export, 306k of 875k rows had the same sort key as another row.

## Solution
Without an explicit `order`, the export has no `ORDER BY`.
A client that needs stable pages must set `order`.

## Data/proof it works
We exported 875,623 rows with `limit=25000`, idle and with 3 concurrent exports.
Each run returned each row exactly one time, in the same order.
Postgres used the same plan at offsets 0, 425k and 850k.
Not checked: parallel plans and writes during paging.

AI Assisted
