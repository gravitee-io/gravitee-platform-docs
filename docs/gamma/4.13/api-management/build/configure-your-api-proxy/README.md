---
hidden: false
noIndex: false
---

# Configure your API proxy
<!-- GAP-STRUCTURAL: Missing procedural content source -->

After creating and securing an API proxy, you can refine its behavior through additional configuration. This section covers endpoint configuration, consumer access management, and policy enforcement.

## Configuration areas

| Area                  | What you configure                                                                      | Page                                                                            |
| --------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Endpoints**         | Upstream endpoints, load balancing, SSL/TLS, proxy settings, and HTTP connection tuning | [Configure endpoints](configure-backend-security.md)      |
| **Consumer access**   | Applications, subscriptions, and API key management for consumers                       | [Establish consumer access](establish-consumer-access.md) |
| **Security policies** | Fine-grained authorization and request/response policies enforced at the Gateway        | [Apply security policies](apply-security-policies.md)     |

## Accessing API configuration

1. From the Gamma console sidebar, select **API Management**.
2. Navigate to the **API Proxies** list.
3. Select the API proxy you want to configure.
4. Use the API detail sidebar to navigate between configuration areas.

## API detail sidebar navigation

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-b2a381ecbe2cdeba026688f3c0f0db0a5442c77d%2Fgamma-api-general.png?alt=media" alt="API proxy general settings showing the detail sidebar navigation"><figcaption><p>The API detail sidebar groups configuration into seven sections: General, Gateway, Design, Consumer Access, Security, Observability, and Operations.</p></figcaption></figure>

The API detail page organizes configuration into groups in the sidebar:

### General

| Tab                    | Description                                                                          | Status      |
| ---------------------- | ------------------------------------------------------------------------------------ | ----------- |
| **Overview**           | Onboarding checklist and API snapshot (endpoints configured, plans, team members).   | Implemented |
| **General**            | API name, version, description, labels, and categories.                              | Implemented |
| **API Properties**     | Key-value properties and dynamic properties.                                         | Implemented |
| **Resources**          | Shared components (OAuth2 resources, cache stores) referenced by plans and policies. | Coming soon |
| **Notifications**      | Notification settings for API events.                                                | Implemented |
| **API Score**          | Quality and completeness scoring for the API.                                        | Coming soon |
| **Response Templates** | Custom error response templates.                                                     | Coming soon |
| **CORS**               | Cross-origin resource sharing configuration.                                         | Implemented |

### Gateway

| Tab                          | Description                                                                                        | Status      |
| ---------------------------- | -------------------------------------------------------------------------------------------------- | ----------- |
| **Entrypoints**              | Context paths and exposed entrypoints (virtual hosts).                                             | Implemented |
| **Endpoints**                | Endpoint groups, individual endpoints, load balancing, and connection settings. Contains sub-tabs: | Implemented |
| ↳ **Endpoints** (list)       | Manage endpoint groups and individual endpoints.                                                   | Implemented |
| ↳ **Failover**               | Failover behavior when upstream endpoints are unreachable.                                         | Implemented |
| ↳ **Health Check Dashboard** | Endpoint health monitoring.                                                                        | Coming soon |
| **Reporter Settings**        | Logging, tracing, and analytics export configuration.                                              | Implemented |

### Design

| Tab               | Description                                                       | Status      |
| ----------------- | ----------------------------------------------------------------- | ----------- |
| **Policy Studio** | Visual policy flow editor for request/response processing chains. | Placeholder |

### Consumer Access

| Tab            | Description                                                                     | Status      |
| -------------- | ------------------------------------------------------------------------------- | ----------- |
| **Plans**      | Security plans (API Key, JWT, OAuth2, mTLS, Keyless) with lifecycle management. | Implemented |
| **Consumers**  | Subscription management, approval workflows, and API key management.            | Implemented |
| **Broadcasts** | Consumer notifications and announcements.                                       | Implemented |

### Security

| Tab                  | Description                                                      | Status      |
| -------------------- | ---------------------------------------------------------------- | ----------- |
| **Authorization**    | Fine-grained authorization policies enforced by the gateway PDP. | Coming soon |
| **User Permissions** | Member management and role-based access for the API.             | Implemented |

### Observability

| Tab            | Description                                             | Status      |
| -------------- | ------------------------------------------------------- | ----------- |
| **Alerts**     | Alert triggers for error thresholds and latency spikes. | Implemented |
| **Audit Logs** | Change history and audit trail.                         | Implemented |

### Operations

| Tab                 | Description                                 | Status      |
| ------------------- | ------------------------------------------- | ----------- |
| **Deployment**      | Deployment management. Contains sub-tabs:   | Implemented |
| ↳ **Configuration** | Deployment configuration and sharding tags. | Implemented |
| ↳ **History**       | Deployment version history and rollback.    | Implemented |

{% hint style="info" %}
Tabs marked **Coming soon** are visible in the sidebar with a flask icon and a "Coming soon" tooltip, but are not navigable. Tabs marked **Placeholder** render a stub page with the feature title only. Both will become functional in a future release.

A **Documentation** route also exists (`AppRoutes.tsx:L121`) and renders a placeholder page, but it has no sidebar nav entry and is only reachable via direct URL.
{% endhint %}
