# GRAVITEE-CLOUD 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:CJ-4078 -->
#### **Alert Engine Cluster Mode and Scheduled Alert Improvements**

* Alert Engine now supports cluster mode with automatic primary/replica role election using Hazelcast, enabling high availability for event processing across distributed deployments.
* Window-based alerts anchor their evaluation schedules to the trigger's creation or update timestamp, ensuring consistent evaluation cycles that align with configuration changes rather than restarting from the current time.
* Cluster synchronization is configurable via `cluster.sync.time` properties and requires a Hazelcast configuration file at `${gravitee.home}/config/hazelcast.xml`.
* WebSocket connector default filters (e.g., installation ID constraints) can be disabled via `alerts.alert-engine.ws.defaultFilters.enabled` to support cross-installation alert routing.
* Cluster mode requires a valid Gravitee license key file and Alert Engine version 3.0.0 or later for timestamp-based scheduling support.
<!-- /PIPELINE:CJ-4078 -->

## Improvements

## Bug Fixes
