---
hidden: false
noIndex: true
---

# Create API Products
<!-- GAP-STRUCTURAL: Missing procedural content source -->

API Products let you bundle multiple API proxies into a single consumer-facing product. Instead of subscribing to individual APIs, consumers subscribe to an API Product plan and gain access to all APIs in the product.

## When to use API Products

Use API Products when you want to:

* **Simplify consumer onboarding** — One subscription grants access to multiple APIs.
* **Create tiered offerings** — Free, Standard, and Premium tiers that include different API bundles.
* **Manage cross-API access** — A single plan governs rate limits, quotas, and security across related APIs.
* **Decouple API internals from consumer experience** — Reorganize, split, or merge backend APIs without changing how consumers subscribe.

## API Products vs. API proxies

|                       | API proxy                                         | API Product                                                      |
| --------------------- | ------------------------------------------------- | ---------------------------------------------------------------- |
| **Represents**        | A single upstream API with its own endpoints      | A bundle of API proxies                                          |
| **Plans available**   | API Key, JWT, OAuth2, mTLS, Keyless               | API Key, JWT, mTLS                                               |
| **Restrictions step** | Available (rate limit, quota, resource filtering) | Not available                                                    |
| **Subscriptions**     | Consumers subscribe to the API directly           | Consumers subscribe to the product; access flows to bundled APIs |

## View API Products

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-c3528476320366df937e953cbca2227a042febb3%2Fgamma-api-products-list.png?alt=media" alt="API Products list in the Gamma APIM module"><figcaption><p>The API Products list shows all products with their deployment status, version, and bundled API count.</p></figcaption></figure>

1. From the Gamma console sidebar, select **API Management**.
2. Select **API Products** from the module navigation.

The API Products page displays a searchable, paginated list of all products with:

* **Product name** and primary owner
* **Version**
* **Deployment state** — `Deployed` or `Needs Redeploy`
* **Bundled API count**
* **Creation and last update dates**

## Create an API Product

1. From the **API Products** list, select **Create API Product**.
2. Fill in the product details:

| Field           | Description                                                                                               | Required | Default |
| --------------- | --------------------------------------------------------------------------------------------------------- | -------- | ------- |
| **Name**        | A unique name for the product. The console checks name availability in real time (with a 400ms debounce). | Yes      | —       |
| **Version**     | The product version string (e.g., `1.0.0`).                                                               | Yes      | `1.0.0` |
| **Description** | A freeform description of what the product offers to consumers.                                           | No       | —       |

3. Select **Create API Product**.

After creation, you are redirected to the product detail page where you can attach APIs, create plans, and manage consumers.

## API Product detail

Selecting a product from the list opens its detail page. The sidebar organizes configuration into three groups:

### General

| Tab          | Description                                                                                                 |
| ------------ | ----------------------------------------------------------------------------------------------------------- |
| **Overview** | Onboarding checklist and product snapshot (APIs in product, active consumers, total plans, direct members). |
| **General**  | Edit the product's name, version, description, and settings.                                                |
| **APIs**     | Attach or detach API proxies from the product.                                                              |

### Consumer Access

| Tab           | Description                                                                        |
| ------------- | ---------------------------------------------------------------------------------- |
| **Plans**     | Create and manage subscription plans for the product (API Key, JWT, mTLS).         |
| **Consumers** | Manage subscriptions, approve requests, and handle API keys for product consumers. |

### Security

| Tab                  | Description                                                                         |
| -------------------- | ----------------------------------------------------------------------------------- |
| **User Permissions** | Manage team access — control who can view, edit, publish plans, or own the product. |

## Onboarding checklist

The **Overview** page displays an interactive onboarding checklist that tracks your progress setting up the product:

| Step                                  | What to do                                                                            | Links to             |
| ------------------------------------- | ------------------------------------------------------------------------------------- | -------------------- |
| **Add APIs**                          | Attach HTTP API proxies so they share documentation and access through product plans. | APIs tab             |
| **Add Plans**                         | Create subscription plans with security, quotas, and monetization.                    | Plans tab            |
| **Create your first subscription**    | Add subscriptions, approve requests, and manage API keys.                             | Consumers tab        |
| **Invite teammates and assign roles** | Collaborate — control who can view, edit, publish plans, or own the product.          | User Permissions tab |

The checklist auto-detects progress (e.g., marking "Add APIs" complete when at least one API is attached) and also allows manual override.

**Product snapshot KPIs:**

* APIs in product
* Active consumers
* Total plans
* Direct product members

## Next steps

* [Manage product APIs](configure-your-api-product/manage-product-apis.md) — Attach API proxies to your product.
* [Secure your API proxy](secure-your-api-proxy.md) — Understand plan types and the plan creation wizard.
* [Establish consumer access](configure-your-api-proxy/establish-consumer-access.md) — Create subscriptions and manage API keys.
