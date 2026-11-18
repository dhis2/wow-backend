# Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

**Jira**: [full link to the Jira]

### Problem
1-3 sentences on why the structure must change (duplication, coupling, preparation for later work), linking it to key place or entry point in the code

### Solution
1-3 sentences summarizing the new structure; say that the behaviour stays the same; use bullets for several separate parts

# Example 1 (based on dhis2/dhis2-core#24227)

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-21378

### Problem
`EntityWriteBatch` in the tracker importer has 1767 lines.
It holds the write code for all tracker tables, and `AbstractTrackerPersister` selects the code with `instanceof`.
Each new batched writer must copy about 120 lines.

### Solution
- Split `EntityWriteBatch` into one writer class for each table.
- `EntityWriteBatch` keeps only the staging, `mark`/`rollbackTo` and the flush order.
- Its public API, the SQL, the flush order and the transactions stay the same.


# Example 2 (based on dhis2/dhis2-core#24521)

### Problem
`TrackerEvent` still uses the XML mapping `TrackerEvent.hbm.xml`.
`TrackedEntity` and `Enrollment` already use JPA annotations.

### Solution
- Move the `TrackerEvent` mapping to JPA annotations on `BaseTrackerObject`.
- Table, columns, types and foreign key names stay the same, so the schema does not change.
- `status` uses `@Enumerated(EnumType.STRING)`, and the stored values stay the same.


# Example 3 (based on dhis2/dhis2-core#24541)

Targets #24489. Follows a review comment from Jan.

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-21852

### Problem
The collection filter in `JsonPatchManager.apply()` uses its own Jackson filter.
It builds a mixin and a filter provider on each call.
No other code uses this pattern.

### Solution
- Use the pattern of `FieldFilterService`: a `@JsonFilter` mixin and a `SimpleBeanPropertyFilter`.
- `JsonPatchManager` keeps one `ObjectMapper` copy for each entity type.
- The rule that selects the collections stays the same.

AI Assisted
