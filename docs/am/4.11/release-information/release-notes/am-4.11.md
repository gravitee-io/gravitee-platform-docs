# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6322 -->
#### **Agent Application Type for AI and Autonomous Systems**

* Introduces a new Agent application type for secure integration of AI assistants and autonomous agents with OAuth 2.0 flows.
* Enforces stricter security defaults by restricting grant types to `authorization_code` only and prohibiting `implicit`, `password`, and `refresh_token` grants.
* Supports AgentCard metadata discovery via the A2A specification, allowing agents to expose machine-readable capabilities through a proxied endpoint with SSRF protection and JSON validation.
* Automatically sanitizes OAuth configurations during application creation and Dynamic Client Registration (DCR) to remove forbidden grant types.
* Requires AM 4.11.0 or later and `APPLICATION[CREATE]` permission to create agent applications.
<!-- /PIPELINE:AM-6322 -->

## Improvements

## Bug Fixes
