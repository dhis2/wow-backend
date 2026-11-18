# PR 25859: refresh session user details in place instead of logging out

Author: Morten Svanæs

- Code PR: dhis2/dhis2-core#25859, `feat: refresh session user details in place instead of logging out [DHIS2-22326]`
- Jira: https://dhis2.atlassian.net/browse/DHIS2-22326
- Base: dhis2/dhis2-core#25854 (branch `fix/DHIS2-22326-expire-sessions-on-group-change`). Retarget to `master` when dhis2/dhis2-core#25854 merges.
- Supersedes dhis2/dhis2-core#24493, with a much lighter design.
- This document describes the PR at head `f2dc90395780` (2026-11-18): +6309/-653, 63 files.

Sources: the PR body before the 2026-11-18 rewrite, and the PR diff at `f2dc90395780`.
Statements about test runs and measurements come from the old PR body. This document did not run them again.

## Problem

The session principal (`UserDetails`) is a copy that the server makes at login.
On master, a role change or a role authority change logs out the affected users.
The logout makes the change take effect.
dhis2/dhis2-core#25854 does the same for group membership changes.
The users lose their session and their unsaved work because an admin made an edit.

## Design

The server refreshes the principal in place on the next request of the user.
The session and its id stay the same.

### Change token per user

- After commit, `UserDetailsChangeListener` writes a random token per affected username to a `UserDetailsChangeTracker`.
- With `redis.enabled`, `RedisUserDetailsChangeTracker` keeps the token in Redis, with the session timeout as time to live.
- Without Redis, `InMemoryUserDetailsChangeTracker` keeps the token in a map.
- The session keeps the token of the last change that it applied.
- The change executor queue is unbounded, so the server does not drop change marks in a burst.

### The refresh filter

- `UserDetailsRefreshFilter` runs after `ConcurrentSessionFilter`.
- It works only on authentications that the session keeps: form logins (also LDAP and 2FA), HTTP basic and OIDC.
- Personal access tokens and JWT bearer tokens authenticate each request on their own.
- When the token differs from the token of the session, `UserDetailsSessionRefresher` rebuilds the `Authentication` from the database.
- The rebuild keeps the authentication details, the 2FA factor and the OIDC wrapper.
  The refresher saves the result to the same session.
- On one node a lock per session id serializes the refresh of a session.
  A request that waited reads the session again and does not rebuild when a different request already applied the change.
- With Redis sessions each request has its own copy of the session. The last writer wins.
- `UserDetailsRefreshState` keeps the refresh state of a session in one class.
  The filter uses that state only for the session authentication that it checked in the same request.

### Fail closed

The refresher ends the session instead of a refresh when:

- the session impersonates a user, and that user changed.
  A refresh could give the impersonating user authorities that it may not impersonate;
- the session impersonates a user, and the impersonating user changed after the impersonation started;
- the refresh interval is due, and the impersonating user no longer exists, is disabled or expired;
- the refresh interval is due, and the impersonating user may no longer impersonate;
- the user no longer exists, is disabled or expired;
- a local-password login must set up two-factor authentication.

The refresher never rebuilds the authentication of an impersonation session.

### Hard logouts do not change

Password change, disable, account expiry and `DELETE /api/sessions/{username}` still log the user out.

### Triggers

