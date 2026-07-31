---
hidden: false
noIndex: false
---

# Configure API products

After creating an API product, use the product detail page to attach APIs, create plans, manage consumers, control team access, and choose where the product is deployed.

## Licensing

API Products are an enterprise feature, and they are gated in two places:

* **In the console.** The **API Products** section only opens when your organization's license includes the `apim-api-products` feature. Without it, selecting **API Products** shows an upgrade dialog instead of the product list.
* **In the Management API.** Creating, updating, and deploying an API Product all require an organization license on the `universe` tier. On any other tier the API rejects the request as a forbidden feature.

## Configuration areas

| Area                 | What you configure                                                | Page                                                                                  |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **APIs**             | Attach and detach API proxies from the product                    | [Manage product APIs](manage-product-apis.md)                                         |
| **Plans**            | Create subscription plans (API Key, JWT, mTLS) for the product    | [Secure your API proxy](../secure-your-api-proxy.md)                                  |
| **Consumers**        | Subscriptions, approvals, and API key management                  | [Establish consumer access](../configure-your-api-proxy/establish-consumer-access.md) |
| **User Permissions** | Direct and inherited members, roles, and ownership                | [Manage members and ownership](manage-members-and-ownership.md)                        |
| **Deployment**       | Sharding tags that decide which gateways load the product         | [Configure product deployment](configure-product-deployment.md)                        |

## Accessing product configuration

1. From the Gamma console sidebar, select **API Management**.
2. Select **API Products** from the module navigation.
3. Select the product you want to configure.
4. Use the product detail sidebar to navigate between configuration areas.

The product detail sidebar organizes configuration into four groups: **General** (Overview, General, APIs), **Consumer Access** (Plans, Consumers), **Security** (User Permissions), and **Operations** (Deployment).

## Which APIs can be attached

An API only appears in the **Add API** panel when both of the following are true:

* The API uses the V4 API definition. The Management API rejects anything else with `Only V4 API definition is supported`.
* The API has **Allow in API Products** enabled on its **General** page. The panel repeats this as a hint: *APIs must have API products enabled before they appear in this list.*

APIs keep their own plans and subscriptions after they are attached, so consumers can still subscribe to an individual API independently of the product. For the underlying flag and the validation errors it produces, see [API product configuration reference](api-product-configuration-reference.md#api-eligibility).

## Product plans vs. API proxy plans

API Products support a subset of plan types. When creating a plan for an API product:

* **Available plan types**: API Key, JWT, mTLS
* **OAuth2 and Keyless plans are not available** for API products. The Management API rejects a Keyless plan with `Plan Security Type KeyLess is not allowed.`
* **The Restrictions step (rate limiting, quota, resource filtering) is not available** — product plans use only the General and Security wizard steps
* **The General step is shorter.** The **Conditions** section (page of general conditions) and the **Access Control** section (excluded groups) appear only on API proxy plans.

For the full plan security type matrix, see [API product configuration reference](api-product-configuration-reference.md#supported-plan-security-types).

## Policies and flows

An API Product carries no flows or policies of its own, and product plans have no Restrictions step. Define policies on the API proxies bundled in the product instead, using the Policy Studio on each API.

## Gateway sync state

Each API Product reports whether the gateway has its latest configuration. The state appears as a badge next to the product name in the detail sidebar header, and in the **Gateway sync** row of the **General** page:

| Badge            | Description                                                                     |
| ---------------- | --------------------------------------------------------------------------------- |
| **Synced**       | The gateway has the current product configuration.                              |
| **Out of sync**  | The product has changed since the gateway last picked it up.                    |

The Management API returns these states as `DEPLOYED` and `NEED_REDEPLOY`. The Gamma console has no separate deploy or redeploy action for API Products.

A product that has APIs attached is only deployable once it has a published or deprecated plan of its own, or every attached API has a published or deprecated plan of its own. For more detail, see [Configure product deployment](configure-product-deployment.md).
