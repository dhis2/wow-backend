# Flyway versioning

This document describes why [Flyway](https://flywaydb.org/) versioning is needed and a list of versions which can be reserved by developers.

## Overview

Flyway requires that a migration has a unique and incremental version. This implies that The DHIS 2 version notation follows this format:

```
V2_<DHIS 2 major version>_<Incrementing number>__<Description>.(sql|java)
```


Flway migrations are applied in order exactly once. Flyway migrations should not be changed after being commited or applied in a way that changes the checksum of the migration, as it will cause the startup process to fail.

When working on multiple pull requests concurrently, there is a chance of those PRs being applied in a way where more than one PR uses the same migration version. To mitigate this problem, DHIS 2 developers should *reserve* a version in this document once a PR which contains a migration is raised.

It is important to take into account:

* The reservation should not be done too early, as it will make it more complex to merge. Make the reservation at the time of raising the PR for review.
* PRs which contain migrations must be merged in the order of the migration versions. This is done so that migrations will be applied in the appropriate, ascending order.

## Reservations

The table below contains a list of potential migration versions. Please reserve the appropriate version using a link to the PR.

### 2.34

| Version | Pull request URL |
| -- | -- |
| V2_34_1 | https://github.com/dhis2/dhis2-core/pull/3829 |
| V2_34_2 | https://github.com/dhis2/dhis2-core/pull/3803 |
| V2_34_3 | https://github.com/dhis2/dhis2-core/pull/3968 |
| V2_34_4 | https://github.com/dhis2/dhis2-core/pull/3929 |
| V2_34_5 | |
| V2_34_6 | |
| V2_34_7 | |
| V2_34_8 | |
| V2_34_9 | |
| V2_34_10 | |
| V2_34_11 | |
| V2_34_12 | |
| V2_34_13 | |
| V2_34_14 | |
| V2_34_15 | |
| V2_34_16 | |
| V2_34_17 | |
| V2_34_18 | |
| V2_34_19 | |
| V2_34_20 | |


### 2.35

| Version | Pull request URL |
| -- | -- |
| V2_34_1 | |
| V2_35_2 | |
| V2_35_3 | |
| V2_35_4 | |
| V2_35_5 | |
| V2_35_6 | |
| V2_35_7 | |
| V2_35_8 | |
| V2_35_9 | |
| V2_35_10 | |
| V2_35_11 | |
| V2_35_12 | |
| V2_35_13 | |
| V2_35_14 | |
| V2_35_15 | |
| V2_35_16 | |
| V2_35_17 | |
| V2_35_18 | |
| V2_35_19 | |
| V2_35_20 | |

### 2.36

| Version | Pull request URL |
| -- | -- |
| V2_36_1 | |
| V2_36_2 | |
| V2_36_3 | |
| V2_36_4 | |
| V2_36_5 | |
| V2_36_6 | |
| V2_36_7 | |
| V2_36_8 | |
| V2_36_9 | |
| V2_36_10 | |
| V2_36_11 | |
| V2_36_12 | |
| V2_36_13 | |
| V2_36_14 | |
| V2_36_15 | |
| V2_36_16 | |
| V2_36_17 | |
| V2_36_18 | |
| V2_36_19 | |
| V2_36_20 | |

### 2.37

| Version | Pull request URL |
| -- | -- |
| V2_37_1 | |
| V2_37_2 | |
| V2_37_3 | |
| V2_37_4 | |
| V2_37_5 | |
| V2_37_6 | |
| V2_37_7 | |
| V2_37_8 | |
| V2_37_9 | |
| V2_37_10 | |
| V2_37_11 | |
| V2_37_12 | |
| V2_37_13 | |
| V2_37_14 | |
| V2_37_15 | |
| V2_37_16 | |
| V2_37_17 | |
| V2_37_18 | |
| V2_37_19 | |
| V2_37_20 | |

