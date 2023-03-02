---
title: APIM 3.19.x changelog
tags:
  - APIM 3.19.x changelog
  - Changelog
  - Release notes
  - Upgrades
---

# APIM 3.19.x changelog

## APIM 3.19.x changelog

This page contains the changelog entries for APIM 3.19.0 and all subsequent minor APIM 3.19.x releases.

## About upgrades

For upgrade instructions, please refer to the [APIM Migration Guide](../../changelog/installation-guide/installation-guide-migration.md).

!!! warning

```
**Important:** If you plan to skip versions when you upgrade, ensure that you read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.
```

## APIM - 3.19.6 (2023-01-05)

### API

* Add a default value in liquibase script when adding a non-nullable constraint on `commands` table

## APIM - 3.19.5 (2023-01-04)

### Gateway

* API key plan was not useable after migration to 3.18 [#8762](https://github.com/gravitee-io/issues/issues/8762)
* Non-explicit "invalid version format: 0" log message fixed [#8754](https://github.com/gravitee-io/issues/issues/8754)

### API

* Handle flow steps order in database [#8805](https://github.com/gravitee-io/issues/issues/8805)
* Handle query with page number higher than max page with data [#8773](https://github.com/gravitee-io/issues/issues/8773)
* PostgreSQL: management API failed to start after 3.18 migration [#8774](https://github.com/gravitee-io/issues/issues/8774)
* Import API erased plan general conditions [#8767](https://github.com/gravitee-io/issues/issues/8767)
* API key revocation raised an error in non-default environment

### Portal

* Category name was not properly displayed on API page [#8628](https://github.com/gravitee-io/issues/issues/8628)

## [APIM - 3.19.4 (2022-12-02)](https://github.com/gravitee-io/issues/milestone/620?closed=1)

### Bug fixes

_**General**_

* Avoid to evict subscription when we close it and accept a new one [#8637](https://github.com/gravitee-io/issues/issues/8637)
* Merge 3.18.13 into 3.19.x [#8682](https://github.com/gravitee-io/issues/issues/8682)

## [APIM - 3.19.1 (2022-10-21)](https://github.com/gravitee-io/issues/milestone/607?closed=1)

### Bug fixes

_**Management**_

* Paths based APIs failed to match subscription [#8570](https://github.com/gravitee-io/issues/issues/8570)

## [APIM - 3.19.0 (2022-10-04)](https://github.com/gravitee-io/issues/milestone/553?closed=1)

### Bug fixes

_**General**_

* Merge `3.18.x` into `3.19.0` [#8500](https://github.com/gravitee-io/issues/issues/8500)

_**Management**_

* Response template config asks for Content-Type but Accept header param is taken into account instead [#8263](https://github.com/gravitee-io/issues/issues/8263)
* Subscription start date is ignored [#7311](https://github.com/gravitee-io/issues/issues/7311)

### Features

[Beta - Gravitee Kubernetes Operator](../../getting-started/configuration/kubernetes/apim-kubernetes-operator-overview.md)

* Make the gateway listen to ConfigMap [#8189](https://github.com/gravitee-io/issues/issues/8189)
* Define ManagementContext to target specific environment [#7982](https://github.com/gravitee-io/issues/issues/7982)
* Create API using CRD on Management API [#7980](https://github.com/gravitee-io/issues/issues/7980)
* Start/stop an API on gateway using CRD [#8136](https://github.com/gravitee-io/issues/issues/8136)
* Update an API using CRD [#7981](https://github.com/gravitee-io/issues/issues/7981)

[Beta - New gateway execution engine](../../guides/create-apis/v4-beta/v4-beta-new-policy-execution-engine-introduction.md)

* Issue with response template and invoker timeout [#8075](https://github.com/gravitee-io/issues/issues/8075)
* Reactive Timeout [#7988](https://github.com/gravitee-io/issues/issues/7988)
* Security plan execution [#7991](https://github.com/gravitee-io/issues/issues/7991)
* Support Failover [#8086](https://github.com/gravitee-io/issues/issues/8086)

[Alpha - Introducing Event-Native API Management](../../guides/create-apis/v4-beta/v4-beta-event-native-apim-introduction.md)

* Introduce v4 api defitinion to support sync & async APIs [#8068](https://github.com/gravitee-io/issues/issues/8068)
* Deploy v4 api definition [#8009](https://github.com/gravitee-io/issues/issues/8009)
* Subscribe to V4 APIs [#8287](https://github.com/gravitee-io/issues/issues/8287)
* Http-post entrypoint [#8036](https://github.com/gravitee-io/issues/issues/8036)
* \[Kafka endpoint] Publish to topic [#8247](https://github.com/gravitee-io/issues/issues/8247)
* \[Kafka endpoint] Subscribe to topic [#8245](https://github.com/gravitee-io/issues/issues/8245)
