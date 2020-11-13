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

Regarding backports of Flyway migrations, extreme caution must be taken in order to avoid issues. Only critical Flyway migrations should be backported and we should stay on the conservative side. For non-critical clean-ups, SQL scripts can be made available and run manually.

## Reservations

The table below contains a list of migration versions. Please reserve the appropriate version using the migration version and the link to the corresponding PR.

### 2.34

| Version | Pull request URL |
| -- | -- |
| V2_34_1 | https://github.com/dhis2/dhis2-core/pull/3829 |
| V2_34_2 | https://github.com/dhis2/dhis2-core/pull/3803 |
| V2_34_3 | https://github.com/dhis2/dhis2-core/pull/3968 |
| V2_34_4 | https://github.com/dhis2/dhis2-core/pull/3929 |
| V2_34_5 | https://github.com/dhis2/dhis2-core/pull/4387 |
| V2_34_6 | |
| V2_34_7 | https://github.com/dhis2/dhis2-core/pull/4478 |
| V2_34_8 | https://github.com/dhis2/dhis2-core/pull/4411 |
| V2_34_9 | https://github.com/dhis2/dhis2-core/pull/4414 |
| V2_34_10 | https://github.com/dhis2/dhis2-core/pull/4587 |
| V2_34_11 | https://github.com/dhis2/dhis2-core/pull/4661 |
| V2_34_12 | https://github.com/dhis2/dhis2-core/pull/4432 |
| V2_34_13 | https://github.com/dhis2/dhis2-core/pull/4432 |
| V2_34_14 | https://github.com/dhis2/dhis2-core/pull/4627 |
| V2_34_15 | https://github.com/dhis2/dhis2-core/pull/4721 |
| V2_34_16 | https://github.com/dhis2/dhis2-core/pull/4727 |
| V2_34_17 | https://github.com/dhis2/dhis2-core/pull/4696 |
| V2_34_18 | https://github.com/dhis2/dhis2-core/pull/4851 |
| V2_34_19 | https://github.com/dhis2/dhis2-core/pull/4913 |
| V2_34_20 | https://github.com/dhis2/dhis2-core/pull/4963 |
| V2_34_21 | ? |
| V2_34_22 | https://github.com/dhis2/dhis2-core/pull/5836 |
| V2_34_23 | ? |
| V2_34_24 | https://github.com/dhis2/dhis2-core/pull/5949 |
| V2_35_25 | https://github.com/dhis2/dhis2-core/pull/6336 |
| V2_34_26 | DHIS2-9295-1 |
| V2_34_27 | DHIS2-9295-2 |
| V2_34_28 | DHIS2-8911 |


### 2.35

| Version | Pull request URL |
| -- | -- |
| V2_35_1 | https://github.com/dhis2/dhis2-core/pull/5145 |
| V2_35_2 | ? |
| V2_35_3 | ? |
| V2_35_4 | https://github.com/dhis2/dhis2-core/pull/5757 |
| V2_35_5 | https://github.com/dhis2/dhis2-core/pull/5649 |
| V2_35_6 | https://github.com/dhis2/dhis2-core/pull/5766 |
| V2_35_7 | https://github.com/dhis2/dhis2-core/pull/5766 |
| V2_35_8 | https://github.com/dhis2/dhis2-core/pull/5779 |
| V2_35_9 | https://github.com/dhis2/dhis2-core/pull/5784 |
| V2_35_10 | https://github.com/dhis2/dhis2-core/pull/5644 |
| V2_35_11 | https://github.com/dhis2/dhis2-core/pull/5876 |
| V2_35_12 | https://github.com/dhis2/dhis2-core/pull/5885 |
| V2_35_13 | https://github.com/dhis2/dhis2-core/pull/5891 |
| V2_35_14 | ? |
| V2_35_15 | https://github.com/dhis2/dhis2-core/pull/5916 |
| V2_35_16 | https://github.com/dhis2/dhis2-core/pull/5913 |
| V2_35_17 | https://github.com/dhis2/dhis2-core/pull/5820 |
| V2_35_18 | https://github.com/dhis2/dhis2-core/pull/5935 |
| V2_35_19 | https://github.com/dhis2/dhis2-core/pull/5940 |
| V2_35_20 | ? |
| V2_35_21 | https://github.com/dhis2/dhis2-core/pull/6044 |
| V2_35_22 | https://github.com/dhis2/dhis2-core/pull/6154 |
| V2_35_23 | https://github.com/dhis2/dhis2-core/pull/6338 |
| V2_35_24 | DHIS2-9295-1 |
| V2_35_25 | DHIS2-9295-2 |
| V2_35_26 | DHIS2-8911 |



### 2.36

| Version | Pull request URL |
| -- | -- |
| V2_36_1 | https://github.com/dhis2/dhis2-core/pull/6302 |
| V2_36_2 | https://github.com/dhis2/dhis2-core/pull/6302 |
| V2_36_3 | https://github.com/dhis2/dhis2-core/pull/6334 |
| V2_36_4 | DHIS2 - 9295-1 |
| V2_36_5 | DHIS2 - 8411 |
| V2_36_6 | DHIS2 - 9295-2 |
| V2_36_7 | DHIS2 - 1561, DHIS2 - 5587 |
| V2_36_8 | https://github.com/dhis2/dhis2-core/pull/5862 |
| V2_36_9 | https://github.com/dhis2/dhis2-core/pull/5862 |
| V2_36_10 | https://github.com/dhis2/dhis2-core/pull/5862 |
| V2_36_11 | https://github.com/dhis2/dhis2-core/pull/5862 |
| V2_36_12 | DHIS2-8911 |
| V2_36_13 | DHIS2-8096 |
| V2_36_14 | DHIS2-9841 |
| V2_36_ | |
| V2_36_ | |
| V2_36_ | |
| V2_36_ | |
| V2_36_ | |
| V2_36_ | |

### 2.37

| Version | Pull request URL |
| -- | -- |
| V2_37_1 | |
| V2_37_2 | |
| V2_37_3 | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |
| V2_37_ | |

