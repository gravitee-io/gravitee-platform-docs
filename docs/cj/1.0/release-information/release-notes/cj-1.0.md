# CJ 1.0

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:CJ-4078 -->
#### **Alert Engine Cluster Mode with High Availability**

* Alert Engine now supports cluster deployment with automatic primary node election, enabling horizontal scaling and high availability for alert processing.
* Multiple Alert Engine nodes coordinate via Hazelcast, with one primary node processing events while others remain on standby. If the primary fails, another node is automatically elected.
* Window-based triggers use schedule anchoring to maintain consistent evaluation cycles across restarts, preventing schedule drift by calculating intervals relative to the trigger's creation or update timestamp.
* Requires a Gravitee license key and Hazelcast configuration file for production deployments. Configure cluster synchronization intervals and node count via Docker Compose environment variables or Helm chart parameters.
<!-- /PIPELINE:CJ-4078 -->

## Improvements

## Bug Fixes
