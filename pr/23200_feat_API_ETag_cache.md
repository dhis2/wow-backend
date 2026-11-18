# PR 23200: API ETag cache

Author: Morten Svanæs

- Code PR: dhis2/dhis2-core#23200, `feat: API ETag cache`
- Jira: https://dhis2.atlassian.net/browse/DHIS2-20736
- This document describes the PR at head `b8841d5fa82d` (2026-11-19).

Source: the PR body before the 2026-11-19 rewrite.
Statements about test runs and measurements come from that body.
This document did not run them again.

## Summary

The PR adds conditional caching (`ETag`, `If-None-Match`, `304 Not Modified`) to the read-only API.
Database writes drive it:

- A JDBC-level DML observer watches INSERT, UPDATE and DELETE statements.
  It bumps a version counter per entity type when the transaction commits.
- A Spring MVC interceptor turns those counters into per-user ETags for the endpoints that it covers.
  It answers a matching `If-None-Match` with 304 **before the controller runs**.
- `ETagFilter` on `/api/*` keeps those smart ETags.
  It gives every other GET a body-hash ETag, as the shallow ETag filter of master did.

The version counters live in memory.
No external store is needed.

## When it is on, and when it is forced off

`cache.api.etag.enabled` defaults to `on`.
At startup, the server **forces off** the smart tier and the DML observer when the install looks multi-node.
Process-local counters cannot invalidate peers.
An install looks multi-node when it has one of these:

- DHIS2 clustering: `cluster.members` and `cluster.hostname`.
- Redis cache invalidation: `redis.cache.invalidation.enabled=on`.

`ETagCacheActivation` makes this decision and logs a WARN.
Those installs get the body-hash ETag of `ETagFilter` on every eligible GET.
Installs with the cache switched off get the same.
This is exactly how master behaves today.
Multi-node smart ETags are out of scope.
A follow-up is planned.

## ETagFilter: two tiers

`ETagFilter` (bean `etagFilter`, a `ShallowEtagHeaderFilter`) is mapped to `/api/*` in `DhisWebApiWebAppInitializer`.
It has two tiers:

1. **Smart ETag.** This tier applies when the interceptor covers a request.
   The response gets the version-based ETag before the body is written.
   Spring then streams the body without buffering and keeps that ETag.
   A smart 304 has no body and skips the controller.
2. **Body-hash fallback.** Every other GET that answers 2xx without `no-store` gets an MD5 ETag of its body (`"0<md5>"`).
   A match gets a 304.
   This tier covers:
   - endpoints that the interceptor does not map;
   - deep `fields=` requests;
   - controllers that write the body themselves;
   - every request while the smart tier is off.

The exclusions of master do not change.
These paths skip buffering entirely:

- `dataValueSets`, `dataValues`, `fileResources`, `dataEntry/metadata`;
- tracker event and tracked-entity `file|image`;
- `metadata/version/{v}/data(.gz)`.

## Smart ETags

### Coverage

`ETagConditionalInterceptor` resolves a GET or HEAD path in three ways:

- Schema-derived metadata endpoints.
  The dependencies are the type and its direct references.
  `UserGroup` is a dependency when the type is shareable.
  `Attribute` is a dependency when the type has attribute values.
  Only three paths of a metadata resource get the smart ETag:
  list (`/<resource>`), object (`/<resource>/{uid}`) and property (`/<resource>/{uid}/{property}`).
  Custom sub-endpoints such as `/{uid}/generate`, `/{uid}/data` or `/{uid}/form` get the body hash of `ETagFilter`.
  Their data is not in the dependency set of the resource.
- Composite endpoints with hand-picked dependencies:
  `/me*`, `/systemSettings`, `/userSettings`, `/dimensions`, `/dataStatistics`, `/dataStore/**`, `/userDataStore/**`.
- Named-key endpoints: `/apps`, `/staticContent`, `/schemas`, `/locales`, `/periodTypes`.

Requests whose `fields=` crosses two or more reference hops skip the smart tier (`ETagFieldsHopAnalyzer`).

`/loginConfig` is outside the security chain.
Thus no request to it has a user.
It gets the body-hash ETag, for the anonymous login page and for logged-in callers.

### ETag inputs

`ETagConditionalService` builds the ETag as a SHA-256 hash of:

- the user UID;
- the UI locale and the DB locale of the user;
- the build revision;
- the TTL time window;
- the all-cache version;
- the version of each dependency type and named key;
- the request path, the query string and the `Accept` header.

The all-cache version starts at a random value in every process.
Thus an ETag from before a restart never matches after it.

Headers on 2xx responses:

- `Cache-Control: max-age=0, private`, plus `stale-while-revalidate=<n>` when configured;
- `Vary: Accept, Cookie, Authorization`.

### Dependencies worth knowing

