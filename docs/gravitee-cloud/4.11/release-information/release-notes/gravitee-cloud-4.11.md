# GRAVITEE-CLOUD 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:CJ-4078 -->
#### **Alert Engine Cluster Mode with Schedule Anchoring**

* Alert Engine now supports cluster deployment with Hazelcast-based synchronization, enabling high availability and multi-tenant alert processing across multiple nodes.
* Window-based alerts use schedule anchoring to maintain independent evaluation timelines based on each trigger's creation or update timestamp, eliminating shared global schedules and time drift.
* Cluster nodes synchronize trigger state every 30 seconds by default, with one PRIMARY node and zero or more REPLICA nodes automatically coordinating alert evaluation.
* Production deployments require a Gravitee license key and Hazelcast TCP-IP configuration with explicit member addresses for reliable cluster discovery.
* Alert Engine WebSocket connector (v2.3.0+) automatically applies installation ID filters to triggers when enabled, ensuring alerts only evaluate events from their originating Gravitee installation in multi-tenant environments.
<!-- /PIPELINE:CJ-4078 -->

## Improvements

## Bug Fixes
