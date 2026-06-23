# Deploy API Products to Specific Gateways

## Creating API Product Deployment Configuration

Organization-level sharding tags must be defined at [**Organization → Entrypoints & Sharding Tags**](../../configure-and-manage-the-platform/gravitee-gateway/sharding-tags.md#sharding-tags) before they can be assigned to API Products.

Navigate to **API Products → Deployment** to assign sharding tags that control where the product is deployed. The Deployment navigation item uses the rocket icon and requires `api_product-definition-r` permission for visibility. The page header displays "Manage sharding tags and where this API Product is deployed."

1. Select one or more **Sharding Tags** from the dropdown. The form loads sharding tags from the `/configuration/tags` endpoint and displays each tag's name and description in the dropdown. Only tags you are allowed to assign (unrestricted tags or group-restricted tags for groups you belong to) are accepted on save.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-01.png" alt="API deployment configuration page showing sharding tags dropdown with 'shared' tag selected"><figcaption></figcaption></figure>

2. Click **Save** to persist the tags on the API Product definition. The form shows a save bar when the form is dirty and valid. On save, the page triggers an `ApiProductChanged` notification and reloads the product after successful save.

3. If you attempt to save a restricted tag that you are not a member of, the system displays an error message at the bottom of the page: "You are not allowed to use deployment on the tag(s) [restricted]." The save operation is blocked until you select only allowed tags.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-02.png" alt="API Product deployment page showing error message 'You are not allowed to use deployment on the tag(s) [restricted]' with sharding tags dropdown displaying 'restricted-tag-api1-not-a-member'"><figcaption></figcaption></figure>

4. Click **Deploy** in the API Product header to synchronize the product (including its tags and published plans) to gateway instances. Gateway instances index and serve the product only when product tags match their configured sharding tags.

| Field | Description | Example |
|:------|:------------|:--------|
| **Sharding Tags** | Choose the sharding tags that you want to assign to the API Product. This dictates where it is deployed. Sharding tags are configured at the Organization level. | `eu`, `us-west` |

**Permissions:**
- Viewing the Deployment tab requires `api_product-definition-r`.
- Updating tags requires `API_PRODUCT_DEFINITION:UPDATE`.
- Deploying the product requires `API_PRODUCT_DEFINITION:UPDATE`.
- Verifying deployment (license and compatibility check) requires `API_PRODUCT_DEFINITION:READ`.

**Behavior notes:**
- Saving tags marks the product out of sync until you run **Deploy**. An "out of sync" banner does not mean the product is undeployed on gateways.
- When you remove a tag from the API Product, that tag is automatically removed from all plans within the product. If a plan's tag set becomes empty, the plan inherits the product's full deployment scope.
- Expanding product tags does not retroactively add tags to existing plans.
- Clearing all product tags clears all plan tags on that product's plans.
- Deleting an organization-level tag removes it from all API Products and their plans in all environments.
- All tag changes on API Products produce audit log entries on the affected resource.

### Member API Deployment Eligibility

A member API is eligible for deployment on a gateway if either:
- Its own sharding tags match the gateway, or
- It has at least one published or deprecated API Product plan indexed on that gateway, where:
  - The product's tags match the gateway (a tagless product matches all gateways), and
  - The plan's tags are empty (inherits product placement) or match the gateway (subset of product tags).

Standalone APIs (not relying on product eligibility) are unchanged: they deploy only when their own tags match the gateway.

### Product Change Propagation

When an API Product is undeployed or its tags/plans change such that member APIs are no longer eligible, affected APIs are undeployed on that gateway. Product deploy/update events trigger ordered resync and re-evaluation of member APIs: newly eligible APIs are deployed before ineligible ones are undeployed.
