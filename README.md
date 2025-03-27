# Backend Team Way of Work

The purpose of this document is to works as a resource for any developer working with the DHIS 2 source code.

## Table of contents

1. Using this document
2. Contributing
3. Guides
3. Coordination

## Using this document

This document is split into multiple files, all written in markdown. There is two ways to navigate the repository:

* Using the file-browser, find the topic you are looking for.
* Using the links from this document, navigate from topic to topic.

## Contributing

Guides are placed in the _/guides_ directory. Start guides with the \# h1 header, then use subsequent header numbering (\## h2, and so on). Coordination pages are placed in the _/coordination_ directory.

## Guides

The following section lists guides on various topics.

**Collaboration**
* [Flyway database migration](guides/flyway_db_migration.md)
* [Component owners](guides/component_owners.md)
* [Git PR & commit messages](guides/git_commit_messages.md)
* [Git pull requests](guides/git_pull_requests.md)

**General Coding**
* [Code Best Practices and Conventions](guides/code-guide.md)
* [OpenAPI](guides/open_api.md)
* [Code formatting](guides/code_formatting.md)

**Running**
* [Embedded Jetty API build](guides/embedded_jetty.md)
* [IDEA and Tomcat setup (includes hot swapping)](guides/idea_tomcat_setup.md)
* [Monitoring](guides/monitoring.md)
* [Ubuntu Linux Android app mirroring](guides/ubuntu_android_app_mirroring.md)

**Testing**
* [API testing](guides/testing/api_testing.md)
* [Spring controller testing](guides/testing/spring_controller_testing.md)
* [Test mocking with Mockito](guides/testing/test_mocking.md)
* [Testing](guides/testing/testing.md)

**Database**
* [JPA and database functions](guides/jpa_database_functions.md)
* [JPA queries](guides/jpa_api.md)
* [New database table Flyway migration](guides/new_database_table_flyway_migration.md)
* [PostgreSQL JSONB](guides/postgres/postgres_jsonb.md)
* [PostgreSQL commands](guides/postgres/postgresql_commands.md)
* [PostgreSQL read replica](guides/postgres/postgres_read_replica.md)

## Coordination

The following section lists various areas of coordination.

* [Flyway versioning](coordination/flyway_versioning.md)

## Developer documentation

The following pages contain high-level developer documentation for various solutions.

* [Job scheduling](docs/job_scheduling.md)
* [Data value set import/export](docs/datavalueset.md)
* [Auditing](guides/auditing.md)

## Talks

The following pages are slides used in talks from Thursday meetings:

* [JSON stream processing](talks/json_stream_processing.md) ([html slides](talks/json_stream_processing.html))
* [PEG parsers](talks/peg_parsers.md) ([html slides](talks/peg_parsers.html))
* [Reflection, generics & type erasure](talks/generics.md) ([html slides](talks/generics.html))
