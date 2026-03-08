# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6322 -->
#### **Agent Application Type for Agentic OAuth Clients**

* Introduces a dedicated Agent application type for AI assistants and autonomous agents, enforcing stricter OAuth grant type constraints than traditional clients.
* Restricts agent applications to `authorization_code` and `client_credentials` grant types only, blocking implicit, password, and refresh token flows to align with agentic security requirements.
* Supports optional AgentCard metadata import via the A2A specification, allowing administrators to fetch and display agent capabilities, tools, and prompts from a publicly accessible URL.
* Agent applications appear in a dedicated "Agents" section in the UI and are tracked separately in audit logs for improved governance.
* AgentCard fetching enforces SSRF protection, 512 KB size limits, and 5-second timeouts to prevent security risks and resource exhaustion.
<!-- /PIPELINE:AM-6322 -->

## Improvements

## Bug Fixes
