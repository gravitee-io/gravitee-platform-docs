# Federated API Access Information Display

## Overview

The Developer Portal displays API access information only when it is available and relevant to the API type. For federated APIs—APIs ingested from third-party providers and served outside the Gravitee gateway—the portal hides empty access sections that would otherwise confuse subscribers. This ensures a cleaner, more intuitive subscription experience for APIs managed by external providers.

## Key Concepts

### Federated APIs

Federated APIs are discovered from third-party providers and ingested into APIM. Unlike native Gravitee APIs, federated APIs remain hosted and managed by the provider—there is no Gravitee gateway proxying. Federated APIs are distinguished by `definitionVersion: FEDERATED` in the API schema. Because the actual API endpoints reside with the provider, the `entrypoints` array may be empty or undefined. The portal handles this gracefully by hiding inapplicable access information.

### API Access Card

The API Access card displays connection details for subscribed APIs, including base URLs, authentication credentials, and example curl commands. The card's visibility is controlled by conditional logic that evaluates whether the subscription status is `ACCEPTED` or the plan security is `KEY_LESS`, then checks whether relevant content exists.

For native APIs, the card is always displayed regardless of entrypoint availability. For federated APIs with empty entrypoints, the card's visibility depends on the plan's security type:

| Plan Security | Entrypoints Empty | Card Behavior |
|---------------|-------------------|---------------|
| `KEY_LESS` | Yes | Entire card hidden |
| `API_KEY` | Yes | API keys table shown; "Calling the API" section hidden (if no active keys) |
| `OAUTH2`, `JWT`, `API_KEY` | No | Full card shown |
| Any | N/A (Native API) | Full card always shown |

### Calling the API Section

The "Calling the API" section within the API Access card displays base URLs and example curl commands. Its visibility is controlled by conditional logic that checks three conditions: entrypoint URLs are available AND (plan security is not `API_KEY` OR subscription status is not `ACCEPTED` OR active API keys exist).

For `API_KEY` plans with `ACCEPTED` subscription status, the "Calling the API" section is hidden when entrypoints are empty only if there are no active API keys. If active API keys exist, the section remains visible even when entrypoints are empty.

### Subscription Status Display

When a subscription status is not `ACCEPTED` and the plan security is not `KEY_LESS`, the API Access card displays a status message instead of access details. Status messages include "Subscription in progress," "Subscription rejected," "Subscription paused," and "Subscription closed."

## Prerequisites

* Access to the Next-Generation Developer Portal
* An active subscription to a federated API (or permission to create one)

## Creating a Subscription to a Federated API

When subscribing to a federated API in the Developer Portal, the subscription flow is identical to native APIs. However, the API Access card displayed after subscription approval adapts to the availability of entrypoint information.

For keyless federated APIs with no entrypoints defined, the entire API Access card is hidden after subscription approval, preventing users from seeing an empty access section.

For API key-based federated APIs with no entrypoints, the API Access card displays the API keys section (showing provider-provisioned keys with **Renew API Key** and **Revoke** actions), but hides the "Calling the API" section (which would otherwise show empty **Base URL** fields and curl command examples) when there are no active API keys. If active API keys exist, the "Calling the API" section remains visible. If no API keys are available, the message "No API keys available." is displayed.

For OAuth2 or JWT federated APIs with entrypoints defined, the full API Access card is shown, including **Client ID**, **Client Secret**, **Base URL** or **Base URLs**, and example commands.

For native APIs (non-federated), the API Access card is always displayed regardless of entrypoint availability.

## Managing Federated API Subscriptions

Federated API subscriptions are managed identically to native API subscriptions in the Developer Portal. Users can view subscription status, renew or revoke API keys (for `API_KEY` plans), and monitor subscription state changes.

Because federated APIs are provider-managed, authentication credentials (API keys, OAuth2 client credentials) are provisioned by the external provider. Usage instructions and endpoint documentation may differ from native Gravitee APIs and should be obtained from the provider's documentation.

When a subscription is in a non-accepted state (`PENDING`, `REJECTED`, `PAUSED`, or `CLOSED`), the API Access card displays a status-specific message instead of access details:

| Status | Header | Content |
|--------|--------|---------|
| `PENDING` | Subscription in progress | Your subscription request is being validated. Come back later. |
| `REJECTED` | Subscription rejected | _(status-specific content)_ |
| `PAUSED` | Subscription paused | _(status-specific content)_ |
| `CLOSED` | Subscription closed | _(status-specific content)_ |
