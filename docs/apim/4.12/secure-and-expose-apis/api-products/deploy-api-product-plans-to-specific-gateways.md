# Deploy API Product Plans to Specific Gateways

## Managing Plan Deployment

Navigate to **API Product → Consumers → Plans** and create or edit a plan. On the **General** step, scroll to the **Deployment** section to assign sharding tags to the plan.

1. Locate the **Sharding tags** dropdown in the **Deployment** section.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-07.png" alt="Plan configuration form showing deployment section with empty sharding tags dropdown"><figcaption></figcaption></figure>

2. Click the **Sharding tags** dropdown to view available tags. The dropdown displays only tags defined on the parent API Product. For information on configuring product-level tags, see [Deploy API Products to Specific Gateways](deploy-api-products-to-specific-gateways.md). Tags are constrained to the intersection of the product's tags and the user's allowed tags (from `/user/tags`). Tags outside this intersection are disabled.

3. Select zero or more tags from the dropdown. In the example shown, the available tags are `external`, `internal`, and `shared`.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-08.png" alt="Plan form showing deployment section with sharding tags dropdown expanded to show 'external', 'internal', and 'shared' options with 'external' selected"><figcaption></figcaption></figure>

4. Save the plan. Plan tags must be a subset of the API Product's tags. If you attempt to assign a tag not present on the product, you will receive a validation error: `"Plan tags mismatch the tags defined by the API Product"`.

| Field | Description | Example |
|:------|:------------|:--------|
| **Sharding Tags** | Select zero or more sharding tags for the plan. Plan tags must be a subset of the API Product's tags. An empty plan tag set means the plan is eligible on every gateway where the parent product is eligible. | `external` |

**Permissions:**
- Creating a plan with tags requires `API_PRODUCT_PLAN:CREATE`.
- Updating plan tags requires `API_PRODUCT_PLAN:UPDATE`.

**Behavior notes:**
- An empty plan tag set means the plan is eligible on every gateway where the parent product is eligible. Gateway instances treat tagless plans as matching all gateways that already matched the product.
- When tags are removed from the API Product, any plan tags that are no longer on the product are automatically stripped from affected plans.
- Only published or deprecated plans are indexed on gateways. Draft plans are excluded regardless of tags.
- All tag changes on plans produce audit log entries on the affected resource.

### Viewing Product Tags in the API Products List

The API Products table includes a **Sharding Tags** column. For each product, the column displays the first sharding tag. If the product has additional tags, a badge appears showing the count (e.g., "1 More"). Hovering over the badge displays a tooltip listing all assigned tags.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-11.png" alt="API Products list showing product-1 with sharding tags 'external' and '1 More' displayed in tooltip showing 'external, internal'"><figcaption></figcaption></figure>

### Viewing Plan Tags in the Plan List

When viewing an API Product's Plans list under **Consumers > Plans**, the **Deploy on** column displays the sharding tags assigned to each published plan.

For a single plan with one tag, the **Deploy on** column shows the tag value directly (e.g., "shared").

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-09.png" alt="Plans list showing a published plan with 'shared' displayed in the Deploy on column"><figcaption></figcaption></figure>

When multiple plans are published with different tags, each plan displays its assigned tag in the **Deploy on** column (e.g., "external" and "internal").

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-10.png" alt="Plans list showing two published plans with 'external' and 'internal' tags in the Deploy on column"><figcaption></figcaption></figure>

### Member API Deployment Behavior

A member API is eligible to deploy on a gateway if either:
- Its own sharding tags match the gateway, or
- It has at least one published or deprecated API Product plan indexed on that gateway, where the product's tags match the gateway and the plan's tags are empty or match the gateway.

Standalone APIs (not relying on product eligibility) deploy only when their own tags match the gateway. When an API Product is undeployed or its tags or plans change such that member APIs are no longer eligible, affected APIs are undeployed on that gateway. Product deploy and update events trigger ordered resync and re-evaluation of member APIs. The ordered resync ensures newly eligible APIs are deployed before ineligible ones are undeployed, preventing brief unavailability windows during product tag changes.

### Management API

**Update API Product tags:**
- **Endpoint:** `PUT /management/v2/environments/{envId}/api-products/{productId}`
- **Payload field:** `tags` (array of strings)
- **Validation:** Tags are validated against organization-level tags. Group-restricted tags are rejected if the user is not a member of the restricted groups.

**Update plan tags:**
- **Endpoint:** `PUT /management/v2/environments/{envId}/api-products/{productId}/plans/{planId}`
- **Payload field:** `tags` (array of strings)
- **Validation:** Plan tags must be a subset of the API Product's tags. Validation error: `"Plan tags mismatch the tags defined by the API Product"`.