- Group membership changes (the collector from dhis2/dhis2-core#25854, now `UserDetailsChangeCollector`).
- Role authority and restriction changes (`UserRoleSecurityChangedEvent`).
- User role changes of a user. These now mark the user after commit.
  Before, `UserObjectBundleHook` logged the user out in `postUpdate`.
- Org unit changes of a user: `User.organisationUnits`, `User.dataViewOrganisationUnits` and `User.teiSearchOrganisationUnits` (`UserDetailsCollectionListener`).
- Changes of these user properties: `disabled`, `accountExpiry`, `dataViewMaxOrganisationUnitLevel`, `externalAuth`, `twoFactorType` (`UserDetailsEntityListener`).
- A deleted user, by username. The next request of a session of that user finds no user and ends the session.

### Cached personal access tokens

`ApiTokenAuthManager` keeps the change token of the owner with each cached API token.
When the change token of the owner moved, the cached token authenticates again from the database.

### Timer backstop

The new `dhis.conf` setting `system.session.user_details_refresh_interval` sets an interval in seconds.
The default is 900. The value 0 turns the timed rebuild off.
The filter rebuilds a principal that is older than the interval.
This limits how long a change that the tracker does not see stays invisible.
Examples: group or role deletion, direct SQL, and lost marks.

### Memberships read with SQL

`DefaultUserService.createUserDetails` reads the groups, roles, authorities and restrictions with SQL (`UserStore.getMemberships`).
It does not use the cached `User.groups` and `User.userRoles` collections.
A different node of a cluster does not evict those collections for each change.

### Migration

`V2_44_36__add_usergroupmembers_userid_index.sql` adds the index `in_usergroupmembers_userid` on `usergroupmembers(userid)`.
dhis2/wow-backend#146 reserves the number.
The migration uses `if not exists`, so a large installation can make the index first with `CREATE INDEX CONCURRENTLY` and the same name.

### Renames

| Before | After |
|---|---|
| `UserGroupMembershipChangeCollector` | `UserDetailsChangeCollector` |
| `UserSessionInvalidationListener` | `UserDetailsChangeListener` |
| `UserRoleAuthoritiesChangedEvent` | `UserRoleSecurityChangedEvent` |
| `UserGroupMembershipChangedEvent` | removed; `UserDetailsChangedEvent` is new |

The old PR body also said: no new `UserDetailsImpl` fields, and no epoch or generation stamps.
This document did not check that statement against the diff.

## Review fixes after `1ac7bd687e5d`

| Commits | Fix |
|---|---|
| `0e3e7f1464`, `e89c43dbfb` | Impersonation with HTTP basic or a personal access token. An impersonation that a self-authenticated request started stays on the next request. Before, it ended there when the impersonating user had a recent change. It also ended when the request sent the cookie of a session of a different user. The same happened with the cookie of a session without a login. The refresh state of a session now applies only to the session authentication that the filter checked in that request. |
| `08a9504123` | No lost change marks. The change executor queue is unbounded. Before, it refused tasks after 1000, and those sessions kept the old principal until the refresh interval. |
| `09a94a3023`, `da1eac953f` | Locked accounts. A cached API token of an account that failed logins locked gets 401. The request does not lift the lock. The token works again when the lock expires. The failed login limit does not change existing sessions, also not impersonation sessions of that user. |
| `a11a63df2c`, `bddff148d5` | Index on `usergroupmembers(userid)`. The old PR body reports these timings. Reading the groups of one user went from 46 ms to 0.9 ms on 539,128 memberships. Building the index took 0.11 s. After a membership change each logged-in user reads their groups. |
| `468c3e96d9` | Same access on each node. The groups, roles, authorities and restrictions of a principal come from SQL, not from the cached collections. |
| `abbeef7fd0` | `/api/me` on each node. The user groups, user roles and authorities in `/api/me` come from the same SQL read. Before, a different node listed the old groups until its cache was cleared. Its access checks were already correct. |
| `28a820184f` | API token deleted on a different node. The token lookup by key no longer uses the query cache. Before, that cache on a different node still held the deleted token, for example after the owner was deleted. The request got HTTP 500 there instead of 401. Master has the same bug. |
| `c17de1609c` | Test for impersonation on a checked session. An impersonation request that its session authenticates takes the refresh state of that session. A change of the impersonating user after the check ends the impersonation on the next request. |
| `f97924b16b` | Refresh settings. A `system.session.user_details_refresh_interval` that is not a number (for example `900s`) gives the default 900 and a warning. Before, it turned the timed rebuild off. The value 0 still turns the timed rebuild off, now with a warning. A `system.session.timeout` of 0 or less keeps changes without expiry. Before, the in-memory tracker forgot them at once, and Redis refused each change token. One startup log line tells how the server keeps changes and if the timed rebuild is on. |
| `f58a8f83a8` | More filter chain tests. A new user group and a new org unit are visible on the next request of the same session. |
| `c2672d0c04` | `/api/me` lists groups that the user can read through a new group. `/api/me` loads the user groups and user roles without the sharing filter of the query. That filter takes the groups of the user from a cache that only the changing node clears. Before, a different node left out some groups and roles. The user could read those groups and roles only through a group that the user just joined. The read check against the user details still leaves out each group and role that the user cannot read. |
| `321bcaea71` | Migration renumbered. Master took `V2_44_35` (`V2_44_35__remove_search_in_all_authority.sql`), so the index migration is now `V2_44_36`. |
| `68a45e19be` | Refresh settings helpers. `UserDetailsRefreshSettings` takes the `dhis.conf` values, not the configuration provider. |

## How the behaviour is proven

New test classes in the diff:

- Unit: `UserDetailsRefreshFilterTest`, `UserDetailsRefreshConcurrencyTest`, `UserDetailsRefreshStateTest`, `ImpersonationSessionRefreshTest`, `InMemoryUserDetailsChangeTrackerTest`, `RedisUserDetailsChangeTrackerTest` (Redis mocked, as in the other Redis tests), `UserDetailsChangeListenerTest`, `UserDetailsChangeTaskExecutorTest`, `ApiTokenAuthManagerTest`.
- Integration: `UserDetailsMembershipsTest`, `ApiTokenKeyLookupTest`.
- Controller: `UserDetailsRefreshTest`, `UserDetailsWritePathRefreshTest`, `UserSessionRefreshControllerTest`, `UserOrgUnitSessionRefreshControllerTest`, `MeControllerMembershipsTest`, `MeControllerStaleGroupInfoTest`.
  `UserDetailsRefreshTest` uses the real filter chain.
  It checks that a new role, user group and org unit are visible on the same session.
  It also checks that disable still logs out and that impersonation ends.
  It checks that the failed login limit keeps impersonation sessions.
- Logout tests replaced by refresh tests: `UserGroupSessionInvalidationControllerTest` by `UserGroupSessionRefreshControllerTest`, `UserRoleSessionInvalidationControllerTest` by `UserRoleSessionRefreshControllerTest`, `UserSessionInvalidationListenerTest` by `UserDetailsChangeListenerTest`. `UserControllerTest` now expects a refresh.

Results, as the old PR body reports them:

- The `unit-test`, `integration-h2-test` and `integration-test` profiles pass.
  The only failure, `AppControllerTest.testInstalledAppReturnsShortcuts`, also fails on master.
- Two nodes with one Redis: a group membership change on node B changes the access of the old session.
  The old session gets the new access on node A and node B within 2 s.
  `/api/me` on both nodes lists the new groups.
  The API token of a user that node B deleted gets 401 on both nodes.

## Intended behaviour: accounts locked by failed logins

A session of an account that reaches the failed login limit stays logged in until it expires, as on master.
The lock protects the login path.
While the lock lasts, the server refuses new logins and API tokens of that account.
If the server ended the existing sessions, anyone who knows a username could log that user out with wrong passwords.
Thus `da1eac953f` keeps the sessions, also impersonation sessions.
