# API Products

## Overview

API Products enable administrators to bundle multiple V4 HTTP Proxy APIs into a single subscribable package with unified access control. Instead of managing subscriptions to individual APIs, organizations define product-level plans that grant access to all APIs within the product.

This feature requires an Enterprise Universe tier license.

<!-- TODO: Screenshot of the API Products list page in the APIM Console showing the "API Products" navigation item in the left sidebar and the list table -->
<figure><img src="../../../../.gitbook/assets/PLACEHOLDER-api-products-list.png" alt=""><figcaption><p>API Products list page in the APIM Console</p></figcaption></figure>

## What is an API Product?

An API Product is an environment-level resource that groups V4 HTTP Proxy APIs under a single subscription model. Each product has:

- A unique name within its environment (name comparison is case-sensitive, so "My Product" and "my product" are treated as different names)
- A version
- An optional description
- Product-level plans (API Key, JWT, or mTLS only — Keyless and OAuth plans are not supported)
- Product-level subscriptions

## How APIs, products, plans, and subscriptions relate

An API Product groups one or more V4 HTTP Proxy APIs. Each API Product has its own plans and subscriptions, separate from the plans and subscriptions of the individual APIs it contains.

APIs within a product retain their own plans and subscriptions. Consumers can subscribe to an individual API's plans independently of the product, and existing API-level subscriptions remain active when an API is added to a product.

An API can belong to multiple products simultaneously.

### Gateway subscription validation order

When a request reaches the gateway, the gateway validates subscriptions in the following priority order:

1. The gateway checks the request against the API Product plan subscription first.
2. If no valid API Product subscription exists, the gateway falls back to validating against the individual API plan.

API Product plans take priority, but access through API-level plans is still possible when no product-level subscription applies.

## API eligibility

Only V4 HTTP Proxy APIs with the **Allow in API Products** toggle enabled can be added to API Products. This toggle:

- Defaults to `true` for new V4 HTTP Proxy APIs created in version 4.11.0 or later
- Defaults to `false` for existing V4 HTTP Proxy APIs created before version 4.11.0
- Is unavailable for non-HTTP Proxy API types (message APIs, Kafka APIs, etc.)
- Is unavailable for read-only APIs (for example, Kubernetes-managed APIs)
- Cannot be disabled once an API is included in a product (the toggle is greyed out in the Console)

<!-- TODO: Screenshot of the API General Info page showing the "Allow in API Products" toggle for a V4 HTTP Proxy API -->
<figure><img src="../../../../.gitbook/assets/PLACEHOLDER-allow-in-api-products-toggle.png" alt=""><figcaption><p>"Allow in API Products" toggle on the API General Info page</p></figcaption></figure>

## Prerequisites

- Gravitee APIM Enterprise license with Universe tier
- Environment-level permissions for API Product management (`api_product-definition-*`)
- V4 HTTP Proxy APIs with the **Allow in API Products** toggle enabled

## Create an API Product

1. In the APIM Console, select **API Products** in the left sidebar.
2. Click **Create API Product**.
3. Enter a unique **Name** for the product. Names are case-sensitive — "My Product" and "my product" are treated as different names.
4. Enter a **Version** number.
5. Optionally, enter a **Description**.
6. Click **Create API Product**.

<!-- TODO: Screenshot of the Create API Product form showing the Name, Version, and Description fields -->
<figure><img src="../../../../.gitbook/assets/PLACEHOLDER-create-api-product.png" alt=""><figcaption><p>Create API Product form</p></figcaption></figure>

## Add APIs to a product

1. Open the API Product and select **APIs** in the left sidebar.
2. Click **Add API**.
3. In the **Add API** dialog, search for and select the APIs to add. Only V4 HTTP Proxy APIs with the **Allow in API Products** toggle enabled appear in the search results.
4. Click **Add API**.

<!-- TODO: Screenshot of the Add API dialog showing the API search field, the info banner ("APIs must have API products enabled before they appear in the list"), and the selected APIs chips -->
<figure><img src="../../../../.gitbook/assets/PLACEHOLDER-add-api-to-product.png" alt=""><figcaption><p>Add API dialog for an API Product</p></figcaption></figure>

## Create a plan for an API Product

1. Open the API Product and select **Consumers** in the left sidebar, then select the **Plans** tab.
2. Click the **+** button and select a plan type: **API Key**, **JWT**, or **mTLS**.
3. Configure the plan settings.
4. Click **Create**.
5. To activate the plan, select the **Publish** action on the plan.

Keyless and OAuth plan types are not available for API Products.

<!-- TODO: Screenshot of the Plans tab showing the plan type selection menu with API Key, JWT, and mTLS options -->
<figure><img src="../../../../.gitbook/assets/PLACEHOLDER-api-product-plan-types.png" alt=""><figcaption><p>Plan type selection for an API Product</p></figcaption></figure>

## Deploy an API Product

After creating plans and adding APIs, deploy the API Product to make it available at the gateway. When the product is out of sync, a warning banner displays "This API Product is out of sync." with a **Deploy API Product** button.

1. Click **Deploy API Product** in the banner, or trigger a deployment from the API Product detail page.
2. In the **Deploy your API Product** dialog, click **Deploy**.

Deployment requires an active Enterprise Universe tier license.

<!-- TODO: Screenshot of the deployment confirmation dialog showing "Deploy your API Product" title and the Deploy button -->
<figure><img src="../../../../.gitbook/assets/PLACEHOLDER-deploy-api-product.png" alt=""><figcaption><p>Deploy API Product confirmation dialog</p></figcaption></figure>

## P0 limitations

The initial release of API Products has the following limitations:

- No OAuth or Keyless plans
- No policies or flows at the product level

## Next steps

- [Consuming APIs via API Products](consuming-api-products.md)
- [API Products restrictions and licensing](restrictions-and-licensing.md)
- [Managing API Products via Management API](manage-api-products-via-management-api.md)
