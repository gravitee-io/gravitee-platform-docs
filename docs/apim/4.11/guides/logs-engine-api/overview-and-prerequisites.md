### Overview

The Logs Engine API provides environment-level visibility into v4 HTTP proxy API connection logs. Platform administrators and SREs can search, filter, and inspect runtime logs across all v4 APIs in an environment from a single interface, enabling faster incident investigation without navigating between per-API screens.

### Connection Logs

Connection logs capture runtime request/response data for v4 HTTP proxy APIs. Each log entry represents a single API call and includes the following metadata:

* Timestamp
* API identifier
* Application
* Plan
* HTTP method
* URI
* Status code
* Response time
* Gateway identifier
* Optional error diagnostics (error key, component name, component type, warnings)

Logs are stored in Elasticsearch or OpenSearch and queried via the Management API.

### User Context and Authorization

The API enforces permission-based filtering: users only see logs for APIs they have access to. The `UserContextLoader` resolves authorized API IDs for the current user before executing log queries. Application, plan, and gateway names are resolved from their respective repositories and merged into the response payload.

### Prerequisites

Before using the Logs Engine API, ensure the following requirements are met:

* Gravitee APIM 4.11 or later
* Elasticsearch or OpenSearch reporter configured
* User must have `RolePermission.API_ANALYTICS` with `RolePermissionAction.READ` for the environment
* v4 HTTP proxy APIs must be deployed and generating connection logs

#### Restrictions

The following restrictions apply:

* Only v4 HTTP proxy API logs are included in the Logs Engine API
* v2 HTTP proxy logs remain in the legacy environment logs view
* Kafka Native APIs do not produce connection logs and are not supported
* Message-level logs are not included
* Health-check logs are excluded
* Webhook logs are accessed via the dedicated webhook logs view

### Gateway Configuration

<!-- EMPTY: Gateway Configuration -->
