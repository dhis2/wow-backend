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

The table below contains a list of migration versions. Please reserve the appropriate version using the migration version and the link to the corresponding Jira issue or PR.

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
| V2_34_29 | https://github.com/dhis2/dhis2-core/pull/6917 |
| V2_34_30 | ? |
| V2_34_31 | ? |
| V2_34_32 | DHIS2-10556 |
| V2_34_33 | DHIS2-5587 |
| V2_34_34 | tracker-query-sql performance |
| V2_34_35 | https://github.com/dhis2/dhis2-core/pull/7571 |
| V2_34_36 | https://github.com/dhis2/dhis2-core/pull/7582 |
| V2_34_37 | DHIS2-10697 |
| V2_34_38 | ? |
| V2_34_39 | DHIS2-1127 |
| V2_34_40 | DHIS2-1164 |
| V2_34_41 | https://jira.dhis2.org/browse/DHIS2-11030 |
| V2_34_42 | https://jira.dhis2.org/browse/DHIS2-9674  |
| V2_34_43 | https://jira.dhis2.org/browse/DHIS2-11599  |
| V2_34_44 | https://jira.dhis2.org/browse/DHIS2-11693  |
| V2_34_45 | https://jira.dhis2.org/browse/TECH-823 |

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
| V2_35_27 | https://github.com/dhis2/dhis2-core/pull/6915 |
| V2_35_28 | DHIS2-8911 - fix |
| V2_35_29 | ? |
| V2_35_30 | DHIS2-10556 |
| V2_35_31 | DHIS2-5587 |
| V2_35_32 | tracker-query-sql performance |
| V2_35_33 | https://github.com/dhis2/dhis2-core/pull/7581 |
| V2_35_34 | DHIS2-10697 |
| V2_35_35 | ? |
| V2_35_36 | https://github.com/dhis2/dhis2-core/pull/7795 |
| V2_35_37 | DHIS2-1127 |
| V2_35_38 | DHIS2-1164 |
| V2_35_39 | https://jira.dhis2.org/browse/DHIS2-11030  |
| V2_35_40 | https://jira.dhis2.org/browse/DHIS2-9674  |
| V2_35_41 | https://jira.dhis2.org/browse/DHIS2-11599  |
| V2_35_42 | https://jira.dhis2.org/browse/DHIS2-11792 |
| V2_35_43 | https://jira.dhis2.org/browse/DHIS2-11693 |
| V2_35_44 | https://jira.dhis2.org/browse/DHIS2-11574 |
| V2_35_45 | https://jira.dhis2.org/browse/DHIS2-11574 |
| V2_35_46 | https://jira.dhis2.org/browse/TECH-823 |


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
| V2_36_15 | https://github.com/dhis2/dhis2-core/pull/6567 |
| V2_36_16 | ~~[https://github.com/dhis2/dhis2-core/pull/6929]~~ |
| V2_36_17 | https://github.com/dhis2/dhis2-core/pull/6914 |
| V2_36_18 | https://github.com/dhis2/dhis2-core/pull/6918 |
| V2_36_19 | https://github.com/dhis2/dhis2-core/pull/6975 |
| V2_36_20 | https://github.com/dhis2/dhis2-core/pull/7039|
| V2_36_21 | DHIS2-10212 |
| V2_36_22 | DHIS2-10214 |
| V2_36_23 | https://github.com/dhis2/dhis2-core/pull/7116 |
| V2_36_24 | https://github.com/dhis2/dhis2-core/pull/7194 |
| V2_36_25 | https://github.com/dhis2/dhis2-core/pull/7296 |
| V2_36_26 | DHIS2-8937 |
| V2_36_27 | DHIS2-8937 |
| V2_36_28 | DHIS2-8937 |
| V2_36_29 | ??? |
| V2_36_30 | https://github.com/dhis2/dhis2-core/pull/7368 |
| V2_36_31 | ??? |
| V2_36_32 | ??? |
| V2_36_33 | DHIS2-10556 |
| V2_36_34 | tracker-query-sql performance |
| V2_36_35 | https://github.com/dhis2/dhis2-core/pull/7580 |
| V2_36_36 | https://jira.dhis2.org/browse/DHIS2-10642 |
| V2_36_37 | DHIS2-10697 |
| V2_36_38 | ? |
| V2_36_39 | https://github.com/dhis2/dhis2-core/pull/7797 |
| V2_36_40 | DHIS2-1127 |
| V2_36_41 | DHIS2-1164 |
| V2_36_42 | https://jira.dhis2.org/browse/DHIS2-11030  |
| V2_36_43 | https://jira.dhis2.org/browse/DHIS2-9674  |
| V2_36_44 | https://jira.dhis2.org/browse/DHIS2-11599  |
| V2_36_45 | https://jira.dhis2.org/browse/DHIS2-11720 |
| V2_36_46 | https://jira.dhis2.org/browse/DHIS2-11693 |
| V2_36_47 | https://jira.dhis2.org/browse/DHIS2-11574 |
| V2_36_48 | https://jira.dhis2.org/browse/DHIS2-11574 |
| V2_36_49 | https://jira.dhis2.org/browse/TECH-823 |
| V2_36_50 | https://jira.dhis2.org/browse/DHIS2-12222 |
| V2_36_52 | https://jira.dhis2.org/browse/DHIS2-12182 |
| V2_36_53 | https://jira.dhis2.org/browse/DHIS2-12590 |
| V2_36_54 | ? |
| V2_36_55 | https://jira.dhis2.org/browse/DHIS2-13002 |
| V2_36_56 | https://jira.dhis2.org/browse/DHIS2-12816 |

### 2.37

| Version  | Pull request URL |
| -- | --  |
| V2_37_1  | https://github.com/dhis2/dhis2-core/pull/7563 |
| V2_37_2  | tracker-query-sql performance |
| V2_37_3  |  https://jira.dhis2.org/browse/DHIS2-10642 |
| V2_37_4  | DHIS2-10697 |
| V2_37_5  | ? |
| V2_37_6  | ? |
| V2_37_7  | https://github.com/dhis2/dhis2-core/pull/7798 |
| V2_37_8  | DHIS2-1127 |
| V2_37_9  | DHIS2-7029-1, https://github.com/dhis2/dhis2-core/pull/7867|
| V2_37_10 | ? |
| V2_37_11 | DHIS2-7776, https://jira.dhis2.org/browse/DHIS2-7776 |
| V2_37_12 | https://jira.dhis2.org/browse/DHIS2-11030 | 
| V2_37_13 | https://jira.dhis2.org/browse/TECH-608 | 
| V2_37_14 | https://jira.dhis2.org/browse/DHIS2-11172 |
| V2_37_15 | https://jira.dhis2.org/browse/DHIS2-9674 |
| V2_37_16 | https://jira.dhis2.org/browse/DHIS2-8328 |
| V2_37_17 | https://jira.dhis2.org/browse/DHIS2-11047 |
| V2_37_18 | https://jira.dhis2.org/browse/DHIS2-11347 |
| V2_37_19 | https://jira.dhis2.org/browse/DHIS2-11370 |
| V2_37_20 | https://jira.dhis2.org/browse/DHIS2-716 |
| V2_37_21 | https://jira.dhis2.org/browse/DHIS2-11347 |
| V2_37_22 | https://jira.dhis2.org/browse/DHIS2-11437 |
| V2_37_23 | https://jira.dhis2.org/browse/TECH-648 |
| V2_37_24 | https://jira.dhis2.org/browse/TECH-648 |
| V2_37_25 | https://jira.dhis2.org/browse/DHIS2-11599 |
| V2_37_26 | https://jira.dhis2.org/browse/DHIS2-11057 |
| V2_37_27 | https://jira.dhis2.org/browse/DHIS2-2162 |
| V2_37_28 | https://jira.dhis2.org/browse/DHIS2-11607 |
| V2_37_29 | https://jira.dhis2.org/browse/DHIS2-11574 |
| V2_37_30 | https://jira.dhis2.org/browse/DHIS2-11574 |
| V2_37_31 | https://jira.dhis2.org/browse/DHIS2-10287 |
| V2_37_32 | https://jira.dhis2.org/browse/DHIS2-11690 |
| V2_37_33 | https://jira.dhis2.org/browse/DHIS2-11700 |
| V2_37_34 | https://jira.dhis2.org/browse/DHIS2-11720 |
| V2_37_35 | https://jira.dhis2.org/browse/DHIS2-11738 |
| V2_37_36 | https://jira.dhis2.org/browse/DHIS2-11737 |
| V2_37_37 | https://jira.dhis2.org/browse/DHIS2-11767 |
| V2_37_38 | https://jira.dhis2.org/browse/DHIS2-11951 |
| V2_37_41 | https://jira.dhis2.org/browse/TECH-823 |
| V2_37_42 | https://jira.dhis2.org/browse/DHIS2-12222 |
| V2_37_44 | https://jira.dhis2.org/browse/DHIS2-12182 |
| V2_37_45 | https://jira.dhis2.org/browse/DHIS2-12590 |
| V2_37_46 | ? |
| V2_37_47 | https://jira.dhis2.org/browse/DHIS2-13002 |
| V2_37_48 | https://jira.dhis2.org/browse/DHIS2-13002 |
| V2_37_49 | https://jira.dhis2.org/browse/DHIS2-13002 |
| V2_37_50 | https://jira.dhis2.org/browse/DHIS2-11534 |
| V2_37_51 | https://jira.dhis2.org/browse/DHIS2-12816 |
| V2_37-52 | https://dhis2.atlassian.net/browse/TECH-1521 |


### 2.38

| Version  | Pull request URL |
| -- | --  |
| V2_38_1  | https://jira.dhis2.org/browse/DHIS2-7317 |
| V2_38_2  | https://jira.dhis2.org/browse/DHIS2-7317 |
| V2_38_3  | https://jira.dhis2.org/browse/DHIS2-7317 |
| V2_38_4  | https://jira.dhis2.org/browse/DHIS2-5075 |
| V2_38_5  | https://jira.dhis2.org/browse/DHIS2-11767 |
| V2_38_6  | https://jira.dhis2.org/browse/DHIS2-3789 |
| V2_38_7  | https://jira.dhis2.org/browse/DHIS2-4828 |
| V2_38_8  | https://jira.dhis2.org/browse/TECH-689 |
| V2_38_9  | https://jira.dhis2.org/browse/DHIS2-11801 |
| V2_38_10 | https://jira.dhis2.org/browse/DHIS2-11951 |
| V2_38_11 | https://jira.dhis2.org/browse/TECH-703 |
| V2_38_12 | https://jira.dhis2.org/browse/TECH-703 |
| V2_38_13 | https://jira.dhis2.org/browse/DHIS2-12018 |
| V2_38_14 | https://jira.dhis2.org/browse/DHIS2-11234 |
| V2_38_15 | https://jira.dhis2.org/browse/TECH-811 |
| V2_38_16 | https://jira.dhis2.org/browse/DHIS2-9833 |
| V2_38_17 | https://jira.dhis2.org/browse/DHIS2-11929 |
| V2_38_18 | https://jira.dhis2.org/browse/TECH-795 |
| V2_38_19 | https://jira.dhis2.org/browse/DHIS2-12222 |
| V2_38_20 | https://jira.dhis2.org/browse/TECH-820 |
| V2_38_21 | https://jira.dhis2.org/browse/DHIS2-12154 |
| V2_38_22 | https://jira.dhis2.org/browse/TECH-891 |
| V2_38_23 | https://jira.dhis2.org/browse/TECH-905 |
| V2_38_24 | https://jira.dhis2.org/browse/DHIS2-12356 |
| V2_38_25 | https://jira.dhis2.org/browse/DHIS2-9897 |
| V2_38_26 | https://jira.dhis2.org/browse/DHIS2-9897 |
| V2_38_27 | https://jira.dhis2.org/browse/DHIS2-12373 |
| V2_38_28 | https://jira.dhis2.org/browse/DHIS2-12249 |
| V2_38_29 | https://jira.dhis2.org/browse/DHIS2-12279 |
| V2_38_31 | https://jira.dhis2.org/browse/DHIS2-12376 |
| V2_38_32 | https://jira.dhis2.org/browse/DHIS2-12605 |
| V2_38_33 | https://jira.dhis2.org/browse/DHIS2-12647 |
| V2_38_34 | https://jira.dhis2.org/browse/DHIS2-12577 |
| V2_38_35 | https://jira.dhis2.org/browse/DHIS2-12577 |
| V2_38_36 | https://jira.dhis2.org/browse/DHIS2-12577 |
| V2_38_37 | https://jira.dhis2.org/browse/DHIS2-12574 |
| V2_38_38 | https://jira.dhis2.org/browse/DHIS2-12590 |
| V2_38_39 | https://jira.dhis2.org/browse/DHIS2-12734 |
| V2_38_40 | https://jira.dhis2.org/browse/DHIS2-12182 |
| V2_38_41 | ? |
| V2_38_42 | https://jira.dhis2.org/browse/DHIS2-13002 |
| V2_38_43 | https://jira.dhis2.org/browse/DHIS2-13002 |
| V2_38_44 | https://jira.dhis2.org/browse/DHIS2-13002 |
| V2_38_45 | https://jira.dhis2.org/browse/DHIS2-12039 |
| V2_38_46 | https://jira.dhis2.org/browse/DHIS2-11534 |
| V2_38_47 | https://jira.dhis2.org/browse/DHIS2-12816 |
| V2_38_48 | https://dhis2.atlassian.net/browse/TECH-1521 |
| V2_38_49 | https://dhis2.atlassian.net/browse/DHIS2-15305 |
| V2_38_50 | https://dhis2.atlassian.net/browse/DHIS2-15689 |
| V2_38_51 | https://dhis2.atlassian.net/browse/DHIS2-14956 |

### 2.39

| Version  | Pull request URL |
| -- | --  |
| V2_39_1  | https://jira.dhis2.org/browse/DHIS2-12182 |
| V2_39_2  | https://jira.dhis2.org/browse/DHIS2-13002 |
| V2_39_3  | https://jira.dhis2.org/browse/DHIS2-13002 |
| V2_39_4  | https://jira.dhis2.org/browse/DHIS2-13002 |
| V2_39_5  | https://jira.dhis2.org/browse/DHIS2-10688 |
| V2_39_6  | https://jira.dhis2.org/browse/DHIS2-10688 |
| V2_39_7  | https://jira.dhis2.org/browse/DHIS2-10688 |
| V2_39_8  | ??? |
| V2_39_9  | https://jira.dhis2.org/browse/DHIS2-13244 |
| V2_39_10 | https://jira.dhis2.org/browse/DHIS2-13036 |
| V2_39_11 | https://jira.dhis2.org/browse/DHIS2-13264 |
| V2_39_12 | https://jira.dhis2.org/browse/DHIS2-13105 |
| V2_39_13 | https://jira.dhis2.org/browse/DHIS2-11534 |
| V2_39_14 | https://jira.dhis2.org/browse/DHIS2-13300 |
| V2_39_15 | https://jira.dhis2.org/browse/DHIS2-13042 |
| V2_39_16 | https://jira.dhis2.org/browse/DHIS2-13301 |
| V2_39_17 | https://jira.dhis2.org/browse/DHIS2-12816 |
| V2_39_18 | https://jira.dhis2.org/browse/DHIS2-13105 |
| V2_39_19 | https://jira.dhis2.org/browse/DHIS2-12249 |
| V2_39_21 | https://jira.dhis2.org/browse/DHIS2-7882 |
| V2_39_22 | https://jira.dhis2.org/browse/DHIS2-9378 |
| V2_39_23 | https://jira.dhis2.org/browse/DHIS2-9900 |
| V2_39_24 | https://dhis2.atlassian.net/browse/TECH-1521 |
| V2_39_25 | https://jira.dhis2.org/browse/DHIS2-15305 |
| V2_39_26 | https://jira.dhis2.org/browse/DHIS2-15689 |
| V2_39_27 | https://dhis2.atlassian.net/browse/DHIS2-14956 |


### 2.40

| Version  | Pull request URL |
| -- | --  |
| V2_40_1  | https://dhis2.atlassian.net/browse/DHIS2-13988 |
| V2_40_2  | https://dhis2.atlassian.net/browse/DHIS2-13988 |
| V2_40_3  | https://dhis2.atlassian.net/browse/DHIS2-12744 |
| V2_40_4  | https://dhis2.atlassian.net/browse/DHIS2-14314 |
| V2_40_5  | https://dhis2.atlassian.net/browse/DHIS2-12194 |
| V2_40_6  | https://dhis2.atlassian.net/browse/DHIS2-13373 |
| V2_40_7  | https://dhis2.atlassian.net/browse/DHIS2-13333 |
| V2_40_8  | https://dhis2.atlassian.net/browse/DHIS2-13333 |
| V2_40_9  | https://dhis2.atlassian.net/browse/DHIS2-14305 |
| V2_40_10 | https://dhis2.atlassian.net/browse/DHIS2-14102 |
| V2_40_11 | https://dhis2.atlassian.net/browse/DHIS2-12911 |
| V2_40_12 | https://dhis2.atlassian.net/browse/DHIS2-14691 |
| V2_40_13 | https://dhis2.atlassian.net/browse/DHIS2-14606 |
| V2_40_14 | https://dhis2.atlassian.net/browse/DHIS2-12193 |
| V2_40_15 | https://dhis2.atlassian.net/browse/DHIS2-14367 |
| V2_40_16 | https://dhis2.atlassian.net/browse/DHIS2-14526 |
| V2_40_17 | https://dhis2.atlassian.net/browse/DHIS2-14526 |
| V2_40_18 | https://dhis2.atlassian.net/browse/DHIS2-7093 |
| V2_40_19 | https://dhis2.atlassian.net/browse/DHIS2-14815 |
| V2_40_20 | https://dhis2.atlassian.net/browse/DHIS2-14460 |
| V2_40_21 | https://dhis2.atlassian.net/browse/DHIS2-15010 |
| V2_40_22 | https://dhis2.atlassian.net/browse/DHIS2-15106 |
| V2_40_23 | https://dhis2.atlassian.net/browse/TECH-1521 |
| V2_40_24 | https://dhis2.atlassian.net/browse/DHIS2-15305 |
| V2_40_25 | https://dhis2.atlassian.net/browse/TECH-1576 |
| V2_40_26 | https://dhis2.atlassian.net/browse/DHIS2-14956 |
| V2_40_27 | https://dhis2.atlassian.net/browse/DHIS2-15689 |


### 2.41
| Version  | Pull request URL |
| -- | --  |
| V2_41_1  | https://dhis2.atlassian.net/browse/DHIS2-13776 |
| V2_41_2  | https://dhis2.atlassian.net/browse/DHIS2-15038 |
| V2_41_3  | https://dhis2.atlassian.net/browse/DHIS2-7763 |
| V2_41_4  | https://dhis2.atlassian.net/browse/DHIS2-15106 |
| V2_41_5  | https://dhis2.atlassian.net/browse/DHIS2-14902 |
| V2_41_6  | https://dhis2.atlassian.net/browse/DHIS2-5091 |
| V2_41_7  | https://dhis2.atlassian.net/browse/TECH-1521 |
| V2_41_10  | https://dhis2.atlassian.net/browse/DHIS2-14925 |
| V2_41_16  | https://dhis2.atlassian.net/browse/TECH-1576 |
| V2_41_17  | https://dhis2.atlassian.net/browse/DHIS2-14956 |
| V2_41_18 | https://dhis2.atlassian.net/browse/DHIS2-14847 |
| V2_41_19 | https://dhis2.atlassian.net/browse/DHIS2-14847 |
| V2_41_20 | https://dhis2.atlassian.net/browse/TECH-1542 |
| V2_41_21 | https://dhis2.atlassian.net/browse/DHIS2-15288 |
| V2_41_22 | https://dhis2.atlassian.net/browse/DHIS2-15027 |
| V2_41_23 | https://dhis2.atlassian.net/browse/DHIS2-1593 |
| V2_41_24 | https://dhis2.atlassian.net/browse/DHIS2-1594 |
| V2_41_25 | https://dhis2.atlassian.net/browse/DHIS2-1596 |
| V2_41_26 | https://dhis2.atlassian.net/browse/DHIS2-1597 |
| V2_41_27 | https://dhis2.atlassian.net/browse/DHIS2-15689 |
| V2_41_28 | https://dhis2.atlassian.net/browse/TECH-1614 |
| V2_41_29 | https://dhis2.atlassian.net/browse/DHIS2-15725 |
| V2_41_30 | https://dhis2.atlassian.net/browse/TECH-1636 |
| V2_41_31 | https://dhis2.atlassian.net/browse/DHIS2-15666 |
| V2_41_32 | https://dhis2.atlassian.net/browse/DHIS2-15276 |
| V2_41_33 | https://dhis2.atlassian.net/browse/TECH-680 |
| V2_41_34 | https://dhis2.atlassian.net/browse/DHIS2-15276 |
| V2_41_35 | https://dhis2.atlassian.net/browse/TECH-1615 |
| V2_41_36 | https://dhis2.atlassian.net/browse/TECH-1615 |
| V2_41_37 | https://dhis2.atlassian.net/browse/TECH-1655 |
| V2_41_38 | https://dhis2.atlassian.net/browse/TECH-1655 |
| V2_41_39 | https://dhis2.atlassian.net/browse/DHIS2-15757 |
| V2_41_41 | https://dhis2.atlassian.net/browse/DHIS2-15805 |
| V2_41_42 | https://dhis2.atlassian.net/browse/DHIS2-16369 |

