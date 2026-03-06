# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6322 -->
#### **Agent Application Type for AI and Autonomous Systems**

* Introduces a new `AGENT` application type designed for secure integration of AI assistants and autonomous agents with OAuth 2.0 flows.
* Automatically enforces restricted grant types by blocking `implicit`, `password`, and `refresh_token` grants to prevent insecure authentication patterns.
* Supports optional AgentCard metadata via URL, enabling A2A (Agent-to-Agent) specification compliance with automatic validation and SSRF protection.
* Defaults to `authorization_code` grant and `client_secret_basic` authentication when creating agent applications.
* Requires AM 4.11.0 or later and appropriate `APPLICATION[CREATE]` or `APPLICATION[UPDATE]` permissions.
<!-- /PIPELINE:AM-6322 -->

## Improvements

## Bug Fixes
