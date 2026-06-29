---
hidden: false
noIndex: true
---

# Configure API products
<!-- GAP-STRUCTURAL: Missing procedural content source -->

After creating an API product, use the product detail page to attach APIs, create plans, manage consumers, and control team access.

## Configuration areas

| Area          | What you configure                                             | Page                                                                            |
| ------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **APIs**      | Attach and detach API proxies from the product                 | [Manage product APIs](manage-product-apis.md)           |
| **Plans**     | Create subscription plans (API Key, JWT, mTLS) for the product | [Secure your API proxy](../secure-your-api-proxy.md)                                  |
| **Consumers** | Subscriptions, approvals, and API key management               | [Establish consumer access](../configure-your-api-proxy/establish-consumer-access.md) |

## Accessing product configuration

1. From the Gamma console sidebar, select **API Management**.
2. Select **API Products** from the module navigation.
3. Select the product you want to configure.
4. Use the product detail sidebar to navigate between configuration areas.

The product detail sidebar organizes configuration into three groups: **General** (Overview, General, APIs), **Consumer Access** (Plans, Consumers), and **Security** (User Permissions).

## Product plans vs. API proxy plans

API Products support a subset of plan types. When creating a plan for an API product:

* **Available plan types**: API Key, JWT, mTLS
* **OAuth2 and Keyless plans are not available** for API products
* **The Restrictions step (rate limiting, quota, resource filtering) is not available** — product plans use only the General and Security wizard steps

## Deployment state

API Products track deployment state:

| State              | Description                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------- |
| **Deployed**       | The product configuration is synchronized with the Gateway.                                       |
| **Needs Redeploy** | The product has been modified since the last deployment. Redeploy to sync changes to the Gateway. |
