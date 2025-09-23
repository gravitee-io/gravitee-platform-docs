# Changelog

## Introduction

The changelog provides in-depth overviews of what's new in Gravitee major, minor, and patch releases.

## Alert Engine changelog


### 2.3.2 (2025-09-16)

_**General**_

* enable skip Xms and Xmx with `GIO_DISABLE_STARTING_MEMORY`


### 2.3.1 (2025-06-23)

_**General**_

* fix: update gravitee-notifier-email to v2.0.0 to fix email alerts


### 2.3.0 (2025-05-12)

_**General**_

* resolve security vulnerabilities in dependencies (org.json, Logback, Netty)
* upgrade project to Java 21


### 2.2.1 (2025-04-14)

_**General**_

* fix: remove deprecated hazelcast-kubernetes dependency
* fix: upgrade hazelcast configuration

### 2.2.0 (2025-02-24)

_**General**_

* docker image: run the engine with gravitee user rather than root
* docker image: build image for linux/arm64 and linux/amd64
* update dependencies version
* rework CI to avoid usage of external but dedicated AE orb and add some cleanup + build perf-test docker images

### 2.1.6 (2024-06-24)

_**General**_

* fix: resolve relaxing count reset on dampening
* fix: do not reach the channel address on notification when resolving properties for APIM and AM

### 2.1.5 (2023-08-18)

_**General**_

* fix: webhook notifier 1.1.2

### 2.1.4 (2023-07-06)

_**General**_

* update gravitee-notifier-webhook dependency to keep query param in webhook URL

### 2.1.3 (2023-06-09)

_**General**_

* update org-json dependency to fix security issue
  * Note: hazelcast is still in 5.2.1, but its internal dependency is upgraded.

### 2.1.2 (2023-06-02)

_**General**_

* fix: correct dependency to run on kubernetes

### 2.1.1 (2023-04-26)

_**General**_

* fix: fixed dependencies to avoid error on startup

### 2.1.0 (2023-04-26)

_**General**_

* fix issue about missing reset in case of window condition
* fix license INFO logging level enforced
* upgrade dependencies also to fix vulnerabilities

### 2.0.0 (2022-12-29)

#### Improvement

_**General**_

* Refactor core engine to replace Drools over RXjava3. Consequently, we have better performance.
  * Now, the hazelcast backup and synchronization of dampening and bucket are asynchronous. A schedule time is configurable in `gravitee.yml` by default to 30sec.
