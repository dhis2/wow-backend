# DHIS2 Monitoring

## General monitoring infrastructure

The DHIS2 monitoring infrastructure is designed to expose metrics related to the application runtime and other application-related information.
Infrastucture related metrics (such as host metrics, Tomcat or Postgres) are not directly exposed by the application monitoring engine and they have to be collected separately.

The DHIS2 monitoring infrastructure is designed to work with Prometheus (https://prometheus.io/). Prometheus is, at its core, a time-series database that scrapes metrics from HTTP endpoints.
A time series is a stream of timestamped values that belong to the same metric and the same labels. The labels cause the metrics to be multi-dimensional.
Prometheus pulls data from a number of targets (as opposed to a push-based monitoring infrastructure). Prometheus is not an event-based system and this is very different from other time series databases. Prometheus is not designed to catch individual and punctual events in time (such as a service outage for example) but it is designed to **gather pre-aggregated metrics about one or more services**.

## DHIS2 application monitoring

DHIS2 exposes a series of metrics which can be scraped by Prometheus.
Currently, the metrics exposed by the application are:

- DHIS2 API (response time, number of calls, etc.)
- JVM (Heap size, Garbage collection, etc.)
- Hibernate (Queries, cache, etc)
- C3P0 Database pool
- Application uptime
- CPU

Metrics are exported by micrometer.io (http://micrometer.io/). Micrometer is a Java based framework that acts as a facade over the instrumentation clients for the most popular monitoring systems. It supports many monitoring engines, including Prometheus.

The complete set of metrics is available from the following API endpoint:

```
/api/metrics
```

### API Monitoring

API monitoring works by intercepting incoming HTTP requests and records metrics about Spring MVC execution time and results.

The following metrics are exposed for each API endpoint exposed by DHIS2 (`/api/*`).


| name            | type    | description                                                                               |
|-----------------|---------|-------------------------------------------------------------------------------------------|
| `seconds_max`   | gauge   | a moving window of the maximum recorded value in a client-side configurable interval      |
| `seconds_count` | summary | the number of times the API has been called                                               |
| `seconds_sum`   | summary | the accumulated duration of the API call                                                  |

Each metric exposes is additionally disaggregated by the following tags:

| tag name    | description                                                                                                                                                               |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `method`    | the HTTP method (for example, `GET` or `PUT`)                                                                                                                             |
| `status`    | the numeric HTTP status code (for example, `200`, `201`, `500`)                                                                                                           |
| `uri`       | the URI template prior to variable substitution (for example, `/api/analytics/`)                                                                                          |
| `exception` | the simple name of the exception class thrown (only if an exception is thrown)                                                                                            |
| `outcome`   | request’s outcome based on the status code of the response. `1xx` is INFORMATIONAL, `2xx` is SUCCESS, `3xx` is REDIRECTION, `4xx` CLIENT_ERROR, and `5xx` is SERVER_ERROR |


This is an example of metrics for the `/29/analytics` endpoint:

```
dhis2_seconds_max{exception="None",method="GET",outcome="SUCCESS",status="200",uri="/29/analytics",} 2.715992829
dhis2_seconds_sum{exception="None",method="GET",outcome="SUCCESS",status="200",uri="/29/analytics",} 15.404253163
dhis2_seconds_count{exception="None",method="GET",outcome="SUCCESS",status="200",uri="/29/analytics",} 40.0
```


### JVM Monitoring

JVM Monitoring exposes a set of metrics related to the JVM used by the application.

| name                                 | type    | description                                                                                                 |
|--------------------------------------|---------|-------------------------------------------------------------------------------------------------------------|
| `jvm_memory_used_bytes`              | gauge   | The amount of used memory                                                                                   |
| `jvm_memory_committed_bytes`         | gauge   | The amount of memory in bytes that is committed for the Java virtual machine to use                         |
| `jvm_memory_max_bytes`               | gauge   | The maximum amount of memory in bytes that can be used for memory management                                |
| `jvm_gc_pause_seconds`               | summary | Time spent in GC pause                                                                                      |
| `jvm_gc_pause_seconds_max`           | gauge   | Time spent in GC pause                                                                                      |
| `jvm_gc_max_data_size_bytes`         | gauge   | Max size of old generation memory pool                                                                      |
| `jvm_gc_live_data_size_bytes`        | gauge   | Size of old generation memory pool after a full GC                                                          |
| `jvm_gc_memory_promoted_bytes_total` | counter | Count of positive increases in the size of the old generation memory pool before GC to after GC             |
| `jvm_gc_memory_allocated_bytes`      | counter | Incremented for an increase in the size of the young generation memory pool after one GC to before the next |
| `jvm_classes_loaded_classes`         | gauge   | The number of classes that are currently loaded in the Java virtual machine                                 |
| `jvm_classes_unloaded_classes_total` | counter | The total number of classes unloaded since the Java virtual machine has started execution                   |
| `jvm_threads_states_threads`         | gauge   | The current number of threads having NEW state                                                              |
| `jvm_threads_peak_threads`           | gauge   | The peak live thread count since the Java virtual machine started or peak was reset                         |
| `jvm_threads_live_threads`           | gauge   | The current number of live threads including both daemon and non-daemon threads                             |
| `jvm_threads_daemon_threads`         | gauge   | The current number of live daemon threads                                                                   |
| `jvm_buffer_memory_used_bytes`       | gauge   | An estimate of the memory that the Java virtual machine is using for this buffer pool                       |
| `jvm_buffer_total_capacity_bytes`    | gauge   | An estimate of the total capacity of the buffers in this pool                                               |

### Uptime status monitoring

| name                         | type  | description                                 |
|------------------------------|-------|---------------------------------------------|
| `process_uptime_seconds`     | gauge | The uptime of the Java virtual machine      |
| `process_start_time_seconds` | gauge | Start time of the process since unix epoch. |


### CPU monitoring

| name                         | type  | description                                 |
|------------------------------|-------|---------------------------------------------|
| `system_load_average_1m`     | gauge | The sum of the number of runnable entities queued to available processors and the number of runnable entities running on the available processors averaged over a period of time      |
| `system_cpu_count`           | gauge | The number of processors available to the Java virtual machine |
| `process_cpu_usage`          | gauge | The "recent cpu usage" for the Java Virtual Machine process    |
| `system_cpu_usage`           | gauge | The "recent cpu usage" for the whole system    |


### C3P0 Connection pool monitoring

| name                         | type  | description                                 |
|------------------------------|-------|---------------------------------------------|
| `jdbc_connections_idle`      | gauge | Number of idle connections                  |
| `jdbc_connections_active`    | gauge | Number of active connections                |
| `jdbc_connections_max`       | gauge | Number of max connections available in the pool |
| `jdbc_connections_min`       | gauge | Number of min connections in the pool       |


### Hibernate monitoring

| name                                                | type    | description                                                                                                                                                               |
|-----------------------------------------------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hibernate_sessions_open_total`                     | counter | Sessions opened                                                                                                                                                           |
| `hibernate_sessions_closed_total`                   | counter | Session closed                                                                                                                                                            |
| `hibernate_transactions_total`                      | counter | The number of transactions we know to have been successful                                                                                                                |
| `hibernate_transactions_total`                      | counter | The number of transactions we know to have failed                                                                                                                         |
| `hibernate_optimistic_failures_total`               | counter | The number of `StaleObjectStateExceptions` that have occurred                                                                                                             |
| `hibernate_flushes_total`                           | counter | The global number of flushes executed by sessions (either implicit or explicit)                                                                                           |
| `hibernate_connections_obtained_total`              | counter | Get the global number of connections asked by the sessions (the actual number of connections used may be much smaller depending whether you use a connection pool or not) |
| `hibernate_statements_total`                        | counter | The number of prepared statements that were acquired                                                                                                                      |
| `hibernate_statements_total`                        | counter | The number of prepared statements that were released                                                                                                                      |
| `hibernate_second_level_cache_requests_total`       | counter | The number of cacheable entities/collections successfully retrieved from the cache                                                                                        |
| `hibernate_second_level_cache_requests_total`       | counter | The number of cacheable entities/collections not found in the cache and loaded from the database                                                                          |
| `hibernate_second_level_cache_puts_total`           | counter | The number of cacheable entities/collections put in the cache                                                                                                             |
| `hibernate_entities_deletes_total`                  | counter | The number of entity deletes                                                                                                                                              |
| `hibernate_entities_fetches_total`                  | counter | The number of entity fetches                                                                                                                                              |
| `hibernate_entities_inserts_total`                  | counter | The number of entity inserts                                                                                                                                              |
| `hibernate_entities_loads_total`                    | counter | The number of entity loads                                                                                                                                                |
| `hibernate_entities_updates_total`                  | counter | The number of entity updates                                                                                                                                              |
| `hibernate_collections_deletes_total`               | counter | The number of collection deletes                                                                                                                                          |
| `hibernate_collections_fetches_total`               | counter | The number of collection fetches                                                                                                                                          |
| `hibernate_collections_loads_total`                 | counter | The number of collection loads                                                                                                                                            |
| `hibernate_collections_recreates_total`             | counter | The number of collections recreated                                                                                                                                       |
| `hibernate_collections_updates_total`               | counter | The number of collection updates                                                                                                                                          |
| `hibernate_cache_natural_id_puts_total`             | counter | The number of cacheable naturalId lookups put in cache                                                                                                                    |
| `hibernate_cache_natural_id_requests_total`         | counter | The number of cached naturalId lookups successfully retrieved from cache                                                                                                  |
| `hibernate_cache_natural_id_requests_total`         | counter | The number of cached naturalId lookups not found in cache                                                                                                                 |
| `hibernate_query_natural_id_executions_max_seconds` | gauge   | The maximum query time for naturalId queries executed against the database                                                                                                |
| `hibernate_query_natural_id_executions_total`       | counter | The number of naturalId queries executed against the database                                                                                                             |
| `hibernate_query_executions_total`                  | counter | The number of executed queries                                                                                                                                            |
| `hibernate_query_executions_max_seconds`            | gauge   | The time of the slowest query                                                                                                                                             |

## DHIS2 Monitoring architecture

The monitoring subsytem revolves around the concept of Micrometer *registry*. A `MeterRegistry` collects metrics and exports them in the specified format defined by the chosen monitoring platform. Each supported monitoring system has an implementation of 
`MeterRegistry`. Since DHIS2 supports `Prometheus`, the configuration class `org.hisp.dhis.monitoring.prometheus.config.PrometheusMonitoringConfig` is responsible for configuring and initializing the `PrometheusMeterRegistry`.

DHIS2 exports the metrics described above through `micrometer` exporters, which are configured as Spring `@Configuration` classes.

All the exporters are located in the `dhis-support-system` module, under the `monitoring` package.

The API exporter is configured as a Servlet filter. The  `webMetricsFilter` filter is declared in the `web.xml` file of the `dhis-web-portal` module.

Finally, the `PrometheusScrapeEndpointController` is the controller responsible for exposing the `/api/metrics` endpoint. The controller simply access the `PrometheusMeterRegistry` and renders the metrics using the appropriate Prometheus-friendly format.

## DHIS2 Monitoring configuration

The monitoring subsystem is disabled by default, and can be enabled by defining a set of properties in the `dhis.conf` DHIS 2 configuration file.

Each metrics cluster has to be explicitely enabled in order for the metrics to be exported.
The metrics can be enabled by setting to `true` the following configuration keys:

| key name                       | metrics              |
|--------------------------------|----------------------|
| `monitoring.api.enabled`       | API                  |
| `monitoring.jvm.enabled `      | JVM                  |
| `monitoring.dbpool.enabled`    | Connection Pool      |
| `monitoring.hibernate.enabled` | Hibernate            |
| `monitoring.uptime.enabled`    | Uptime               |
| `monitoring.cpu.enabled`       | CPU                  |

Please note that the Hibernate metrics activates the Hibernate property `hibernate.generate_statistics`.
Hibernate statistics are designed to help debug performance problems and are not supposed to be used on a production environment on a permanent basis.



