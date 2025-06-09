# Shadow CTE Optimization for Enrollment Analytics

## Problem Definition

Enrollment-based analytics requests that reference complex Program Indicators and use pagination may generate SQL queries with poor performance characteristics on large datasets. The core issue occurs when multiple Common Table Expressions (CTEs) are generated for program indicators, each scanning entire analytics tables before pagination (`LIMIT/OFFSET`) is applied at the final query level.

This results in processing a larger set of records across multiple CTEs only to return a small subset (e.g., 101 records) in the final result, leading to increased execution times.

Let's examine a typical enrollment query that references a program indicator with the expression:

```
((firstNonNull(A{B6TnnFMgmCk}, A{B6TnnFMgmCk}) + greatest(V{zero_pos_value_count}) * A{B6TnnFMgmCk} + 10)) - d2:countIfCondition(#{hYyB7FUS5eR.JINgGHgqzSN}, '>0') + d2:zing(V{value_count}) + d2:oizp(A{B6TnnFMgmCk})
```

This expression generates the following SQL query structure:

```sql
WITH ynzln AS (
    SELECT enrollment, "a3kGcGDCuk6" AS value,
           ROW_NUMBER() OVER (PARTITION BY enrollment ORDER BY "occurreddate" DESC) AS rn
    FROM analytics_event_IpHINAT79UW
    WHERE "a3kGcGDCuk6" IS NOT NULL AND ps = 'A03MvHHogjR'
      AND "enrollmentdate" >= '2015-01-01' AND "enrollmentdate" < '2025-01-01'
),
klrwf AS (
    SELECT enrollment, "UXz7xuGCEhU" AS value,
           ROW_NUMBER() OVER (PARTITION BY enrollment ORDER BY "occurreddate" DESC) AS rn
    FROM analytics_event_IpHINAT79UW
    WHERE "UXz7xuGCEhU" IS NOT NULL AND ps = 'A03MvHHogjR'
      AND "enrollmentdate" >= '2015-01-01' AND "enrollmentdate" < '2025-01-01'
),
-- ... 5 more similar CTEs scanning the full event table
qZOBw051LSf AS (
    SELECT subax.enrollment,
           SUM(complex_expression_referencing_all_ctes) AS value
    FROM analytics_enrollment_iphinat79uw AS subax
    LEFT JOIN ynzln ON ynzln.enrollment = subax.enrollment AND ynzln.rn = 1
    LEFT JOIN klrwf ON klrwf.enrollment = subax.enrollment AND klrwf.rn = 1
    -- ... joins to all other CTEs
    WHERE complex_enrollment_level_conditions
    GROUP BY subax.enrollment
)
SELECT ax.enrollment, ax.trackedentity, /* ... other columns */,
       coalesce(rzhjt.value, 0) AS qZOBw051LSf
FROM analytics_enrollment_iphinat79uw AS ax
LEFT JOIN qZOBw051LSf rzhjt ON rzhjt.enrollment = ax.enrollment
WHERE enrollment_filters
ORDER BY "lastupdated" DESC NULLS LAST
LIMIT 101 OFFSET 0  -- Pagination applied AFTER all CTEs have processed millions of rows
```

### Performance Problem

Each of the individual CTEs (`ynzln`, `klrwf`, `hlyst`, `dphzo`, `mdjsb`, `vlbjm`, `rkmfo`, `yiijt`) scans the entire `analytics_event_IpHINAT79UW` table independently, processing (potentially millions) of events across all enrollments, even though the final result only needs data for 101 enrollments.

For example:

- **ynzln CTE**: Scans 2M events → processes all → returns data for 500K enrollments
- **klrwf CTE**: Scans 2M events → processes all → returns data for 500K enrollments
- **Final query**: Joins all CTE results → applies pagination → returns 101 enrollments

This results in approximately 14M+ unnecessary row operations for a query that should only process data related to 101 enrollments.

## Goal

Implement a Shadow CTE optimization strategy that applies pagination early in the query execution pipeline, dramatically reducing the dataset size before expensive program indicator CTE operations are performed, while maintaining identical query results and full compatibility with existing analytics logic.

### Shadow CTE Strategy

The Shadow CTE optimization introduces a three-phase approach that reorders query execution to prioritize data reduction:

