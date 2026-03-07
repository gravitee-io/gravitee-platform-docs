# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6322 -->
#### **Agent Application Type for AI and Autonomous Systems**

* Introduces a dedicated `AGENT` application type for secure integration of AI assistants and autonomous agents with OAuth 2.0 flows.
* Automatically enforces secure authentication by restricting forbidden grant types (`implicit`, `password`, `refresh_token`) and defaulting to `authorization_code` or `client_credentials`.
* Supports optional AgentCard metadata discovery via URL configuration, enabling agents to expose capabilities, tools, and resources per the A2A specification.
* AgentCard fetching includes SSRF protection (blocks localhost/private IPs), 512 KB size limit, and 5-second timeout.
* Available via standard application creation endpoints and Dynamic Client Registration (DCR) by setting `application_type` to `agent`.
<!-- /PIPELINE:AM-6322 -->

## Improvements

## Bug Fixes
