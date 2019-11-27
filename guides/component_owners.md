# Component Owners

## Overview

The purpose of the component owner concept is to have at least one person making sure that changes and improvements are well-aligned with the overall design and architecture of a component. This is meant to ensure that the code quality remains high and to avoid "patchwork" code fixes.

The list of components and owners can be found at the following link, and in the last section of this guide:

[Components and owners](https://jira.dhis2.org/projects/DHIS2?selectedItem=com.atlassian.jira.jira-projects-plugin:components-page)

## Responsibility

The component owner is responsible for:

* Having the complete oversight over the code base related to the component.
* Having a strong understanding of the design and architecture of the component code.
* Reviewing and testing PRs related to the component.
* Providing feedback and helping out other developers working on the component.
* Ensuring PRs align with the design of the current solution.
* Ensuring PRs maintain or improve performance, conversely avoid that PRs introduce bottlenecks.


Being a component owner does _not_ mean that you need or should to do all coding work on that component. Assignment of work is done as usual by the product manager and team lead.
   
## Workflow

When working on a PR you need to ask the component owner for review. If you _are_ the component owner, you can ask some other developer with knowledge about the code.

## Component owners

The following table describes the various components and their leads.

|Component                     |Lead                |Description                                                              |
|------------------------------|--------------------|-------------------------------------------------------------------------|
|[API] Analytics               |Luciano Fiandesio   |Analytics API and engine                                                 |
|[API] App management          |Mohamed Ameen       |App management                                                           |
|[API] App Store               |Viktor Varland      |App store backend service                                                |
|[API] Data administration     |Stian Sandvold      |Maintenance, SQL views, resource tables and scheduling                   |
|[API] Data approval           |Jim Grace           |Data approval, approval levels and approval workflows                    |
|[API] Data store              |Stian Sandvold      |System and user data store API                                           |
|[API] Data value set          |Abyot Asalefew Gizaw|Data value set API and service                                           |
|[API] Database migration      |Mohamed Ameen       |Database migration and upgrade scripts                                   |
|[API] Events                  |Morten Hansen       |Event API and service                                                    |
|[API] Frameworks/libraries    |Morten Hansen       |Upgrades of application frameworks and libraries                         |
|[API] Job scheduler           |Stian Sandvold      |Background job scheduling                                                |
|[API] Messaging               |Zubair Asghar       |Message conversations and program messages                               |
|[API] Metadata import-export  |Morten Hansen       |Metadata API and import-export                                           |
|[API] Metadata model          |Stian Sandvold      |Metadata model and storage                                               |
|[API] Other                   |Stian Sandvold      |All other API resources and services                                     |
|[API] Predictors              |Jim Grace           |Predictors API and service                                               |
|[API] Program rules           |Zubair Asghar       |Program rules service and API                                            |
|[API] Security                |Morten Svanæs       |Application security, access control and authorization                   |
|[API] Synchronization         |David Katuscak      |Server-to-server synchronization of data and metadata                    |
|[API] System configuration    |Mohamed Ameen       |Configuration including settings and configuration files|
|[API] Tracker                 |Morten Hansen       |Tracked entity and enrollment API and service                            |
|[API] Translations            |Jason Pickering     |User interface and database translations                                 |
|[API] User                    |Mohamed Ameen       |User data model, service and API                                         |
|[API] Validation              |Jim Grace           |Data validation and data quality services                                |
