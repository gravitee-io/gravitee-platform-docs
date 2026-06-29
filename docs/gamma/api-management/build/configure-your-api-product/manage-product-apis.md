---
hidden: false
noIndex: false
---

# Manage product APIs
<!-- GAP-STRUCTURAL: Missing procedural content source -->

The **APIs** tab in the API Product detail page lets you attach and detach API proxies from the product. Consumers who subscribe to the product's plans gain access to all attached APIs.

## Attach APIs to a product

1. Navigate to the API product detail page.
2. In the sidebar, select **General → APIs**.
3. Select **Add API**.
4. In the dialog, search for and select the API proxies to attach.
5. Confirm to add them to the product.

## View attached APIs

The APIs tab displays a list of all API proxies currently bundled in the product. Each entry shows the API name and allows you to navigate to the individual API detail page.

The product Overview page also shows the **APIs in product** count as a snapshot KPI.

## Detach an API from a product

1. On the **APIs** tab, locate the API proxy to remove.
2. Select the remove action.
3. Confirm the removal.

Detaching an API does not delete the API proxy itself — it only removes it from the product bundle. Existing subscriptions to the product no longer grant access to the detached API.

## How product subscriptions grant API access

When a consumer subscribes to an API Product plan:

1. The Gateway validates the consumer's credentials against the product's plan.
2. If the request targets an API that is bundled in the product, the Gateway permits the request.
3. If the API is not part of the product, the request is rejected.

This means consumers do not need individual subscriptions to each API — a single product subscription covers all bundled APIs.

## Next steps

* [Secure your API proxy](../secure-your-api-proxy.md) — Create plans for your product.
* [Establish consumer access](../configure-your-api-proxy/establish-consumer-access.md) — Manage subscriptions for product consumers.