1. **Early Pagination Phase**: Create a `top_enrollments` CTE that applies all enrollment-level filters, sorting, and pagination to select only the target enrollments
2. **Table Masking Phase**: Generate shadow CTEs with identical names to the real analytics tables, but referencing only the filtered data
3. **Transparent Processing Phase**: Allow existing program indicator CTEs to operate on the masked tables without any code modification

## Implementation Architecture

### Phase 1: Top Enrollments CTE

```sql
WITH top_enrollments AS (
    SELECT ax.enrollment, ax.trackedentity, ax.enrollmentdate, /* all needed columns */
    FROM analytics_enrollment_iphinat79uw AS ax
    WHERE enrollment_filters AND org_unit_filters AND date_filters
    ORDER BY "lastupdated" DESC NULLS LAST
    LIMIT 101 OFFSET 0  -- Pagination applied early!
)
```

## Implementation Architecture

### Phase 1: Top Enrollments CTE

The `top_enrollments` CTE introduces a new **pagination-first CTE type** that fundamentally reorders query execution by applying **enrollment-level** filtering and pagination before any Program Indicator processing.

```sql
WITH top_enrollments AS (
    SELECT
        ax.enrollment,                    -- Primary key for joins
        ax.trackedentity,                -- Standard enrollment columns
        ax.enrollmentdate,
        ax.occurreddate,
        /* ... other standard columns ... */
        ST_AsGeoJSON(enrollmentgeometry) AS enrollmentgeometry_geojson,  -- Aliased formulas
        ax."B6TnnFMgmCk"                 -- Program indicator dependencies
    FROM analytics_enrollment_iphinat79uw AS ax
    WHERE enrollment_filters AND org_unit_filters AND date_filters
    ORDER BY "lastupdated" DESC NULLS LAST
    LIMIT 101 OFFSET 0  -- Pagination applied early!
)
```

**Key Characteristics:**

- **Complete column coverage**: Includes all standard enrollment columns plus dynamically detected program indicator dependencies
- **Formula aliasing**: Functions like `ST_AsGeoJSON()` are aliased to enable proper column referencing
- **Early pagination**: Transforms query execution from `process-then-paginate` to `paginate-then-process`

### Phase 2: Shadow Table CTEs

Phase 2 introduces **table masking CTEs** - CTEs with identical names to real analytics tables but containing only filtered data.

#### Shadow Enrollment Table CTE

```sql
analytics_enrollment_iphinat79uw AS (
    SELECT * FROM top_enrollments
)
```

This **enrollment masking CTE** creates a complete replacement for the enrollment table containing only the target enrollments (for instance 101 rows instead of thousands).

#### Shadow Event Table CTE

```sql
analytics_event_IpHINAT79UW AS (
    SELECT ae.*
    FROM analytics_event_IpHINAT79UW ae  -- References real table
    INNER JOIN top_enrollments te ON te.enrollment = ae.enrollment
    WHERE (
        -- Aggregated conditions from all program indicator CTEs
        (ae."a3kGcGDCuk6" IS NOT NULL AND ae.ps = 'A03MvHHogjR') OR
        (ae."UXz7xuGCEhU" IS NOT NULL AND ae.ps = 'A03MvHHogjR') OR
        (ae."GQY2lXrypjO" IS NOT NULL AND ae.ps = 'ZzYYXq4fJie') OR
        /* ... other program indicator conditions ... */
    ) AND ae."enrollmentdate" >= '2015-01-01'
      AND ae."enrollmentdate" < '2025-01-01'
)
```

This **event masking CTE** implements a pre-filtering strategy by:

- **Enrollment filtering**: Only includes events for the target 101 enrollments
- **Program indicator analysis**: Only includes events that could contribute to any program indicator CTE
- **Compound optimization**: Reduces 2M events to typically 500-1000 events

### Phase 3: Transparent CTE Processing

Phase 3 leverages **SQL table name resolution precedence** where CTE names automatically mask physical table names, enabling existing program indicator CTEs to operate transparently on optimized datasets.

#### Automatic Table Reference Resolution

Existing program indicator CTEs **automatically reference** shadow tables:

