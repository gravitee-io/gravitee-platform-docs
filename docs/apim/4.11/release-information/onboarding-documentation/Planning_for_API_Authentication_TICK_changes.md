# Planning for API Authentication

This page outlines the strategy for selecting authentication mechanisms within Gravitee to secure API resources. Learn how to evaluate authentication models—from simple API keys to complex OpenID Connect (OIDC) integrations—and establish security layers, such as threat protection and credential management, for a robust identity posture.

## Deliverables

* **Authentication Strategy Document:** A mapping of API use cases to specific Gravitee consumer plans.
* **Security Configuration Schema:** Validated settings for JWKS URLs, issuer constraints, and audience claims.
* **Integrated Identity Architecture:** A technical plan for connecting Gravitee to your enterprise identity providers (IdPs).
* **Threat Protection Policy Suite:** A set of automated rules for JSON, XML, and regex threat protection.

## Stakeholders

Involve the following stakeholders in authentication planning:

* **Security Architects:** To define identity standards and compliance requirements.
* **API Platform Engineers:** To configure Gravitee plans and gateway policies.
* **Identity Team:** To provide OIDC and OAuth 2.0 metadata and manage the enterprise IdP.
* **Backend Service Owners:** To coordinate principal propagation and downstream authorization.

## Prerequisites

* **License:** Gravitee Enterprise Edition is required for advanced policies like OIDC and specialized secret providers.
* **People:** Knowledge of OAuth 2.0 and OIDC protocols and experience with TLS and mTLS certificate management.
* **Knowledge:** Understanding of your network topology, specifically the connectivity between the gateway and internal IdPs.

## Anticipated Duration

* **Two weeks:** Minimum one week for initial design, with an additional week for IdP integration and testing.

## Potential Risks and Challenges

* **Latency Overhead:** High-frequency token introspection in OAuth 2.0 plans can impact performance. Local JWT validation is preferred for high-traffic environments.
* **Token Revocation:** Managing stateless JWT invalidation requires an external fast-access store, such as Redis, to handle denylists.
* **Clock Skew:** Differences in system time between the IdP and the gateway can cause valid tokens to be rejected.

## Actions and Activities

### Define the Authentication Model
Select the appropriate method based on the client type:

* **API Key:** For legacy server-to-server traffic.
* **JWT:** For performant stateless validation.
* **OAuth 2.0:** For delegated access requiring introspection.

### Configure the IdP Connection
Gather the OIDC metadata or JWKS URL from your enterprise identity platform. Ensure the gateway has network line-of-sight to these endpoints.

### Create a Gravitee Plan
1. In the Management Console, create a new **Plan**.
2. Select the authentication type, such as a **JWT plan** or an **OAuth 2.0 plan**.
3. Input security constraints, such as expected issuers and allowed signing algorithms like RS256.

### Map Scopes to Policies
Define scope mappings within the plan to link specific identity claims, such as `orders.read`, to gateway-level permissions.

### Layer Threat Protection
Add **JSON/XML Threat Protection** and **Regex Threat Protection** policies to the API flow. These complement the authentication layer and prevent malicious payload injections.

### Secure the Backend Connection
Configure mTLS between the Gravitee Gateway and backend microservices to ensure end-to-end encryption.

## Best Practices

{% hint style="info" %}
Use the **JWT policy** when the gateway and IdP are on separate networks or when performance is critical. Use the **OAuth 2.0 policy** for opaque tokens that require server-side introspection.
{% endhint %}

### Identify Broken Object Level Authorization
Authentication only proves identity. You must still perform object-level checks, such as verifying if a user owns a specific order, within your backend application logic.

### Use Token Redaction
Configure your logging and monitoring tools to automatically redact `Authorization` headers. This prevents sensitive tokens from appearing in plain text logs.

### Set Token Lifetimes
Follow industry standards by using short-lived access tokens (5 to 15 minutes) combined with refresh token rotation to minimize the impact of stolen credentials.

### Secure Web Applications
Avoid storing tokens in `localStorage`. Use `HttpOnly`, `Secure`, and `SameSite` cookies, or implement a Backend-for-Frontend (BFF) pattern to mitigate XSS risks.
