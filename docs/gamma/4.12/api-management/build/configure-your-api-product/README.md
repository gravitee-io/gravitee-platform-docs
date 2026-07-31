---
hidden: false
noIndex: false
---

# Configure API products

After you create an API product, use the product detail page to attach APIs, create plans, manage consumers, control team access, and choose where the product is deployed.

## Licensing

API Products are an enterprise feature. Your organization's license must include the `apim-api-products` feature, which is available on the Galaxy tier and above, to create, update, or deploy an API Product. Without it, the Management API rejects the request as a forbidden feature.

## Configuration areas

| Area                 | What you configure                                                | Page                                                                                  |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **APIs**             | Attach and detach API proxies from the product                    | [Manage product APIs](manage-product-apis.md)                                         |
| **Plans**            | Create API Key, JWT, and mTLS subscription plans for the product  | [Secure your API proxy](../secure-your-api-proxy.md)                                  |
| **Consumers**        | Subscriptions, approvals, and API key management                  | [Establish consumer access](../configure-your-api-proxy/establish-consumer-access.md) |
| **User Permissions** | Direct and inherited members, roles, and ownership                | [Manage members and ownership](manage-members-and-ownership.md)                        |
| **Deployment**       | Sharding tags that decide which Gateways load the product         | [Configure product deployment](configure-product-deployment.md)                        |

## Access product configuration

1. From the Gamma console sidebar, select **API Management**.
2. From the module navigation, select **API Products**.
3. Select the product you want to configure.
4. Use the product detail sidebar to navigate between configuration areas.

The product detail sidebar organizes configuration into the following four groups:

* **General**. Contains Overview, General, and APIs.
* **Consumer Access**. Contains Plans and Consumers.
* **Security**. Contains User Permissions.
* **Operations**. Contains Deployment.

## Which APIs can be attached

An API only appears in the **Add API** panel when both of the following are true:

* The API uses the V4 API definition. The Management API rejects anything else with `Only V4 API definition is supported`.
* The API has **Allow in API Products** enabled on its **General** page. The panel repeats this as a hint: *APIs must have API products enabled before they appear in this list.*

APIs keep their own plans and subscriptions after they are attached, so consumers can still subscribe to an individual API independently of the product. For the underlying flag and the validation errors it produces, see [API product configuration reference](api-product-configuration-reference.md#api-eligibility).

## Product plans compared with API proxy plans

API Products support a subset of plan types. The following constraints apply when you create a plan for an API product:

* **Available plan types.** Product plans support API Key, JWT, and mTLS.
* **OAuth2 and Keyless plans.** These plan types are not available for API products. The Management API rejects a Keyless plan with `Plan Security Type KeyLess is not allowed.`
* **The Restrictions step.** This step, which covers rate limiting, quota, and resource filtering, is not available. Product plans use only the General and Security wizard steps.
* **The General step is shorter.** The **Conditions** section for a page of general conditions and the **Access Control** section for excluded groups appear only on API proxy plans.

For the full plan security type matrix, see [API product configuration reference](api-product-configuration-reference.md#supported-plan-security-types).

## Policies and flows

An API Product carries no flows or policies of its own, and product plans have no Restrictions step. Define policies on the API proxies bundled in the product instead, using the Policy Studio on each API.

## Gateway sync state

Each API Product reports whether the Gateway has its latest configuration. The state appears as a badge next to the product name in the detail sidebar header, and in the **Gateway sync** row of the **General** page:

| Badge            | Description                                                                     |
| ---------------- | --------------------------------------------------------------------------------- |
| **Synced**       | The Gateway has the current product configuration.                              |
| **Out of sync**  | The product has changed since the Gateway last retrieved it.                    |

The Management API returns these states as `DEPLOYED` and `NEED_REDEPLOY`. The Gamma console has no separate deploy or redeploy action for API Products.

A product that has APIs attached is only deployable when one of the following is true:

* The product has a published or deprecated plan of its own.
* Every attached API has a published or deprecated plan of its own.

For more detail, see [Configure product deployment](configure-product-deployment.md).
