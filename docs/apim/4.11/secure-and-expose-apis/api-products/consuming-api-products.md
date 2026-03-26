# Consuming APIs via API Products

## Overview

Clients consume APIs within an API Product using the same authentication mechanisms as individual API subscriptions. A single API Product subscription grants access to all APIs contained in the API Product.

## Authentication methods

**API Key plans:**

- Include the key in the `X-Gravitee-Api-Key` header, or
- Pass the key as a query parameter

**JWT plans:**

- Provide the token in the `Authorization: Bearer` header

**mTLS plans:**

- Present the client certificate during the TLS handshake

## Gateway subscription validation order

When a request reaches the gateway, the gateway validates subscriptions in the following priority order:

1. The gateway checks the request against the API Product plan subscription first.
2. If no valid API Product subscription exists, the gateway falls back to validating against the individual API plan.

API Product plans take priority, but access through API-level plans is still possible when no API Product-level subscription applies. APIs within an API Product retain their own plans and subscriptions, so consumers can continue to subscribe to individual API plans independently of the API Product.

## Gateway context attributes

For API Product subscriptions, the gateway sets the following context attributes:

- `apiProductId`: The API Product ID, exposed in the Expression Language context

To execute API Product-specific policies, use flow conditions that reference the `apiProductId` attribute.

## Subscribe to an API Product

1. In the APIM Console, open the API Product and select **Consumers** in the left sidebar, then select the **Subscriptions** tab.
2. Click **Create a subscription**.
3. Select a published plan and an application.
4. Confirm the subscription.

The subscription is created with a status based on the plan's validation setting:

- **AUTO** validation: the subscription is immediately **Accepted**
- **MANUAL** validation: the subscription is set to **Pending** and requires approval

After the subscription is accepted, the client authenticates requests using the method defined by the plan type (API Key header, JWT bearer token, or client certificate).

<figure><img src="../../.gitbook/assets/api-product-subscriptions.png" alt=""><figcaption><p>API Product subscriptions list</p></figcaption></figure>
