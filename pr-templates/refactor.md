## Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

### Problem
1-2 paragraphs on why the structure must change (duplication, coupling, preparation for later work), linking it to key place or entry point in the code

### Solution
1-2 paragraphs summarizing the new structure; say that the behaviour stays the same

**Changes/Caveats/...** (optional bullet list of changes for larger PRs)
* public API of X stays the same
* SQL does not change

1 indicator line on AI disclaimer/use

1 indicator line qualifying test coverage


## Example 1 (based on dhis2/dhis2-core#24227)

### Problem
`EntityWriteBatch` in the tracker importer has 1767 lines.
It holds the write code for all tracker tables, and `AbstractTrackerPersister` selects the code with `instanceof`.
Each new batched writer must copy about 120 lines.

### Solution
Split `EntityWriteBatch` into one writer class for each table.
`EntityWriteBatch` keeps only the staging, `mark`/`rollbackTo` and the flush order.
Its public API stays the same.

**Caveats**
- SQL, column order, flush order and transactions do not change.

Changes made by AI 🤖

Existing tracker import tests pass without changes.


## Example 2 (based on dhis2/dhis2-core#24521)

### Problem
`TrackerEvent` still uses the XML mapping `TrackerEvent.hbm.xml`.
`TrackedEntity` and `Enrollment` already use JPA annotations.

### Solution
Move the `TrackerEvent` mapping to JPA annotations on `BaseTrackerObject`.
Table, columns, types and foreign key names stay the same, so the schema does not change.

**Caveats**
- `status` uses `@Enumerated(EnumType.STRING)`. The stored values stay the same.

Changes made by AI 🤖

Existing tracker tests pass on the new mapping.


## Example 3 (based on dhis2/dhis2-core#24541)

Targets #24489. Follows a review comment from Jan.

### Problem
The collection filter in `JsonPatchManager.apply()` uses its own Jackson filter.
It builds a mixin and a filter provider on each call.
No other code uses this pattern.

### Solution
Use the pattern of `FieldFilterService`: a `@JsonFilter` mixin and a `SimpleBeanPropertyFilter`.
`JsonPatchManager` keeps one `ObjectMapper` copy for each entity type.
The rule that selects the collections stays the same.

Changes made by AI 🤖

Existing JSON Patch tests pass.