- Every `/me*` endpoint depends on `User`.
  Role, group and org unit assignments write join tables.
  Each join table bumps the owners of the collections stored in it.
- The observer sees `jobconfiguration` writes.
  Thus `/api/jobConfigurations` shows new jobs and status changes.
- The login write (`lastLogin`) has a `/* dml-skip */` marker.
  It does not bump `User`.

### Gist lists

The Gist bridge serves some schema-driven metadata lists.
These lists keep the smart ETag and a cacheable `Cache-Control`.
Gist sets `no-store` only when the response has no ETag.

### Manual invalidation

`PUT /api/maintenance/etagCacheClear` bumps the all-cache version.

## DML observer

- `DmlObserverListener` is a datasource-proxy listener on the primary `DataSource`.
  The server registers it only when the smart tier is on.
  - It batches events per connection.
    It deduplicates them per table and operation.
  - On commit (or close), the listener bumps each observed type once.
    Rollback discards the batch.
    Auto-commit statements bump immediately.
  - A connection can write and then show no commit, rollback or close.
    After 5 minutes without a write, a sweep publishes the batch of that connection.
    The sweep bumps the types of the batch instead of dropping them.
- `DmlSqlParser` is a small tokenizer that reads the operation and the table name.
  Writes that it cannot parse bump nothing.
  Examples: `WITH … DELETE`, or statements with leading whitespace.
  `UnmatchedDmlLog` logs them at WARN, at most once a minute, with the number suppressed in between.
- `HibernateTableEntityRegistry` maps entity tables to their class.
  It maps collection (join) tables to the owners of the collections stored in them.
- `DmlObserverExclusions` skips bookkeeping tables and high-volume data tables:
  `audit`, `flyway_schema_history`, `hibernate_sequence`, `spring_session*`, `icon`, messaging join tables, `datavalue`, `trackedentityattributevalue`, `trackerevent`, `singleevent`, `enrollment`.
- Observed types are every `MetadataObject`, plus the types marked `ETagObserved`:
  - `Configuration`, `FileResource`, `UserSetting`;
  - `DatastoreEntry`, `UserDatastoreEntry`;
  - `DataStatistics`, `DataStatisticsEvent`, `SystemSetting`.

  The rule is `ETagService.isObservedType`.

## Classes

| Module | Classes |
|---|---|
| dhis-api | `ETagService`, `ETagObserved`, `DmlEvent`, `DmlOperation`, `DmlETagMetrics` |
| dhis-support-external | `ETagCacheActivation`, `ETagCacheEnabledCondition`, `ETagCacheDisabledCondition`, config keys |
| dhis-support-cache-invalidation | `ETagLocalService`, `ETagNoOpService` |
| dhis-support-hibernate | `DmlObserverConfig`, `DmlObserverListener`, `DmlSqlParser`, `UnmatchedDmlLog`, `DmlObserverExclusions`, `HibernateTableEntityRegistry`, `DataSourceConfig` (wiring) |
| dhis-web-api | `ETagFilter`, `ETagConditionalInterceptor`, `ETagConditionalResponseBodyAdvice`, `ETagConditionalService`, `ETagFieldsHopAnalyzer`; small changes in `AbstractFullReadOnlyController`, `AbstractGistReadOnlyController`, `UserContextInterceptor`, `MeController`, `SystemSettingsController`, `MaintenanceController`, `DhisWebApiWebAppInitializer` |

`UserContextInterceptor` now clears the thread-bound user settings in `afterCompletion`.
That callback also runs when a later interceptor answers with 304, or when the handler throws.

## Configuration

| Key | Default | Description |
|---|---|---|
| `cache.api.etag.enabled` | `on` | Smart tier and DML observer. Forced off on multi-node installs (see above). |
| `cache.api.etag.ttl.minutes` | `10` | TTL window. Smart ETags change at least this often. This is a safety net for writes that the observer cannot see. |
| `cache.api.etag.stale.seconds` | `0` | `stale-while-revalidate` grace in seconds. With `0` (default), browsers revalidate before they show a cached response. |
| `monitoring.cache.etag.enabled` | `off` | The Micrometer metrics below. |

Metrics (from `DmlETagMetrics`):

- `dhis2_dml_observer_statements_total{result}`, `dhis2_dml_observer_batches_published_total`, `..._discarded_total`, `..._stale_sweeps_total`, `dhis2_dml_observer_batch_size`, `dhis2_dml_observer_pending_batches`;
- `dhis2_etag_version_bumps_total{entity_type}`, `dhis2_etag_cache_requests_total{result=hit|miss|skip|skip_deep_fields}`, `dhis2_etag_cache_endpoint_type_total{endpoint_type}`, `dhis2_etag_entity_versions_size`, `dhis2_etag_named_versions_size`.

## Release note