* A new HTTP endpoint is available to register triggers along with its [OpenAPI specification](https://raw.githubusercontent.com/gravitee-io/gravitee-docs/master/ae/spec/2.0/alert-engine-spec.yml).
* Update some dependencies.

_**Migration**_

* This version is backward compatible feature wise compared to the latest 1.6.x version.
* **Rolling updates are not supported by this version during the migration**
* If you deploy via helm, the latest update configures [the hazelcast synchronization](https://github.com/gravitee-io/helm-charts/pull/315/files#diff-08ec83b3c29e4230bed0273b28b4112cc76c9e5571f0a667f29e69fb079743db) as expected by the 2.0.0 engine.

### 1.6.7 (2022-11-24)

#### Improvement

_**General**_

* chore: upgrade email notifier for authentication methods

### 1.6.6 (2022-10-26)

#### Bug fixes

_**Upgrade**_

* update dependencies

### 1.6.5 (2022-08-02)

#### Bug fixes

_**General**_

* fix: handle notification.message on simple buckets

### 1.6.4 (2022-06-27)

#### Bug fixes

_**General**_

* fix(engine): Use a temporary structure for not modifying the iterator (gravitee-io/gravitee-alert-engine#366)

### 1.6.3 (2022-06-21)

#### Bug fixes

_**Build**_

* update CI config to use keeper as secret provider

### 1.6.2 (2022-06-20)

#### Bug fixes

_**General**_

* backport update from 1.5.x

### 1.6.1 (2022-02-02)

#### Bug fixes

_**Upgrade**_

* update gravitee-bom.version to upgrade dependencies

### 1.6.0 (2022-01-27)

#### Improvement

_**General**_

* feat: allow aggregation on any kind of condition

#### Bug fixes

_**Upgrade**_

* chore: Support for Java 17
* upgrade dependencies

### 1.5.7 (2021-12-17)

#### Bug fixes

_**General**_

* upgrade gravitee-node.version to add required rx Vertx bean

### 1.5.6 (2022-02-17)

#### Bug fixes

_**General**_

* fix: concurrent modification exception during trigger reload

### 1.5.5 (2022-02-02)

#### Bug fixes

_**Upgrade**_

* upgrade gravitee-notifier-email.version to 1.3.2 to split the recipients once the parameter has been processed by Freemarker (gravitee-io/issues#6992)

### 1.5.4 (2021-12-17)

#### Bug fixes

_**Security**_

* security update org.apache.logging.log4j:log4j-to-slf4j to 2.16.0

### 1.5.3 (2021-12-10)

#### Bug fixes

_**Security**_

* security update org.apache.logging.log4j:log4j-to-slf4j to 2.15.0

### 1.5.2 (2021-12-02)

#### Bug fixes

_**Upgrade**_

* upgrade gravitee-node.version to 1.18.0

### 1.5.1 (2021-11-30)

#### Bug fixes

_**Connector**_

* fix: make sure connector reconnects after losing AE connection

### 1.5.0 (2021-11-18)

#### Improvements

_**General**_

* Multi-tenancy support
* feat(multi-env): add multi env, org and install support
* feat(events): allow to send event over http instead of websocket

#### Bug fixes

_**Upgrade**_

* update dependencies
* feat(docker): update from image to eclipse-temurin:11-jre-focal

### 1.4.2 (2022-02-02)

#### Bug fixes

_**Upgrade**_

* update [notifier-email to 1.3.2](https://github.com/gravitee-io/gravitee-notifier-email/releases?q=1%5C.3\&expanded=true)
* chore(docker): Update base imager to Temurin

### 1.4.1 (2022-01-31)

#### Bug fixes

_**General**_

* AE 1.4 installation java.lang.ClassNotFoundExceptionorg.LatencyUtils.PauseDetector

### 1.4.0 (2022-01-31)

#### Bug fixes

_**General**_

* Merge 1.3.2

### 1.3.5 (2022-01-31)

#### Bug fixes

_**General**_

* Possible OOM with hazelcast Queue

### 1.3.4 (2022-01-31)

#### Bug fixes

_**General**_

* Properties not available for freemarker template

### 1.3.3 (2021-07-08)

#### Bug fixes

_**Processor**_

* NPE when processing null notification event

#### Features

_**General**_

* Allow to use filters from the notification

### 1.3.2 (2022-01-31)

#### Bug fixes

_**Ws-connector**_

* Enable configuration is ignored

### 1.3.1 (2022-01-31)

#### Improvements

_**General**_

* Allow to use conditions in notifications messages

### 1.3.0 (2021-03-03)

#### Bug fixes

_**General**_

* Better support of Kubernetes

### 1.2.18 (2021-01-25)

#### Bug fixes

_**General**_

* Switch from reliable-topic to a simple topic

### 1.2.17 (2020-11-19)

#### Bug fixes

_**General**_

* Provide more logs when running rules engine + remove elements from queue

### 1.2.16 (2020-11-19)

#### Bug fixes

_**General**_

* Only master node is processing events

### 1.2.15 (2020-11-17)

#### Improvements

_**General**_

* Optimize serialization / deserialization

### 1.2.14 (2020-11-17)

#### Bug fixes

_**General**_

* Notifications are not sent sometimes

#### Improvements

_**General**_

* Hazelcastconfigure properties from hazelcast.xml
* Rules must be run only by the master node

### 1.2.13 (2020-10-23)

#### Bug fixes

_**Notification**_

* Do not propagate notification to cluster’s members.

_**Websocket**_

* Ensure websocket connection concurrency

#### Improvements

_**Technical-api**_

* Add endpoints to list current channels

### 1.2.12 (2020-10-23)

#### Bug fixes

_**Notification**_

* Do not send alert history command if not master node

### 1.2.11 (2020-10-23)

#### Bug fixes

_**Websocket**_

* Run registration / unregistration steps outside event-loop

### 1.2.10 (2020-10-21)

#### Bug fixes

_**General**_

* Com.hazelcast.nio.serialization.HazelcastSerializationExceptionjava.lang.ClassNotFoundExceptioncom.graviteesource.ae.engine.dampening.DampeningState

### 1.2.9 (2020-10-21)

#### Improvements

_**Cluster**_

* Asynchronous cluster operations

_**Engine**_

* Provide more logs

### 1.2.8 (2020-10-12)

#### Bug fixes

_**Engine**_

* An unexpected error while firing triggersConcurrentModificationException
* Do not process shared trigger if rules engine not started

### 1.2.6 (2020-10-07)

#### Bug fixes

_**Websocket**_

* Unexpected end-of-input was expecting closing quote for a string value for long trigger definitions

### 1.2.5 (2020-09-25)

#### Bug fixes

_**General**_

* Add configuration schema on the notifier email
* Downgrade parent version from 19 to 17.1 to get the correct version of Vertx

### 1.2.4 (2020-09-23)

#### Bug fixes

_**Notification**_

* An error occurs while preparing notification parameters

#### Improvements

_**Websocket**_

* Log the path when invalid WS request

### 1.2.3 (2020-09-11)

#### Bug fixes

_**General**_

* Thread blocked when running AE with very few core-CPU

### 1.2.2 (2020-08-27)

#### Bug fixes

_**Notification**_

* Thread blocked

#### Improvements

_**Notification**_

* Provide bucket results to template

### 1.2.1 (2020-08-24)

#### Bug fixes

_**Boot**_

* License not well loaded

_**Launcher**_

* AE is not working on Windows

#### Improvements

_**Bucket**_

* Track last event for notification purpose

### 1.2.0 (2020-06-26)

#### Bug fixes

_**General**_

* Display both compared properties on the notification message
* Reinit dampening on trigger refresh

_**Notifier**_

* \[slack] No information when the notification failed

#### Features

_**General**_

* Templatehuman-readable information
* Websocket connectorAdd support for Mutual TLS

#### Improvements

_**General**_

* Initialize user-agent processor during startup
* Manage channels to send commands to pluggable systems

### 1.0.1 (2020-01-23)

#### Bug fixes

_**General**_

* Bucket are not distributed correctly and its values are reinitialized
* Trigger does not always reload when condition’s property is changed

### 1.0.0 (2020-01-09)

#### Bug fixes

_**General**_

* Concurrent modification exception
* No more notification are sent
* Websocket support must be enabled by default

#### Features

_**General**_

* Define a master node for a cluster of engines
* Ensure that AE plugin can only be run on an enterprise node
* License module integration
* Secure communication between an event / trigger provider and the engine
* Support of websocket

#### Improvements

_**General**_

* Allows to use event on freemarker templates
* Support for multiple alert-engine
