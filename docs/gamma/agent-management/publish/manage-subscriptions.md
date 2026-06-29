---
hidden: false
noIndex: false
---

# Manage subscriptions

Consumers access your LLM Proxies and MCP Proxies by subscribing to the security plans you've configured. As an API publisher, you must manage the lifecycle of these subscriptions.

## Subscription lifecycle

<!-- Source: gravitee-gamma-module-aim/src/test/java/com/graviteesource/gamma/module/aim/infra/service_provider/subscription/SubscriptionApimInMemory.java @ 9e2bb196 -->
Subscriptions to Agent Management resources follow a strict approval lifecycle:

1. **Pending**: When a consumer requests access to a plan that requires validation, the subscription is placed in a `PENDING` state.
2. **Accepted**: You can review the request and **Accept** the subscription. Once accepted, the status changes to `ACCEPTED`, an API key (if applicable) is generated, and the consumer can invoke the proxy.
3. **Rejected**: If the consumer should not have access, you can **Reject** the subscription. The status changes to `REJECTED`, and the consumer is denied access.
4. **Closed**: If an existing consumer should no longer have access (e.g., a departing team or a deprecated application), you can **Close** their subscription. The status changes to `CLOSED`, immediately revoking their access credentials.

## Manage requests

To accept, reject, or close a subscription:
1. Navigate to your LLM Proxy or MCP Proxy in the console.
2. Select **Subscriptions** from the inner navigation menu.
3. Locate the subscription in the list.
4. Use the actions menu to **Accept**, **Reject**, or **Close** the subscription.

When accepting a subscription, you can optionally specify a custom starting and ending date for the access grant.
