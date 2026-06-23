# Configure Plan Deployment

## Managing API Product Plans

### Assigning sharding tags to plans

Navigate to **API Product → Consumers → Plans** and create or edit a plan. On the **General** step, scroll down to the **Deployment** section to assign sharding tags to the plan.

1. Locate the **Deployment** section below the **Subscriptions** section. The **Sharding tags** dropdown is initially empty.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-21.png" alt="Plan configuration page showing deployment section with empty sharding tags dropdown"><figcaption></figcaption></figure>

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-22.png" alt="Plan configuration form showing deployment section with empty sharding tags dropdown"><figcaption></figcaption></figure>

2. Click the **Sharding tags** dropdown to expand the list of available tags. Select zero or more tags from the dropdown. The dropdown is constrained to the parent API Product's tags—only tags present in both the product's tag set and the user's allowed tags are enabled for selection.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-23.png" alt="Plan configuration form with deployment section showing sharding tags dropdown expanded with 'external' selected"><figcaption></figcaption></figure>

3. Complete the remaining plan configuration steps (Name, Description, Characteristics, Subscriptions, and Access-Control) and save the plan.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-24.png" alt="Plan configuration form showing General section with name field, Description field, Characteristics field, Subscriptions section, and Deployment section"><figcaption></figcaption></figure>

| Field | Description | Example |
|:------|:------------|:--------|
| **Sharding Tags** | Sharding tags assigned to the plan. Must be a subset of the API Product's tags. An empty tag set means the plan is eligible on every gateway where the parent product is eligible. | `external` |

When tags are removed from the API Product, any plan tags that are no longer on the product are automatically stripped from affected plans. Expanding product tags does not retroactively add tags to existing plans. Clearing all product tags clears all plan tags on that product's plans.

Users with the `API_PRODUCT_PLAN:CREATE` permission can assign tags when creating plans. Users with the `API_PRODUCT_PLAN:UPDATE` permission can modify tags on existing plans. Users without these permissions cannot access the plan editor or see the Deployment section.

### Viewing Subscriptions

After a plan is created and subscribed to, you can view subscription details by navigating to **API Product → Consumers → Subscriptions**. Select a subscription to view its details page, which displays the plan name, subscription status, consumer status, subscribed user, application information, and timestamps.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-25.png" alt="Subscription details page showing plan information and consumer status"><figcaption></figcaption></figure>

The subscription details page is also accessible from the **APIs → Consumers → Subscriptions** view for individual APIs. The page displays the same subscription metadata, including the plan name (e.g., `shared (API_KEY)`), status (`ACCEPTED`), consumer status (`STARTED`), and associated application.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-26.png" alt="Subscription details page for API with plan and application information"><figcaption></figcaption></figure>

### Viewing Plan Deployment in the API Products List

Navigate to **API Products → Consumers → Plans** to view the deployment tags for each published plan. The **Deploy on** column displays the sharding tag(s) assigned to each plan. This column was previously hidden for API Product plans and is now visible.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-27.png" alt="Plans list showing published plan with 'shared' deployment tag in the Deploy on column"><figcaption></figcaption></figure>

If a product has multiple plans with different deployment tags, each plan displays its assigned tag(s) in the **Deploy on** column.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-28.png" alt="Plans list showing two published plans with 'external' and 'internal' deployment tags"><figcaption></figcaption></figure>

For APIs included in an API Product, navigate to **APIs → [API Name] → Consumers → Plans** to view the deployment tags for that API's plans.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-29.png" alt="Plans list for API showing single published plan with 'shared' deployment tag"><figcaption></figcaption></figure>

The **API Products** list table includes a **Sharding Tags** column. For each product, the column displays the first tag name. If the product has more than one tag, a badge with the text `"1 More"` (or the appropriate count) appears. Hovering over the badge shows a tooltip with all tag names (comma-separated).

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-30.png" alt="API Products list showing product with multiple sharding tags including external and internal"><figcaption></figcaption></figure>

When a subscription is created for a plan with deployment tags, the generated API key can be used to access the API through the gateways matching those tags. View the subscription details and API key in **API Products → Consumers → Subscriptions**.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-31.png" alt="Subscription details page showing subscriber information, application details, timestamps, and API Keys section with generated key"><figcaption></figcaption></figure>

### Gateway Runtime Behavior

Gateway instances apply the following rules when indexing API Products, plans, and member APIs:

| Gateway Configuration | Behavior |
|:----------------------|:---------|
| No sharding tags configured | Gateway retrieves all API Products, plans, and APIs. |
| One or more sharding tags configured | Gateway indexes only entities whose tags intersect with its configured tags. Within an eligible product, only published or deprecated plans whose plan tags match the gateway are indexed. Tagless plans match any gateway that already matched the product. |

A member API is deployed on a gateway if either its own sharding tags match the gateway, or it has at least one published or deprecated API Product plan indexed on that gateway. For the product plan path, the product's tags must match the gateway, and the plan's tags must be empty (inheriting product placement) or match the gateway (subset of product tags). Standalone APIs (not relying on product eligibility) deploy only when their own tags match the gateway.

When an API Product is undeployed or its tags or plans change such that member APIs are no longer eligible, affected APIs are undeployed on that gateway. Product deploy and update events trigger ordered resync and re-evaluation of member APIs.

To verify that a member API is accessible through its API Product context path, send a GET request to the product entrypoint with the appropriate API key in the `X-Gravitee-Api-Key` header. A successful response with status `200 OK` confirms the API is deployed and the sharding tags are correctly configured.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-32.png" alt="API request in Postman showing successful response with status 200 OK"><figcaption></figcaption></figure>

### Validation and Error Handling

Plan tags are validated against the API Product's tags when creating or updating plans. If a plan includes tags that are not present in the product's tag set, the operation fails with the error message: `"Plan tags mismatch the tags defined by the API Product"`. The error response includes the plan's tags and the product's tags for debugging.

When a user attempts to assign a group-restricted sharding tag without membership in the tag's restricted groups, the save operation fails with a validation error.

Organization-level tag deletion cascades to all API Products and plans in all environments. Deleting a tag removes it from every product and plan that references it. This operation cannot be undone.

When an API Product's sharding tag configuration is modified, the product enters an out-of-sync state. The Consumers page displays a warning banner indicating the product is out of sync, with a **Deploy API Product** button to synchronize the changes.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-33.png" alt="API Product consumers page showing out of sync warning banner with Deploy API Product button"><figcaption></figcaption></figure>

Until the API Product is redeployed, API requests to endpoints associated with the modified sharding tags will fail. Consumers attempting to access the API receive a 404 Not Found error response.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-34.png" alt="API request in Postman showing 404 Not Found error response"><figcaption></figcaption></figure>
