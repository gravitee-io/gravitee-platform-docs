---
title: APIM pre-3.15.x changelog
tags:
  - APIM pre-3.15.x changelog
  - Changelog
  - Release notes
  - Upgrades
  - End-of-support versions
---

# APIM pre-3.15.x changelog

This page contains the changelog entries for APIM 3.19.0 and all subsequent minor APIM 3.19.x releases.

# About upgrades

For upgrade instructions, please refer to the [APIM Migration Guide](installation-guide/installation-guide-migration.md).

!!! warning

    **Important:** If you plan to skip versions when you upgrade, ensure that you read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.



# APIM - 3.10.21 (2022-09-16)

## Improvements

***Gateway***

-   We have added a new property that enables you to configure the
    worker pool size of the HTTP handlers in Bridge mode. To do so, set
    the desired size using the `services.bridge.http.workerPoolSize`
    property (the default value is `20`) and ensure that it is set on
    the Gateway Bridge Server side.

## Bug fixes

***Management***

-   Restore plan selection to the behavior it had in APIM 3.10.18 and
    lower.

# [APIM - 3.17.6 (2022-08-03)](https://github.com/gravitee-io/issues/milestone/580?closed=1)

## Bug fixes

***Management***

-   Application client\_id update is ignored
    [\#8281](https://github.com/gravitee-io/issues/issues/8281)

## General information

The version 3.17.6 is the last version of the 3.17. We encourage
everybody to migrate to 3.18. == [APIM - 3.10.19
(2022-08-03)](https://github.com/gravitee-io/issues/milestone/579?closed=1)

## Bug fixes

***Console***

-   An error is displayed when trying to send a message to Users, Owners
    and Application Read only
    [\#7253](https://github.com/gravitee-io/issues/issues/7253)

-   Link to my account is broken in org settings
    [\#6848](https://github.com/gravitee-io/issues/issues/6848)

-   Subscription pull-down menu displays APIs the user doesn’t have
    access to
    [\#7890](https://github.com/gravitee-io/issues/issues/7890)

***Gateway***

-   Heartbeat service do not handle database and timeout exceptions
    [\#8267](https://github.com/gravitee-io/issues/issues/8267)

***Management***

-   Better select plan based on subscription
    [\#7824](https://github.com/gravitee-io/issues/issues/7824)

-   Improve email template sanitization
    [\#8163](https://github.com/gravitee-io/issues/issues/8163)

-   Information button on Dictionary doesn’t display anything
    [\#5056](https://github.com/gravitee-io/issues/issues/5056)

-   Restore an application with an existing clientId create duplication
    [\#6380](https://github.com/gravitee-io/issues/issues/6380)

***Policy***

-   OpenId Connect - UserInfo - Do not use payload in header
    [\#7915](https://github.com/gravitee-io/issues/issues/7915)

***Regex-threat-support-policy***

-   Policy failed silently on a call with a boolean parameter
    [\#8272](https://github.com/gravitee-io/issues/issues/8272)

## Improvements

***Console***

-   Login form error handling, when login with no environment
    permissions
    [\#6532](https://github.com/gravitee-io/issues/issues/6532)

## General information

The version 3.10.19 is the last version of the 3.10. We encourage
everybody to migrate to 3.18. == [APIM - 3.17.5
(2022-08-01)](https://github.com/gravitee-io/issues/milestone/577?closed=1)

## Bug fixes

***Console***

-   Closed subscription is displayed as still subscribed
    [\#7879](https://github.com/gravitee-io/issues/issues/7879)

-   Debug mode join multi value headers
    [\#7809](https://github.com/gravitee-io/issues/issues/7809)

***General***

-   Log file are not created
    [\#8066](https://github.com/gravitee-io/issues/issues/8066)

-   Merge 3.16.4 in 3.17.x
    [\#7869](https://github.com/gravitee-io/issues/issues/7869)

-   Merge 3.15.13 into 3.17.x
    [\#8225](https://github.com/gravitee-io/issues/issues/8225)

***Management***

-   Update a role API requires an `id` field when this is not
    necessary/required based on the doc
    [\#7661](https://github.com/gravitee-io/issues/issues/7661)

***Policies***

-   Groovy policy error on HTTP headers
    [\#7810](https://github.com/gravitee-io/issues/issues/7810)

-   Truncated `request.content` in Callout Http Policy when body
    contains accents
    [\#8109](https://github.com/gravitee-io/issues/issues/8109)

## Features

***Node***

-   Expose endpoints for retrieving heap dump and thread dump
    [\#8222](https://github.com/gravitee-io/issues/issues/8222) ==
    [APIM - 3.10.18
    (2022-07-20)](https://github.com/gravitee-io/issues/milestone/573?closed=1)

## Bug fixes

***Console***

-   Listening host in virtual-host mode is changed to *null* when saving
    [\#7856](https://github.com/gravitee-io/issues/issues/7856)

***Management***

-   Application update removes Oauth client data if DCR unreachable
    [\#7953](https://github.com/gravitee-io/issues/issues/7953)

-   Fixed API import process failing when creating member roles
    [\#7822](https://github.com/gravitee-io/issues/issues/7822)

-   Subscription created without API Key
    [\#7332](https://github.com/gravitee-io/issues/issues/7332)

-   Fixed the display of healthcheck logs (backport of 3.15)
    [\#8107](https://github.com/gravitee-io/issues/issues/8107) ==
    [APIM - 3.17.4
    (2022-07-05)](https://github.com/gravitee-io/issues/milestone/562?closed=1)

## Bug fixes

***APIM***

-   API alerts do not show in analytics
    [\#7480](https://github.com/gravitee-io/issues/issues/7480)

***General***

-   Merge 3.16.5 in 3.17.x
    [\#7787](https://github.com/gravitee-io/issues/issues/7787) ==
    [APIM - 3.16.5
    (2022-07-04)](https://github.com/gravitee-io/issues/milestone/560?closed=1)

## Bug fixes

***General***

-   Merge 3.15.10 in 3.16.x
    [\#7868](https://github.com/gravitee-io/issues/issues/7868)

-   Merge 3.15.11 in 3.16.x
    [\#7961](https://github.com/gravitee-io/issues/issues/7961) ==
    [APIM - 3.10.17
    (2022-06-24)](https://github.com/gravitee-io/issues/milestone/558?closed=1)

## Bug fixes

***Console***

-   BestMatch Flow mode does not work for Platform flow
    [\#7625](https://github.com/gravitee-io/issues/issues/7625)

***Gateway***

-   Service Discovery error when configured with more than one API
    [\#7821](https://github.com/gravitee-io/issues/issues/7821)

***General***

-   Update Logback library
    [\#7837](https://github.com/gravitee-io/issues/issues/7837)

***Management***

-   Can Transfer Ownership via cURL or Postman where there is no Primary
    Owner in the Group.
    [\#6994](https://github.com/gravitee-io/issues/issues/6994)

-   Regression in API imports
    [\#7807](https://github.com/gravitee-io/issues/issues/7807)

***Repository***

-   \[JDBC\] Api disappears for all users including org admin when group
    default role is changed to non primary\_owner
    [\#7428](https://github.com/gravitee-io/issues/issues/7428)

# [APIM - 3.10.16 (2022-06-13)](https://github.com/gravitee-io/issues/milestone/556?closed=1)

## Bug fixes

***Gateway***

-   Filter disabled flows and flows steps
    [\#7794](https://github.com/gravitee-io/issues/issues/7794)

-   Hazelcast is referring to a queue but get a topic
    [\#7681](https://github.com/gravitee-io/issues/issues/7681)

-   Headers are not forwarded to websocket upstream
    [\#7750](https://github.com/gravitee-io/issues/issues/7750)

-   OOM when heartbeat event can’t be delivered
    [\#7806](https://github.com/gravitee-io/issues/issues/7806)

-   OOM in case of Connect timeouts in health-check
    [\#7709](https://github.com/gravitee-io/issues/issues/7709)

-   Max logging size must accept smaller size than MB
    [\#7761](https://github.com/gravitee-io/issues/issues/7761)

-   ElasticSearch indexing data is getting out of bounds on Server Sent
    Event APIs (api-response-time)
    [\#7094](https://github.com/gravitee-io/issues/issues/7094)

***Repositories***

-   Switch implementation to IO thread
    [\#7682](https://github.com/gravitee-io/issues/issues/7682)

# [APIM - 3.10.15 (2022-05-25)](https://github.com/gravitee-io/issues/milestone/550?closed=1)

## Bug fixes

***Console***

-   Alert not correctly displayed/saved
    [\#6705](https://github.com/gravitee-io/issues/issues/6705)

-   An organization user (and environnement admin) can’t delete a
    dictionary he has created
    [\#6556](https://github.com/gravitee-io/issues/issues/6556)

-   Count function, when saving alert, not saved properly
    [\#7279](https://github.com/gravitee-io/issues/issues/7279)

-   Error in console when opening APIM Console
    [\#7737](https://github.com/gravitee-io/issues/issues/7737)

-   Padding issue on content of some Console screen
    [\#7738](https://github.com/gravitee-io/issues/issues/7738)

***Gateway***

-   Connexion not closed with Server Sent Event APIs
    [\#7093](https://github.com/gravitee-io/issues/issues/7093)

-   Elasticsearch ilm index\_mode is missing rollover\_alias and first
    index is not created
    [\#7110](https://github.com/gravitee-io/issues/issues/7110)

-   First dynamic dictionary start causes an IllegalArgumentException on
    the gateway
    [\#6044](https://github.com/gravitee-io/issues/issues/6044)

***General***

-   Error when importing an API without logging on an env with
    `Logging audit events` activated
    [\#7612](https://github.com/gravitee-io/issues/issues/7612)

***Management***

-   Allow to use System Proxy on Generic Oauth2 resource as already
    present for AM resource
    [\#7258](https://github.com/gravitee-io/issues/issues/7258)

-   Can’t update a dynamic dictionary
    [\#6043](https://github.com/gravitee-io/issues/issues/6043)

-   Cannot import APi with primary owner of type group and empty members
    list in group mode
    [\#6808](https://github.com/gravitee-io/issues/issues/6808)

-   Dynamic Property does not get updated after it was created
    [\#7684](https://github.com/gravitee-io/issues/issues/7684)

-   Error while deleting a user
    [\#7613](https://github.com/gravitee-io/issues/issues/7613)

-   Fix EnvironmentNotFoundException for task
    [\#7635](https://github.com/gravitee-io/issues/issues/7635)

-   Issue when deleting the properties of a dictionary
    [\#6996](https://github.com/gravitee-io/issues/issues/6996)

-   Logging condition with timestamp returns status 500
    [\#7367](https://github.com/gravitee-io/issues/issues/7367)

-   Wrong log audit date for refresh dictionary events
    [\#6045](https://github.com/gravitee-io/issues/issues/6045)

***Portal***

-   Delete/remove member button does not work
    [\#7241](https://github.com/gravitee-io/issues/issues/7241)

-   Unable to reply to a rating
    [\#6869](https://github.com/gravitee-io/issues/issues/6869)

## Improvements

***Management***

-   Add Secure Flag by default on each cookie
    [\#7725](https://github.com/gravitee-io/issues/issues/7725)

# [APIM - 3.17.3 (2022-05-12)](https://github.com/gravitee-io/issues/milestone/546?closed=1)

## Bug fixes

***General***

-   Cannot connect to APIM from Cockpit
    [\#7649](https://github.com/gravitee-io/issues/issues/7649)

***Management***

-   Mongodb queries fail when encountering a document with a field set
    to `undefined`
    [\#7610](https://github.com/gravitee-io/issues/issues/7610)

# [APIM - 3.17.2 (2022-05-03)](https://github.com/gravitee-io/issues/milestone/545?closed=1)

## Bug fixes

***General***

-   Merge 3.16.4 in 3.17.x
    [\#7615](https://github.com/gravitee-io/issues/issues/7615)

# [APIM - 3.16.4 (2022-04-29)](https://github.com/gravitee-io/issues/milestone/543?closed=1)

## Bug fixes

***General***

-   500 Internal Server Error when using Transform Headers policy in
    combination with API-Key validationkey
    [\#7499](https://github.com/gravitee-io/issues/issues/7499)

-   Merge 3.15.8 in 3.16.x
    [\#7585](https://github.com/gravitee-io/issues/issues/7585)

***Management***

-   Backport \#7450 on 3.16 One shot upgraders run on each APIM startup
    with cockpit
    [\#7452](https://github.com/gravitee-io/issues/issues/7452)

# [APIM - 3.10.14 (2022-04-21)](https://github.com/gravitee-io/issues/milestone/541?closed=1)

## Bug fixes

***APIM***

-   All APIs in the Console that do not have Group/s as direct members
    have all Groups in Members. Only with Postgresql.
    [\#7429](https://github.com/gravitee-io/issues/issues/7429)

***General***

-   Backport of \#7489 in 3.10.x
    [\#7490](https://github.com/gravitee-io/issues/issues/7490)

-   When filtering through the logs, showing results as the maximum
    alows, and no other pages even though there are more results
    [\#6913](https://github.com/gravitee-io/issues/issues/6913)

***Management***

-   Alerts are not scoped to environment
    [\#6079](https://github.com/gravitee-io/issues/issues/6079)

-   Backport \#7450 on 3.10 One shot upgraders run on each APIM startup
    with cockpit
    [\#7454](https://github.com/gravitee-io/issues/issues/7454)

-   Org. admin is not allowed to transfer API ownership
    [\#7395](https://github.com/gravitee-io/issues/issues/7395)

***Repository***

-   MongoDB with self-signed SSL certificate
    [\#7539](https://github.com/gravitee-io/issues/issues/7539)

## Improvements

***General***

-   Set Version V3\_X by default on creation form
    [\#6454](https://github.com/gravitee-io/issues/issues/6454)

# [APIM - 3.17.1 (2022-04-07)](https://github.com/gravitee-io/issues/milestone/534?closed=1)

## Bug fixes

***General***

-   $facet operator not supported in documentDB causes errors in 3.17.0
    [\#7422](https://github.com/gravitee-io/issues/issues/7422)

-   Merge 3.16.3 in 3.17.x
    [\#7442](https://github.com/gravitee-io/issues/issues/7442)

***Management***

-   Backport \#7450 on 3.17 One shot upgraders run on each APIM startup
    with cockpit
    [\#7451](https://github.com/gravitee-io/issues/issues/7451)

-   Java heap space when requesting the OpenAPI specification
    [\#7460](https://github.com/gravitee-io/issues/issues/7460)

-   Platform Flows deleted after a restart when connected to Cockpit
    [\#7421](https://github.com/gravitee-io/issues/issues/7421)

# [APIM - 3.16.3 (2022-04-04)](https://github.com/gravitee-io/issues/milestone/536?closed=1)

## Bug fixes

***General***

-   Content policies returning null stream not displayed in debug mode
    [\#7396](https://github.com/gravitee-io/issues/issues/7396)

-   Merge 3.15.7 in 3.16.x
    [\#7441](https://github.com/gravitee-io/issues/issues/7441)

# [APIM - 3.10.13 (2022-04-01)](https://github.com/gravitee-io/issues/milestone/531?closed=1)

## Bug fixes

***Gateway***

-   Best match doesn’t match any flow
    [\#7412](https://github.com/gravitee-io/issues/issues/7412)

***Management***

-   Platform Flows deleted after a restart when connected to cockpit
    [\#7423](https://github.com/gravitee-io/issues/issues/7423)

## Features

***Policy***

-   Prevent following policies to reach endpoint when input is invalid:
    JSON Validation, JSON Threat Protection, XML Threat Protection and
    Regex Threat Protection
    [\#7301](https://github.com/gravitee-io/issues/issues/7301) ==
    [APIM - 3.17.0
    (2022-03-29)](https://github.com/gravitee-io/issues/milestone/508?closed=1)

## Bug fixes

***General***

-   Merge 3.16.1
    [\#7268](https://github.com/gravitee-io/issues/issues/7268)

-   Merge 3.16.2
    [\#7402](https://github.com/gravitee-io/issues/issues/7402)

***Console***

-   In Debug mode (fka Try-It), request does not return the good path
    [\#7220](https://github.com/gravitee-io/issues/issues/7220)

## Features

***Console***

-   Debug mode:

    -   Dynamic table for request headers
        [\#7149](https://github.com/gravitee-io/issues/issues/7149)

    -   Quick access timeline
        [\#6767](https://github.com/gravitee-io/issues/issues/6767)

    -   Allow use of user context-path
        [\#7072](https://github.com/gravitee-io/issues/issues/7072)

    -   View API call metrics
        [\#7111](https://github.com/gravitee-io/issues/issues/7111)

    -   View condition applied on a policy
        [\#7226](https://github.com/gravitee-io/issues/issues/7226)

    -   View if a policy is set at platform or API level
        [\#7183](https://github.com/gravitee-io/issues/issues/7183)

-   Shared API Key:

    -   Toggle Shared API Key mode in settings
        [\#6990](https://github.com/gravitee-io/issues/issues/6990)

    -   Manage Shared API Key at application level
        ([\#6798](https://github.com/gravitee-io/issues/issues/6798),
        [\#6801](https://github.com/gravitee-io/issues/issues/6801),
        [\#6800](https://github.com/gravitee-io/issues/issues/6800),
        [\#6804](https://github.com/gravitee-io/issues/issues/6804),
        [\#6796](https://github.com/gravitee-io/issues/issues/6796),
        [\#6797](https://github.com/gravitee-io/issues/issues/6797),
        [\#7192](https://github.com/gravitee-io/issues/issues/7192),
        [\#6795](https://github.com/gravitee-io/issues/issues/6795))

    -   Choose Shared API-Key mode at application level
        [\#6793](https://github.com/gravitee-io/issues/issues/6793)

    -   De-correlate API-Key and Subscription lifecycle
        [\#7266](https://github.com/gravitee-io/issues/issues/7266)

    -   Prevent Shared API-key Key revocation at API Level
        [\#6799](https://github.com/gravitee-io/issues/issues/6799)

    -   View subscriptions for a Shared-API Key
        [\#6794](https://github.com/gravitee-io/issues/issues/6794)
        ***Policy***

        -   Define headers based on the request or on the response
            payload
            [\#7358](https://github.com/gravitee-io/issues/issues/7358)

***Portal***

-   Shared API Key:

    -   Manage a shared API Key
        [\#6819](https://github.com/gravitee-io/issues/issues/6819)

    -   Use a shared API Key
        ([\#6816](https://github.com/gravitee-io/issues/issues/6816),
        [\#6817](https://github.com/gravitee-io/issues/issues/6817),
        [\#6818](https://github.com/gravitee-io/issues/issues/6818))

## Improvements

***Management***

-   Migrate management API documentation from openAPI V2 (aka swagger)
    to v3 [\#6224](https://github.com/gravitee-io/issues/issues/6224)

# [APIM - 3.16.2 (2022-03-28)](https://github.com/gravitee-io/issues/milestone/530?closed=1)

## Bug fixes

***General***

-   Merge 3.15.6 in 3.16.x
    [\#7388](https://github.com/gravitee-io/issues/issues/7388)

-   Platform policies not executed in multi environments context
    [\#7379](https://github.com/gravitee-io/issues/issues/7379)

## Features

***Policy***

-   Define headers based on the request or on the response payload
    [\#7333](https://github.com/gravitee-io/issues/issues/7333)

-   Prevent following policies to reach endpoint when input is invalid:
    JSON Validation, JSON Threat Protection, XML Threat Protection and
    Regex Threat Protection
    [\#7301](https://github.com/gravitee-io/issues/issues/7301) ==
    [APIM - 3.10.12
    (2022-03-22)](https://github.com/gravitee-io/issues/milestone/528?closed=1)

## Bug fixes

***APIM***

-   Events not being displayed correctly
    [\#7300](https://github.com/gravitee-io/issues/issues/7300)

***Console***

-   Can’t access a newly created API with import
    [\#7216](https://github.com/gravitee-io/issues/issues/7216)

-   Condition Logging on API is not displayed after saving
    [\#6978](https://github.com/gravitee-io/issues/issues/6978)

***Gateway***

-   Best Match flow mode doesn’t execute the best matching flow
    [\#6654](https://github.com/gravitee-io/issues/issues/6654)

***Gateway-api***

-   Bad behavior on TransformationException if no policyChain
    [\#7130](https://github.com/gravitee-io/issues/issues/7130)

***General***

-   Let the API Owner choose the Accept-Encoding
    [\#7181](https://github.com/gravitee-io/issues/issues/7181)

***Helm***

-   Api template doesn’t support opening of service core port
    [\#6895](https://github.com/gravitee-io/issues/issues/6895)

***Management***

-   Notify API Consumers contact too many people
    [\#7213](https://github.com/gravitee-io/issues/issues/7213)

***Metrics-reporter-policy***

-   Metrics reporting not done at the good time (backport 7194 in
    3.10.x) [\#7196](https://github.com/gravitee-io/issues/issues/7196)

***Policy***

-   Policy-ssl-enforcementsupport x509 attributes
    [\#7276](https://github.com/gravitee-io/issues/issues/7276)

# [APIM - 3.16.1 (2022-03-09)](https://github.com/gravitee-io/issues/milestone/525?closed=1)

## Bug fixes

***General***

-   Merge 3.15.4 in 3.16.x
    [\#7224](https://github.com/gravitee-io/issues/issues/7224)

-   Merge 3.15.5 in 3.16.x
    [\#7265](https://github.com/gravitee-io/issues/issues/7265)

***Management***

-   Policy studio - Save reload the page
    [\#7238](https://github.com/gravitee-io/issues/issues/7238)

# [APIM - 3.14.1 (2022-03-03)](https://github.com/gravitee-io/issues/milestone/522?closed=1)

## Bug fixes

***Gateway***

-   Error when discovery service creates new endpoints
    [\#6727](https://github.com/gravitee-io/issues/issues/6727)

-   Javascript Policy returns 500 OK in case of failure
    [\#6831](https://github.com/gravitee-io/issues/issues/6831)

***General***

-   Environment variables GRAVITEE\_PLUGINS\_PATH\_X are not working for
    gateway service
    [\#6909](https://github.com/gravitee-io/issues/issues/6909)

-   Merge 3.10.11 in 3.14.x
    [\#7160](https://github.com/gravitee-io/issues/issues/7160) ==
    [APIM - 3.16.0
    (2022-02-28)](https://github.com/gravitee-io/issues/milestone/493?closed=1)

## Bug fixes

***Gateway***

-   Platform policies should not be executed first on response
    [\#7138](https://github.com/gravitee-io/issues/issues/7138)

***General***

-   Login redirection is sometimes not working
    [\#7141](https://github.com/gravitee-io/issues/issues/7141)

## Features

***General***

-   Add crossId, identifying entities across environments
    [\#7003](https://github.com/gravitee-io/issues/issues/7003)

-   Enhance ci/cd url with crossId
    [\#7084](https://github.com/gravitee-io/issues/issues/7084)

-   Debug mode
    [\#6760](https://github.com/gravitee-io/issues/issues/6760)

# [APIM - 3.10.11 (2022-02-25)](https://github.com/gravitee-io/issues/milestone/517?closed=1)

## Bug fixes

***Console***

-   Not full log message is displayed in logs while the full one is
    received.
    [\#7017](https://github.com/gravitee-io/issues/issues/7017)

-   User Information - Label display problem
    [\#5625](https://github.com/gravitee-io/issues/issues/5625)

***Gateway***

-   Http requestTimeout prevents the gateway to log Analytics
    [\#6961](https://github.com/gravitee-io/issues/issues/6961)

-   Platform policies should not be executed first on response (Backport
    \#7138 in 3.10.x)
    [\#7143](https://github.com/gravitee-io/issues/issues/7143)

***General***

-   API Primary Owner role check
    [\#6360](https://github.com/gravitee-io/issues/issues/6360)

-   Anchor links are not working anymore in AsciiDoc files
    [\#6952](https://github.com/gravitee-io/issues/issues/6952)

-   Merge 3.5.29 in 3.10.x
    [\#6974](https://github.com/gravitee-io/issues/issues/6974)

-   Merge 3.5.30 in 3.10.x

-   Not able to publish documentation in APIM Portal in a desired order
    [\#6652](https://github.com/gravitee-io/issues/issues/6652)

***Management***

-   Checking "Show the URL to download the content" in the swagger
    documentation generates and error
    [\#6713](https://github.com/gravitee-io/issues/issues/6713)

***Node***

-   Node\_health metric returns null values in 3.10
    [\#6924](https://github.com/gravitee-io/issues/issues/6924)

***Repository***

-   Fix invalid SQL syntax when finding alert triggers
    [\#7163](https://github.com/gravitee-io/issues/issues/7163)

## Features

***Alert***

-   Alert per endpoint when healthcheck status change
    [\#6728](https://github.com/gravitee-io/issues/issues/6728)

## Improvements

***Management***

-   Support OpenSearch
    [\#6890](https://github.com/gravitee-io/issues/issues/6890)

# [APIM - 3.5.30 (2022-02-25)](https://github.com/gravitee-io/issues/milestone/515?closed=1)

## Bug fixes

***Management***

-   Improve personal token matching performance
    [\#7187](https://github.com/gravitee-io/issues/issues/7187)

# [APIM - 3.5.29 (2022-01-19)](https://github.com/gravitee-io/issues/milestone/498?closed=1)

## Bug fixes

***Gateway***

-   Starting is very slow when there is a lot of events in database
    [\#6955](https://github.com/gravitee-io/issues/issues/6955)

-   \[bridge\] Bridge repository client is not backward compatible
    [\#6884](https://github.com/gravitee-io/issues/issues/6884)

***Management***

-   Deleted dynamic dictionary is never undeployed
    [\#6870](https://github.com/gravitee-io/issues/issues/6870)

-   Path-mapping import is failing
    [\#6856](https://github.com/gravitee-io/issues/issues/6856)

-   When importing an API through file or URL path-mapping for analytics
    are not created.
    [\#6723](https://github.com/gravitee-io/issues/issues/6723)

-   \[design studio\] Conflict with keyboard shortcuts
    [\#6935](https://github.com/gravitee-io/issues/issues/6935)

## Improvements

***Management***

-   Support OpenSearch
    [\#6889](https://github.com/gravitee-io/issues/issues/6889)

# [APIM - 3.10.10 (2022-01-14)](https://github.com/gravitee-io/issues/milestone/496?closed=1)

## Bug fixes

***Console***

-   Transfer Group Primary Ownership
    [\#6359](https://github.com/gravitee-io/issues/issues/6359)

***General***

-   Merge 3.5.28 in 3.10.x
    [\#6874](https://github.com/gravitee-io/issues/issues/6874)

# [APIM - 3.14.0 (2022-01-12)](https://github.com/gravitee-io/issues/milestone/372?closed=1)

## Bug fixes

***Console***

-   Alerts page documentation is not properly displayed
    [\#6680](https://github.com/gravitee-io/issues/issues/6680)

***Gateway***

-   Vhost mode does not work with HTTP/2
    [\#6574](https://github.com/gravitee-io/issues/issues/6574)

-   \[perf\] Some ignored metrics are no longer ignored
    [\#6555](https://github.com/gravitee-io/issues/issues/6555)

***General***

-   Merge 3.13.2 into master
    [\#6749](https://github.com/gravitee-io/issues/issues/6749)

## Features

***Console***

-   View domain used by application
    [\#6384](https://github.com/gravitee-io/issues/issues/6384)

***Management***

-   Add a domain field for application creation
    [\#6383](https://github.com/gravitee-io/issues/issues/6383)

-   Generate a group token
    [\#6210](https://github.com/gravitee-io/issues/issues/6210)

-   \[Analytics\] OpenSearch support
    [\#6423](https://github.com/gravitee-io/issues/issues/6423)

-   \[CICD\] Access token management by administrator
    [\#6468](https://github.com/gravitee-io/issues/issues/6468)

-   \[CICD\] Creation of service account
    [\#6467](https://github.com/gravitee-io/issues/issues/6467)

***Portal***

-   Possibilty to disable promoted card on page list
    [\#6472](https://github.com/gravitee-io/issues/issues/6472)

## Improvements

***Elasticsearch-reporter***

-   Enable default plugins for all ES versions, and allow disabling them
    from configuration
    [\#6683](https://github.com/gravitee-io/issues/issues/6683)

***Gateway***

-   Add support of native OpenSSL on http connector
    [\#6561](https://github.com/gravitee-io/issues/issues/6561)

***Portal***

-   API Card - Add OwnerName info
    [\#6485](https://github.com/gravitee-io/issues/issues/6485)

-   Application page list pagination
    [\#6665](https://github.com/gravitee-io/issues/issues/6665)

-   Direct Search from the API Info
    [\#6486](https://github.com/gravitee-io/issues/issues/6486)

# [APIM - 3.5.28 (2022-01-06)](https://github.com/gravitee-io/issues/milestone/494?closed=1)

## Bug fixes

***Console***

-   Creating simultaneous changes in dictionaries(one user, two tabs)
    overwrites the changes in one or the other.
    [\#6750](https://github.com/gravitee-io/issues/issues/6750)

-   Expression language completion isn’t usable with code editor
    [\#6577](https://github.com/gravitee-io/issues/issues/6577)

-   When you check/activate HTTP Proxy with System Proxy in Endpoint
    configuration, Save button goes grey.
    [\#6619](https://github.com/gravitee-io/issues/issues/6619)

-   Wrong Units for Request/Response Content length in Analytics
    Dashboards
    [\#5706](https://github.com/gravitee-io/issues/issues/5706)

***Management***

-   Stop/start of dynamic dictionaries do not get redeployed on gateways
    [\#6847](https://github.com/gravitee-io/issues/issues/6847)

***Portal***

-   Documentation Page cannot handle lots of menu options
    [\#6618](https://github.com/gravitee-io/issues/issues/6618)

# [APIM - 3.13.3 (2021-12-29)](https://github.com/gravitee-io/issues/milestone/488?closed=1)

## Bug fixes

***General***

-   Merge 3.12.6 in 3.13.x
    [\#6806](https://github.com/gravitee-io/issues/issues/6806)

# [APIM - 3.12.6 (2021-12-24)](https://github.com/gravitee-io/issues/milestone/487?closed=1)

## Bug fixes

***General***

-   Merge 3.10.9 in 3.12.x
    [\#6805](https://github.com/gravitee-io/issues/issues/6805)

# [APIM - 3.10.9 (2021-12-23)](https://github.com/gravitee-io/issues/milestone/486?closed=1)

## Bug fixes

***Console***

-   Login Error after password reset
    [\#6488](https://github.com/gravitee-io/issues/issues/6488)

-   Resource can not be saved after being updated
    [\#6781](https://github.com/gravitee-io/issues/issues/6781)

***General***

-   Merge 3.5.26 in 3.10.x
    [\#6756](https://github.com/gravitee-io/issues/issues/6756)

-   Merge 3.5.27 in 3.10.x
    [\#6789](https://github.com/gravitee-io/issues/issues/6789)

***Management***

-   Healthcheck scheduled every seconds instead of configured value
    after import
    [\#6775](https://github.com/gravitee-io/issues/issues/6775)

***Portal***

-   Jump to anchors in Markdown documents does not work - Syntax bug
    [\#6659](https://github.com/gravitee-io/issues/issues/6659)

## Improvements

***Reporter***

-   \[elasticsearch\] Backport \#6683 on 3.10 ES plugins management
    [\#6710](https://github.com/gravitee-io/issues/issues/6710)

# [APIM - 3.5.27 (2021-12-21)](https://github.com/gravitee-io/issues/milestone/485?closed=1)

## Bug fixes

***Console***

-   Design studioselecting policies are pushing the menu right side
    [\#5242](https://github.com/gravitee-io/issues/issues/5242)

***Gateway***

-   System proxy is not managed for health-check
    [\#6731](https://github.com/gravitee-io/issues/issues/6731)

# [APIM - 3.5.26 (2021-12-17)](https://github.com/gravitee-io/issues/milestone/484?closed=1)

## Bug fixes

***Gateway***

-   Executable jar start with an error
    [\#6733](https://github.com/gravitee-io/issues/issues/6733)

-   \[policy\] retry policy may cause OOM
    [\#6684](https://github.com/gravitee-io/issues/issues/6684)

***Portal***

-   Different representation of date format in 'Try it out" swagger
    admin console/dev portal
    [\#6506](https://github.com/gravitee-io/issues/issues/6506)

-   When login is required on portal, an error is displayed
    [\#5727](https://github.com/gravitee-io/issues/issues/5727)

## Features

***Gateway***

-   Shutdown gracefully
    [\#6722](https://github.com/gravitee-io/issues/issues/6722)

# [APIM - 3.13.2 (2021-12-15)](https://github.com/gravitee-io/issues/milestone/474?closed=1)

## Bug fixes

***Connector***

-   \[kafka\] Improve assignment and seeking
    [\#6686](https://github.com/gravitee-io/issues/issues/6686)

***Console***

-   Analytics/metrics are no more present if index\_per\_typetrue with
    ES 5.x [\#6630](https://github.com/gravitee-io/issues/issues/6630)

-   Can’t configure healthcheck on an old API
    [\#6736](https://github.com/gravitee-io/issues/issues/6736)

***Gateway***

-   Executable jar start with an error
    [\#6732](https://github.com/gravitee-io/issues/issues/6732)

***General***

-   Merge 3.12.5 in 3.13.x
    [\#6704](https://github.com/gravitee-io/issues/issues/6704)

***Management***

-   HealthCheck does not take into account Proxy settings
    [\#6698](https://github.com/gravitee-io/issues/issues/6698)

***Policy***

-   \[groovy\] Groovy scripts fails to resolve method even if
    whitelisted
    [\#6681](https://github.com/gravitee-io/issues/issues/6681)

# [APIM - 3.12.5 (2021-12-10)](https://github.com/gravitee-io/issues/milestone/473?closed=1)

## Bug fixes

***Gateway***

-   OpenTracing hanging gateway
    [\#6366](https://github.com/gravitee-io/issues/issues/6366)

***General***

-   Merge 3.10.8 into 3.12.x
    [\#6701](https://github.com/gravitee-io/issues/issues/6701)

***Management***

-   Fetching Documentation Page from external source (GitHub/Gitlab)
    return 401 or 404
    [\#6331](https://github.com/gravitee-io/issues/issues/6331)

# [APIM - 3.10.8 (2021-12-08)](https://github.com/gravitee-io/issues/milestone/472?closed=1)

## Bug fixes

***Console***

-   API Logs - Consumer response is no longer displayed
    [\#6596](https://github.com/gravitee-io/issues/issues/6596)

-   Error log on delete action
    [\#6583](https://github.com/gravitee-io/issues/issues/6583)

***General***

-   Merge 3.5.24 into 3.10.x
    [\#6611](https://github.com/gravitee-io/issues/issues/6611)

-   Merge 3.5.25 in 3.10.x
    [\#6687](https://github.com/gravitee-io/issues/issues/6687)

***Management***

-   Fix plans inconsistencies in database
    [\#6586](https://github.com/gravitee-io/issues/issues/6586)

-   Rollback introduces duplicated plans
    [\#6595](https://github.com/gravitee-io/issues/issues/6595)

***Portal***

-   "page not found" after Google authentication
    [\#6235](https://github.com/gravitee-io/issues/issues/6235)

-   Error message on login page
    [\#6203](https://github.com/gravitee-io/issues/issues/6203)

-   Subscriptions menu should not be displayed if user does not have
    access rights on Applications subscriptions
    [\#6021](https://github.com/gravitee-io/issues/issues/6021)

# [APIM - 3.5.25 (2021-12-06)](https://github.com/gravitee-io/issues/milestone/471?closed=1)

## Bug fixes

***Console***

-   API:ALERT:read permission doesn’t activate API alert detail
    [\#5974](https://github.com/gravitee-io/issues/issues/5974)

***Gateway***

-   Api HealthCheck of endpoints consume too much resources
    [\#6658](https://github.com/gravitee-io/issues/issues/6658)

-   EndpointHealthcheckService not ready when Api sync starts
    [\#6657](https://github.com/gravitee-io/issues/issues/6657)

-   Heartbeat may cause infinite loop and server crash under certain
    circumptances
    [\#6655](https://github.com/gravitee-io/issues/issues/6655)

-   Make entrypoints concurrently available
    [\#6656](https://github.com/gravitee-io/issues/issues/6656)

-   \[perf\] ensure ClassLoaders are well released after api undeploy
    [\#6678](https://github.com/gravitee-io/issues/issues/6678)

***Management***

-   Handle null value when getting instances
    [\#6639](https://github.com/gravitee-io/issues/issues/6639)

-   Search API should keep the search score order
    [\#5744](https://github.com/gravitee-io/issues/issues/5744)

# [APIM - 3.13.1 (2021-11-26)](https://github.com/gravitee-io/issues/milestone/475?closed=1)

## Bug fixes

***Console***

-   Cannot configure healthcheck at API Level
    [\#6569](https://github.com/gravitee-io/issues/issues/6569)

***General***

-   Merge 3.12.4 in 3.13.x
    [\#6606](https://github.com/gravitee-io/issues/issues/6606)

# [APIM - 3.5.24 (2021-11-23)](https://github.com/gravitee-io/issues/milestone/469?closed=1)

## Bug fixes

***Gateway***

-   Inconsistent entrypoint resolution may cause 500 errors
    [\#6543](https://github.com/gravitee-io/issues/issues/6543)

# [APIM - 3.12.4 (2021-11-22)](https://github.com/gravitee-io/issues/milestone/466?closed=1)

## Bug fixes

***Console***

-   Organization Roles - Member list is empty
    [\#6527](https://github.com/gravitee-io/issues/issues/6527)

***General***

-   Merge 3.10.7 in 3.12.x
    [\#6603](https://github.com/gravitee-io/issues/issues/6603)

***Management***

-   "Role not found" exception when importing an API to a new
    environment
    [\#6448](https://github.com/gravitee-io/issues/issues/6448)

# [APIM - 3.10.7 (2021-11-22)](https://github.com/gravitee-io/issues/milestone/465?closed=1)

## Bug fixes

***Gateway***

-   API call always returns 500 internal error after redeploy
    [\#6601](https://github.com/gravitee-io/issues/issues/6601)

# [APIM - 3.13.0 (2021-11-19)](https://github.com/gravitee-io/issues/milestone/356?closed=1)

## Bug fixes

***General***

-   Merge 3.12.2
    [\#6557](https://github.com/gravitee-io/issues/issues/6557)

-   Merge 3.12.3
    [\#6594](https://github.com/gravitee-io/issues/issues/6594)

***Management***

-   Fix Jetty’s class loader
    [\#6495](https://github.com/gravitee-io/issues/issues/6495)

## Features

***Console***

-   Display excluded groups in plans
    [\#5259](https://github.com/gravitee-io/issues/issues/5259)

-   Support webhook on API update event
    [\#5426](https://github.com/gravitee-io/issues/issues/5426)

***Management***

-   Service Management Ecosystem (SME): API HTTP Connector Integration
    [\#6132](https://github.com/gravitee-io/issues/issues/6132)

-   Service Management Ecosystem (SME): Kafka connector *(available next
    week)* [\#6133](https://github.com/gravitee-io/issues/issues/6133)

***Portal***

-   Add an API search bar in the portal homepage
    [\#5323](https://github.com/gravitee-io/issues/issues/5323)

## Improvements

***Policy***

-   JWT-PolicyCache management improvements
    [\#6046](https://github.com/gravitee-io/issues/issues/6046)

# [APIM - 3.12.3 (2021-11-18)](https://github.com/gravitee-io/issues/milestone/463?closed=1)

## Bug fixes

***General***

-   Merge 3.10.6 in 3.12.x
    [\#6593](https://github.com/gravitee-io/issues/issues/6593)

# [APIM - 3.10.6 (2021-11-18)](https://github.com/gravitee-io/issues/milestone/457?closed=1)

## Bug fixes

***Console***

-   Not possible to change the logs configuration
    [\#6282](https://github.com/gravitee-io/issues/issues/6282)

***General***

-   Merge 3.5.23 in 3.10.x
    [\#6576](https://github.com/gravitee-io/issues/issues/6576)

***Management***

-   Plan is duplicated when importing an api with one plan
    [\#6042](https://github.com/gravitee-io/issues/issues/6042)

***Reporter-file***

-   Monitor logs (node-\*) get empty if output is set to elasticsearch
    [\#6564](https://github.com/gravitee-io/issues/issues/6564)

## Improvements

***Console***

-   \[alerts\] Add HTTP\_SIGNATURE\_INVALID\_SIGNATURE to api metrics
    list [\#6462](https://github.com/gravitee-io/issues/issues/6462)

# [APIM - 3.5.23 (2021-11-17)](https://github.com/gravitee-io/issues/milestone/458?closed=1)

## Bug fixes

***Console***

-   API search doesn’t return all expected results
    [\#6565](https://github.com/gravitee-io/issues/issues/6565)

-   Signup not possible on console using JDBC
    [\#6330](https://github.com/gravitee-io/issues/issues/6330)

***Gateway***

-   Avoid 404 and 500 error during api redeploy or stop
    [\#6553](https://github.com/gravitee-io/issues/issues/6553)

-   ILM managed indice are not handled by elasticsearch reporter
    [\#6507](https://github.com/gravitee-io/issues/issues/6507)

# [APIM - 3.12.2 (2021-11-12)](https://github.com/gravitee-io/issues/milestone/449?closed=1)

## Bug fixes

***General***

-   Merge 3.11.3 in 3.12.x
    [\#6511](https://github.com/gravitee-io/issues/issues/6511)

## Improvements

***Console***

-   Customize HTTP\_SIGNATURE\_INVALID\_SIGNATURE response template
    [\#6320](https://github.com/gravitee-io/issues/issues/6320)

# [APIM - 3.11.3 (2021-11-12)](https://github.com/gravitee-io/issues/milestone/448?closed=1)

## Bug fixes

***General***

-   Merge 3.10.4 in 3.11.x
    [\#6512](https://github.com/gravitee-io/issues/issues/6512)

-   Merge 3.10.5 in 3.11.x
    [\#6548](https://github.com/gravitee-io/issues/issues/6548)

# [APIM - 3.10.5 (2021-11-10)](https://github.com/gravitee-io/issues/milestone/447?closed=1)

## Bug fixes

***Console***

-   Policy - Pressing tab in EL fields add a transparent \t
    [\#6534](https://github.com/gravitee-io/issues/issues/6534)

***Gateway***

-   Cannot use JWT multiple plans
    [\#6529](https://github.com/gravitee-io/issues/issues/6529)

-   Inconsistent entrypoint resolution may cause 500 errors
    [\#6544](https://github.com/gravitee-io/issues/issues/6544)

-   Irrelevant bean injection warning for apis with health check
    [\#6105](https://github.com/gravitee-io/issues/issues/6105)

-   Sync probe ends with an exception when calling /\_node/sync
    [\#6541](https://github.com/gravitee-io/issues/issues/6541)

***Policy***

-   \[geoip-filtering\] Upgrade for APIM &gt;= 3.10
    [\#6531](https://github.com/gravitee-io/issues/issues/6531)

# [APIM - 3.5.22 (2021-11-10)](https://github.com/gravitee-io/issues/milestone/453?closed=1)

## Bug fixes

***Console***

-   Design studio - Policy disappear after save
    [\#6517](https://github.com/gravitee-io/issues/issues/6517)

-   Plan level policies are not displayed in the history
    [\#6524](https://github.com/gravitee-io/issues/issues/6524)

-   Policy - Pressing tab in EL fields add a transparent \t
    [\#6533](https://github.com/gravitee-io/issues/issues/6533)

-   Policy Mock unexpected behavior
    [\#6438](https://github.com/gravitee-io/issues/issues/6438)

***Gateway***

-   Cannot use JWT multiple plans
    [\#6528](https://github.com/gravitee-io/issues/issues/6528)

-   Inconsistent entrypoint resolution may cause 500 errors
    [\#6543](https://github.com/gravitee-io/issues/issues/6543)

-   Sync probe ends with an exception when calling /\_node/sync
    [\#6539](https://github.com/gravitee-io/issues/issues/6539)

# [APIM - 3.10.4 (2021-11-05)](https://github.com/gravitee-io/issues/milestone/430?closed=1)

## Bug fixes

***Console***

-   Documentation page configuration imported from external source can
    not be edited
    [\#6149](https://github.com/gravitee-io/issues/issues/6149)

-   Organization Settings get reinitialized after changing
    Authentication configuration.
    [\#6114](https://github.com/gravitee-io/issues/issues/6114)

-   Portal Settings get reinitialized after changing Portal
    Authentication configuration
    [\#6154](https://github.com/gravitee-io/issues/issues/6154)

-   Quality Metrics lost after upgrade
    [\#6290](https://github.com/gravitee-io/issues/issues/6290)

-   Reset button in settings does not work
    [\#6497](https://github.com/gravitee-io/issues/issues/6497)

***Gateway***

-   Can not start gateway if Hazelcast ratelimt enabled
    java.lang.ClassNotFoundExceptioncom.hazelcast.core.IMap
    [\#6117](https://github.com/gravitee-io/issues/issues/6117)

-   Health-check stops working after gateway is stopped/started.
    [\#6306](https://github.com/gravitee-io/issues/issues/6306)

-   Unable to start gateway when activating TLS and HTTP/2
    [\#6232](https://github.com/gravitee-io/issues/issues/6232)

-   \[policy\] fix license management of data-logging-masking and
    assign-metrics policies
    [\#6435](https://github.com/gravitee-io/issues/issues/6435)

***General***

-   Backport \#6101 in 3.10.x
    [\#6279](https://github.com/gravitee-io/issues/issues/6279)

-   Backport 6173 in 3.10.x
    [\#6174](https://github.com/gravitee-io/issues/issues/6174)

-   Backport of \#5966 in 3.10.x
    [\#6085](https://github.com/gravitee-io/issues/issues/6085)

-   Merge 3.5.21 into 3.10.4
    [\#6496](https://github.com/gravitee-io/issues/issues/6496)

***Management***

-   Error when creating an alert with system email notification
    [\#6231](https://github.com/gravitee-io/issues/issues/6231)

-   Swagger description of APIM Console API is empty
    [\#6494](https://github.com/gravitee-io/issues/issues/6494)

***Policy***

-   \[data-logging-masking\] datas are no longer masked
    [\#6122](https://github.com/gravitee-io/issues/issues/6122)

***Portal***

-   Filters on path on the logs in APIM Portal do not work.
    [\#6238](https://github.com/gravitee-io/issues/issues/6238)

***Repository***

-   \[sqlserver\] Rest API database setup
    [\#6447](https://github.com/gravitee-io/issues/issues/6447)

## Improvements

***Console***

-   Enable/Disable API Status dashboard
    [\#6365](https://github.com/gravitee-io/issues/issues/6365)

***Management***

-   Customize HTTP SIGNATURE response template
    [\#6319](https://github.com/gravitee-io/issues/issues/6319)

# [APIM - 3.5.21 (2021-11-02)](https://github.com/gravitee-io/issues/milestone/442?closed=1)

## Bug fixes

***Console***

-   500 error when importing definition of an API, null pointer
    exception
    [\#6052](https://github.com/gravitee-io/issues/issues/6052)

-   Change button labels (dashboard types) on Settings &gt; Analytics
    page [\#6363](https://github.com/gravitee-io/issues/issues/6363)

-   Deleted plan is not removed from design studio
    [\#5942](https://github.com/gravitee-io/issues/issues/5942)

-   Documentation page configuration imported from external source can
    not be edited
    [\#6461](https://github.com/gravitee-io/issues/issues/6461)

-   Top failed APIs shows 100% Failed on 200 status in Application
    Analytics
    [\#5703](https://github.com/gravitee-io/issues/issues/5703)

## Improvements

***Gateway***

-   Provide information for accurate Kubernetes Probes support
    [\#6455](https://github.com/gravitee-io/issues/issues/6455)

***Policy***

-   Print more accurate logs in case of invalid configuration
    [\#6479](https://github.com/gravitee-io/issues/issues/6479)

***Reporter***

-   Improve reporters performances
    [\#6430](https://github.com/gravitee-io/issues/issues/6430)

***Repository***

-   Optimize mongodb searchLatest events
    [\#6481](https://github.com/gravitee-io/issues/issues/6481)

# [APIM - 3.12.1 (2021-10-25)](https://github.com/gravitee-io/issues/milestone/435?closed=1)

## Bug fixes

***General***

-   Merge 3.11.2
    [\#6451](https://github.com/gravitee-io/issues/issues/6451)

***Portal***

-   APIKey isn’t the right one
    [\#6413](https://github.com/gravitee-io/issues/issues/6413)

***Repository***

-   \[sqlserver\] Rest API database setup
    [\#6453](https://github.com/gravitee-io/issues/issues/6453) ==
    [APIM - 3.11.2
    (2021-10-25)](https://github.com/gravitee-io/issues/milestone/438?closed=1)

## Bug fixes

***Repository***

-   \[jdbc\] APIs are not loaded at gateway startup after migration
    [\#6449](https://github.com/gravitee-io/issues/issues/6449)

# [APIM - 3.5.20 (2021-10-14)](https://github.com/gravitee-io/issues/milestone/426?closed=1)

## Bug fixes

***Gateway***

-   Fix JWT and OAuth2 plans
    [\#6391](https://github.com/gravitee-io/issues/issues/6391)

# [APIM - 3.5.19 (2021-10-07)](https://github.com/gravitee-io/issues/milestone/413?closed=1)

## Bug fixes

***Gateway***

-   Backport of
    [\#5649](https://github.com/gravitee-io/issues/issues/5649) :
    Heartbeat stops after 1h
    [\#6183](https://github.com/gravitee-io/issues/issues/6183)

-   Wrong settings for SyncService
    [\#5977](https://github.com/gravitee-io/issues/issues/5977)

-   \[sync\] In case of dictionary sync issue, APIs are fully resync
    [\#6301](https://github.com/gravitee-io/issues/issues/6301)

-   \[sync\] Sync process is trying to deploy APIs twice
    [\#6300](https://github.com/gravitee-io/issues/issues/6300)

***General***

-   Backport of
    [\#5966](https://github.com/gravitee-io/issues/issues/5966) : Node
    stop event are not well propagated when node is stopped
    [\#6084](https://github.com/gravitee-io/issues/issues/6084)

-   Backport of
    [\#5982](https://github.com/gravitee-io/issues/issues/5982) : JSON
    Threat Protection Policy : unable to adjust default values
    [\#5983](https://github.com/gravitee-io/issues/issues/5983)

***Management***

-   Application Dashboard inconsistent filtering on "Top Failed" widget
    [\#5771](https://github.com/gravitee-io/issues/issues/5771)

-   Plans get lost when imported with different user with admin rights
    [\#6008](https://github.com/gravitee-io/issues/issues/6008)

-   Reorder issue on PageServiceImpl.java
    [\#5931](https://github.com/gravitee-io/issues/issues/5931)

-   SMTP TLS negotiation error
    [\#6101](https://github.com/gravitee-io/issues/issues/6101)

-   SQL error when trying to search application to subscribe with
    [\#5812](https://github.com/gravitee-io/issues/issues/5812)

-   User can list all applications without permissions
    [\#6307](https://github.com/gravitee-io/issues/issues/6307)

-   \[repository\] missing mongodb index makes impossible to start
    management api
    [\#5995](https://github.com/gravitee-io/issues/issues/5995)

***Policy***

-   \[json threat\] - MAX JSON Array size issue not taken into account
    [\#6050](https://github.com/gravitee-io/issues/issues/6050)

-   \[ratelimit\] Error 429 is being returned while using two Rate Limit
    Policies.
    [\#6218](https://github.com/gravitee-io/issues/issues/6218)

-   \[ratelimit\] Redis AsyncRateLimitRepositoryError
    NumberFormatExceptionnull
    [\#5988](https://github.com/gravitee-io/issues/issues/5988)

***Portal***

-   API name not displayed correctly when multiple labels
    [\#5761](https://github.com/gravitee-io/issues/issues/5761)

-   Long paths/names are not well displayed in Analytics and Logs
    widgets [\#5767](https://github.com/gravitee-io/issues/issues/5767)

-   Scopes (Available Authorizations) can’t be displayed in API
    Documentation (swagger)
    [\#5661](https://github.com/gravitee-io/issues/issues/5661)

## Features

***Management***

-   

## Improvements

***Management***

-   Allow spaces in the declaration of dictionaries, at the dynamic
    routing level
    [\#5938](https://github.com/gravitee-io/issues/issues/5938)

-   Startup performance improvements
    [\#6066](https://github.com/gravitee-io/issues/issues/6066)

# [APIM - 3.12.0 (2021-09-30)](https://github.com/gravitee-io/issues/milestone/352?closed=1)

## Bug fixes

***General***

-   Merge 3.11.1
    [\#6240](https://github.com/gravitee-io/issues/issues/6240)

***Repository***

-   \[mongo\] Wrong total number of elements in paginated search
    [\#6173](https://github.com/gravitee-io/issues/issues/6173)

## Features

***Gateway***

-   Update Gateway API to add an access to the SSLSession
    [\#5322](https://github.com/gravitee-io/issues/issues/5322)

***Platform***

-   Handle duplicate API keys
    [\#6006](https://github.com/gravitee-io/issues/issues/6006)

***Policy***

-   \[generate-http-signature\] Genrate HTTP Signature policy
    [\#4899](https://github.com/gravitee-io/issues/issues/4899)

***Portal***

-   Advanced search on APIs
    [\#2839](https://github.com/gravitee-io/issues/issues/2839)

# [APIM - 3.11.1 (2021-09-22)](https://github.com/gravitee-io/issues/milestone/422?closed=1)

## Bug fixes

***Gateway***

-   Try It Mode - Number of instances provided should be set
    [\#6073](https://github.com/gravitee-io/issues/issues/6073)

-   Try It Mode - issues if api has health check configured
    [\#6069](https://github.com/gravitee-io/issues/issues/6069)

-   Try It Mode - issues with configuration
    [\#6072](https://github.com/gravitee-io/issues/issues/6072)

***General***

-   Merge 3.10.1
    [\#6056](https://github.com/gravitee-io/issues/issues/6056)

-   Merge 3.10.2
    [\#6217](https://github.com/gravitee-io/issues/issues/6217)

-   Merge 3.10.3
    [\#6219](https://github.com/gravitee-io/issues/issues/6219)

## Improvements

***Management***

-   Try It Mode - check api configuration when requesting debug
    [\#6017](https://github.com/gravitee-io/issues/issues/6017)

# [APIM - 3.10.3 (2021-09-17)](https://github.com/gravitee-io/issues/milestone/429?closed=1)

## Bug fixes

***Platform***

-   Fix APIM Dockerfile
    [\#6206](https://github.com/gravitee-io/issues/issues/6206)

# [APIM - 3.10.2 (2021-09-17)](https://github.com/gravitee-io/issues/milestone/421?closed=1)

## Bug fixes

***Gateway***

-   \[oauth-am-resource\] memory leak
    [\#6119](https://github.com/gravitee-io/issues/issues/6119)

***Management***

-   Add missing script and missing documentation
    [\#6142](https://github.com/gravitee-io/issues/issues/6142)

***Repository***

-   \[rate-limit\] redis health check throws an exception
    [\#6111](https://github.com/gravitee-io/issues/issues/6111)

***Resource-oauth2-provider***

-   Exceptions occur when two many concurrent requests are made
    [\#6176](https://github.com/gravitee-io/issues/issues/6176)

## Improvements

***Platform***

-   Upgrade Docker Images
    [\#6139](https://github.com/gravitee-io/issues/issues/6139)

-   Update APIM dependencies
    [\#6152](https://github.com/gravitee-io/issues/issues/6152)

# [APIM - 3.10.1 (2021-09-06)](https://github.com/gravitee-io/issues/milestone/419?closed=1)

## Bug fixes

***Console***

-   Logo disappeared after migration to 3.10
    [\#6038](https://github.com/gravitee-io/issues/issues/6038)

-   Metrics of instances are not displayed
    [\#6039](https://github.com/gravitee-io/issues/issues/6039)

-   Pending Tasks are visible to any users in the Console
    [\#6036](https://github.com/gravitee-io/issues/issues/6036)

-   Portal Settings get reinitialized after changes
    [\#6009](https://github.com/gravitee-io/issues/issues/6009)

-   \[3.10.0\] "Authentication button color" set in Console OIDC
    Authentication Settings not propagated to Portal
    [\#6010](https://github.com/gravitee-io/issues/issues/6010)

***Gateway***

-   Enabling prometheus Metrics gives
    java.lang.ClassNotFoundExceptionorg.LatencyUtils.PauseDetector
    [\#5996](https://github.com/gravitee-io/issues/issues/5996)

***General***

-   Cannot access API as a User
    [\#6033](https://github.com/gravitee-io/issues/issues/6033)

-   Merge 3.9.4
    [\#5945](https://github.com/gravitee-io/issues/issues/5945)

***Management***

-   Enable to sync APIs due to NPE
    [\#5980](https://github.com/gravitee-io/issues/issues/5980)

***Platform***

-   El expression request.method leads to an InvocationTargetException
    [\#6051](https://github.com/gravitee-io/issues/issues/6051)

## Features

***Reporter***

-   Add the ability to filter or rename properties / fields
    [\#5831](https://github.com/gravitee-io/issues/issues/5831)

## Improvements

***Gateway***

-   Enhance certificate management in keystore to enable to
    differenciate certificates per domain
    [\#5894](https://github.com/gravitee-io/issues/issues/5894)

-   Resource hogging when using many certificates in keystore
    [\#5895](https://github.com/gravitee-io/issues/issues/5895)

***Management***

-   Set spring security dependencies as provided in IDP plugins
    [\#5947](https://github.com/gravitee-io/issues/issues/5947)

# [APIM - 3.11.0 (2021-08-31)](https://github.com/gravitee-io/issues/milestone/333?closed=1)

## Bug fixes

***General***

-   OAuth2 plan parsing must accept tokens other than JWT (example 1)
    [\#5828](https://github.com/gravitee-io/issues/issues/5828)

-   OAuth2 plan parsing must accept tokens other than JWT (example 2)
    [\#5829](https://github.com/gravitee-io/issues/issues/5829)

-   The "Access control" tab of a documentation page does not return the
    correct list of roles
    [\#5789](https://github.com/gravitee-io/issues/issues/5789)

***Management***

-   Logging is enabled on the wrong api
    [\#5991](https://github.com/gravitee-io/issues/issues/5991)

## Features

***General***

-   Add `Try it` in Design Studio
    [\#5901](https://github.com/gravitee-io/issues/issues/5901)

-   Define the request
    [\#5804](https://github.com/gravitee-io/issues/issues/5804)

-   Display the response
    [\#5805](https://github.com/gravitee-io/issues/issues/5805)

-   Encrypt API properties
    [\#5638](https://github.com/gravitee-io/issues/issues/5638)

-   Javascript policy
    [\#5948](https://github.com/gravitee-io/issues/issues/5948)

-   Write documentation with AsyncAPI
    [\#5575](https://github.com/gravitee-io/issues/issues/5575)

***Policy***

-   \[gravitee-policy-callout-http\] fire & forget mode
    [\#5972](https://github.com/gravitee-io/issues/issues/5972)

## Improvements

***Policy-groovy***

-   Improve form
    [\#6027](https://github.com/gravitee-io/issues/issues/6027)

# [APIM - 3.9.4 (2021-08-23)](https://github.com/gravitee-io/issues/milestone/416?closed=1)

## Bug fixes

***Console***

-   Probem on registration of the proxy conf
    [\#5896](https://github.com/gravitee-io/issues/issues/5896)

***General***

-   Merge 3.8.7
    [\#5944](https://github.com/gravitee-io/issues/issues/5944)

***Management***

-   JSON Threat Protection Policy unable to adjust default values
    [\#5982](https://github.com/gravitee-io/issues/issues/5982)

***Ratelimit***

-   Rate limiting not working with Redis
    [\#5882](https://github.com/gravitee-io/issues/issues/5882)

# [APIM - 3.8.7 (2021-08-12)](https://github.com/gravitee-io/issues/milestone/414?closed=1)

## Bug fixes

***General***

-   Merge 3.5.18
    [\#5943](https://github.com/gravitee-io/issues/issues/5943)

***Management***

-   Error while importing a file
    [\#5933](https://github.com/gravitee-io/issues/issues/5933)

-   Metadata of type URL do not support all characters
    [\#5964](https://github.com/gravitee-io/issues/issues/5964)

# [APIM - 3.5.18 (2021-08-04)](https://github.com/gravitee-io/issues/milestone/409?closed=1)

## Bug fixes

***Definition***

-   Virtual host with */* is not saved
    [\#5859](https://github.com/gravitee-io/issues/issues/5859)

***Gateway***

-   Sync process optimisations
    [\#5615](https://github.com/gravitee-io/issues/issues/5615)

-   Upgrade dependency for AE 1.3.3 plugin
    [\#5890](https://github.com/gravitee-io/issues/issues/5890)

***Management***

-   "order" field of Plans get reseted when imported from 3.5.x to 3.8.x
    [\#5696](https://github.com/gravitee-io/issues/issues/5696)

-   Allow to specify multiple roles to map with ldap idp
    [\#5619](https://github.com/gravitee-io/issues/issues/5619)

-   Check plan policy configuration
    [\#5952](https://github.com/gravitee-io/issues/issues/5952)

-   Flows property not accepted in request payload for Update Plan
    [\#5694](https://github.com/gravitee-io/issues/issues/5694)

-   Plan Flows get lost on updating an API with an existing API
    definition (updateApiWithDefinition)
    [\#5820](https://github.com/gravitee-io/issues/issues/5820)

-   \[analytics\] "Display percentage" is never checked
    [\#5495](https://github.com/gravitee-io/issues/issues/5495)

-   \[github idp\] user without space in their username fail to
    authenticate
    [\#5507](https://github.com/gravitee-io/issues/issues/5507)

***Policy-ratelimit***

-   Unable to use quota notification.properties
    [\#5834](https://github.com/gravitee-io/issues/issues/5834)

***Reporter-file***

-   \[reporter-tcp\] manage user-agent in the elasticsearch output
    [\#5893](https://github.com/gravitee-io/issues/issues/5893)

## Improvements

***General***

-   Add the created\_at value in the Get API definition response
    [\#5455](https://github.com/gravitee-io/issues/issues/5455)

***Management***

-   Re-enable "retainDays" configuration in file-reporter plugin
    [\#5463](https://github.com/gravitee-io/issues/issues/5463)

# [APIM - 3.10.0 (2021-08-03)](https://github.com/gravitee-io/issues/milestone/243?closed=1)

## Bug fixes

***Gateway***

-   Heartbeat stops after 1h
    [\#5649](https://github.com/gravitee-io/issues/issues/5649)

-   \[apim\] gRPC in Server streaming mode the call is never close
    [\#5494](https://github.com/gravitee-io/issues/issues/5494)

***General***

-   Lost documentation pages when duplicating an API
    [\#5849](https://github.com/gravitee-io/issues/issues/5849)

-   Merge 3.9.2
    [\#5814](https://github.com/gravitee-io/issues/issues/5814)

-   Merge 3.9.3
    [\#5818](https://github.com/gravitee-io/issues/issues/5818)

***Management***

-   Error while importing a file
    [\#5932](https://github.com/gravitee-io/issues/issues/5932)

-   Not redirect to dashboard when click on gravitee logo
    [\#5768](https://github.com/gravitee-io/issues/issues/5768)

## Features

***Gateway***

-   OpenTracing support
    [\#1581](https://github.com/gravitee-io/issues/issues/1581)

***General***

-   API Promotion
    [\#5530](https://github.com/gravitee-io/issues/issues/5530)

-   Accepting/Rejecting an API promotion request
    [\#5528](https://github.com/gravitee-io/issues/issues/5528)

-   Handle `groups` during API Promotion
    [\#5844](https://github.com/gravitee-io/issues/issues/5844)

-   Handle `pages` during API Promotion
    [\#5841](https://github.com/gravitee-io/issues/issues/5841)

-   Handle `plans` during API Promotion
    [\#5842](https://github.com/gravitee-io/issues/issues/5842)

-   Logging events for API promotion
    [\#5531](https://github.com/gravitee-io/issues/issues/5531)

-   Making requests for API promotion
    [\#5526](https://github.com/gravitee-io/issues/issues/5526)

-   Managing in progress API promotion requests
    [\#5746](https://github.com/gravitee-io/issues/issues/5746)

-   Support Redis for cache resource
    [\#5712](https://github.com/gravitee-io/issues/issues/5712)

-   Viewing tasks for API promotion requests
    [\#5527](https://github.com/gravitee-io/issues/issues/5527)

***Management***

-   Allows to use Expression Language in health check configuration
    [\#4943](https://github.com/gravitee-io/issues/issues/4943)

-   Manage AsciiDoc pages
    [\#4717](https://github.com/gravitee-io/issues/issues/4717)

-   Notify consumer before the expiration of its subscription
    [\#3887](https://github.com/gravitee-io/issues/issues/3887)

***Policy***

-   \[groovy\] add XML support
    [\#5891](https://github.com/gravitee-io/issues/issues/5891)

# [APIM - 3.9.3 (2021-07-16)](https://github.com/gravitee-io/issues/milestone/410?closed=1)

## Bug fixes

***General***

-   APIM Console Plan creation with Rate Limiting causes an exception
    [\#5833](https://github.com/gravitee-io/issues/issues/5833)

-   Merge 3.8.6
    [\#5817](https://github.com/gravitee-io/issues/issues/5817)

-   The GW instance is no longer displayed on the nightly
    [\#5782](https://github.com/gravitee-io/issues/issues/5782)

# [APIM - 3.8.6 (2021-07-16)](https://github.com/gravitee-io/issues/milestone/408?closed=1)

## Bug fixes

***General***

-   GetGroupMembers align documentation vs real output
    [\#5614](https://github.com/gravitee-io/issues/issues/5614)

-   Merge 3.5.17
    [\#5816](https://github.com/gravitee-io/issues/issues/5816)

## Features

***Gateway***

-   \[response template\] add a GATEWAY\_TIMEOUT response template
    [\#5501](https://github.com/gravitee-io/issues/issues/5501)

# [APIM - 3.5.17 (2021-07-06)](https://github.com/gravitee-io/issues/milestone/404?closed=1)

## Bug fixes

***General***

-   Backport 5756
    [\#5757](https://github.com/gravitee-io/issues/issues/5757)

***Management***

-   Strange UI behaviour in the console
    [\#5807](https://github.com/gravitee-io/issues/issues/5807)

-   \[alerting\] When creating "Alert on the health status of the node",
    CREATE button is disabled
    [\#5808](https://github.com/gravitee-io/issues/issues/5808)

***Managment***

-   API Analytics response payload not displayed, fails with javascript
    error e.getTextArea is not a function
    [\#5364](https://github.com/gravitee-io/issues/issues/5364)

***Policy***

-   Allow array.length with groovy sandbox
    [\#5557](https://github.com/gravitee-io/issues/issues/5557)

-   \[transform headers\] support null in arrays
    [\#5778](https://github.com/gravitee-io/issues/issues/5778)

## Features

***Resource***

-   \[auth-provider\] Support HTTP-based authentication provider
    [\#5737](https://github.com/gravitee-io/issues/issues/5737)

## Improvements

***Policy***

-   \[basic-authentication\] Manage async auth providers
    [\#5733](https://github.com/gravitee-io/issues/issues/5733)

# [APIM - 3.9.2 (2021-06-29)](https://github.com/gravitee-io/issues/milestone/400?closed=1)

## Bug fixes

***General***

-   Merge 3.8.4
    [\#5721](https://github.com/gravitee-io/issues/issues/5721)

-   Merge 3.8.5
    [\#5793](https://github.com/gravitee-io/issues/issues/5793)

# [APIM - 3.8.5 (2021-06-29)](https://github.com/gravitee-io/issues/milestone/398?closed=1)

## Bug fixes

***General***

-   Merge 3.5.15
    [\#5740](https://github.com/gravitee-io/issues/issues/5740)

-   Merge 3.5.16
    [\#5758](https://github.com/gravitee-io/issues/issues/5758)

***Management***

-   API\_REVIEW\_\* Audit Event filters are missing in the scrolling
    list (API and Global Levels)
    [\#5673](https://github.com/gravitee-io/issues/issues/5673)

-   Redirection problem when connecting to console from cockpit
    [\#5785](https://github.com/gravitee-io/issues/issues/5785)

-   Roles initialized to default after removing a role mapping
    configuration
    [\#5756](https://github.com/gravitee-io/issues/issues/5756)

-   Subscription approval link not correct
    [\#5724](https://github.com/gravitee-io/issues/issues/5724)

***Reporter***

-   Bad timestamp format by reporters
    [\#5707](https://github.com/gravitee-io/issues/issues/5707)

-   \[file\] NPEs thrown in log
    [\#5668](https://github.com/gravitee-io/issues/issues/5668)

***Resource-cache***

-   Error when redeploy an api
    [\#5671](https://github.com/gravitee-io/issues/issues/5671)

## Improvements

***Helm***

-   Adapt liveness probe of the gateway to check API synchronization
    [\#5734](https://github.com/gravitee-io/issues/issues/5734)

# [APIM - 3.5.16 (2021-06-18)](https://github.com/gravitee-io/issues/milestone/401?closed=1)

## Bug fixes

***Gateway***

-   API health check is duplicating slash in some case
    [\#5752](https://github.com/gravitee-io/issues/issues/5752)

***Portal***

-   Login issue on the portal
    [\#5748](https://github.com/gravitee-io/issues/issues/5748)

# [APIM - 3.5.15 (2021-06-17)](https://github.com/gravitee-io/issues/milestone/396?closed=1)

## Bug fixes

***Console***

-   Allow to disable "maintenance" mode
    [\#5731](https://github.com/gravitee-io/issues/issues/5731)

-   CORS settings doesn’t display
    [\#5729](https://github.com/gravitee-io/issues/issues/5729)

***Gateway***

-   Unable to establish websocket connection using Firefox
    [\#5722](https://github.com/gravitee-io/issues/issues/5722)

***General***

-   Backport \#5632
    [\#5697](https://github.com/gravitee-io/issues/issues/5697)

-   Check consistency of Plans on API update
    [\#5718](https://github.com/gravitee-io/issues/issues/5718)

***Management***

-   Can not Auto-fetch Documentation Page from an external source
    [\#5699](https://github.com/gravitee-io/issues/issues/5699)

-   Inconsistent Sharding Tags behavior compared to the documentation
    [\#5600](https://github.com/gravitee-io/issues/issues/5600)

-   Newsletter subscribe link not working anymore
    [\#5720](https://github.com/gravitee-io/issues/issues/5720)

## Features

***Policy***

-   \[Http Signature\] Support non quoted String in the signature
    [\#5684](https://github.com/gravitee-io/issues/issues/5684)

# [APIM - 3.8.4 (2021-06-14)](https://github.com/gravitee-io/issues/milestone/391?closed=1)

## Bug fixes

***General***

-   Backport \#5649
    [\#5704](https://github.com/gravitee-io/issues/issues/5704)

-   Merge 3.5.13
    [\#5690](https://github.com/gravitee-io/issues/issues/5690)

-   Merge 3.5.14
    [\#5698](https://github.com/gravitee-io/issues/issues/5698)

***Management***

-   Categories order field not set at creation
    [\#5632](https://github.com/gravitee-io/issues/issues/5632)

***Resource-cache***

-   Error when redeploy an api
    [\#5671](https://github.com/gravitee-io/issues/issues/5671)

# [APIM - 3.9.1 (2021-06-12)](https://github.com/gravitee-io/issues/milestone/399?closed=1)

## Bug fixes

***Management***

-   Loss of data when migrating on 3.9.0 for jdbc users
    [\#5711](https://github.com/gravitee-io/issues/issues/5711)

# [APIM - 3.5.14 (2021-06-09)](https://github.com/gravitee-io/issues/milestone/393?closed=1)

## Bug fixes

***General***

-   Group/role mapping lost after OIDC login
    [\#5686](https://github.com/gravitee-io/issues/issues/5686)

***Management***

-   Allow to specify multiple roles to map with ldap idp
    [\#5619](https://github.com/gravitee-io/issues/issues/5619)

-   Gravitee\_http\_cors\_alloworigin environment variable setting not
    reflected in UI
    [\#5583](https://github.com/gravitee-io/issues/issues/5583)

# [APIM - 3.9.0 (2021-06-08)](https://github.com/gravitee-io/issues/milestone/242?closed=1)

## Bug fixes

***General***

-   Merge 3.8.1
    [\#5497](https://github.com/gravitee-io/issues/issues/5497)

-   Merge 3.8.2
    [\#5554](https://github.com/gravitee-io/issues/issues/5554)

-   Merge 3.8.3
    [\#5634](https://github.com/gravitee-io/issues/issues/5634)

***Management***

-   Cannot ask for review anymore
    [\#5558](https://github.com/gravitee-io/issues/issues/5558)

-   Cannot publish / unpublish a page with a link
    [\#5559](https://github.com/gravitee-io/issues/issues/5559)

-   Check existance of confirmUrl
    [\#5567](https://github.com/gravitee-io/issues/issues/5567)

-   Error when updating user’s avatar
    [\#5533](https://github.com/gravitee-io/issues/issues/5533)

-   \[gateway\] reintroduce serializers/deserializers on
    gravitee-definition
    [\#5642](https://github.com/gravitee-io/issues/issues/5642)

## Features

***Console***

-   Custom templates for alert notifications (HTTP Status Code and
    Average Response Time)
    [\#5481](https://github.com/gravitee-io/issues/issues/5481)

***Gateway***

-   Allow to associate a gateway to a specific environment
    [\#5357](https://github.com/gravitee-io/issues/issues/5357)

-   Platform policies
    [\#4460](https://github.com/gravitee-io/issues/issues/4460)

***Management***

-   Allow an API Publisher to push API Metrics to a specific target
    [\#5349](https://github.com/gravitee-io/issues/issues/5349)

-   Configure an alert on a timeframe
    [\#4894](https://github.com/gravitee-io/issues/issues/4894)

***Portal***

-   Allow to define alerts for a consumer
    [\#5341](https://github.com/gravitee-io/issues/issues/5341)

# [APIM - 3.5.13 (2021-06-04)](https://github.com/gravitee-io/issues/milestone/386?closed=1)

## Bug fixes

***General***

-   Backport \#5621
    [\#5633](https://github.com/gravitee-io/issues/issues/5633)

-   Default\_api\_logo.png can not be overriden
    [\#5524](https://github.com/gravitee-io/issues/issues/5524)

-   Merge 3.0.17
    [\#5647](https://github.com/gravitee-io/issues/issues/5647)

***Helm***

-   Cannot disable the Alert Engine connector
    [\#5662](https://github.com/gravitee-io/issues/issues/5662)

***Management***

-   CORS Access-Control-Allow-Origin regex fails on pattern as
    ".\*.mydomain.com"
    [\#5611](https://github.com/gravitee-io/issues/issues/5611)

-   Cannot update Quality Rules
    [\#5626](https://github.com/gravitee-io/issues/issues/5626)

-   Invalid logout url construction with external OIDC Provider
    [\#5593](https://github.com/gravitee-io/issues/issues/5593)

-   Plan Flows get lost when re-importing API from a swagger/oas3
    specification
    [\#5651](https://github.com/gravitee-io/issues/issues/5651)

-   Policies on path are not updated when updating an API with swagger
    [\#4970](https://github.com/gravitee-io/issues/issues/4970)

-   Unable to use default image on API
    [\#5303](https://github.com/gravitee-io/issues/issues/5303)

***Management-api***

-   Unable to change admin password with the environment variables in
    Openshift
    [\#2680](https://github.com/gravitee-io/issues/issues/2680)

***Portal***

-   Do not display "Create an Application" in Portal if user has
    insufficient privileges
    [\#5403](https://github.com/gravitee-io/issues/issues/5403)

# [APIM - 3.8.3 (2021-05-26)](https://github.com/gravitee-io/issues/milestone/387?closed=1)

## Bug fixes

***General***

-   Merge 3.7.4
    [\#5602](https://github.com/gravitee-io/issues/issues/5602)

***Management-ui***

-   Loss of path when OIDC logout process
    [\#5621](https://github.com/gravitee-io/issues/issues/5621)

# [APIM - 3.0.17 (2021-05-20)](https://github.com/gravitee-io/issues/milestone/365?closed=1)

## Bug fixes

***General***

-   Backport \#5468
    [\#5503](https://github.com/gravitee-io/issues/issues/5503)

-   Backport \#5517
    [\#5534](https://github.com/gravitee-io/issues/issues/5534)

-   The API footer overlap the redoc documentation
    [\#5597](https://github.com/gravitee-io/issues/issues/5597)

***Management***

-   Update start date label for audit logs
    [\#5256](https://github.com/gravitee-io/issues/issues/5256)

-   User search is not accurate
    [\#5150](https://github.com/gravitee-io/issues/issues/5150)

***Portal***

-   "information" is singular
    [\#5595](https://github.com/gravitee-io/issues/issues/5595)

-   Unable to create an App from the portal
    [\#5563](https://github.com/gravitee-io/issues/issues/5563)

# [APIM - 3.7.4 (2021-05-22)](https://github.com/gravitee-io/issues/milestone/388?closed=1)

## Bug fixes

***General***

-   Merge 3.5.12
    [\#5601](https://github.com/gravitee-io/issues/issues/5601)

# [APIM - 3.5.12 (2021-05-18)](https://github.com/gravitee-io/issues/milestone/384?closed=1)

## Bug fixes

***General***

-   Backport \#5558
    [\#5568](https://github.com/gravitee-io/issues/issues/5568)

-   Backport \#5564
    [\#5590](https://github.com/gravitee-io/issues/issues/5590)

-   Backport \#5567
    [\#5589](https://github.com/gravitee-io/issues/issues/5589)

-   Default\_api\_logo.png can not be overriden
    [\#5524](https://github.com/gravitee-io/issues/issues/5524)

***IdentityProvider***

-   Not default role when user created with external IDP
    [\#5561](https://github.com/gravitee-io/issues/issues/5561)

***Management***

-   Disabling Newsletter does not disable bottom right Pop-in
    [\#5502](https://github.com/gravitee-io/issues/issues/5502)

## Improvements

***Elasticsearch***

-   Do not include date as part of the index name for ILM managed
    indices [\#5551](https://github.com/gravitee-io/issues/issues/5551)

***General***

-   Add postman for /applications?query=A accessible to unauthorized
    users [\#5535](https://github.com/gravitee-io/issues/issues/5535)

# [APIM - 3.8.2 (2021-05-14)](https://github.com/gravitee-io/issues/milestone/383?closed=1)

## Bug fixes

***General***

-   Backport \#5559
    [\#5569](https://github.com/gravitee-io/issues/issues/5569)

-   Backport 5533
    [\#5552](https://github.com/gravitee-io/issues/issues/5552)

-   Merge 3.7.3
    [\#5553](https://github.com/gravitee-io/issues/issues/5553)

***Management***

-   Missing plan selection rule for V2 Definition APIs
    [\#5564](https://github.com/gravitee-io/issues/issues/5564)

***Management-ui***

-   As a user I should see user assigned to the group without refreshing
    the page [\#5401](https://github.com/gravitee-io/issues/issues/5401)

# [APIM - 3.7.3 (2021-05-12)](https://github.com/gravitee-io/issues/milestone/381?closed=1)

## Bug fixes

***General***

-   Merge 3.5.11
    [\#5541](https://github.com/gravitee-io/issues/issues/5541)

***Management***

-   API Health-check screen is broken
    [\#5511](https://github.com/gravitee-io/issues/issues/5511)

-   Environment permission is needed to display the api events in
    analytics
    [\#5473](https://github.com/gravitee-io/issues/issues/5473)

# [APIM - 3.5.11 (2021-05-07)](https://github.com/gravitee-io/issues/milestone/376?closed=1)

## Bug fixes

***Gateway***

-   File descriptors exhaustion on POST method with form-data inputfile
    [\#5517](https://github.com/gravitee-io/issues/issues/5517)

-   Issue when flushing inbound request queue on an already ended
    request [\#5539](https://github.com/gravitee-io/issues/issues/5539)

***General***

-   Backport \#5468
    [\#5504](https://github.com/gravitee-io/issues/issues/5504)

-   CVE#2168 [\#5450](https://github.com/gravitee-io/issues/issues/5450)

***Management***

-   /applications?query=A accessible to unauthorized users
    [\#5518](https://github.com/gravitee-io/issues/issues/5518)

-   A Membership for member USER and ref GROUP already exists.
    [\#5413](https://github.com/gravitee-io/issues/issues/5413)

-   API logs and permissions
    [\#5412](https://github.com/gravitee-io/issues/issues/5412)

-   Get an API by its context-path doesn’t seem to work on latest
    version [\#5298](https://github.com/gravitee-io/issues/issues/5298)

-   Make /portal protected by authentication
    [\#5435](https://github.com/gravitee-io/issues/issues/5435)

-   Plan id not preserved on API import
    [\#5489](https://github.com/gravitee-io/issues/issues/5489)

-   \[healthcheck\] add a query parameter in the path without /
    [\#5433](https://github.com/gravitee-io/issues/issues/5433)

***Portal***

-   Do not display "Create an Application" in Portal if user has
    insufficient privileges
    [\#5403](https://github.com/gravitee-io/issues/issues/5403)

***Reporter***

-   \[file\] OOM when flush takes a long time
    [\#5515](https://github.com/gravitee-io/issues/issues/5515)

# [APIM - 3.8.1 (2021-04-28)](https://github.com/gravitee-io/issues/milestone/378?closed=1)

## Bug fixes

***General***

-   Merge 3.7.2
    [\#5467](https://github.com/gravitee-io/issues/issues/5467)

## Features

***General***

-   APIM dependencies upgrade
    [\#5471](https://github.com/gravitee-io/issues/issues/5471)

-   EE docker image jdk upgrade openjdk11:jre-11.0.10\_9-alpine
    [\#5472](https://github.com/gravitee-io/issues/issues/5472)

# [APIM - 3.7.2 (2021-04-23)](https://github.com/gravitee-io/issues/milestone/371?closed=1)

## Bug fixes

***General***

-   Backport \#5416
    [\#5421](https://github.com/gravitee-io/issues/issues/5421)

-   Merge 3.5.10
    [\#5466](https://github.com/gravitee-io/issues/issues/5466)

-   Merge 3.6.3
    [\#5446](https://github.com/gravitee-io/issues/issues/5446)

## Improvements

***Management***

-   Default Schema is now set to "public" for jdbc
    [\#5468](https://github.com/gravitee-io/issues/issues/5468)

# [APIM - 3.5.10 (2021-04-21)](https://github.com/gravitee-io/issues/milestone/364?closed=1)

## Bug fixes

***General***

-   API Design Cannot save and deploy policy more than once
    [\#5336](https://github.com/gravitee-io/issues/issues/5336)

-   Backport \#5159
    [\#5381](https://github.com/gravitee-io/issues/issues/5381)

-   CVE#2168 [\#5450](https://github.com/gravitee-io/issues/issues/5450)

-   CVE#2169 [\#5451](https://github.com/gravitee-io/issues/issues/5451)

***Management***

-   502 response received on health-check timeout
    [\#5342](https://github.com/gravitee-io/issues/issues/5342)

-   A Membership for member USER and ref GROUP already exists.
    [\#5413](https://github.com/gravitee-io/issues/issues/5413)

-   Health availability is KO when HC is disabled on a specific endpoint
    [\#5365](https://github.com/gravitee-io/issues/issues/5365)

-   Health-check details Response colors to be consistent with colors in
    the Platform logs
    [\#5309](https://github.com/gravitee-io/issues/issues/5309)

-   Improve the user account screen
    [\#5376](https://github.com/gravitee-io/issues/issues/5376)

-   Nullpointer exception on OIDC provider login after migration from
    1.30 [\#5410](https://github.com/gravitee-io/issues/issues/5410)

-   Policies configuration form not well displayed
    [\#5351](https://github.com/gravitee-io/issues/issues/5351)

-   Search criteria and table offset get lost when clicking *back to
    Health-check*
    [\#5302](https://github.com/gravitee-io/issues/issues/5302)

-   \[portal\] unable to logout with OIDC provider
    [\#5247](https://github.com/gravitee-io/issues/issues/5247)

***Managment***

-   API Analytics response payload not displayed, fails with javascript
    error e.getTextArea is not a function
    [\#5364](https://github.com/gravitee-io/issues/issues/5364)

***Portal***

-   AddressException when trying to submit a Ticket with custom "from"
    configuration that contains &lt;&gt;
    [\#5352](https://github.com/gravitee-io/issues/issues/5352)

-   Documentation pages not displayed (imported from 1.30)
    [\#5192](https://github.com/gravitee-io/issues/issues/5192)

-   Inconsistent display in Portal search box
    [\#5160](https://github.com/gravitee-io/issues/issues/5160)

## Features

***Management***

-   Add icon on policies
    [\#5399](https://github.com/gravitee-io/issues/issues/5399)

## Improvements

***Management***

-   Allows to sort the logs by API response time
    [\#3391](https://github.com/gravitee-io/issues/issues/3391)

-   Naming confusion between path authorizations and resource filtering
    [\#5464](https://github.com/gravitee-io/issues/issues/5464)

# [APIM - 3.8.0 (2021-04-16)](https://github.com/gravitee-io/issues/milestone/241?closed=1)

## Bug fixes

***Management***

-   API creation and permissions
    [\#5416](https://github.com/gravitee-io/issues/issues/5416)

## Features

***Gateway***

-   Readiness vs Liveness
    [\#4902](https://github.com/gravitee-io/issues/issues/4902)

-   Resource information in health API
    [\#4903](https://github.com/gravitee-io/issues/issues/4903)

***Management***

-   Allow to navigate to previous / next log
    [\#4871](https://github.com/gravitee-io/issues/issues/4871)

-   Allows to restore an archived application
    [\#4453](https://github.com/gravitee-io/issues/issues/4453)

-   Contact subscribers as an API publisher
    [\#4896](https://github.com/gravitee-io/issues/issues/4896)

-   Dashboard of all alerts
    [\#4892](https://github.com/gravitee-io/issues/issues/4892)

-   Display groups in user account information
    [\#4870](https://github.com/gravitee-io/issues/issues/4870)

-   Private page
    [\#4893](https://github.com/gravitee-io/issues/issues/4893)

-   Traffic shadowing
    [\#5186](https://github.com/gravitee-io/issues/issues/5186)

***Policy***

-   \[jwt\] Allows to configure the client id claims
    [\#4900](https://github.com/gravitee-io/issues/issues/4900)

***Portal***

-   Allows to change favicon
    [\#4855](https://github.com/gravitee-io/issues/issues/4855)

-   Override the main sentence in the homepage
    [\#4856](https://github.com/gravitee-io/issues/issues/4856)

## Improvements

***Gateway***

-   Allow to filter probes on health resource
    [\#5236](https://github.com/gravitee-io/issues/issues/5236)

***Management***

-   Add ACL on the custom links
    [\#4563](https://github.com/gravitee-io/issues/issues/4563)

-   \[portal\] Update ui-component library to 2.3.1
    [\#5389](https://github.com/gravitee-io/issues/issues/5389)

***Policy***

-   Endpoint reference from policy
    [\#5268](https://github.com/gravitee-io/issues/issues/5268)

# [APIM - 3.6.3 (2021-04-15)](https://github.com/gravitee-io/issues/milestone/370?closed=1)

## Bug fixes

***Cockpit***

-   Backport \#5170 (delete installation)
    [\#5430](https://github.com/gravitee-io/issues/issues/5430)

***Management***

-   Cannot login with new users with newsletter
    [\#5423](https://github.com/gravitee-io/issues/issues/5423)

## Features

***General***

-   New http-signature policy with support for base64 encoding
    [\#5408](https://github.com/gravitee-io/issues/issues/5408)

# [APIM - 3.7.1 (2021-04-10)](https://github.com/gravitee-io/issues/milestone/363?closed=1)

## Bug fixes

***General***

-   . This error mainly occurs when the policy is linked to a missing
    resource, for example a cache or an oauth2 resource. Please check
    your policy configuration!"
    [\#5354](https://github.com/gravitee-io/issues/issues/5354)

-   Merge 3.6.2
    [\#5360](https://github.com/gravitee-io/issues/issues/5360)

# [APIM - 3.6.2 (2021-04-06)](https://github.com/gravitee-io/issues/milestone/358?closed=1)

## Bug fixes

***General***

-   Merge 3.5.9
    [\#5326](https://github.com/gravitee-io/issues/issues/5326)

***Management***

-   As a simple USER I can see the Analytics dashboard but I have a
    permission error
    [\#5251](https://github.com/gravitee-io/issues/issues/5251)

-   In a multi env context search of APIs is not working well
    [\#5296](https://github.com/gravitee-io/issues/issues/5296)

-   Portal authentication settings has disappeared
    [\#5278](https://github.com/gravitee-io/issues/issues/5278)

-   Unable to save an api Cron expression must consist of 6 fields
    (found 0 in \\"\\")
    [\#5118](https://github.com/gravitee-io/issues/issues/5118)

-   User pre-registration does not work with an OIDC provider
    [\#5159](https://github.com/gravitee-io/issues/issues/5159)

***Portal***

-   Example and schema imported from swagger document not displayed in
    portal [\#5202](https://github.com/gravitee-io/issues/issues/5202)

# [APIM - 3.5.9 (2021-03-30)](https://github.com/gravitee-io/issues/milestone/361?closed=1)

## Bug fixes

***General***

-   Merge 3.0.16
    [\#5299](https://github.com/gravitee-io/issues/issues/5299)

-   ResonseContainer Annotation does not work for `Page` and
    `PagedResult`
    [\#5289](https://github.com/gravitee-io/issues/issues/5289)

***Management***

-   Dates are not updated when create/update a category
    [\#5275](https://github.com/gravitee-io/issues/issues/5275)

-   JWT Plan - resolver param using JWKS URL with EL get unresolved
    (Error 404)
    [\#5206](https://github.com/gravitee-io/issues/issues/5206)

-   Minimum limit on IDP name is too short
    [\#5297](https://github.com/gravitee-io/issues/issues/5297)

-   Unable to subscribe to public apis from an application
    [\#5223](https://github.com/gravitee-io/issues/issues/5223)

-   \[portal\] Groups get lost while changing the Application image in
    Portal [\#5274](https://github.com/gravitee-io/issues/issues/5274)

-   \[portal\] unable to logout with OIDC provider
    [\#5247](https://github.com/gravitee-io/issues/issues/5247)

***Repository***

-   \[jdbc\] Make the repositories transactional
    [\#5284](https://github.com/gravitee-io/issues/issues/5284)

## Improvements

***Management***

-   Dynamic newsletter taglines
    [\#5269](https://github.com/gravitee-io/issues/issues/5269)

# [APIM - 3.0.16 (2021-03-24)](https://github.com/gravitee-io/issues/milestone/337?closed=1)

## Bug fixes

***Console***

-   User can not access application analytics
    [\#4843](https://github.com/gravitee-io/issues/issues/4843)

***General***

-   Merge 1.30.30
    [\#4962](https://github.com/gravitee-io/issues/issues/4962)

-   Merge 1.30.31
    [\#5288](https://github.com/gravitee-io/issues/issues/5288)

***Management***

-   Client side code injection
    [\#5031](https://github.com/gravitee-io/issues/issues/5031)

-   Do not use system proxy by default for OAuth authentication
    [\#5281](https://github.com/gravitee-io/issues/issues/5281)

-   Enable to search APIs
    [\#5043](https://github.com/gravitee-io/issues/issues/5043)

-   Event type button in dashboards are too big
    [\#4983](https://github.com/gravitee-io/issues/issues/4983)

***Oauth2***

-   Oauth2 Authentication of API Portal and API Management have not the
    same behavior
    [\#4058](https://github.com/gravitee-io/issues/issues/4058)

***Policy***

-   \[assign-content\] Template Injection
    [\#5033](https://github.com/gravitee-io/issues/issues/5033)

***Portal***

-   Do not display the "add application members" section if the current
    user has not the permission
    [\#4635](https://github.com/gravitee-io/issues/issues/4635)

## Improvements

***Management***

-   Access-Control-Allow-Origin regex fail and do not conform with
    rfc6454 and rfc3986
    [\#4796](https://github.com/gravitee-io/issues/issues/4796)

***Repository***

-   \[jdbc\] Add ability to set db schema name
    [\#4940](https://github.com/gravitee-io/issues/issues/4940)

# [APIM - 3.7.0 (2021-03-23)](https://github.com/gravitee-io/issues/milestone/240?closed=1)

## Bug fixes

***General***

-   Merge 3.6.1
    [\#5273](https://github.com/gravitee-io/issues/issues/5273)

## Features

***Management***

-   Define Group as Primary Owner of an API
    [\#5016](https://github.com/gravitee-io/issues/issues/5016)

-   Global markdown template pages
    [\#4465](https://github.com/gravitee-io/issues/issues/4465)

-   Searchable Metadata
    [\#5017](https://github.com/gravitee-io/issues/issues/5017)

***Policy***

-   \[cache\] Support of cache replication across an APIM cluster
    [\#599](https://github.com/gravitee-io/issues/issues/599)

-   \[oauth2\] Add a cache at the policy level
    [\#2298](https://github.com/gravitee-io/issues/issues/2298)

***Repository***

-   Allows to define a prefix for collections / tables
    [\#4715](https://github.com/gravitee-io/issues/issues/4715)

## Improvements

***Gateway***

-   Add the libraries to allow to write application logs in JSON by
    changing the logback configuration
    [\#5139](https://github.com/gravitee-io/issues/issues/5139)

***Reporter***

-   Metrics do not expose timestamp for formatters
    [\#5097](https://github.com/gravitee-io/issues/issues/5097)

***Resource***

-   \[cache\] Allows to limit the cache usage at the platform level
    [\#4455](https://github.com/gravitee-io/issues/issues/4455)

# [APIM - 3.6.1 (2021-03-19)](https://github.com/gravitee-io/issues/milestone/348?closed=1)

## Bug fixes

***General***

-   Merge 3.5.5
    [\#5246](https://github.com/gravitee-io/issues/issues/5246)

-   Merge 3.5.6
    [\#5248](https://github.com/gravitee-io/issues/issues/5248)

-   Merge 3.5.7
    [\#5249](https://github.com/gravitee-io/issues/issues/5249)

-   Merge 3.5.8
    [\#5264](https://github.com/gravitee-io/issues/issues/5264)

-   Migration from 3.5.x to 3.6.x fails with MySQL
    [\#5175](https://github.com/gravitee-io/issues/issues/5175)

***Management***

-   Error when trying to log in using an OpenIDConnect Provider
    [\#5144](https://github.com/gravitee-io/issues/issues/5144)

-   \[multi-org\] Allow to change the current organization in the
    console [\#5044](https://github.com/gravitee-io/issues/issues/5044)

***Policy***

-   \[hmac\]Error 500 on HMAC Http Signature policy
    [\#5180](https://github.com/gravitee-io/issues/issues/5180)

***Portal***

-   Fix the api subscription screen
    [\#5103](https://github.com/gravitee-io/issues/issues/5103)

# [APIM - 3.5.8 (2021-03-18)](https://github.com/gravitee-io/issues/milestone/355?closed=1)

## Bug fixes

***Management***

-   Cannot create dynamic properties
    [\#5230](https://github.com/gravitee-io/issues/issues/5230)

-   I18n base path reference is incorrect
    [\#5240](https://github.com/gravitee-io/issues/issues/5240)

-   Quality metrics not shown in APIs main page
    [\#5238](https://github.com/gravitee-io/issues/issues/5238)

-   Using the right naming convention
    [\#5235](https://github.com/gravitee-io/issues/issues/5235)

-   \[portal\] image media uri is not right
    [\#5244](https://github.com/gravitee-io/issues/issues/5244)

***Policy***

-   \[rest-to-soap\] Can not use query parameters from SOAP envelope
    template [\#5209](https://github.com/gravitee-io/issues/issues/5209)

***Portal***

-   Application menus are not correctly displayed
    [\#5207](https://github.com/gravitee-io/issues/issues/5207)

-   Cannot read menu entries when is in a sticky mode
    [\#5233](https://github.com/gravitee-io/issues/issues/5233)

-   Dasboard list have wrong style
    [\#5121](https://github.com/gravitee-io/issues/issues/5121)

-   Display type selector cannot be seen well
    [\#5234](https://github.com/gravitee-io/issues/issues/5234)

***Repository***

-   \[http\] Improve server to execute repository requests
    [\#5203](https://github.com/gravitee-io/issues/issues/5203)

-   \[http\] Remove strong constraint on client / server version
    [\#5204](https://github.com/gravitee-io/issues/issues/5204)

# [APIM - 3.5.7 (2021-03-11)](https://github.com/gravitee-io/issues/milestone/353?closed=1)

## Bug fixes

***Management***

-   Cannot delete a deprecated API anymore
    [\#5113](https://github.com/gravitee-io/issues/issues/5113)

-   Some API Logging settings get lost after saving
    [\#5164](https://github.com/gravitee-io/issues/issues/5164)

***Reporter***

-   \[tcp | file\] Monitor elasticsearch output contains a wrong id
    value [\#5181](https://github.com/gravitee-io/issues/issues/5181)

-   \[tcp\] Reporter must be disabled by default
    [\#5183](https://github.com/gravitee-io/issues/issues/5183)

## Improvements

***Gateway***

-   Add SNI support
    [\#5194](https://github.com/gravitee-io/issues/issues/5194)

-   Heartbeat is storing unlimited events which may cause OOM
    [\#5191](https://github.com/gravitee-io/issues/issues/5191)

# [APIM - 3.5.6 (2021-03-09)](https://github.com/gravitee-io/issues/milestone/349?closed=1)

## Bug fixes

***Management***

-   Can’t access a group page if too many users
    [\#5083](https://github.com/gravitee-io/issues/issues/5083)

-   Closed plans are visible in the design studio
    [\#5122](https://github.com/gravitee-io/issues/issues/5122)

***Portal***

-   Permissions issue when accessing category documentation
    [\#5114](https://github.com/gravitee-io/issues/issues/5114)

***Repository***

-   \[bridge\] Unable to retrieve subscriptions for some APIs
    [\#5176](https://github.com/gravitee-io/issues/issues/5176)

## Features

***Repository***

-   \[bridge\] Add support for HTTP/S proxy
    [\#5178](https://github.com/gravitee-io/issues/issues/5178)

## Improvements

***Management***

-   Improve /apis performance
    [\#5045](https://github.com/gravitee-io/issues/issues/5045)

# [APIM - 3.5.5 (2021-02-24)](https://github.com/gravitee-io/issues/milestone/344?closed=1)

## Bug fixes

***Gateway***

-   \[hc\] handle DAYS time unit
    [\#5085](https://github.com/gravitee-io/issues/issues/5085)

***Management***

-   A user should only see APIs it can manage
    [\#5096](https://github.com/gravitee-io/issues/issues/5096)

-   EL inputs should be in single line mode
    [\#5086](https://github.com/gravitee-io/issues/issues/5086)

-   Handle default value during policy schema validation
    [\#5095](https://github.com/gravitee-io/issues/issues/5095)

-   Missing response templates when creating or updating a plan
    [\#5110](https://github.com/gravitee-io/issues/issues/5110)

-   User not found when looking for subscriptions
    [\#5091](https://github.com/gravitee-io/issues/issues/5091)

***Policy***

-   \[circuit-breaker\] Use the correct types in the UI form
    [\#5116](https://github.com/gravitee-io/issues/issues/5116)

***Portal***

-   Css issue when displaying my subscriptions
    [\#5094](https://github.com/gravitee-io/issues/issues/5094)

## Improvements

***Management-ui***

-   Hide swagger authorization button if try it option is disabled
    [\#5100](https://github.com/gravitee-io/issues/issues/5100)

# [APIM - 3.6.0 (2021-02-18)](https://github.com/gravitee-io/issues/milestone/239?closed=1)

## Bug fixes

***General***

-   Merge 3.5.2
    [\#4961](https://github.com/gravitee-io/issues/issues/4961)

-   Merge 3.5.3
    [\#5025](https://github.com/gravitee-io/issues/issues/5025)

-   Merge 3.5.4
    [\#5084](https://github.com/gravitee-io/issues/issues/5084)

## Features

***Management***

-   Advanced API logging configuration
    [\#4745](https://github.com/gravitee-io/issues/issues/4745)

-   Associate a label to an API deployment
    [\#4742](https://github.com/gravitee-io/issues/issues/4742)

-   Be able to enable / disable health-check during some periods
    [\#4043](https://github.com/gravitee-io/issues/issues/4043)

-   Cockpit authentication support
    [\#4522](https://github.com/gravitee-io/issues/issues/4522)

-   Console dashboard page
    [\#4747](https://github.com/gravitee-io/issues/issues/4747)

-   Define HTTP verb for dynamic properties and dictionaries
    [\#4746](https://github.com/gravitee-io/issues/issues/4746)

-   Display deployments markups on analytics charts
    [\#4743](https://github.com/gravitee-io/issues/issues/4743)

-   Improve logging configuration for GDPR compliance
    [\#3919](https://github.com/gravitee-io/issues/issues/3919)

-   Manage Cockpit installation registration
    [\#4766](https://github.com/gravitee-io/issues/issues/4766)

-   Move organization & environment creation to command handler
    [\#4287](https://github.com/gravitee-io/issues/issues/4287)

-   Policy studio history preview
    [\#4749](https://github.com/gravitee-io/issues/issues/4749)

-   Propagate installation events to APIM
    [\#4945](https://github.com/gravitee-io/issues/issues/4945)

-   Status page for endpoints based on HC
    [\#4750](https://github.com/gravitee-io/issues/issues/4750)

-   \[multi-env\] Display current environment id in the console URL
    [\#4778](https://github.com/gravitee-io/issues/issues/4778)

***Policy***

-   \[assign-metrics\] Allows to add some custom metrics in analytics
    [\#4769](https://github.com/gravitee-io/issues/issues/4769)

-   \[hmac\] Enable HMAC authentication
    [\#4813](https://github.com/gravitee-io/issues/issues/4813)

***Reporter***

-   \[elasticsearch\] Auto-enable geo-ip, user-agent when Elasticsearch
    &gt;= 7.x
    [\#4744](https://github.com/gravitee-io/issues/issues/4744)

## Improvements

***Analytics***

-   Improve Log detail view
    [\#4815](https://github.com/gravitee-io/issues/issues/4815)

***Identity-providers***

-   \[multi-env\] Adapt role mapping screen for multi-environment
    [\#4803](https://github.com/gravitee-io/issues/issues/4803)

***Management***

-   Add more configuration options on dynamic dictionaries / properties
    [\#4447](https://github.com/gravitee-io/issues/issues/4447)

-   Allows to select groups while creating an API
    [\#4449](https://github.com/gravitee-io/issues/issues/4449)

-   \[multi-env\] Handle environment switching
    [\#4777](https://github.com/gravitee-io/issues/issues/4777)

-   \[multi-env\] Handle user without environments permissions
    [\#4774](https://github.com/gravitee-io/issues/issues/4774)

-   \[multi-env\]Default application creation
    [\#4776](https://github.com/gravitee-io/issues/issues/4776)

***Policy***

-   \[json-xml\] Allows to transform a JSON to a XML
    [\#4561](https://github.com/gravitee-io/issues/issues/4561)

***Portal***

-   Display the category selected to navigate to the current API page
    [\#4466](https://github.com/gravitee-io/issues/issues/4466)

-   EN typo [\#4857](https://github.com/gravitee-io/issues/issues/4857)

# [APIM - 3.5.4 (2021-02-15)](https://github.com/gravitee-io/issues/milestone/342?closed=1)

## Bug fixes

***Gateway***

-   Policies are executed following wrong order for response stream
    policy flow
    [\#5054](https://github.com/gravitee-io/issues/issues/5054)

-   \[healthcheck\] Exception on HC request should return a 502 instead
    of 503 [\#5059](https://github.com/gravitee-io/issues/issues/5059)

***General***

-   Backport \#4653
    [\#5076](https://github.com/gravitee-io/issues/issues/5076)

***Management***

-   Enable to search APIs
    [\#5080](https://github.com/gravitee-io/issues/issues/5080)

-   Unable to delete a metadata when I delete an API
    [\#5000](https://github.com/gravitee-io/issues/issues/5000)

-   \[policy-studio\] Impossible to scroll on code field when have long
    text [\#5060](https://github.com/gravitee-io/issues/issues/5060)

***Management-api***

-   Do not expose sensitive information from settings endpoint
    [\#5034](https://github.com/gravitee-io/issues/issues/5034)

***Management-ui***

-   Calendar widget is not accurate
    [\#5027](https://github.com/gravitee-io/issues/issues/5027)

***Policy***

-   \[groovy\] add documentation in the studio
    [\#5077](https://github.com/gravitee-io/issues/issues/5077)

-   \[groovy\] unable to whitelist array.getAt
    [\#5075](https://github.com/gravitee-io/issues/issues/5075)

***Repository***

-   \[mongodb\] Unable to save dictionary with properties containing a
    dot [\#5072](https://github.com/gravitee-io/issues/issues/5072)

## Improvements

***General***

-   Missing id\_token\_hint on logout endpoint
    [\#4975](https://github.com/gravitee-io/issues/issues/4975)

# [APIM - 3.5.3 (2021-02-06)](https://github.com/gravitee-io/issues/milestone/339?closed=1)

## Bug fixes

***Gateway***

-   Problem with the execution order of the policies of a response flow
    [\#4973](https://github.com/gravitee-io/issues/issues/4973)

***General***

-   Merge 3.4.3
    [\#5001](https://github.com/gravitee-io/issues/issues/5001)

***Management***

-   Cannot deploy APIs with configured HTTP headers at the endpoint
    level or health check
    [\#4963](https://github.com/gravitee-io/issues/issues/4963)

-   Manage WSDL imports when creating or updating an API
    [\#4976](https://github.com/gravitee-io/issues/issues/4976)

-   Policies on path are not updated when updating an API with swagger
    [\#4970](https://github.com/gravitee-io/issues/issues/4970)

-   SecurityDefinition is missing when migrating API from v1 to v2
    definition
    [\#4979](https://github.com/gravitee-io/issues/issues/4979)

# [APIM - 3.4.3 (2021-02-01)](https://github.com/gravitee-io/issues/milestone/327?closed=1)

## Bug fixes

***General***

-   Backport \#4592 to 3.4.x
    [\#4864](https://github.com/gravitee-io/issues/issues/4864)

-   Backport \#4797 to 3.4.x
    [\#4800](https://github.com/gravitee-io/issues/issues/4800)

-   Backport 4761
    [\#4783](https://github.com/gravitee-io/issues/issues/4783)

-   Client ID and Client Secret are not shown in developer portal
    [\#4779](https://github.com/gravitee-io/issues/issues/4779)

-   Merge 3.0.14
    [\#4853](https://github.com/gravitee-io/issues/issues/4853)

-   Merge 3.0.15
    [\#4923](https://github.com/gravitee-io/issues/issues/4923)

***Management***

-   A new invited user does not have environment role
    [\#4833](https://github.com/gravitee-io/issues/issues/4833)

-   Dictionary start/stop API fails in case of empty Accept header
    [\#4740](https://github.com/gravitee-io/issues/issues/4740)

-   Duplicate pages when importing an API
    [\#4944](https://github.com/gravitee-io/issues/issues/4944)

-   Fix swagger documentation
    [\#4726](https://github.com/gravitee-io/issues/issues/4726)

-   Improve attach media feature
    [\#4702](https://github.com/gravitee-io/issues/issues/4702)

-   Manage rights on the plans displayed on the policy studio
    [\#4770](https://github.com/gravitee-io/issues/issues/4770)

-   OpenAPI with external $ref is not well parsed
    [\#4967](https://github.com/gravitee-io/issues/issues/4967)

-   Swagger type is not sync with API model
    [\#4788](https://github.com/gravitee-io/issues/issues/4788)

-   \[studio\] scope is not automaticaly selected
    [\#4801](https://github.com/gravitee-io/issues/issues/4801)

***Portal***

-   Enable to subscribe to a jwt plan with an app with a client\_id
    [\#4724](https://github.com/gravitee-io/issues/issues/4724)

-   Has invalid dates when viewing a pending subscription
    [\#4873](https://github.com/gravitee-io/issues/issues/4873)

## Improvements

***Gateway***

-   Allow to use the system proxy for the endpoint health check
    [\#4627](https://github.com/gravitee-io/issues/issues/4627)

***Management***

-   Handle input type password in schema form
    [\#4701](https://github.com/gravitee-io/issues/issues/4701)

***Repository***

-   \[mongodb\] Improve 3.4.0 update script
    [\#4881](https://github.com/gravitee-io/issues/issues/4881)

# [APIM - 3.5.2 (2021-01-22)](https://github.com/gravitee-io/issues/milestone/334?closed=1)

## Bug fixes

***Gateway***

-   PathParametersIndexProcessor error for specific request pathInfo
    [\#4960](https://github.com/gravitee-io/issues/issues/4960)

***Management***

-   Disable default username / password for SMTP
    [\#4913](https://github.com/gravitee-io/issues/issues/4913)

-   Error when trying to access Design menu with new design studio and
    without admin rights
    [\#4925](https://github.com/gravitee-io/issues/issues/4925)

-   Social authentication is not working anymore
    [\#4937](https://github.com/gravitee-io/issues/issues/4937)

***Policy***

-   \[ip-filtering\] Empty IPs can be defined as part of whitelist /
    blacklist
    [\#4912](https://github.com/gravitee-io/issues/issues/4912)

-   \[rest-to-soap\] do not override request path info
    [\#4860](https://github.com/gravitee-io/issues/issues/4860)

***Repository***

-   \[elasticsearch\] Retry is not working in case of non 2xx status
    code [\#4919](https://github.com/gravitee-io/issues/issues/4919)

## Improvements

***Management***

-   Newsletter improvment
    [\#4692](https://github.com/gravitee-io/issues/issues/4692)

-   Social idp are not enabled after creation
    [\#4956](https://github.com/gravitee-io/issues/issues/4956)

***Portal***

-   Align delete link in aside box
    [\#4926](https://github.com/gravitee-io/issues/issues/4926)

# [APIM - 3.0.15 (2021-01-18)](https://github.com/gravitee-io/issues/milestone/329?closed=1)

## Bug fixes

***Management***

-   Add HTTP proxy configuration for the OAuth2AuthenticationResource
    [\#4398](https://github.com/gravitee-io/issues/issues/4398)

-   I18n error on console start in production mode
    [\#4878](https://github.com/gravitee-io/issues/issues/4878)

-   Input not disable for application group
    [\#4710](https://github.com/gravitee-io/issues/issues/4710)

-   Unable to finalize user invitation
    [\#4858](https://github.com/gravitee-io/issues/issues/4858)

***Repository***

-   \[jdbc\] Cannot remove a group anymore in some case
    [\#4785](https://github.com/gravitee-io/issues/issues/4785)

## Improvements

***Resource***

-   \[am\] Add trailing slash to the URL automatically
    [\#4907](https://github.com/gravitee-io/issues/issues/4907)

# [APIM - 3.5.1 (2021-01-13)](https://github.com/gravitee-io/issues/milestone/324?closed=1)

## Bug fixes

***Console***

-   Contextual documentation
    `management-configuration-identityproviders.md` is missing
    [\#4890](https://github.com/gravitee-io/issues/issues/4890)

-   Revoked apikey can not be reactived
    [\#4850](https://github.com/gravitee-io/issues/issues/4850)

***Gateway***

-   ALPN is enabled by default if ssl is disabled
    [\#4887](https://github.com/gravitee-io/issues/issues/4887)

***Management***

-   Mails are not sent anymore with authenticated smtp
    [\#4904](https://github.com/gravitee-io/issues/issues/4904)

-   Missing environment id when fetching current user tasks
    [\#4862](https://github.com/gravitee-io/issues/issues/4862)

-   Swagger parsing with fully resolve mode may result in OOM
    [\#4906](https://github.com/gravitee-io/issues/issues/4906)

-   WSDL import generate wrong scope for `xml-to-json` policy
    [\#4879](https://github.com/gravitee-io/issues/issues/4879)

***Ui***

-   Alert menu does not appears anymore at API level
    [\#4908](https://github.com/gravitee-io/issues/issues/4908)

## Improvements

***Policy***

-   \[Retry\] Use Expression Language Editor in schema-form
    [\#4844](https://github.com/gravitee-io/issues/issues/4844)

# [APIM - 3.0.14 (2020-12-28)](https://github.com/gravitee-io/issues/milestone/316?closed=1)

## Bug fixes

***Gateway***

-   Unable to disable websockets support
    [\#4476](https://github.com/gravitee-io/issues/issues/4476)

-   Unable to establish websocket connection
    [\#4768](https://github.com/gravitee-io/issues/issues/4768)

***General***

-   Backport \#4798 to 3.0.x
    [\#4846](https://github.com/gravitee-io/issues/issues/4846)

-   Backport \#4825 to 3.0.x
    [\#4826](https://github.com/gravitee-io/issues/issues/4826)

-   Backport 4669 to 3.0.x
    [\#4670](https://github.com/gravitee-io/issues/issues/4670)

-   Backport 4678
    [\#4679](https://github.com/gravitee-io/issues/issues/4679)

-   Backport 4680
    [\#4681](https://github.com/gravitee-io/issues/issues/4681)

-   Backport 4823 to 3.0.x
    [\#4824](https://github.com/gravitee-io/issues/issues/4824)

-   Inconsistent synchronization between portal and management ui when
    using OIDC
    [\#4532](https://github.com/gravitee-io/issues/issues/4532)

-   Merge 1.30.29
    [\#4794](https://github.com/gravitee-io/issues/issues/4794)

***Management***

-   API import not working with a documentation fetcher from a future
    version (configuration not compatible)
    [\#4806](https://github.com/gravitee-io/issues/issues/4806)

-   Add HTTP proxy configuration for the AMAuthenticationResource
    [\#4832](https://github.com/gravitee-io/issues/issues/4832)

-   Cannot define a scope on Authentication creation but only on update
    [\#4684](https://github.com/gravitee-io/issues/issues/4684)

-   Closing a subscription with an expiry date is still active
    [\#4799](https://github.com/gravitee-io/issues/issues/4799)

-   Hits by country not well sorted
    [\#4668](https://github.com/gravitee-io/issues/issues/4668)

-   Markdown generation issue with too big images
    [\#4810](https://github.com/gravitee-io/issues/issues/4810)

***Portal***

-   Do not display error when metrics cannot be retrieved on an
    application
    [\#4677](https://github.com/gravitee-io/issues/issues/4677)

-   Link to an unpublished API should not be display in subscriptions
    [\#4836](https://github.com/gravitee-io/issues/issues/4836)

-   User without rights on Applications should not see the menu and be
    able to browse the dashboard
    [\#4675](https://github.com/gravitee-io/issues/issues/4675)

## Improvements

***Management***

-   Update user profile information
    [\#4618](https://github.com/gravitee-io/issues/issues/4618)

# [APIM - 3.5.0 (2020-12-23)](https://github.com/gravitee-io/issues/milestone/238?closed=1)

## Bug fixes

***Gateway***

-   Avoid usage of URI.create to handle properly path and query
    parameters with special caracters
    [\#4837](https://github.com/gravitee-io/issues/issues/4837)

***General***

-   Merge 3.4.1
    [\#4775](https://github.com/gravitee-io/issues/issues/4775)

-   Merge 3.4.2
    [\#4790](https://github.com/gravitee-io/issues/issues/4790)

-   Report bug 4756 to master
    [\#4757](https://github.com/gravitee-io/issues/issues/4757)

***Identity-providers***

-   Can’t sign in on console with an IDP that is not enabled for portal
    [\#4797](https://github.com/gravitee-io/issues/issues/4797)

***Management***

-   An api-key can not be reactivated for a closed plan
    [\#4798](https://github.com/gravitee-io/issues/issues/4798)

-   Cannot change an existing plan to add restrictions
    [\#4761](https://github.com/gravitee-io/issues/issues/4761)

-   Environment Role is not being set with Role Mapping
    [\#4762](https://github.com/gravitee-io/issues/issues/4762)

***Policy***

-   \[CalloutHttp\] variables should be optional
    [\#4818](https://github.com/gravitee-io/issues/issues/4818)

***Portal***

-   404 when filtering on all APIs
    [\#4823](https://github.com/gravitee-io/issues/issues/4823)

-   Missing one API when filtering by category
    [\#4825](https://github.com/gravitee-io/issues/issues/4825)

## Features

***Gateway***

-   Fine-grained conditional policies
    [\#60](https://github.com/gravitee-io/issues/issues/60)

-   Handle best match on the policy flows
    [\#4598](https://github.com/gravitee-io/issues/issues/4598)

***Management***

-   Allows to migrate from policy studio v1 to v2
    [\#4589](https://github.com/gravitee-io/issues/issues/4589)

-   Default response template per API
    [\#4464](https://github.com/gravitee-io/issues/issues/4464)

***Policy***

-   Retry policy
    [\#4802](https://github.com/gravitee-io/issues/issues/4802)

## Improvements

***Gateway***

-   Support for cipher suites configuration
    [\#4541](https://github.com/gravitee-io/issues/issues/4541)

***General***

-   Change the subject of emails about adding members
    [\#4809](https://github.com/gravitee-io/issues/issues/4809)

***Management***

-   Better handling of settings (report \#4787)
    [\#4804](https://github.com/gravitee-io/issues/issues/4804)

-   Make APIM Console multi-env ready
    [\#4151](https://github.com/gravitee-io/issues/issues/4151)

-   Multi tenancy parameters - implementation
    [\#4642](https://github.com/gravitee-io/issues/issues/4642)

***Policies***

-   Update documentation
    [\#4831](https://github.com/gravitee-io/issues/issues/4831)

***Repository***

-   \[redis\] Add support for Redis Sentinel
    [\#79](https://github.com/gravitee-io/issues/issues/79)

# [APIM - 3.4.2 (2020-12-13)](https://github.com/gravitee-io/issues/milestone/321?closed=1)

## Bug fixes

***General***

-   Backport 4762 to 3.4.x
    [\#4780](https://github.com/gravitee-io/issues/issues/4780)

***Management***

-   Wrong email template when resetting a password
    [\#4756](https://github.com/gravitee-io/issues/issues/4756)

## Improvements

***Management***

-   Better handling of settings
    [\#4787](https://github.com/gravitee-io/issues/issues/4787)

# [APIM - 3.4.1 (2020-12-08)](https://github.com/gravitee-io/issues/milestone/317?closed=1)

## Bug fixes

***Management***

-   API importing block is too small and does not scroll
    [\#4723](https://github.com/gravitee-io/issues/issues/4723)

-   Cannot create a plan with rate limiting restriction on an API
    created with the new design studio
    [\#4700](https://github.com/gravitee-io/issues/issues/4700)

-   Cannot save good script values on Grooy policy with policy-studio
    [\#4712](https://github.com/gravitee-io/issues/issues/4712)

-   Create or Update API with duplicated label fails with
    SQLIntegrityConstraintViolationException
    [\#4704](https://github.com/gravitee-io/issues/issues/4704)

-   Ignore missing properties when updating settings.
    [\#4682](https://github.com/gravitee-io/issues/issues/4682)

-   Not able to define mock body with policy studio
    [\#4665](https://github.com/gravitee-io/issues/issues/4665)

-   Sometimes APIs are not well deployed in gateway
    [\#4707](https://github.com/gravitee-io/issues/issues/4707)

-   Wrong format of securitydefinition when create a plan
    [\#4714](https://github.com/gravitee-io/issues/issues/4714)

-   \[policy-validate-request\] unable to create a complex validation
    [\#4722](https://github.com/gravitee-io/issues/issues/4722)

***Portal***

-   Media links are not well computed
    [\#4669](https://github.com/gravitee-io/issues/issues/4669)

# [APIM - 3.3.4 (2020-12-01)](https://github.com/gravitee-io/issues/milestone/309?closed=1)

## Bug fixes

***General***

-   Backport \#4655 to 3.3.x
    [\#4657](https://github.com/gravitee-io/issues/issues/4657)

-   Backport 4578
    [\#4608](https://github.com/gravitee-io/issues/issues/4608)

-   Backport 4591
    [\#4607](https://github.com/gravitee-io/issues/issues/4607)

-   Backport 4620 and 4669 to 3.3.x
    [\#4630](https://github.com/gravitee-io/issues/issues/4630)

-   Backport 4634 to 3.3.x
    [\#4636](https://github.com/gravitee-io/issues/issues/4636)

-   Merge 3.2.3
    [\#4676](https://github.com/gravitee-io/issues/issues/4676)

***Portal***

-   Example cURL not displayed for an unpublished API on subscriptions
    [\#4680](https://github.com/gravitee-io/issues/issues/4680)

***Reporter***

-   \[elasticsearch\] Template mapping of log is incorrect with ES 7.x
    [\#4685](https://github.com/gravitee-io/issues/issues/4685)

***Repository***

-   \[jdbc\] Simple user without groups can see all the applications
    [\#4678](https://github.com/gravitee-io/issues/issues/4678)

## Improvements

***Management***

-   Check that the version of the accepted CGU is the current one
    [\#4603](https://github.com/gravitee-io/issues/issues/4603)

-   Manage attached resources in API import/export
    [\#4315](https://github.com/gravitee-io/issues/issues/4315)

# [APIM - 3.2.3 (2020-11-27)](https://github.com/gravitee-io/issues/milestone/304?closed=1)

## Bug fixes

***General***

-   Merge 3.0.13
    [\#4671](https://github.com/gravitee-io/issues/issues/4671)

***Management***

-   Backport \#4551 on 3.2.x
    [\#4552](https://github.com/gravitee-io/issues/issues/4552)

-   Cannot reorder a page anymore
    [\#4417](https://github.com/gravitee-io/issues/issues/4417)

-   Forbidden access with a Authorization bearer token
    [\#4440](https://github.com/gravitee-io/issues/issues/4440)

-   Null constraint violation with jdbc repository at startup
    [\#4521](https://github.com/gravitee-io/issues/issues/4521)

# [APIM - 3.0.13 (2020-11-26)](https://github.com/gravitee-io/issues/milestone/310?closed=1)

## Bug fixes

***General***

-   Backport \#4620 to 3.0.x
    [\#4629](https://github.com/gravitee-io/issues/issues/4629)

-   Backport 4585
    [\#4606](https://github.com/gravitee-io/issues/issues/4606)

-   Backport 4591 to 3.0.x
    [\#4619](https://github.com/gravitee-io/issues/issues/4619)

-   Merge 1.30.26
    [\#4663](https://github.com/gravitee-io/issues/issues/4663)

***Management***

-   API not found on global dashboard when deleted
    [\#4573](https://github.com/gravitee-io/issues/issues/4573)

-   Cannot create an API and ask for review
    [\#4571](https://github.com/gravitee-io/issues/issues/4571)

-   Config file user roles are ignored when user is assigned to a group
    before his first login
    [\#4586](https://github.com/gravitee-io/issues/issues/4586)

-   Export logs in CSV should contain the user when it is displayed
    [\#4659](https://github.com/gravitee-io/issues/issues/4659)

-   Importing theme with images fails
    [\#4179](https://github.com/gravitee-io/issues/issues/4179)

-   Improve UI when search user to add
    [\#4599](https://github.com/gravitee-io/issues/issues/4599)

-   Location header does not contain full path to resource
    [\#4624](https://github.com/gravitee-io/issues/issues/4624)

-   Unable to delete the homepage background
    [\#4213](https://github.com/gravitee-io/issues/issues/4213)

***Portal***

-   Cannot list more than 10 plans during the subscription
    [\#4653](https://github.com/gravitee-io/issues/issues/4653)

-   Cannot search on labels with some special characters
    [\#4661](https://github.com/gravitee-io/issues/issues/4661)

-   Missing X-Xsrf-Token header from the portal UI in APIM
    [\#4628](https://github.com/gravitee-io/issues/issues/4628)

-   Size list of application log is not well updated
    [\#4662](https://github.com/gravitee-io/issues/issues/4662)

## Improvements

***Management***

-   Allows to export all the logs in a CSV and not only the current page
    [\#4664](https://github.com/gravitee-io/issues/issues/4664)

# [APIM - 3.4.0 (2020-11-24)](https://github.com/gravitee-io/issues/milestone/237?closed=1)

## Bug fixes

***Gateway***

-   Graceful shutdown on streamFailWith
    [\#4648](https://github.com/gravitee-io/issues/issues/4648)

-   Manage graceful shutdown for 3.x
    [\#4632](https://github.com/gravitee-io/issues/issues/4632)

***General***

-   Add an API from another docker-compose stack than the Gravitee one
    [\#4640](https://github.com/gravitee-io/issues/issues/4640)

-   Typo in french portal translation when connection issues
    [\#4504](https://github.com/gravitee-io/issues/issues/4504)

***Management***

-   Cannot create an API from a Gravitee.io definition anymore
    [\#4570](https://github.com/gravitee-io/issues/issues/4570)

-   Default admin can’t see/go to the dashboard and settings menu
    [\#4591](https://github.com/gravitee-io/issues/issues/4591)

-   Default application is not correctly created for social / OAuth
    login [\#4634](https://github.com/gravitee-io/issues/issues/4634)

-   Impossible to move documentation page to folder
    [\#4655](https://github.com/gravitee-io/issues/issues/4655)

-   Portal and Schedulers sections appear two times in settings
    [\#4578](https://github.com/gravitee-io/issues/issues/4578)

-   Redoc is not working with a private API on dist
    [\#4585](https://github.com/gravitee-io/issues/issues/4585)

-   \[quality-rules\]unable to create a new quality-rule
    [\#4602](https://github.com/gravitee-io/issues/issues/4602)

***Plugin***

-   Ensure plugin loading order
    [\#4486](https://github.com/gravitee-io/issues/issues/4486)

***Portal***

-   Image links are broken on portal documentation
    [\#4620](https://github.com/gravitee-io/issues/issues/4620)

## Features

***Gateway***

-   Forward the X-Forwarded-Prefix to the backend endpoint
    [\#4434](https://github.com/gravitee-io/issues/issues/4434)

-   Support for path-named parameters in Expression Language (EL)
    [\#4431](https://github.com/gravitee-io/issues/issues/4431)

***Management***

-   Allows to manage authentication identity providers on the portal
    [\#3963](https://github.com/gravitee-io/issues/issues/3963)

-   Global reviewer
    [\#4436](https://github.com/gravitee-io/issues/issues/4436)

-   Label’s dictionary
    [\#4437](https://github.com/gravitee-io/issues/issues/4437)

-   Move CORS from static to dynamic configuration
    [\#4432](https://github.com/gravitee-io/issues/issues/4432)

-   Move SMTP from static to dynamic configuration
    [\#4433](https://github.com/gravitee-io/issues/issues/4433)

-   Move notification templates in the UI
    [\#4297](https://github.com/gravitee-io/issues/issues/4297)

-   Override settings via envvars
    [\#4452](https://github.com/gravitee-io/issues/issues/4452)

-   Support tickets history
    [\#4435](https://github.com/gravitee-io/issues/issues/4435)

-   \[audit\] Adapt audit system to Orgs & Envs
    [\#3976](https://github.com/gravitee-io/issues/issues/3976)

***Policy***

-   \[api-key\] Allows to define custom api-key
    [\#4318](https://github.com/gravitee-io/issues/issues/4318)

***Reporter***

-   \[file\] File reporter to write raw data (csv format)
    [\#4236](https://github.com/gravitee-io/issues/issues/4236)

-   \[tcp\] Add support for a TCP reporter
    [\#4584](https://github.com/gravitee-io/issues/issues/4584)

***Repository***

-   \[hazelcast\] Rate-limit support
    [\#4527](https://github.com/gravitee-io/issues/issues/4527)

## Improvements

***Management***

-   Allows to configure statically the theme
    [\#4456](https://github.com/gravitee-io/issues/issues/4456)

-   Allows to define the background color of the login page from the
    theme [\#4458](https://github.com/gravitee-io/issues/issues/4458)

-   Improve API Quality checks display
    [\#3201](https://github.com/gravitee-io/issues/issues/3201)

-   Remove i18n support on the management UI
    [\#4485](https://github.com/gravitee-io/issues/issues/4485)

***Policy***

-   \[aws-lambda\] Allows to extract data in execution context from
    payload [\#4395](https://github.com/gravitee-io/issues/issues/4395)

# [APIM - 3.0.12 (2020-11-15)](https://github.com/gravitee-io/issues/milestone/303?closed=1)

## Bug fixes

***General***

-   Backport 4602
    [\#4604](https://github.com/gravitee-io/issues/issues/4604)

-   Merge 1.30.25
    [\#4610](https://github.com/gravitee-io/issues/issues/4610)

***Swagger***

-   Only validate swagger content on create/update
    [\#4605](https://github.com/gravitee-io/issues/issues/4605)

***Ui-components***

-   Double icon rendering on gv-table
    [\#4523](https://github.com/gravitee-io/issues/issues/4523)

## Improvements

***Gateway***

-   HTTP code 414 (URL too long) with gateway
    [\#4534](https://github.com/gravitee-io/issues/issues/4534)

-   Support for TLS 1.3
    [\#4065](https://github.com/gravitee-io/issues/issues/4065)

# [APIM - 3.3.3 (2020-11-04)](https://github.com/gravitee-io/issues/milestone/306?closed=1)

## Bug fixes

***Management***

-   Cannot update roles of a user anymore
    [\#4551](https://github.com/gravitee-io/issues/issues/4551)

# [APIM - 3.3.2 (2020-11-03)](https://github.com/gravitee-io/issues/milestone/305?closed=1)

## Bug fixes

***Management-ui***

-   Connection pool min limit for an endpoint should be 1 and not 10
    [\#4543](https://github.com/gravitee-io/issues/issues/4543)

# [APIM - 3.3.1 (2020-11-03)](https://github.com/gravitee-io/issues/milestone/292?closed=1)

## Bug fixes

***General***

-   Merge 3.2.2
    [\#4559](https://github.com/gravitee-io/issues/issues/4559)

***Management***

-   Impossible to create Cache Policy
    [\#4478](https://github.com/gravitee-io/issues/issues/4478)

## Improvements

***Management***

-   Coherence between api import with definition and with swagger
    [\#4411](https://github.com/gravitee-io/issues/issues/4411)

-   Typo in \_depreciate subpath
    [\#4414](https://github.com/gravitee-io/issues/issues/4414)

# [APIM - 3.2.2 (2020-11-04)](https://github.com/gravitee-io/issues/milestone/291?closed=1)

## Bug fixes

***General***

-   Merge 3.0.10
    [\#4515](https://github.com/gravitee-io/issues/issues/4515)

-   Merge 3.0.11
    [\#4558](https://github.com/gravitee-io/issues/issues/4558)

-   Merge 3.0.9
    [\#4424](https://github.com/gravitee-io/issues/issues/4424)

***Management***

-   Missing description in operation response when import WSDL
    [\#4416](https://github.com/gravitee-io/issues/issues/4416)

# [APIM - 3.0.11 (2020-10-31)](https://github.com/gravitee-io/issues/milestone/301?closed=1)

## Bug fixes

***Jdbc-repository***

-   Liquibase checksum fail when migrating from 3.0.6 to 3.0.7
    [\#4526](https://github.com/gravitee-io/issues/issues/4526)

## Improvements

***Gateway***

-   Allowing constructors in expression language
    [\#4514](https://github.com/gravitee-io/issues/issues/4514)

# [APIM - 3.0.10 (2020-10-27)](https://github.com/gravitee-io/issues/milestone/294?closed=1)

## Bug fixes

***General***

-   Create dedicated resource to change user password
    [\#4480](https://github.com/gravitee-io/issues/issues/4480)

-   Ensure bad response are considered as errors
    [\#4513](https://github.com/gravitee-io/issues/issues/4513)

-   Merge 1.30.24
    [\#4491](https://github.com/gravitee-io/issues/issues/4491)

-   Missing mapping for orgId and envId in swagger definition generated
    for management Rest-API
    [\#4394](https://github.com/gravitee-io/issues/issues/4394)

***Management***

-   As standard user i see an administration link on portal UI
    [\#4399](https://github.com/gravitee-io/issues/issues/4399)

-   Change background color for theme logo
    [\#4444](https://github.com/gravitee-io/issues/issues/4444)

-   Error while searching through LDAP to transfer application
    [\#4441](https://github.com/gravitee-io/issues/issues/4441)

-   Improve the force login feature
    [\#4412](https://github.com/gravitee-io/issues/issues/4412)

-   Removing a user from a role, removes the user from all roles of the
    scope [\#4501](https://github.com/gravitee-io/issues/issues/4501)

-   Resetting password from Portal UI should not invalidate password
    [\#4410](https://github.com/gravitee-io/issues/issues/4410)

***Portal***

-   Anchor links not working correctly
    [\#2161](https://github.com/gravitee-io/issues/issues/2161)

-   Code preview display as block for inline code
    [\#4404](https://github.com/gravitee-io/issues/issues/4404)

-   Display of a large API name broken on a table list
    [\#4035](https://github.com/gravitee-io/issues/issues/4035)

-   Version too large in the dashboard’s subscriptions
    [\#4461](https://github.com/gravitee-io/issues/issues/4461)

***Repository***

-   \[http-bridge\] Gateway does not resync (gateway-bridge-http) after
    network issue
    [\#4505](https://github.com/gravitee-io/issues/issues/4505)

## Improvements

***Portal***

-   Allows to get the portal’s version
    [\#4459](https://github.com/gravitee-io/issues/issues/4459)

-   Hide empty categories
    [\#4477](https://github.com/gravitee-io/issues/issues/4477)

# [APIM - 3.3.0 (2020-10-15)](https://github.com/gravitee-io/issues/milestone/236?closed=1)

## Bug fixes

***General***

-   Merge 3.2.1
    [\#4385](https://github.com/gravitee-io/issues/issues/4385)

***Management***

-   Import of OpenAPI/Swagger containing path definition with
    parentheses and url parameters failed
    [\#4336](https://github.com/gravitee-io/issues/issues/4336)

***Policy***

-   \[json-validation\] Scope Enum modification
    [\#4420](https://github.com/gravitee-io/issues/issues/4420)

***Portal***

-   Fix typo in EN
    [\#4379](https://github.com/gravitee-io/issues/issues/4379)

## Features

***Management***

-   Support for custom Swagger tags to define API’s information
    [\#4295](https://github.com/gravitee-io/issues/issues/4295)

-   \[identity-provider\]Users and IdentityProviders can only be
    attached to an organization
    [\#3973](https://github.com/gravitee-io/issues/issues/3973)

***Policy***

-   AWS Lambda Function
    [\#4276](https://github.com/gravitee-io/issues/issues/4276)

-   \[json-validation\] Integration with swagger / OpenAPI
    [\#4293](https://github.com/gravitee-io/issues/issues/4293)

-   \[spike-arrest\] Protect backend against overload
    [\#4296](https://github.com/gravitee-io/issues/issues/4296)

-   \[xml-validation\] Integration with swagger / OpenAPI
    [\#4294](https://github.com/gravitee-io/issues/issues/4294)

# [APIM - 3.0.9 (2020-10-09)](https://github.com/gravitee-io/issues/milestone/287?closed=1)

## Bug fixes

***General***

-   Merge 1.30.22
    [\#4346](https://github.com/gravitee-io/issues/issues/4346)

-   Merge 1.30.23
    [\#4390](https://github.com/gravitee-io/issues/issues/4390)

***Management***

-   Blank page when selecting multiple times the setting menu
    [\#4392](https://github.com/gravitee-io/issues/issues/4392)

-   Error popup after a login with an OIDC provider
    [\#4290](https://github.com/gravitee-io/issues/issues/4290)

-   Import of an existing api fail since 3.2
    [\#4397](https://github.com/gravitee-io/issues/issues/4397)

***Migration***

-   Duplicate memberships after v3 migration
    [\#4382](https://github.com/gravitee-io/issues/issues/4382)

***Portal***

-   Align EN translations for rating
    [\#4388](https://github.com/gravitee-io/issues/issues/4388)

-   Cannot display payloads on a log
    [\#4048](https://github.com/gravitee-io/issues/issues/4048)

-   Fix typo in EN
    [\#4383](https://github.com/gravitee-io/issues/issues/4383)

-   In Prod mode, folders in documentation can not be expanded
    [\#4275](https://github.com/gravitee-io/issues/issues/4275)

-   Log’s title truncated
    [\#4054](https://github.com/gravitee-io/issues/issues/4054)

-   Redoc does not use gateway url but portal url
    [\#4389](https://github.com/gravitee-io/issues/issues/4389)

-   Remove the useless portal title from settings
    [\#4370](https://github.com/gravitee-io/issues/issues/4370)

***Repository***

-   \[jdbc\] Startup repository error when using MySQL 8.0.15
    plugin/driver
    [\#4255](https://github.com/gravitee-io/issues/issues/4255)

## Features

***Management***

-   Remove the Application picture
    [\#4316](https://github.com/gravitee-io/issues/issues/4316)

## Improvements

***Management***

-   Improve canReadAPI method
    [\#4401](https://github.com/gravitee-io/issues/issues/4401)

***Management-api***

-   Create Subscription not returning subscription keys
    [\#4171](https://github.com/gravitee-io/issues/issues/4171)

# [APIM - 3.2.1 (2020-10-01)](https://github.com/gravitee-io/issues/milestone/286?closed=1)

## Bug fixes

***Policy***

-   \[ipfiltering\] Socket leak with DNS resolution
    [\#4362](https://github.com/gravitee-io/issues/issues/4362)

-   \[quota\] Inconsistent body for Quota at V3.2
    [\#4345](https://github.com/gravitee-io/issues/issues/4345)

# [APIM - 3.2.0 (2020-09-22)](https://github.com/gravitee-io/issues/milestone/234?closed=1)

## Bug fixes

***General***

-   Merge 3.1.3
    [\#4261](https://github.com/gravitee-io/issues/issues/4261)

-   Merge 3.1.4
    [\#4299](https://github.com/gravitee-io/issues/issues/4299)

***Reporter***

-   \[elasticsearch\] invalid default value for ILM lifecycle property
    name [\#4303](https://github.com/gravitee-io/issues/issues/4303)

## Features

***Fetcher***

-   Add a cron task to fetch the documentation
    [\#3196](https://github.com/gravitee-io/issues/issues/3196)

***Management***

-   Associate assets to a page
    [\#4066](https://github.com/gravitee-io/issues/issues/4066)

-   Associate page to a category
    [\#4067](https://github.com/gravitee-io/issues/issues/4067)

-   Custom user fields
    [\#4070](https://github.com/gravitee-io/issues/issues/4070)

-   General Conditions of use (when subscribing to a plan)
    [\#4068](https://github.com/gravitee-io/issues/issues/4068)

-   Process to validate an account (registration)
    [\#4069](https://github.com/gravitee-io/issues/issues/4069)

***Management-api***

-   Create api from a WSDL
    [\#322](https://github.com/gravitee-io/issues/issues/322)

***Policy***

-   WS-Security based authentication
    [\#4247](https://github.com/gravitee-io/issues/issues/4247)

-   \[basic-auth\] Protect api w/ simple basic auth
    [\#689](https://github.com/gravitee-io/issues/issues/689)

-   \[rate-limit\] Increase configurability of the rate-limit policy
    [\#4128](https://github.com/gravitee-io/issues/issues/4128)

***Portal***

-   Add versioning on documentation pages
    [\#146](https://github.com/gravitee-io/issues/issues/146)

-   Allows to link pages in markdown
    [\#4072](https://github.com/gravitee-io/issues/issues/4072)

***Resource***

-   \[auth-provider\] Provide user attributes
    [\#4281](https://github.com/gravitee-io/issues/issues/4281)

## Improvements

***Management***

-   Enable / disable swagger’s rendering editor
    [\#4055](https://github.com/gravitee-io/issues/issues/4055)

-   Enable logging without condition
    [\#2778](https://github.com/gravitee-io/issues/issues/2778)

***Management-ui***

-   Provide more logs about CORS issue
    [\#4231](https://github.com/gravitee-io/issues/issues/4231)

-   Show API status icons on API portal page
    [\#4229](https://github.com/gravitee-io/issues/issues/4229)

# [APIM - 3.1.4 (2020-09-16)](https://github.com/gravitee-io/issues/milestone/281?closed=1)

## Bug fixes

***Gateway***

-   NPE on windows environment when using alerting
    [\#4240](https://github.com/gravitee-io/issues/issues/4240)

***General***

-   Merge 3.0.8
    [\#4286](https://github.com/gravitee-io/issues/issues/4286)

***Management-api***

-   Inconsistent behavior of Gravitee
    [\#4130](https://github.com/gravitee-io/issues/issues/4130)

***Portal***

-   Unable to logout when using AM IDP
    [\#4215](https://github.com/gravitee-io/issues/issues/4215)

***Repository***

-   \[jdbc\] Impossible to delete a group
    [\#4234](https://github.com/gravitee-io/issues/issues/4234)

# [APIM - 3.0.8 (2020-09-15)](https://github.com/gravitee-io/issues/milestone/280?closed=1)

## Bug fixes

***General***

-   Merge 1.30.20
    [\#4259](https://github.com/gravitee-io/issues/issues/4259)

-   Merge 1.30.21
    [\#4282](https://github.com/gravitee-io/issues/issues/4282)

***Management***

-   All user invitations are made for the idp "gravitee"
    [\#4226](https://github.com/gravitee-io/issues/issues/4226)

-   Cannot save an API with health check inheritance
    [\#4251](https://github.com/gravitee-io/issues/issues/4251)

-   When we import an api, documentation is brokeninternal link, image,
    order of appearance
    [\#4149](https://github.com/gravitee-io/issues/issues/4149)

***Repository***

-   \[jdbc\] Cannot update custom roles
    [\#4258](https://github.com/gravitee-io/issues/issues/4258)

-   \[mongodb\]index script contains an error on memberships
    [\#4233](https://github.com/gravitee-io/issues/issues/4233)

# [APIM - 3.1.3 (2020-09-02)](https://github.com/gravitee-io/issues/milestone/274?closed=1)

## Bug fixes

***Gateway***

-   Improve websocket continuation support
    [\#4220](https://github.com/gravitee-io/issues/issues/4220)

***General***

-   Merge 3.0.7
    [\#4194](https://github.com/gravitee-io/issues/issues/4194)

-   Requests seems stuck when enabling restrictions (Quota or Rate
    limiting) on a plan
    [\#4175](https://github.com/gravitee-io/issues/issues/4175)

***Management***

-   NPE on login if user has no first connection information
    [\#4196](https://github.com/gravitee-io/issues/issues/4196)

-   Not able to set default API / application role with JDBC repository
    [\#4214](https://github.com/gravitee-io/issues/issues/4214)

***Portal***

-   An error occurred during the subscription for an OAuth 2 Plan
    [\#4195](https://github.com/gravitee-io/issues/issues/4195)

-   Unable to logout when using AM IDP
    [\#4215](https://github.com/gravitee-io/issues/issues/4215)

# [APIM - 3.0.7 (2020-08-19)](https://github.com/gravitee-io/issues/milestone/270?closed=1)

## Bug fixes

***Gateway***

-   APIM gateway 3.0.4 → 3.0.6 causes WARN No plan has been selected and
    apis does not work
    [\#4169](https://github.com/gravitee-io/issues/issues/4169)

***General***

-   Merge 1.30.17
    [\#4157](https://github.com/gravitee-io/issues/issues/4157)

-   Merge 1.30.18
    [\#4163](https://github.com/gravitee-io/issues/issues/4163)

-   Merge 1.30.19
    [\#4181](https://github.com/gravitee-io/issues/issues/4181)

***Management***

-   Make markdown documentation visually similar to the one present in
    version 1.30
    [\#4147](https://github.com/gravitee-io/issues/issues/4147)

-   Members inherited from group doesn’t work on 3.1.1 and 3.0.6
    [\#4154](https://github.com/gravitee-io/issues/issues/4154)

***Portal***

-   Application’s metadata management
    [\#4089](https://github.com/gravitee-io/issues/issues/4089)

## Improvements

***Management***

-   Use URLs of the portal and management from settings
    [\#4144](https://github.com/gravitee-io/issues/issues/4144)

# [APIM - 3.1.2 (2020-08-04)](https://github.com/gravitee-io/issues/milestone/266?closed=1)

## Bug fixes

***Gateway***

-   Disable logging activity
    [\#4131](https://github.com/gravitee-io/issues/issues/4131)

***General***

-   Merge 3.0.6
    [\#4142](https://github.com/gravitee-io/issues/issues/4142)

***Management***

-   Allows to export from 3.1 to 3.0 also with grpc endpoints
    [\#4098](https://github.com/gravitee-io/issues/issues/4098)

***Policy***

-   \[rest-to-soap\] Can not save the form after updating prefill soap
    envelope in some case
    [\#4087](https://github.com/gravitee-io/issues/issues/4087)

## Improvements

***Management***

-   Allows a user to subscribe to the newsletter after first login
    [\#4096](https://github.com/gravitee-io/issues/issues/4096)

***Service-discovery***

-   Consul.io MTLS support
    [\#4116](https://github.com/gravitee-io/issues/issues/4116)

# [APIM - 3.0.6 (2020-07-30)](https://github.com/gravitee-io/issues/milestone/267?closed=1)

## Bug fixes

***General***

-   Merge 1.30.16
    [\#4132](https://github.com/gravitee-io/issues/issues/4132)

***Portal***

-   Confirmation message when deleting a member is not well displayed
    [\#4140](https://github.com/gravitee-io/issues/issues/4140)

-   Copy to sender not work in user contact form
    [\#4136](https://github.com/gravitee-io/issues/issues/4136)

# [APIM - 3.1.1 (2020-07-20)](https://github.com/gravitee-io/issues/milestone/265?closed=1)

## Bug fixes

***Gateway***

-   Bad merge with 1.30.14
    [\#4121](https://github.com/gravitee-io/issues/issues/4121)

***Management***

-   Node cannot start on an empty database in some context
    [\#4118](https://github.com/gravitee-io/issues/issues/4118)

# [APIM - 3.1.0 (2020-07-17)](https://github.com/gravitee-io/issues/milestone/217?closed=1)

## Bug fixes

***General***

-   Merge 3.0.4
    [\#4042](https://github.com/gravitee-io/issues/issues/4042)

## Features

***Gateway***

-   Support zone in order to group analytics
    [\#3858](https://github.com/gravitee-io/issues/issues/3858)

-   Use backup endpoints as secondary choice
    [\#3877](https://github.com/gravitee-io/issues/issues/3877)

***Policy***

-   Json Threat Protection policy
    [\#3950](https://github.com/gravitee-io/issues/issues/3950)

-   Regex Threat Protection Policy
    [\#3949](https://github.com/gravitee-io/issues/issues/3949)

-   Xml Threat Protection Policy
    [\#3951](https://github.com/gravitee-io/issues/issues/3951)

-   \[ip-filtering\] Add DNS resolution option for host filtering
    [\#3880](https://github.com/gravitee-io/issues/issues/3880)

## Improvements

***Gateway***

-   Accept backends/entrypoints supporting only HTTP/2
    [\#3105](https://github.com/gravitee-io/issues/issues/3105)

***Policy***

-   \[request-validation\] support for type "ENUM"
    [\#3556](https://github.com/gravitee-io/issues/issues/3556)

***Portal***

-   Allows to define a background on the APIs/Apps/Categories headers
    [\#3761](https://github.com/gravitee-io/issues/issues/3761)

# [APIM - 3.0.5 (2020-07-17)](https://github.com/gravitee-io/issues/milestone/263?closed=1)

## Bug fixes

***Gateway***

-   Websocket and stompgetting "Error during WebSocket handshakeSent
    non-empty *Sec-WebSocket-Protocol* header but no response was
    received"
    [\#4060](https://github.com/gravitee-io/issues/issues/4060)

***General***

-   Merge 1.30.15
    [\#4083](https://github.com/gravitee-io/issues/issues/4083)

***Management***

-   HtmlSanitizer can sometimes generate an error when creating or
    updating a markdown page
    [\#4077](https://github.com/gravitee-io/issues/issues/4077)

-   Incorrect audit when deleting a portal page
    [\#4099](https://github.com/gravitee-io/issues/issues/4099)

-   Sometimes social login is not working
    [\#4088](https://github.com/gravitee-io/issues/issues/4088)

***Portal***

-   Application image not well displayed if too large in last step of
    application creation
    [\#4063](https://github.com/gravitee-io/issues/issues/4063)

-   Wrong table headers in last step of application creation
    [\#4057](https://github.com/gravitee-io/issues/issues/4057)

# [APIM - 3.0.4 (2020-07-01)](https://github.com/gravitee-io/issues/milestone/259?closed=1)

## Bug fixes

***General***

-   Merge 1.30.13
    [\#4026](https://github.com/gravitee-io/issues/issues/4026)

-   Merge 1.30.14
    [\#4027](https://github.com/gravitee-io/issues/issues/4027)

***Management***

-   Cannot save API in some case with http headers
    [\#4001](https://github.com/gravitee-io/issues/issues/4001)

-   Configuration of logging don’t work
    [\#4021](https://github.com/gravitee-io/issues/issues/4021)

-   Exported APIs to 1.x version incorrect
    [\#3996](https://github.com/gravitee-io/issues/issues/3996)

-   Geo map is not displayed
    [\#4007](https://github.com/gravitee-io/issues/issues/4007)

***Management-ui***

-   Checkbox "override entrypoint" is very big in api virtualhost mode
    [\#3999](https://github.com/gravitee-io/issues/issues/3999)

***Platform***

-   EL sandbox is not well instantiated
    [\#4003](https://github.com/gravitee-io/issues/issues/4003)

***Portal***

-   Cannot list my subscriptions in some cases
    [\#3994](https://github.com/gravitee-io/issues/issues/3994)

-   Configure the baseUrl on default distribution config
    [\#4005](https://github.com/gravitee-io/issues/issues/4005)

-   Try it with oauth2 is not working when the UI is served with a base
    path [\#4038](https://github.com/gravitee-io/issues/issues/4038)

-   With different basePath sends redirect request for openid without
    the basePath
    [\#3993](https://github.com/gravitee-io/issues/issues/3993)

***Repository***

-   \[jdbc\] Increase the client id to allow 128 characters
    [\#4040](https://github.com/gravitee-io/issues/issues/4040)

## Improvements

***Portal***

-   Adapt configuration to be more consistant with the mgmt config
    [\#3968](https://github.com/gravitee-io/issues/issues/3968)

# [APIM - 3.0.3 (2020-06-18)](https://github.com/gravitee-io/issues/milestone/256?closed=1)

## Bug fixes

***General***

-   Merge 1.30.12
    [\#3971](https://github.com/gravitee-io/issues/issues/3971)

***Portal***

-   A simple user without permissions on API plan read get an exception
    on subscription
    [\#3953](https://github.com/gravitee-io/issues/issues/3953)

-   Better handling of logos with a large width
    [\#3892](https://github.com/gravitee-io/issues/issues/3892)

-   Pagination is broken when browsing APIs
    [\#3960](https://github.com/gravitee-io/issues/issues/3960)

-   The subscribe button should not disappear on scroll
    [\#3955](https://github.com/gravitee-io/issues/issues/3955)

-   Unable to get plans list for subscriptions
    [\#3914](https://github.com/gravitee-io/issues/issues/3914)

***Repository***

-   \[jdbc\] When opening portal as not logged in user, getting browser
    error [\#3913](https://github.com/gravitee-io/issues/issues/3913)

-   \[jdbc\] in apim 3 requires super user privilege to gravitee user in
    postgresql
    [\#3909](https://github.com/gravitee-io/issues/issues/3909)

-   \[jdbc\] upgraded users should be linked to an ORGANIZATION
    [\#3912](https://github.com/gravitee-io/issues/issues/3912)

## Features

***Management***

-   Support for redirection after authentication
    [\#3857](https://github.com/gravitee-io/issues/issues/3857)

# [APIM - 3.0.2 (2020-06-03)](https://github.com/gravitee-io/issues/milestone/232?closed=1)

## Bug fixes

***General***

-   APIM3.0.1 Portal-UI uri baseurl not configurable
    [\#3883](https://github.com/gravitee-io/issues/issues/3883)

-   Merge 1.30.11
    [\#3890](https://github.com/gravitee-io/issues/issues/3890)

-   Update in FROM clause Error in MySQL environment when use
    gravitee-repository-jdbc-3.0.0
    [\#3853](https://github.com/gravitee-io/issues/issues/3853)

***Management-api***

-   ID is sent on create View and this cause error
    [\#3882](https://github.com/gravitee-io/issues/issues/3882)

***Portal***

-   Access URL not well displayed when too long
    [\#3898](https://github.com/gravitee-io/issues/issues/3898)

-   Application default icon is not well generated in subscriptions
    lists [\#3847](https://github.com/gravitee-io/issues/issues/3847)

-   Console error when trying to rate an API
    [\#3902](https://github.com/gravitee-io/issues/issues/3902)

-   Error message on application creation & api subscription
    [\#3875](https://github.com/gravitee-io/issues/issues/3875)

-   On the dashboard, the version of API is not well displayed with a
    large API name
    [\#3832](https://github.com/gravitee-io/issues/issues/3832)

-   Should not be able to subscribe to a JWT API without a client id
    [\#3874](https://github.com/gravitee-io/issues/issues/3874)

-   Sometimes my subscriptions are not well displayed on hover
    [\#3804](https://github.com/gravitee-io/issues/issues/3804)

-   Tags and views are not displayed anymore on cards when not
    configured in API’s aside
    [\#3897](https://github.com/gravitee-io/issues/issues/3897)

-   The error message is not displayed until we click
    [\#3817](https://github.com/gravitee-io/issues/issues/3817)

## Improvements

***Management***

-   Better handling of read access on API’s items
    [\#3886](https://github.com/gravitee-io/issues/issues/3886)

-   Change the wording of the views to categories
    [\#3843](https://github.com/gravitee-io/issues/issues/3843)

***Portal***

-   Enable to click on a tag displayed on a card
    [\#3842](https://github.com/gravitee-io/issues/issues/3842)

# [APIM - 3.0.1 (2020-05-26)](https://github.com/gravitee-io/issues/milestone/203?closed=1)

## Bug fixes

***Management***

-   Default admin can’t go to the dashboard and settings menu
    [\#3834](https://github.com/gravitee-io/issues/issues/3834)

-   Unable to create a folder in TopFooter system folder
    [\#3825](https://github.com/gravitee-io/issues/issues/3825)

***Portal***

-   Api rating issues
    [\#3824](https://github.com/gravitee-io/issues/issues/3824)

-   Link in aside reloads all the application
    [\#3810](https://github.com/gravitee-io/issues/issues/3810)

-   Swagger OAuth integration
    [\#3813](https://github.com/gravitee-io/issues/issues/3813)

-   Take care of defined properties to display API’s aside
    [\#3812](https://github.com/gravitee-io/issues/issues/3812)

-   Unpublished pages are displayed on API’s documentation
    [\#3837](https://github.com/gravitee-io/issues/issues/3837)

-   Use the color defined on the identity providers display on the login
    [\#3811](https://github.com/gravitee-io/issues/issues/3811)

-   When creating view the picture is broken
    [\#3841](https://github.com/gravitee-io/issues/issues/3841)

-   When forceLogin is enabled, we cannot register anymore
    [\#3845](https://github.com/gravitee-io/issues/issues/3845)

# [APIM - 3.0.0 (2020-05-20)](https://github.com/gravitee-io/issues/milestone/187?closed=1)

## Bug fixes

***General***

-   Merge 1.30.x
    [\#3392](https://github.com/gravitee-io/issues/issues/3392)

***Management***

-   Empty mode is not well displayed on Gateway Instances screen
    [\#3739](https://github.com/gravitee-io/issues/issues/3739)

-   User/avatar should return 200 with no body when user doesn’t have
    avatar [\#3330](https://github.com/gravitee-io/issues/issues/3330)

***Portal***

-   Display labels on API cards
    [\#3116](https://github.com/gravitee-io/issues/issues/3116)

## Features

***Gateway***

-   Remove the legacy mode for url encoding
    [\#2634](https://github.com/gravitee-io/issues/issues/2634)

***Management***

-   I18n for documentation
    [\#3071](https://github.com/gravitee-io/issues/issues/3071)

-   \[multi-env\] Adapt memberships scopes and permissions to multi-env
    [\#3206](https://github.com/gravitee-io/issues/issues/3206)

***Multi-env***

-   Add organization feature
    [\#3182](https://github.com/gravitee-io/issues/issues/3182)

***Portal***

-   Add a link to admin in user menu
    [\#3109](https://github.com/gravitee-io/issues/issues/3109)

-   Add message for Cookies
    [\#2956](https://github.com/gravitee-io/issues/issues/2956)

-   Add the possibility to comment / rate an API
    [\#3061](https://github.com/gravitee-io/issues/issues/3061)

-   Allow a user to change his avatar
    [\#2806](https://github.com/gravitee-io/issues/issues/2806)

-   Allow a user to consult analytics of an application
    [\#2804](https://github.com/gravitee-io/issues/issues/2804)

-   Allow a user to consult logs of an application
    [\#2805](https://github.com/gravitee-io/issues/issues/2805)

-   Allow a user to consult subscriptions of an application
    [\#3114](https://github.com/gravitee-io/issues/issues/3114)

-   Allow a user to consult/edit global settings of an application
    [\#2799](https://github.com/gravitee-io/issues/issues/2799)

-   Allow a user to consult/edit members of an application
    [\#2803](https://github.com/gravitee-io/issues/issues/2803)

-   Allow a user to create an application
    [\#2798](https://github.com/gravitee-io/issues/issues/2798)

-   Allow a user to reset his password
    [\#2822](https://github.com/gravitee-io/issues/issues/2822)

-   Allow a user to subscribe to notifications on an application
    [\#3115](https://github.com/gravitee-io/issues/issues/3115)

-   Allow users to subscribe to newsletters
    [\#3420](https://github.com/gravitee-io/issues/issues/3420)

-   Allows to consult a subscription
    [\#3108](https://github.com/gravitee-io/issues/issues/3108)

-   Generate a custom default icon for user/apis/application
    [\#2853](https://github.com/gravitee-io/issues/issues/2853)

-   Integrate Google Analytics
    [\#3344](https://github.com/gravitee-io/issues/issues/3344)

## Improvements

***Platform***

-   Update v3 configuration
    [\#3668](https://github.com/gravitee-io/issues/issues/3668)

***Portal***

-   Add a 404 page
    [\#2991](https://github.com/gravitee-io/issues/issues/2991)

-   Generate dist on the root
    [\#3737](https://github.com/gravitee-io/issues/issues/3737)

-   Keep API display preference to the user
    [\#3110](https://github.com/gravitee-io/issues/issues/3110)

-   Work on route transition animations
    [\#3010](https://github.com/gravitee-io/issues/issues/3010)

-   Work on scroll to top strategy router navigation
    [\#3012](https://github.com/gravitee-io/issues/issues/3012)
