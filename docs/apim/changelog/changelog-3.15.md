---
title: APIM 3.15.x changelog
tags:
  - APIM 3.15.x changelog
  - Changelog
  - Release notes
  - Upgrades
---

# APIM 3.15.x changelog

This page contains the changelog entries for APIM 3.15.0 and all subsequent minor APIM 3.15.x releases.

# About upgrades

For upgrade instructions, please refer to the [APIM Migration Guide](installation-guide/installation-guide-migration.md).

!!! warning

    **Important:** If you plan to skip versions when you upgrade, ensure that you read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.

# APIM - 3.15.21 (2023-01-04)

## API

-   Handle flow steps order in database.
    [\#8805](https://github.com/gravitee-io/issues/issues/8805)

# APIM - 3.15.20 (2023-01-03)

## Gateway

-   Json HTTP error message writing ignores multiple types in Accept
    header

## Console

-   \[Policy XSLT\] Prevent usage of external XML DTD

-   Add a default value in the HTTP Methods field of Dynamic
    Dictionaries and Properties
    [\#8631](https://github.com/gravitee-io/issues/issues/8631)

# APIM - 3.15.19 (2022-12-09)

## Bug fixes

***General***

-   Handle auth methods in mail configuration
    [\#8655](https://github.com/gravitee-io/issues/issues/8655)

***Portal***

-   In the metadata tab the field for name is not in English
    [\#7235](https://github.com/gravitee-io/issues/issues/7235)

***Management***

-   Duplicate users on login when special characters in username
    [\#8673](https://github.com/gravitee-io/issues/issues/8673)

# [APIM - 3.15.18 (2022-11-18)](https://github.com/gravitee-io/issues/milestone/614?closed=1)

## Bug fixes

***General***

-   SpEL in endpoint isn’t evaluated
    [\#8639](https://github.com/gravitee-io/issues/issues/8639)

***Management***

-   Error when accessing gateway instance info
    [\#8635](https://github.com/gravitee-io/issues/issues/8635)

-   Max clause count set to 1024 error when searching for apis
    [\#8568](https://github.com/gravitee-io/issues/issues/8568)

***Gateway***

-   Health check not properly reported as unhealthy if timeout occurs
    when reaching the backend
    [\#8510](https://github.com/gravitee-io/issues/issues/8510)

# [APIM - 3.15.17 (2022-11-07)](https://github.com/gravitee-io/issues/milestone/610?closed=1)

## Bug fixes

***General***

-   Regex quantifier wrongly interpreted causing matching issues
    [\#8367](https://github.com/gravitee-io/issues/issues/8367)

-   Allow nested EL expressions
    [\#8564](https://github.com/gravitee-io/issues/issues/8564)

***Management***

-   API primary owner is mandatory, and always set
    [\#8162](https://github.com/gravitee-io/issues/issues/8162)

-   Restore plan selection behavior with multi OAuth plans without
    selection rule
    [\#8460](https://github.com/gravitee-io/issues/issues/8460)

-   Issue when trying to promote API through Cockpit
    [\#8598](https://github.com/gravitee-io/issues/issues/8598)

***Gateway***

-   Dedicated implementation for hybrid deployment standalone mode
    [\#8482](https://github.com/gravitee-io/issues/issues/8482)

-   Plan selector should throw 401 on wrong API-Key even if a keyless
    plan is available
    [\#8452](https://github.com/gravitee-io/issues/issues/8452)

-   Accept-Encoding headers should not be deleted from the gateway
    [\#7935](https://github.com/gravitee-io/issues/issues/7935)

***Policy*** - \[Cache\] Query parameters should be part of the default
cache key [\#8366](https://github.com/gravitee-io/issues/issues/8366)

# [APIM - 3.15.16 (2022-09-09)](https://github.com/gravitee-io/issues/milestone/596?closed=1)

## Bug fixes

***Gateway***

-   Apply request timeout properly
    [\#8400](https://github.com/gravitee-io/issues/issues/8400)

-   Heartbeat service isn’t working anymore
    [\#8417](https://github.com/gravitee-io/issues/issues/8417)

***General***

-   Pagination broken in organization settings
    [\#8346](https://github.com/gravitee-io/issues/issues/8346)

***Policy***

-   \[XSLT\] XSLT parameter get cached depending on the number of
    gateways [\#8382](https://github.com/gravitee-io/issues/issues/8382)

-   \[Cache\] Strange behavior when policy cache TTL is higher than
    resource cache TTL
    [\#7907](https://github.com/gravitee-io/issues/issues/7907)

-   \[Oauth2\] Error when token expiration is greater then cache TTL
    [\#8295](https://github.com/gravitee-io/issues/issues/8295)

# [APIM - 3.15.15 (2022-08-29)](https://github.com/gravitee-io/issues/milestone/588?closed=1)

## Bug fixes

***General***

-   JWT plan causes gateway error 500
    [\#8364](https://github.com/gravitee-io/issues/issues/8364)

# [APIM - 3.15.14 (2022-08-25)](https://github.com/gravitee-io/issues/milestone/586?closed=1)

## Bug fixes

***Console***

-   Analytics - Filters for status codes do not work for the Platform
    Dashboard for the Line Chart (Response status)
    [\#8325](https://github.com/gravitee-io/issues/issues/8325)

-   Analytics - Label issue in the dashboards
    [\#8327](https://github.com/gravitee-io/issues/issues/8327)

-   Analytics - Top APIs and Top Applications links are not working
    [\#8328](https://github.com/gravitee-io/issues/issues/8328)

-   Navigation - The right click menu links does not work properly.
    [\#8326](https://github.com/gravitee-io/issues/issues/8326)

-   Organisation Settings - Wrong confirmation message displayed when
    activating/deactivating an identity provider
    [\#7774](https://github.com/gravitee-io/issues/issues/7774)

-   NullPointerException when deleting a group
    [\#8323](https://github.com/gravitee-io/issues/issues/8323)

-   Unable to use prefix for mongodb collections when running with Java
    17 [\#7918](https://github.com/gravitee-io/issues/issues/7918)

***Gateway***

-   JDBC - Quota and RateLimit Platform Policies do not work as
    expected. X-Quota-Reset header returns -1
    [\#7975](https://github.com/gravitee-io/issues/issues/7975)

-   File reporter headers format feature
    [\#8305](https://github.com/gravitee-io/issues/issues/8305)

-   Websocket connection error when reaching a non secure endpoint
    [\#8228](https://github.com/gravitee-io/issues/issues/8228)

-   Websocket subprotocol not forwarded to the endpoint
    [\#8324](https://github.com/gravitee-io/issues/issues/8324)

-   Improve plan selection based on subscription
    [\#8165](https://github.com/gravitee-io/issues/issues/8165)

***General***

-   Unable to evaluate regex with quantifiers
    [\#8217](https://github.com/gravitee-io/issues/issues/8217)

-   Merge 3.10.19 in 3.15.x
    [\#8279](https://github.com/gravitee-io/issues/issues/8279)

***Policy***

-   \[openid-connect-userinfo\] Gateway never responds in case of
    invalid oauth token
    [\#6883](https://github.com/gravitee-io/issues/issues/6883)

***Portal***

-   404 on trendings page
    [\#8341](https://github.com/gravitee-io/issues/issues/8341)

# [APIM - 3.15.13 (2022-07-27)](https://github.com/gravitee-io/issues/milestone/575?closed=1)

## Bug fixes

***APIM***

-   In version 3.15.9 the display of healthcheck logs is broken
    [\#7841](https://github.com/gravitee-io/issues/issues/7841)

***Gateway***

-   \[expression-language\] String Condition Evaluator not work as
    expected [\#8153](https://github.com/gravitee-io/issues/issues/8153)

***General***

-   Improve email template sanitization
    [\#8093](https://github.com/gravitee-io/issues/issues/8093)

***Reporters***

-   RetainDays configuration of file reporter is inaccurate
    [\#8090](https://github.com/gravitee-io/issues/issues/8090)

# [APIM - 3.15.12 (2022-07-08)](https://github.com/gravitee-io/issues/milestone/565?closed=1)

## Bug fixes

***Gateway***

-   Log file are not created
    [\#8064](https://github.com/gravitee-io/issues/issues/8064)

# [APIM - 3.15.11 (2022-07-01)](https://github.com/gravitee-io/issues/milestone/561?closed=1)

## Bug fixes

***APIM***

-   Not able to fully import an API, issue related to the default page
    (System Folder)
    [\#7876](https://github.com/gravitee-io/issues/issues/7876)

***General***

-   Portal - Filtering by a certain Category on All APIs page will
    return all existing APIs
    [\#7201](https://github.com/gravitee-io/issues/issues/7201)

***Management***

-   Healthcheck is failing to report in ES due to issue on headers.
    [\#7930](https://github.com/gravitee-io/issues/issues/7930)

# [APIM - 3.15.10 (2022-06-28)](https://github.com/gravitee-io/issues/milestone/559?closed=1)

## Bug fixes

***APIM***

-   ApiPrimaryOwner property of a group disappears when the group is
    updated through console/api call
    [\#7448](https://github.com/gravitee-io/issues/issues/7448)

-   CORS no longer read only if configured in .yml file
    [\#7326](https://github.com/gravitee-io/issues/issues/7326)

***APIM-EL***

-   ExpesionLanguage query used to work but it no longer does in newer
    versions.
    [\#7754](https://github.com/gravitee-io/issues/issues/7754)

***Gateway***

-   503 errors may occur when redeploying an api
    [\#6948](https://github.com/gravitee-io/issues/issues/6948)

-   API gateway\_ip:18082/\_node/apis/api.id not working, return 500
    error [\#7287](https://github.com/gravitee-io/issues/issues/7287)

-   Gateway does not start if openssl is enabled
    [\#7742](https://github.com/gravitee-io/issues/issues/7742)

-   Handle client side sse connection close
    [\#7573](https://github.com/gravitee-io/issues/issues/7573)

***General***

-   500 error when accessing user api details in organization settings
    category issue on JDBC
    [\#7882](https://github.com/gravitee-io/issues/issues/7882)

-   APIM Connection with Google connect fails
    [\#7743](https://github.com/gravitee-io/issues/issues/7743)

-   Groovy policy error on HTTP headers (backport of 3.17)
    [\#7811](https://github.com/gravitee-io/issues/issues/7811)

-   HTTP headers breaking changes from 3.15
    [\#7812](https://github.com/gravitee-io/issues/issues/7812)

-   Merge 3.10.17 in 3.15.x
    [\#7867](https://github.com/gravitee-io/issues/issues/7867)

***Management***

-   Service discovery Healthcheck isn’t working
    [\#7533](https://github.com/gravitee-io/issues/issues/7533)

***Policy***

-   Cache Policy cache not cleared/refreshed after Time to Live
    [\#7740](https://github.com/gravitee-io/issues/issues/7740)

***Reporter***

-   File reporter log files are missing headers details
    [\#7741](https://github.com/gravitee-io/issues/issues/7741)

# [APIM - 3.15.9 (2022-06-01)](https://github.com/gravitee-io/issues/milestone/551?closed=1)

## Bug fixes

***APIM***

-   Errors while creating Platform Policies.
    [\#7547](https://github.com/gravitee-io/issues/issues/7547)

-   Transfer ownership option is not available to in memory org admin
    (in memory admin) if primary owner is another user.
    [\#7430](https://github.com/gravitee-io/issues/issues/7430)

***Console***

-   APIs not showing on a selected user page when the group they are in
    is updated.
    [\#7285](https://github.com/gravitee-io/issues/issues/7285)

-   Platform Policies/Flow→Save button stays enabled even after saving
    the flow [\#7651](https://github.com/gravitee-io/issues/issues/7651)

***General***

-   Cannot connect to APIM from Cockpit
    [\#7773](https://github.com/gravitee-io/issues/issues/7773)

-   Error NullPointerException when executing code in Javascript policy
    On-request content script
    [\#7179](https://github.com/gravitee-io/issues/issues/7179)

-   Merge 3.10.15 in 3.15.x
    [\#7749](https://github.com/gravitee-io/issues/issues/7749)

***Management***

-   Auto fetch of documentation is not working
    [\#7589](https://github.com/gravitee-io/issues/issues/7589)

-   Dynamic properties API out of sync
    [\#7269](https://github.com/gravitee-io/issues/issues/7269)

-   When dynamic properties are triggered to update, the API status
    change to out of sync and the front ask for deploy.
    [\#5245](https://github.com/gravitee-io/issues/issues/5245)

-   \[RepositoryJDBC\] Error when trying to create flow with policy on
    organization level
    [\#7399](https://github.com/gravitee-io/issues/issues/7399)

***Portal***

-   How to disable metrics on the APIM Portal?
    [\#7231](https://github.com/gravitee-io/issues/issues/7231)

# [APIM - 3.15.8 (2022-04-27)](https://github.com/gravitee-io/issues/milestone/542?closed=1)

## Bug fixes

***APIM***

-   Policies (or flow) are getting ignored when best match is used in
    flow mode
    [\#7472](https://github.com/gravitee-io/issues/issues/7472)

***Gateway***

-   Analytics in UI stopped working after updating gateway to version
    3.15.5 [\#7288](https://github.com/gravitee-io/issues/issues/7288)

-   Conditional logging on Application prevents to display API logs
    [\#7329](https://github.com/gravitee-io/issues/issues/7329)

***General***

-   Merge 3.10.14 in 3.15.x
    [\#7570](https://github.com/gravitee-io/issues/issues/7570)

***Management***

-   Backport \#7450 on 3.15 One shot upgraders run on each APIM startup
    with cockpit
    [\#7453](https://github.com/gravitee-io/issues/issues/7453)

***Migration***

-   Null pointer exception for old started gateways
    [\#7277](https://github.com/gravitee-io/issues/issues/7277)

## Improvements

***Upgrader***

-   Deploy APIs that gets out of sync by upgrader
    [\#7511](https://github.com/gravitee-io/issues/issues/7511)

# [APIM - 3.15.7 (2022-04-04)](https://github.com/gravitee-io/issues/milestone/535?closed=1)

## Bug fixes

***General***

-   Merge 3.10.13
    [\#7444](https://github.com/gravitee-io/issues/issues/7444)

***APIM***

-   Content not read from JKS and PKCS12 Certificates(Binary Content) in
    Group Endpoint Configuration
    [\#7405](https://github.com/gravitee-io/issues/issues/7405)

***Data-masking-policy***

-   Data masking policy at platform level is not masking data
    [\#7022](https://github.com/gravitee-io/issues/issues/7022)

***Management***

-   "Host" header not overwritten if redefined in Endpoint configuration
    [\#7007](https://github.com/gravitee-io/issues/issues/7007)

# [APIM - 3.15.6 (2022-03-24)](https://github.com/gravitee-io/issues/milestone/529?closed=1)

## Bug fixes

***Console***

-   Contextual Docs no longer works
    [\#7323](https://github.com/gravitee-io/issues/issues/7323)

-   Secondary endpoint feature not working/switching if the Health-check
    is down on the primary endpoint.
    [\#7135](https://github.com/gravitee-io/issues/issues/7135)

***Gateway***

-   Gateway only keeps last set-Cookie header from backend response even
    with different cookie-names
    [\#7325](https://github.com/gravitee-io/issues/issues/7325)

***General***

-   Dictionaries no longer work in expressions
    [\#7303](https://github.com/gravitee-io/issues/issues/7303)

-   Javascript policy input box is only showing a few lines and not the
    whole code
    [\#7028](https://github.com/gravitee-io/issues/issues/7028)

-   Json is only partially visible in editor under API Documentaiton
    [\#7116](https://github.com/gravitee-io/issues/issues/7116)

-   Let the API Owner choose the Accept-Encoding
    [\#6967](https://github.com/gravitee-io/issues/issues/6967)

-   Merge 3.10.12 in 3.15.x
    [\#7363](https://github.com/gravitee-io/issues/issues/7363)

-   Support DocumentDB index name constraints
    [\#7134](https://github.com/gravitee-io/issues/issues/7134)

***Management***

-   Application subscriptions API keys buttons are not visible
    [\#7273](https://github.com/gravitee-io/issues/issues/7273)

***Policy Groovy***

-   Cannot iterate on Map with entry and trim on GStringImpl
    [\#7302](https://github.com/gravitee-io/issues/issues/7302)

***Policy JavaScript***

-   Allows to break request/response on content phase
    [\#7173](https://github.com/gravitee-io/issues/issues/7173)

# [APIM - 3.15.5 (2022-03-09)](https://github.com/gravitee-io/issues/milestone/524?closed=1)

## Bug fixes

***Gateway***

-   Health check does not pull out unhealthy endpoints
    [\#7250](https://github.com/gravitee-io/issues/issues/7250)

# [APIM - 3.15.4 (2022-03-07)](https://github.com/gravitee-io/issues/milestone/523?closed=1)

## Bug fixes

***APIM***

-   Condition generated automatically when maximum time limit is set in
    API logging does not work
    [\#7205](https://github.com/gravitee-io/issues/issues/7205)

-   \[policy-basic-authentication\] Error message is received when using
    basic authentication policy
    [\#7198](https://github.com/gravitee-io/issues/issues/7198)

***General***

-   Merge 3.14.1 in 3.15.x
    [\#7162](https://github.com/gravitee-io/issues/issues/7162)

***Management***

-   OAS - servers without basepath make import fail
    [\#7227](https://github.com/gravitee-io/issues/issues/7227)

***Metrics-reporter-policy***

-   Metrics reporting not done at the good time
    [\#7194](https://github.com/gravitee-io/issues/issues/7194)

***Resource-cache-redis***

-   User cannot save configuration
    [\#7172](https://github.com/gravitee-io/issues/issues/7172)

## Features

***Expression-language***

-   Improve map access with dot
    [\#7228](https://github.com/gravitee-io/issues/issues/7228)

# [APIM - 3.15.3 (2022-02-07)](https://github.com/gravitee-io/issues/milestone/507?closed=1)

## Bug fixes

***Gateway***

-   Error on API deployment on environment without HrId
    [\#7053](https://github.com/gravitee-io/issues/issues/7053)

***Management***

-   Image not found when sending a email
    [\#7057](https://github.com/gravitee-io/issues/issues/7057)

-   Can’t get API plans on JDBC when API has no category
    [\#7060](https://github.com/gravitee-io/issues/issues/7060)

-   SQL error on subscription with PostgreSQL or MsSql
    [\#7051](https://github.com/gravitee-io/issues/issues/7051)

# [APIM - 3.15.2 (2022-02-03)](https://github.com/gravitee-io/issues/milestone/506?closed=1)

## Bug fixes

***Platform***

-   IllegalArgumentException unsupported cipher suite when enforcing tls
    protocols
    [\#7038](https://github.com/gravitee-io/issues/issues/7038)

# [APIM - 3.15.1 (2022-01-31)](https://github.com/gravitee-io/issues/milestone/504?closed=1)

## Bug fixes

***Management***

-   \[policy\] Rest-to-Soap doesn’t work anymore
    [\#7025](https://github.com/gravitee-io/issues/issues/7025)

# [APIM - 3.15.0 (2022-01-27)](https://github.com/gravitee-io/issues/milestone/350?closed=1)

## Bug fixes

***General***

-   Raise error if update API try to update an existing plan belonging
    to another API
    [\#6693](https://github.com/gravitee-io/issues/issues/6693)

-   Use provided page ID when updating API
    [\#6694](https://github.com/gravitee-io/issues/issues/6694)

-   Kubernetes certificate not working with kubernetes &gt;= 1.20
    [\#6906](https://github.com/gravitee-io/issues/issues/6906)

## Features

***Gateway***

-   Performances improvements
    [\#6492](https://github.com/gravitee-io/issues/issues/6492)

***General***

-   API Path-based creation deprecation
    [\#6377](https://github.com/gravitee-io/issues/issues/6377)

***Platform***

-   Update Dockerfile for java 17 support
    [\#6930](https://github.com/gravitee-io/issues/issues/6930)

-   Support for Java 17 runtime
    [\#6708](https://github.com/gravitee-io/issues/issues/6708)

***Policies Management***

-   Conditional policies
    [\#6629](https://github.com/gravitee-io/issues/issues/6629)

-   Add a condition for execution
    [\#6614](https://github.com/gravitee-io/issues/issues/6614)

-   View if a policy is conditional
    [\#6615](https://github.com/gravitee-io/issues/issues/6615)

-   View if a flow is conditional
    [\#6626](https://github.com/gravitee-io/issues/issues/6626)

***Portal alerts***

-   Add a description field for alert
    [\#6803](https://github.com/gravitee-io/issues/issues/6803)

-   Allow alert configuration by API
    [\#6702](https://github.com/gravitee-io/issues/issues/6702)

-   Allow alert notification via webhook
    [\#6703](https://github.com/gravitee-io/issues/issues/6703)
