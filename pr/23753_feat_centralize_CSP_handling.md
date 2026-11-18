# Centralize CSP handling with marker annotations (dhis2-core#23753)

Author: Morten Svanæs

- Code PR: https://github.com/dhis2/dhis2-core/pull/23753
- UI PR: https://github.com/dhis2/app-management-app/pull/621
- Jira: [DHIS2-17931](https://dhis2.atlassian.net/browse/DHIS2-17931), [DHIS2-10695](https://dhis2.atlassian.net/browse/DHIS2-10695)
- Based on dhis2/dhis2-core#22980 by @amcgee.

This document describes the PR at head `51200b36a5f8`.

## Overview

A Content-Security-Policy (CSP) tells the browser which sources a page can load and run.
Before this PR, the server set CSP headers in several places, partly by URL pattern.
Most responses had only `frame-ancestors`.

This PR puts all CSP handling in one place:

- Every response gets a default policy.
- Some endpoints get a different policy. A marker annotation on the controller method selects that policy.
- Each app can get its own policy. An administrator can add sources per app and per entrypoint.
- The browser sends violation reports to the server. Administrators can read them.

The UI for the overrides and the reports is in the App Management app (dhis2/app-management-app#621).

## Main classes

| Class | Job |
|---|---|
| `CspBaselineFilter` | Sets the default policy on every response. This includes 404 responses and responses that do not reach a controller. |
| `CspInterceptor` | Replaces the default policy for controller methods that have a marker annotation. |
| `CspPolicyService` | Builds the headers. |
| `CspConstants` | Holds all fixed policy strings. |
| `CspAppPolicyService` | Builds the policy of an app entrypoint (see [Per-app policies](#per-app-policies)). |
| `CspOverrideValidator` | Validates administrator overrides. |
| `CspAppOverrideController` | API to manage overrides and read violation reports. |
| `CspReportController` | Receives violation reports from the browser. |

This PR removes the old CSP code:

- the URL-pattern `CspFilter`,
- `HeaderUtils.setSecurityHeaders`,
- the CSP headers that the tracker `RequestHandler` set.

Unit tests and H2 controller tests cover the policies, the per-app composition, the validator, the override API, the report intake and the violation store.
The E2E test `CspHeadersE2ETest` checks the headers of user content, apps, the global shell, Maps, the login page and default endpoints.

## Policies

Each marker annotation selects one policy.

| Marker | Policy body | Applied to |
|---|---|---|
| none | `default-src 'self'; style-src 'self' 'unsafe-inline'` | every response |
| `@CspUserUploadedContent` | `default-src 'none'` | downloads of user content (list below). The server sends this policy also when `csp.enabled` is off. |
| `@CspAppHost` | `default-src 'self'; style-src 'self' 'unsafe-inline'; child-src 'self' blob:; img-src 'self' data: blob: https://apps.dhis2.org; connect-src 'self'` | `AppController.renderApp` (`GET /api/apps/{app}/**`). The global shell and the legacy `/dhis-web-*` paths also reach this method. App entrypoints get a per-app policy on top. |
| `@CspOpenApiDocs` | `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:` | the OpenAPI HTML pages |
| `@CspHtmlReport` | `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'` | `GET /api/reports/{uid}/data.html`. These rendered HTML standard reports start with an inline script. |

`@CspUserUploadedContent` is on these endpoints:

- `GET /api/fileResources/{uid}/data`
- `GET /api/documents/{uid}/data`
- `GET /api/audits/files/{uid}`
- `GET /api/icons/{key}/icon` and `GET /api/icons/{key}/icon.svg`
- `GET /api/dataValues/files`
- `GET /api/messageConversations/{mcUid}/{msgUid}/attachments/{fileUid}`
- the `file` and `image` endpoints of `/api/tracker/events`, `/api/tracker/singleEvents` and `/api/tracker/trackerEvents` (event data values)
- the `file` and `image` endpoints of `/api/tracker/trackedEntities` (tracked entity attributes)

### Parts that every policy gets

- Common hardening: `base-uri 'self'; form-action 'self'; object-src 'none'`.
- Footer, in this order:
  1. `upgrade-insecure-requests`, only when `server.https` and `csp.upgrade.insecure.enabled` are both on.
  2. `frame-ancestors 'self'`, plus the origins of the CORS whitelist.
  3. For app entrypoints only: a `report-uri` (see [Violation reports](#violation-reports)).

### Other security headers

- `X-Content-Type-Options: nosniff`: always sent.
- `X-Frame-Options: SAMEORIGIN`: sent only when CSP is disabled.
- `X-XSS-Protection: 1; mode=block`: no longer sent. `HeaderUtils` and the tracker `RequestHandler` sent it before.

### When CSP is disabled

When `csp.enabled` is off, only user content gets a CSP.
That policy has `frame-ancestors 'self'` and no CORS whitelist origins.

### Login page

The fallback `login.html` had an inline script and inline styles.
This PR moves them to `login.js` and `login.css`.
Both files are public.
The login page now runs under the default policy.

## Per-app policies

### Entrypoints

An app has resources below `/api/apps/{app}/`.
`CspInterceptor` finds the entrypoint of each request:

| Entrypoint | Resource |
|---|---|
| `app` | the launch path of the app (`index.html` by default) |
| `plugin` | the plugin launch path of the app |
| `worker` | `service-worker.js` |
| `*` | any other HTML document of the app |

Other resources of the app (scripts, styles, images) get the app-host policy without a per-app lookup.
The global shell is an app of its own.
Thus the global shell never gets the policy of the app that it frames.

### Composition order

`CspAppPolicyService` builds the policy of an entrypoint in this order:

1. The app-host policy (the `@CspAppHost` row above).
2. The core base overrides of the app. The base sources that the administrator disabled for the entrypoint are removed.
3. The administrator additions for `*`, then the administrator additions for the entrypoint.
4. The footer: `upgrade-insecure-requests`, `frame-ancestors` and `report-uri`. No override can change the footer.

The service validates the stored additions again on each read.
It drops values that are not valid now.
Examples: an `http://` origin after an administrator turned `server.https` on, or a value that someone wrote directly into the datastore.

### Core base overrides

`CspBaseOverrides` holds the core base overrides.
They ship with the server, and nobody can edit them.
Only two apps have core base overrides: Maps and Reports.

**Maps** (app key `maps`):

- `img-src` and `connect-src` on the `app`, `plugin` and `worker` entrypoints get these tile hosts:
  `tiles.openfreemap.org`, `tile.openstreetmap.org`, `{a,b,c}.tile.openstreetmap.org`,
  `cartodb-basemaps-{a,b,c}.global.ssl.fastly.net` and `tiles.maps.eox.at`.
  Each host is an `https://` origin.
  While `server.https` is off, the `http://` origins are added too.
  The `worker` entrypoint is included because the Maps service worker fetches tiles for its cache.
- `script-src 'wasm-unsafe-eval'` on the `app` and `plugin` entrypoints.
  The WebAssembly RTL text plugin needs it.
  The API shows it as a base unsafe token.

**Reports** (app key `reports`), on the `app` entrypoint only.
The app page gets `script-src 'self' 'unsafe-inline' 'unsafe-eval'`:

- `'unsafe-inline'`: the Reports app shows HTML standard reports in a `srcdoc` iframe.
  The iframe gets the policy of the app page.
  The report HTML starts with an inline script.
- `'unsafe-eval'`: the Reports app bundle calls `Function("return this")()` at startup (regenerator runtime).
  Without `'unsafe-eval'`, the app shows its error page.
- The API shows both sources as base unsafe tokens.
  No other app gets them.

An administrator can disable each base source per entrypoint with `disabledBaseSources`.
Examples: `"script-src 'wasm-unsafe-eval'"` for Maps, `"script-src 'unsafe-inline'"` or `"script-src 'unsafe-eval'"` for Reports.

### Administrator overrides

Each app has one override document (schema version 1).
The document has an `enabled` flag and one entry per entrypoint.
Each entry can have these fields:

- `enforced.add`: a map from directive to sources.
- `enforced.disabledBaseSources`: the base sources to remove.
- `enforcementMode`: `ENFORCE` (default) or `REPORT_ONLY_EXEMPT`.
  The mode of the most specific entry that sets a mode applies.
- `reportOnlyDraft`: a draft policy to test.
  While the draft is enabled, the server sends a candidate policy as `Content-Security-Policy-Report-Only`.
  The candidate has the draft additions and removals.
  The enforced policy does not change.
  If the draft has `expiresAt` (at most 24 hours ahead), the server also enforces the draft additions until that time.

### Validation

`CspOverrideValidator` validates each override.

Directives:

- Overridable: `connect-src`, `img-src`, `frame-src`, `child-src`, `font-src`, `style-src`, `media-src`, `worker-src`, `script-src`, `form-action`.
- Locked: `default-src`, `object-src`, `base-uri`, `frame-ancestors`, `upgrade-insecure-requests`, `report-uri`, `report-to`.

Values:

- Each value is one source token.
  The validator rejects `;`, `,`, whitespace and control characters.
- A directive takes at most 64 values.

Directives other than `script-src`:

- They take `'self'` or a bare origin `scheme://host[:port]`.
  A path, a bare `*` and a scheme-only source are not allowed.
- `https://` is always allowed.
- `wss://` and `ws://` are allowed only in `connect-src`.
- `http://` and `ws://` are allowed only while `server.https` is off.
- Wildcard hosts such as `https://*.example.org` are allowed only in `img-src` and `connect-src`.

`script-src`:

- It takes `https://` origins, `'self'`, `'strict-dynamic'`, `'report-sample'` and hashes.
- It also takes unsafe sources: `'unsafe-inline'`, `'unsafe-eval'`, `'wasm-unsafe-eval'`, `'unsafe-hashes'`, `data:`, `blob:`, `*`, `https:` and wildcard hosts.
  While `server.https` is off, it also takes `http:` and `http://` origins, which are unsafe too.
- The validator rejects nonces and unknown keywords.

Confirmations:

- To save unsafe sources, the request must have `confirmUnsafe: true`.
  The document stores them as `unsafeTokens`, with `hasUnsafeDirectives`.
  The app summary shows them.
- `REPORT_ONLY_EXEMPT` is the last resort for an app that cannot run under any allowed policy.
  The enforced header keeps only `frame-ancestors`.
  The server sends the composed policy as report-only.
  To save it, the request must have `confirmExempt: true` and an `approvalNote`.
  The mode applies to one app and entrypoint, never to all apps.

Responses:

- A validation error gives 400.
- A missing confirmation gives 409.
- Both response bodies list the error codes.

### Storage and cache

- The overrides are in the protected datastore namespace `csp-app-overrides`, with one key per app.
- Through `/api/dataStore`, a read needs `F_SYSTEM_SETTING` or `M_dhis-web-app-management`.
  A write needs `ALL`.
- The override service validates first.
  Then it writes as the system user.
- The service audits each create, update and delete (`AuditScope.METADATA`) and writes a log line.
- The server caches the overrides for 5 minutes.
  The cache uses Redis when Redis is configured.
- A save or a delete evicts the cache entry.
  Thus the change applies on the next request, without a restart.

The storage in the datastore is a first step.
The store is behind the `CspAppOverrideStore` interface (see [Open points](#open-points)).

### Suggestions for Maps

For the Maps app, the detail view suggests origins from these sources:

- the URL and the legend URL of stored external map layers,
- the configured Bing Maps and Azure Maps keys.

A suggestion grants nothing.
An administrator must add it as an override.

## API

All paths are below `/api/security/csp`.

| Method and path | Purpose | Authority |
|---|---|---|
| `GET /apps` | All installed apps, with: base override, override state, unsafe and exempt flags, active draft, violation counts of the last 24 hours. | read |
| `GET /apps/{appKey}` | Entrypoint paths, overridable and locked directives, app-host policy, base overrides, suggestions, stored override, effective headers per entrypoint, recent violations. | read |
| `POST /apps/{appKey}/validate` | Dry run. Returns the effective headers. | read |
| `PUT /apps/{appKey}` | Save an override. | `F_SYSTEM_SETTING` |
| `DELETE /apps/{appKey}` | Remove an override. | `F_SYSTEM_SETTING` |
| `GET /reports[?app=]` | Deduplicated violations. | read |
| `GET /apps/{appKey}/reports` | Violations of one app. | read |
| `DELETE /apps/{appKey}/reports` | Clear the violations of one app. | `F_SYSTEM_SETTING` |
| `POST /report?app=&ep=` | Intake of browser violation reports. | none |

"read" means `F_SYSTEM_SETTING` or `M_dhis-web-app-management`.

The API must list all apps, also apps that the current user cannot open.
For this, the PR adds `AppManager.getAllApps`.

## Violation reports

### Report URI

While `csp.enabled` and `csp.report.enabled` are both on, app entrypoint policies have this directive:

`report-uri <context>/api/security/csp/report?app=<key>&ep=<entrypoint>`

The server sends only `report-uri`, not `report-to`.

### Intake

- The intake accepts `application/csp-report`, `application/reports+json` and `application/json`.
- The intake needs no login.
  CSRF protection does not apply to it.
- A body over 8 KiB gives 413.
  All other requests give 204, also when the server drops the report.
- Rate limits, in memory on each node:
  30 reports per minute per client IP with a burst of 60, and 500 reports per minute in total.
- The server reads at most 20 reports per payload.
- The server drops a report in these cases:
  - The app is unknown. Installed app keys and `_platform` are accepted.
  - The entrypoint is not valid.
  - The source is a browser extension or `about:`.
  - The payload is not valid.
- The metric `dhis.csp.reports.dropped` counts the dropped reports, with the reason as a tag.

### Stored data

- The server keeps only fixed fields.
- It removes the query and the fragment from the document URI and the source file.
- It reduces the blocked URI to its origin or to a keyword.

### Store

- The server deduplicates reports by app, entrypoint, disposition, directive and blocked URI.
- The store keeps at most 100 entries per app.
- It keeps each entry for 24 hours after the last time the server saw it.
- The store is in memory on each node. It writes nothing to the database.

### Classification

The server classifies each violation, for example external origin, inline or eval.
Each violation also gets:

- a remediation hint,
- a suggested source, when the validator allows one,
- the status `ALLOWED_NOW`, when the current policy already allows the source.

## Configuration

| Key | Change | Default |
|---|---|---|
| `csp.report.enabled` | New. Adds the `report-uri` to app entrypoint policies and accepts reports. It has no effect while `csp.enabled` is off. | `on` |
| `csp.upgrade.insecure.enabled` | Default changes from `off` to `on`. It has an effect only when `server.https` is on. | `on` |
| `csp.header.value` | Removed. It set the CSP on file downloads and tracker file responses (default `script-src 'none'; `). `@CspUserUploadedContent` replaces it with `default-src 'none'`. A custom value in `dhis.conf` has no effect now. | removed |
| `csp.enabled` | No change. | `on` |

There is no global setting for map sources.
To allow more map origins, add per-app overrides on the Maps app.

## Upgrade impact

- With `csp.enabled` on (the default), every response has a full policy.
  Before, most responses had only `frame-ancestors`.
- App pages allow only same-origin scripts and `connect-src 'self'`.
  The base overrides and the administrator overrides of the app add to this.
- The policy blocks apps that use inline scripts or `eval`, or that call third-party hosts.
  An administrator must add an override for such an app.
  Example: Maps layers or basemaps on hosts outside the base override (external map layers, Bing, Azure).
  For those Maps cases, the detail view suggests the origins.
- Scripted HTML standard reports need no override:
  - `GET /api/reports/{uid}/data.html` sends `script-src 'self' 'unsafe-inline'`.
  - The Reports app page gets `script-src 'self' 'unsafe-inline' 'unsafe-eval'` from its base override.
  - An administrator can remove either Reports source with `disabledBaseSources`.
  - All other endpoints and apps keep their policy.
- `form-action 'self'` applies to every page.
  App entrypoints can add bare origins through an override.
- On HTTPS deployments, `upgrade-insecure-requests` is now on by default.
  Thus the browser fetches plain `http://` subresources over HTTPS.
- User content gets `default-src 'none'`, also when `csp.enabled` is off.
- Per app, administrators can add sources, test report-only drafts, or exempt one entrypoint.
- `csp.enabled=off` stays the global switch.

## Open points

- The default rollout is not decided yet.
  The question is whether `csp.enabled` is on at upgrade.
  The team decides this before the merge.
- The datastore storage of overrides is a first step behind the `CspAppOverrideStore` interface.
  A dedicated table is still open.
- App manifests cannot declare CSP sources yet.
  The override document reserves `approvedManifestCspHash`.
  It stays `null` for now.
