---
hidden: false
noIndex: false
---

# Create API Products

API Products let you bundle multiple API proxies into a single consumer-facing product. Instead of subscribing to individual APIs, consumers subscribe to an API Product plan and gain access to all APIs in the product.

{% hint style="info" %}
API Products are an enterprise feature. Your organization's license must include the `apim-api-products` feature to create, update, or deploy a product. See [Configure API products](configure-your-api-product/README.md#licensing).
{% endhint %}

## When to use API Products

Use API Products when you want to do the following:

* **Simplify consumer onboarding**. One subscription grants access to multiple APIs.
* **Create tiered offerings**. You can create Free, Standard, and Premium tiers that include different API bundles.
* **Manage cross-API access**. A single plan governs security and subscription approval across related APIs.
* **Decouple API internals from consumer experience**. Reorganize, split, or merge backend APIs without changing how consumers subscribe.

## API Products compared with API proxies

The following table compares an API proxy with an API Product:

|                        | API proxy                                          | API Product                                                      |
| ---------------------- | -------------------------------------------------- | ---------------------------------------------------------------- |
| **Represents**         | A single upstream API with its own endpoints       | A bundle of API proxies                                          |
| **Plans available**    | API Key, JWT, OAuth2, mTLS, Keyless                | API Key, JWT, mTLS                                               |
| **Plan wizard steps**  | General, Security, Restrictions                    | General, Security                                                |
| **Restrictions step**  | Available for rate limit, quota, and resource filtering | Not available                                               |
| **Plan conditions**    | Page of general conditions and excluded groups     | Not available                                                    |
| **Flows and policies** | Defined on the API in the Policy Studio            | Not available at product level; define them on the bundled APIs  |
| **Subscriptions**      | Consumers subscribe to the API directly            | Consumers subscribe to the product; access flows to bundled APIs |
| **Licensing**          | Not gated by a license feature                     | Requires the `apim-api-products` license feature |

## View API Products

<figure><img src="../../.gitbook/assets/gamma-api-products-list.png" alt="API Products list in the Gamma APIM module"><figcaption><p>The API Products list shows all products with their bundled API count, version, sharding tags, and owner.</p></figcaption></figure>

1. From the Gamma console sidebar, select **API Management**.
2. From the module navigation, select **API Products**.

The API Products page displays a searchable, paginated list of all products. Use **View** to show or hide any of the following columns:

| Column            | Description                                                        |
| ----------------- | -------------------------------------------------------------------- |
| **Product Name**  | The product name, which links to the product detail page.          |
| **Total APIs**    | How many API proxies are bundled in the product.                   |
| **Version**       | The product version string.                                        |
| **Sharding Tags** | The tags that decide which Gateways load the product, or `—`.      |
| **Owner**         | The product's primary owner.                                       |

A product's Gateway sync state is not a column on this list. It appears on the product detail page. See [Configure API products](configure-your-api-product/README.md#gateway-sync-state).

## Create an API Product

1. From the **API Products** list, select **Create API Product**.
2. Enter the following product details:

    | Field           | Description                                                                                                | Required | Default |
    | --------------- | ---------------------------------------------------------------------------------------------------------- | -------- | ------- |
    | **Name**        | A unique name for the product. The console checks name availability in real time, with a 400 ms debounce.  | Yes      | —       |
    | **Version**     | The product version string, for example `1.0.0`.                                                           | Yes      | `1.0.0` |
    | **Description** | A freeform description of what the product offers to consumers.                                            | No       | —       |

3. Select **Create API Product**.

After creation, you are redirected to the product detail page where you can attach APIs, create plans, and manage consumers.

## API Product detail

When you select a product from the list, its detail page opens. The sidebar organizes configuration into four groups:

### General

The **General** group contains the following tabs:

| Tab          | Description                                                                                                 |
| ------------ | ----------------------------------------------------------------------------------------------------------- |
| **Overview** | Onboarding checklist and product snapshot, covering APIs in product, active consumers, total plans, and direct members. |
| **General**  | Edit the product's name, version, and description, and run product lifecycle actions.                       |
| **APIs**     | Attach or detach API proxies from the product.                                                              |

### Consumer Access

The **Consumer Access** group contains the following tabs:

| Tab           | Description                                                                        |
| ------------- | ---------------------------------------------------------------------------------- |
| **Plans**     | Create and manage the product's API Key, JWT, and mTLS subscription plans.         |
| **Consumers** | Manage subscriptions, approve requests, and handle API keys for product consumers. |

### Security

The **Security** group contains the following tab:

| Tab                  | Description                                                                         |
| -------------------- | ----------------------------------------------------------------------------------- |
| **User Permissions** | Manage team access — control who can view, edit, publish plans, or own the product. |

### Operations

The **Operations** group contains the following tab:

| Tab            | Description                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------------- |
| **Deployment** | Assign the sharding tags that decide which Gateway instances load the product.                  |

## Onboarding checklist

The **Overview** page displays an interactive onboarding checklist that tracks your progress configuring the product:

| Step                                  | What to do                                                                            | Links to             |
| ------------------------------------- | ------------------------------------------------------------------------------------- | -------------------- |
| **Add APIs**                          | Attach HTTP API proxies so they share documentation and access through product plans. | APIs tab             |
| **Add Plans**                         | Create subscription plans with security, quotas, and monetization.                    | Plans tab            |
| **Create your first subscription**    | Add subscriptions, approve requests, and manage API keys.                             | Consumers tab        |
| **Invite teammates and assign roles** | Collaborate — control who can view, edit, publish plans, or own the product.          | User Permissions tab |

The checklist autodetects progress. For example, it marks **Add APIs** complete when at least one API is attached. The checklist also allows manual override.

The product snapshot reports the following KPIs:

* APIs in product
* Active consumers
* Total plans
* Direct product members

## Next steps

* [Configure API products](configure-your-api-product/README.md). Review licensing, plan restrictions, and the product detail page.
* [Manage product APIs](configure-your-api-product/manage-product-apis.md). Attach API proxies to your product.
* [Secure your API proxy](secure-your-api-proxy.md). Understand plan types and the plan creation wizard.
* [Establish consumer access](configure-your-api-proxy/establish-consumer-access.md). Create subscriptions and manage API keys.
* [Configure product deployment](configure-your-api-product/configure-product-deployment.md). Choose which Gateways load the product.
