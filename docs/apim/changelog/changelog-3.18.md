---
title: APIM 3.18.x Changelog
tags:
  - APIM 3.18.x Changelog
  - Changelog
  - Release notes
  - Upgrades
---

# APIM 3.18.x Changelog

This page contains the changelog entries for APIM 3.18.0 and all subsequent minor APIM 3.18.x releases.

# About upgrades

For upgrade instructions, please refer to the [APIM Migration Guide](installation-guide/installation-guide-migration.md).

!!! warning

    **Important:** If you plan to skip versions when you upgrade, ensure that you read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.
    

# APIM - 3.18.17 (2023-01-04)

## API

-   Add a default value in liquibase script when adding a non-nullable
    constraint on `commands` table

# APIM - 3.18.16 (2023-01-04)

## API

-   Handle flow steps order in database
    [\#8805](https://github.com/gravitee-io/issues/issues/8805)

-   Handle query with page number higher than max page with data
    [\#8773](https://github.com/gravitee-io/issues/issues/8773)

# APIM - 3.18.15 (2023-01-03)

## Gateway

-   API key plan was not useable after migration to 3.18
    [\#8762](https://github.com/gravitee-io/issues/issues/8762)

-   Non-explicit "invalid version format: 0" log message fixed
    [\#8754](https://github.com/gravitee-io/issues/issues/8754)

## Management

-   PostgreSQL: management API failed to start after 3.18 migration
    [\#8774](https://github.com/gravitee-io/issues/issues/8774)

-   Import API erased plan general conditions
    [\#8767](https://github.com/gravitee-io/issues/issues/8767)

-   API key revocation raised an error in non-default environment

# APIM - 3.18.14 (2022-12-16)

## General

-   Dynamic property schedule is now updateable
    [\#8529](https://github.com/gravitee-io/issues/issues/8529)

-   Log details no longer fail with closed OAuth 2 or JWT plan
    [\#8685](https://github.com/gravitee-io/issues/issues/8685)

-   Optimized database access when searching APIs

## Gateway

-   Manage multiple accept headers with quality factor

-   Handle SSL configuration in Debug mode
    [\#8711](https://github.com/gravitee-io/issues/issues/8711)

## Management

-   Add `authMethods` choices to be used by the Vert.x mail client of
    the Email Notifier to restrict the choices of authentication methods
    [\#8655](https://github.com/gravitee-io/issues/issues/8655)

-   Properly handle special characters in username
    [\#8673](https://github.com/gravitee-io/issues/issues/8673)

## Console

-   Automatically display api subscriptions when browsing the
    subscription screen
    [\#8739](https://github.com/gravitee-io/issues/issues/8739)

-   Include archived applications in the filters available in the log
    screen [\#8690](https://github.com/gravitee-io/issues/issues/8690)

-   Fix display of log details with closed oauth2 or jwt plan
    [\#8685](https://github.com/gravitee-io/issues/issues/8685)

## Portal

-   Remove untranslated metadata name placeholder
    [\#7235](https://github.com/gravitee-io/issues/issues/7235)

# [APIM - 3.18.13 (2022-11-25)](https://github.com/gravitee-io/issues/milestone/615?closed=1)

## Bug fixes

***Console***

-   Design studio’s debug mode is not working in gateway bridge
    configuration
    [\#8486](https://github.com/gravitee-io/issues/issues/8486)

***General***

-   Merge 3.15.18 into 3.18.x
    [\#8658](https://github.com/gravitee-io/issues/issues/8658)

***Management***

-   Api subscribers resource should return nothing when there is no
    subscriptions.
    [\#8630](https://github.com/gravitee-io/issues/issues/8630)

-   Duplicate users on login when special characters
    [\#8672](https://github.com/gravitee-io/issues/issues/8672)

## Improvements

***Gateway***

-   API Keys Synchronization - Lazy loading mechanism implementation
    [\#8680](https://github.com/gravitee-io/issues/issues/8680)

## Features

***Management***

-   Possibility to override the default background image of the APIM
    Developer Portal from the theme customisation page

## Improvements

***General***

-   Support Inline lists in Expression Language
    [\#7894](https://github.com/gravitee-io/issues/issues/7894)

-   Clearly explain how to have the Portal on a dynamic base url
    [\#8518](https://github.com/gravitee-io/issues/issues/8518).  
    More information
    [here](https://docs.gravitee.io/apim/3.x/apim_installguide_migration.html#console_with_a_custom_base_url)

# [APIM - 3.18.12 (2022-11-04)](https://github.com/gravitee-io/issues/milestone/610?closed=1)

## Bug fixes

***Management***

-   Max clause count set to 1024 error when searching for apis
    [\#8568](https://github.com/gravitee-io/issues/issues/8568)

-   Error when trying get the subscribers to an api
    [\#8567](https://github.com/gravitee-io/issues/issues/8567)

-   Issue when trying to promote API through Cockpit
    [\#8598](https://github.com/gravitee-io/issues/issues/8598)

***Gateway***

-   Accept-Encoding headers should not be deleted from the gateway
    [\#7935](https://github.com/gravitee-io/issues/issues/7935)

-   Incorrect Status Code description when using Response Template
    [\#8613](https://github.com/gravitee-io/issues/issues/8613)

***Policy***

-   \[Cache\] Query parameters should be part of the default cache key
    [\#8366](https://github.com/gravitee-io/issues/issues/8366)

## Features

***Management***

-   Possibility to override the default background image of the APIM
    Developer Portal from the theme customisation page

## Improvements

***General***

-   Clearly explain how to have the Portal on a dynamic base url
    [\#8518](https://github.com/gravitee-io/issues/issues/8518).  
    More information
    [here](https://docs.gravitee.io/apim/3.x/apim_installguide_migration.html#console_with_a_custom_base_url)

# [APIM - 3.18.11 (2022-10-13)](https://github.com/gravitee-io/issues/milestone/603?closed=1)

## Bug fixes

***Gateway***

-   Api key synchronization process consumes too much database resources
    [\#8565](https://github.com/gravitee-io/issues/issues/8565)

***General***

-   DELETE user throw errors when user is member of an API
    [\#8566](https://github.com/gravitee-io/issues/issues/8566)

-   Allow nested EL expressions
    [\#8564](https://github.com/gravitee-io/issues/issues/8564)

# [APIM - 3.18.10 (2022-09-23)](https://github.com/gravitee-io/issues/milestone/600?closed=1)

## Bug fixes

***Gateway***

-   Dedicated implementation for hybrid deployment standalone mode
    [\#8482](https://github.com/gravitee-io/issues/issues/8482)

***Management***

-   Server unreachable when trying to subscribe to APIs
    [\#8496](https://github.com/gravitee-io/issues/issues/8496)

-   Status codes in the dashboard are not sorted in order
    [\#8497](https://github.com/gravitee-io/issues/issues/8497)

# [APIM - 3.18.9 (2022-09-16)](https://github.com/gravitee-io/issues/milestone/598?closed=1)

## Bug fixes

***Console***

-   Design studio’s debug mode is not working in gateway bridge
    configuration
    [\#8373](https://github.com/gravitee-io/issues/issues/8373)

-   Subscription Page can not be displayed when having a lot of
    applications (more than 10k)
    [\#8421](https://github.com/gravitee-io/issues/issues/8421)

***Gateway***

-   Plan selector should throw 401 on wrong API-Key even if a keyless
    plan is available
    [\#8452](https://github.com/gravitee-io/issues/issues/8452)

***General***

-   Regex quantifier wrongly interpreted causing matching issues
    [\#8367](https://github.com/gravitee-io/issues/issues/8367)

***Management***

-   Health check not properly reported as unhealthy if timeout occurs
    when reaching the backend
    [\#8429](https://github.com/gravitee-io/issues/issues/8429)

-   Restore plan selection behavior with multi OAuth plans without
    selection rule
    [\#8460](https://github.com/gravitee-io/issues/issues/8460)

***Portal***

-   Validate button does not work when trying to subscribe to an API
    with general conditions set
    [\#8442](https://github.com/gravitee-io/issues/issues/8442)

## Improvements

***General***

-   Support Inline lists in Expression Language
    [\#7894](https://github.com/gravitee-io/issues/issues/7894)

# [APIM - 3.18.8 (2022-09-07)](https://github.com/gravitee-io/issues/milestone/595?closed=1)

## Bug fixes

***General***

-   Api key repository search method causing OOM error on DocumentDB
    [\#8419](https://github.com/gravitee-io/issues/issues/8419)

***Management***

-   Exported paths based APIs can not be imported
    [\#8365](https://github.com/gravitee-io/issues/issues/8365)

-   \[Debug Mode\] Query params are not well displayed
    [\#7779](https://github.com/gravitee-io/issues/issues/7779)

# [APIM - 3.18.7 (2022-08-31)](https://github.com/gravitee-io/issues/milestone/592?closed=1)

## Bug fixes

***Console***

-   Inconsistent behavior for API out of sync banner
    [\#8343](https://github.com/gravitee-io/issues/issues/8343)

-   User’s list of APIs doesn’t display properly
    [\#8344](https://github.com/gravitee-io/issues/issues/8344)

***Gateway***

-   Improve plan selection based on subscription
    [\#8167](https://github.com/gravitee-io/issues/issues/8167)

***Policy***

-   \[XSLT transformation\] parameter get cached depending on the number
    of gateways
    [\#8387](https://github.com/gravitee-io/issues/issues/8387)

***General***

-   Merge 3.15.14 in 3.18.x
    [\#8355](https://github.com/gravitee-io/issues/issues/8355)

-   Merge 3.15.15 in 3.18.x
    [\#8371](https://github.com/gravitee-io/issues/issues/8371)

# [APIM - 3.18.6 (2022-08-23)](https://github.com/gravitee-io/issues/milestone/585?closed=1)

## Improvements

***General***

-   Improve application search in subscription process -
    [\#8329](https://github.com/gravitee-io/issues/issues/8329)

# [APIM - 3.18.5 (2022-08-17)](https://github.com/gravitee-io/issues/milestone/582?closed=1)

## Bug fixes

***Console***

-   Use correct path in constants.json
    [\#8283](https://github.com/gravitee-io/issues/issues/8283)

-   When dragging Json to XML policy in Design Studio, Save button is
    not displayed
    [\#8227](https://github.com/gravitee-io/issues/issues/8227)

***Management***

-   Application client\_id update is ignored
    [\#8278](https://github.com/gravitee-io/issues/issues/8278)

-   NullPointerException when deleting a group
    [\#8320](https://github.com/gravitee-io/issues/issues/8320)

-   Platform alerts never triggered
    [\#8269](https://github.com/gravitee-io/issues/issues/8269)

-   Temporary allow `null` value for host in virtual-hosts
    [\#8300](https://github.com/gravitee-io/issues/issues/8300)

***Portal***

-   Unable to refresh a page when deploying with Docker
    [\#8317](https://github.com/gravitee-io/issues/issues/8317)

***Reporters***

-   File and TCP reporters - filtering feature not fully implemented for
    headers [\#8226](https://github.com/gravitee-io/issues/issues/8226)

## Features

***Console***

-   Disable in-app documentation when Pendo is activated
    [\#8292](https://github.com/gravitee-io/issues/issues/8292)

## Improvements

***Management***

-   Global performances improvement of GET /applications
    [\#7836](https://github.com/gravitee-io/issues/issues/7836)

# [APIM - 3.18.4 (2022-08-02)](https://github.com/gravitee-io/issues/milestone/578?closed=1)

## Bug fixes

***General***

-   Error while trying to connect using IDP with group mapping
    [\#8205](https://github.com/gravitee-io/issues/issues/8205)

-   Merge APIM `3.17.5` into `3.18.x`
    [\#8265](https://github.com/gravitee-io/issues/issues/8265)

## Features

***General***

-   Add `gateway-bridge-http-server` to the APIM REST API bundle
    [\#8133](https://github.com/gravitee-io/issues/issues/8133)

# [APIM - 3.18.3 (2022-07-20)](https://github.com/gravitee-io/issues/milestone/574?closed=1)

## Bug fixes

***Management***

-   Handle Pendo ApiKey with correct attribute in `gravitee.yaml`
    [\#8155](https://github.com/gravitee-io/issues/issues/8155)

-   Mongodb migrations scripts fails
    [\#8147](https://github.com/gravitee-io/issues/issues/8147)

-   Management API fails to start if API without primary
    [\#8130](https://github.com/gravitee-io/issues/issues/8130)

# [APIM - 3.18.2 (2022-07-15)](https://github.com/gravitee-io/issues/milestone/571?closed=1)

## Bug fixes

***Management***

-   Can’t login when using JDBC database
    [\#8110](https://github.com/gravitee-io/issues/issues/8110)

# [APIM - 3.18.1 (2022-07-08)](https://github.com/gravitee-io/issues/milestone/564?closed=1)

## Bug fixes

***Gateway***

-   file reporter log files are not created
    [\#8065](https://github.com/gravitee-io/issues/issues/8065)

***General***

-   Update build version number of Console and Portal
    [\#8072](https://github.com/gravitee-io/issues/issues/8072)

***Portal***

-   OpenAPI specification of the Portal API not available
    [\#8074](https://github.com/gravitee-io/issues/issues/8074)

# [APIM - 3.18.0 (2022-07-07)](https://github.com/gravitee-io/issues/milestone/519?closed=1)

## Bug fixes

***Console***

-   Remove the horizontal scroll bar in the markdown creation page
    [\#5119](https://github.com/gravitee-io/issues/issues/5119)

-   Wrong example when generating Personal Access Token
    [\#5271](https://github.com/gravitee-io/issues/issues/5271)

-   Not\_equals alert filter displays an empty list
    [\#7489](https://github.com/gravitee-io/issues/issues/7489)

-   Icons not rendering with custom nginx configuration
    [\#7569](https://github.com/gravitee-io/issues/issues/7569)

***General***

-   Merge 3.17.2 into master
    [\#7617](https://github.com/gravitee-io/issues/issues/7617)

***Management***

-   DCR providers should be scoped by org
    [\#6604](https://github.com/gravitee-io/issues/issues/6604)

-   One shot upgraders run on each APIM startup with cockpit
    [\#7450](https://github.com/gravitee-io/issues/issues/7450)

-   OpenApi files are never updated
    [\#7631](https://github.com/gravitee-io/issues/issues/7631)

***Policies***

-   Retry Policy: cancel timeout response, manage lastResponse counter
    and tests
    [\#7747](https://github.com/gravitee-io/issues/issues/7747)

-   Data Logging Masking: fix some bugs
    [\#7758](https://github.com/gravitee-io/issues/issues/7758)

## Features

***Console***

-   Promote API Designer
    [\#7645](https://github.com/gravitee-io/issues/issues/7645)

-   Add Pendo analytics tool
    [\#7781](https://github.com/gravitee-io/issues/issues/7781)

***General***

-   Support of RHEL8
    [\#7208](https://github.com/gravitee-io/issues/issues/7208)

***Management***

-   Partial update - PATCH method on Import API
    [\#7443](https://github.com/gravitee-io/issues/issues/7443)

-   Add page to display organization Audit
    [\#7536](https://github.com/gravitee-io/issues/issues/7536)

***Policies***

-   Transform-Header: Define headers based on the request or on the
    response payload
    [\#7359](https://github.com/gravitee-io/issues/issues/7359)

-   Circuit Breaker: Write documentation for policy
    [\#7756](https://github.com/gravitee-io/issues/issues/7756)

## Improvements

***Console***

-   API properties header title change
    [\#6065](https://github.com/gravitee-io/issues/issues/6065)

-   Add Conditional icon in legend
    [\#7457](https://github.com/gravitee-io/issues/issues/7457)

***General***

-   Mutualize System proxy configuration
    [\#7739](https://github.com/gravitee-io/issues/issues/7739)

***Portal***

-   Migrate to last Angular version
    [\#6666](https://github.com/gravitee-io/issues/issues/6666)
