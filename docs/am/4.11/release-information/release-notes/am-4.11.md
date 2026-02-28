# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6339 -->
#### **Certificate Fallback for JWT Signing**

* Provides automatic fallback to a domain-level certificate when a client's primary certificate fails during JWT signing operations, reducing authentication service disruptions.
* Configured via the Management API at the domain level and applies to all clients within that domain without requiring a domain restart.
* Uses an event-driven architecture to hot-reload certificate settings changes in real time.
* Logs warnings when fallback certificates are used, enabling administrators to monitor and address certificate issues proactively.
<!-- /PIPELINE:AM-6339 -->

## Improvements

## Bug Fixes
