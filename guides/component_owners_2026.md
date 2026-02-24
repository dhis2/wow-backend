# Components
A list of software components as experienced by the developers.
This usually means a high level feature that corresponds to a relativly self-contained area of code.

> [!IMPORTANT]
> Ownership is not about being most knowledgeable on the team with regards to a component.
> It is self assigned by maintainers in case they feel confident that they can take
> on the responsibility of guiding the evolution of the component.
> Usually this requires a deep and detailed understanding or a commitment to learn and reach that level.
>
> Secondly ownership also implies available capacity.
> This is why components are given a priority which is induvidual for each maintainer.
> When a lack of capacity is experienced by a maintainer
> the component with the lowest priority (hightest number) is dropped by the owner.
> A new owner with available capacity needs to be found. 

## Platform Team

| Component | Owner  | Priority |
| :---------| :----- | :------- |
| Aggregate Data Entry | Jan | ? |
| Aggregate Data SMS Entry | ? | ? |
| Aggregate Data Changelog | Jan | ? |
| Aggregate Data Export | Jan | ? |
| Aggregate Data Audit | ? | ? |
| Aggregate Data Set-Completeness | ? | ? |
| Aggregate Data Validation Rules | ? | ? |
| Aggregate Data Approval | ? | ? |
| Job Scheduling | Jan | ? |
| System Settings | Jan | ? |
| (Meta)Data Ingetrity (Checks) | Jan | ? |
| Gist Metadata API | Jan | ? |
| JSON-tree lib | Jan | ? |
| OpenAPI | Jan | ? |
| User Settings | Jan? | ? |
| Authentication & IdP | Morten S. | ? |
| User & User group & User roles | Morten S. | ? |
| 2FA | Morten S. | ? |
| OAuth2 & OIDC & JWT | Morten S. | ? |
| LDAP | Morten S. | ? |
| PAT | Morten S. | ? |
| Auditing | Morten S. | ? |
| App support & Bundling | Morten S. | ? |
| Static resource cache | Morten S. | ? |
| API cache | Morten S. | ? |
| L2 Cache invalidaiton | Morten S. | ? |
| Clustering | Morten S. | ? |
| Connection pool | Morten S. | ? |
| Periods (& types, multi-calendar, custom periods) | ? | ? |

## Appendix
A list of components brainstromed in the past 
that might help to find/pick/remember what to add to the above list.

```
# Data

- data sync
- data exchange (ADE)
- others: data special use case APIs (e.g. dedicated app support)
- datastore (former platform)


# Metadata

- metadata API (general reading)
- metadata importer (general writing) (inkl. deletion handlers + bundle hooks)
- metadata patch (partial update support)
- metadata sync
- metadata merge
- metadata sharing
- metadata periods
- others: metadata special use case APIs (e.g. dedicated app support)


# System

- users + roles
- messages
- configuration
- icons + files
- translations
- SQL views
- metrics
- multi-calendar
- app support
- file storage & object storage
- event hooks
- sms support
- route API
- flyway


# Tech + Libs

- builds
- expression-parser
- caching and cluster mode
- emails
```