```sql
-- Variable CTE - automatically uses shadow event table
mdjsb AS (
    SELECT enrollment, "created" as value,
           ROW_NUMBER() OVER (PARTITION BY enrollment ORDER BY occurreddate DESC) as rn
    FROM analytics_event_IpHINAT79UW  -- Resolves to shadow CTE (~500 rows)
    WHERE "created" IS NOT NULL
)

-- Program stage CTE - automatically uses shadow event table
ynzln AS (
    SELECT enrollment, "a3kGcGDCuk6" AS value,
           ROW_NUMBER() OVER (PARTITION BY enrollment ORDER BY "occurreddate" DESC) AS rn
    FROM analytics_event_IpHINAT79UW  -- Resolves to shadow CTE (~500 rows)
    WHERE "a3kGcGDCuk6" IS NOT NULL AND ps = 'A03MvHHogjR'
)

-- D2 function CTE - automatically uses shadow event table
vlbjm AS (
    SELECT enrollment, COUNT("GQY2lXrypjO") as value
    FROM analytics_event_IpHINAT79UW  -- Resolves to shadow CTE (~500 rows)
    WHERE ps = 'ZzYYXq4fJie' AND "GQY2lXrypjO" IS NOT NULL AND "GQY2lXrypjO" = 10.0
    GROUP BY enrollment
)
```

#### Performance Transformation

The shadow CTE architecture creates a **cascading optimization effect**:

- **Before**: Each CTE processes 2M events across 500K enrollments
- **After**: Each CTE processes ~500 events across 101 enrollments
- **Result**: 99.97% reduction in row operations while maintaining identical query semantics

The three CTE types work together to transform enrollment analytics from a **scan-then-filter** pattern to a **filter-then-scan** pattern, achieving dramatic performance improvements with zero functional changes to existing program indicator logic.

#### Maintaining Query Semantics

The goal of this approachis for the shadow CTE to maintain identical query semantics because:

- **Row number calculations** remain consistent (ordering within enrollment partitions unchanged)
- **Aggregation results** are identical (same enrollments processed, just fewer irrelevant rows excluded earlier)
- **Join conditions** remain unchanged (enrollment-based joins work identically)
- **WHERE clause logic** is preserved (same filters applied, just at different query levels)

The optimization represents a **significant performance enhancement** with zero functional impact on query results, making it safe to apply transparently across all compatible enrollment analytics queries.

## Performance Impact

### Before Optimization

- **ynzln CTE**: Processes ~2M events for all enrollments
- **klrwf CTE**: Processes ~2M events for all enrollments
- **7 more CTEs**: Each processes millions of rows
- **Total operations**: ~14M+ row operations
- **Query time**: 30+ seconds

### After Optimization

- **top_enrollments**: Processes enrollment table once, returns 101 enrollments
- **Shadow event CTE**: Pre-filters to ~500 events (only for target enrollments)
- **ynzln CTE**: Processes ~500 events instead of 2M
- **klrwf CTE**: Processes ~500 events instead of 2M
- **7 more CTEs**: Each processes ~500 events instead of millions
- **Total operations**: ~4K row operations (99.97% reduction)
- **Query time**: <1 second (700x improvement)

## Example Transformation

### Original Query Structure

```sql
WITH program_indicator_cte AS (
    SELECT /* complex aggregation across millions of rows */
    FROM full_analytics_tables
    WHERE /* processes all data */
)
SELECT /* final columns */
FROM analytics_enrollment_table
LEFT JOIN program_indicator_cte USING (enrollment)
WHERE /* enrollment filters */
LIMIT 101  -- Applied after all processing
```

### Optimized Query Structure

```sql
WITH top_enrollments AS (
    SELECT /* needed columns */
    FROM analytics_enrollment_table
    WHERE /* enrollment filters */
    LIMIT 101  -- Applied first!
),
analytics_enrollment_table AS (SELECT * FROM top_enrollments),
analytics_event_table AS (
    SELECT ae.* FROM real_analytics_event_table ae
    JOIN top_enrollments te USING (enrollment)
),
program_indicator_cte AS (
    SELECT /* same complex aggregation, but only across filtered data */
    FROM analytics_event_table  -- Now shadow CTE with minimal data
    WHERE /* same conditions */
)
SELECT /* final columns */
FROM top_enrollments  -- Use shadow CTE as base
LEFT JOIN program_indicator_cte USING (enrollment)
```

## Compatibility and Scope

- **Backward Compatibility**: 100% - existing CTE logic remains unchanged
- **Query Result Accuracy**: Identical results to non-optimized queries
- **Scope**: Non-aggregated enrollment analytics queries with pagination that reference program indicators
- **Transparency**: Optimization is completely invisible to existing program indicator and analytics logic
- **Database Support**: Compatible with PostgreSQL, Apache Doris, and ClickHouse