The servlet filter `excludableShallowEtagHeaderFilter` is removed.
`ETagFilter` (bean `etagFilter`, mapped to `/api/*`) replaces it, with the same exclusions.
Where the ETag cache covers an endpoint, `ETagFilter` keeps the smart, version-based API ETag.
Everywhere else, it falls back to the body-MD5 ETag.
This includes clustered installs and `redis.cache.invalidation.enabled` installs, where the ETag cache is forced off.

## Known limits

- Schema-driven metadata endpoints do not depend on `User`.
  A role change does not change their ETags until the TTL window ends.
- The observer cannot see some writes: external SQL, or a second application instance on the same database.
  The TTL window picks up these writes.

## How the behaviour is proven

Results, as the PR body before the 2026-11-19 rewrite reports them.

### Unit tests

All unit tests passed, with these counts per module:

- dhis-api: 1696 (`ETagServiceObservedTypeTest`)
- dhis-support-external: 39 (`ETagCacheActivationTest`, `ETagCacheConditionInverseTest`, `ClusterEnabledConfigMatrixTest`)
- dhis-support-hibernate: 244 (`DmlSqlParserTest`, `DmlObserverListenerTest`, `DmlObserverListenerConcurrencyTest`, `DmlObserverListenerConnectionIdTest`, `DmlObserverListenerGaugeTest`, `DmlObserverExclusionsTest`, `HibernateTableEntityRegistryTest`, `HibernateTableEntityRegistryFailureTest`, `UnmatchedDmlLogTest`)
- dhis-support-cache-invalidation: 28 (`ETagLocalServiceConcurrencyTest`, `ETagLocalServiceCardinalityTest`, `ETagLocalServiceDefaultsTest`, `ETagLocalServiceGaugeTest`, `ETagLocalServiceRestartTest`)
- dhis-service-core: 1097, 2 skipped (`DefaultAppManagerTest`)
- dhis-service-setting: 30
- dhis-web-api: 1112, 2 skipped (`ETagFilterTest`, `ETagFilterTiersTest`, `ETagConditionalInterceptorTest`, `ETagConditionalResponseBodyAdviceTest`, `ETagConditionalServiceTest`, `ETagCompositeIterationOrderTest`, `ETagTtlWindowFlipTest`, `ETagFieldsHopAnalyzerTest`, `GistLazyOutputStreamTest`, `UserContextInterceptorTest`)

### Integration tests

- H2 web-api, targeted set: 1056 run, 1 error, 4 skipped.
  The set covers tracker export, `/me`, users, user groups, settings, maintenance, apps, schemas, Gist, datastore and job configurations.
- The error is `AppControllerTest.testInstalledAppReturnsShortcuts`.
  It fails the same way on master when the class runs alone, because it depends on test order.
- Postgres (run on an earlier revision of this branch): `UserLastLoginTest` and `UserServiceTest` passed.

### End-to-end tests

These ran against a live server started with `cache.api.etag.enabled=on`:

- Cache suite (`dhis-test-e2e`, tag `cache`): 122 of 122 passed.
  - Classes: `MetadataEndpointCacheTest`, `CompositeEndpointCacheTest`, `MeEndpointCacheTest`, `MultiUserCacheIsolationTest`, `DeepFieldsCacheTest`, `NoCacheEndpointTest`.
  - `NoCacheEndpointTest` includes the body-hash fallback class and an anonymous `/loginConfig` probe.
- Smoke script: 26 OK, 1 expected mismatch.
  The mismatch is an absent user-datastore fixture on an empty database.
  The script is `scripts/etag-cache-smoke.sh`, with the manifest `src/test/resources/cache/cache-routes.csv`.
  The manifest classes are cached, shallow, uncached and suspect.
- Parity with master (run on an earlier revision of this branch): the run probed 24 API endpoints on master and on this branch.
  It probed each endpoint with GET and then with `If-None-Match`.
  No endpoint that has an ETag on master lacks one on this branch.
- Benchmark smoke on an empty database (`dhis-test-performance`, run on an earlier revision of this branch):
  - page-load simulation: the 304 share was 61.5% of cacheable responses;
  - mutation staleness: 120 of 120 mutations invalidated on the first conditional probe.

### How to run

```
cd dhis-2/dhis-test-e2e
mvn -Pcache test -Dinstance.url=http://localhost:8080/api

dhis-2/dhis-test-e2e/scripts/etag-cache-smoke.sh \
  --base-url http://localhost:8080/api --username admin --password district
```

## Out of scope

- Multi-node smart ETags: version propagation between nodes.
  With it, the force-off on clustered and Redis-invalidation installs can be lifted.
  A follow-up is planned.
- Moving hand-rolled ETag endpoints onto this mechanism: `/api/dataEntry/metadata`, tracker file endpoints, app static content.
