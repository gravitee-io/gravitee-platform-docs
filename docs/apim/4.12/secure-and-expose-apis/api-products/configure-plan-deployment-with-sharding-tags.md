# Configure Plan Deployment with Sharding Tags

## Managing API Product Plans

{% hint style="info" %}
You must have the API_PRODUCT_PLAN:CREATE or API_PRODUCT_PLAN:UPDATE permission to assign sharding tags to plans.
{% endhint %}

Navigate to **API Product → Consumers → Plans** and select a plan to configure. The plan configuration form displays fields for the plan name, description, characteristics, subscription settings, and deployment options.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-13.png" alt="Plan configuration form showing name field, description field, and subscription settings"><figcaption></figcaption></figure>

1. Scroll down to the **Deployment** section within the plan configuration form.

2. Select zero or more tags from the **Sharding Tags** dropdown. The dropdown is constrained to the parent API Product's tags. Tags not defined on the product cannot be added to the plan. Disabled tags in the dropdown are tags not in both the user's allowed tags and the reference tags (product or API). An empty plan tag set means the plan is eligible on every gateway where the parent product is eligible.

3. Save the plan. If plan tags are not a subset of the API Product's tags, the save operation fails with the error: `"Plan tags mismatch the tags defined by the API Product"`.

| Property | Description | Example |
|:---------|:------------|:--------|
| **Sharding Tags** | Tags that refine deployment placement for the plan. Plan tags must be a subset of the API Product's tags. | `["eu"]` |

The plan list table includes a **Deploy On** column for API Product plans, displaying a comma-separated list of plan tags.

### Deploying the API Product

After assigning or modifying tags, deploy the API Product to synchronize the configuration to gateway instances. Navigate to the **Deployment** section in the left sidebar. If the API Product is out of sync, a notification banner will appear at the top of the page with a **Deploy API Product** button.

Click **Deploy API Product**. A confirmation dialog appears, warning that all subscribed consumers will be affected by the deployment.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-09.png" alt="Deploy API Product confirmation dialog with cancel and deploy buttons"><figcaption></figcaption></figure>

Click **Deploy** to confirm. The deploy action requires the API_PRODUCT_DEFINITION:UPDATE permission. Verifying deployment (license and compatibility checks) requires the API_PRODUCT_DEFINITION:READ permission.

A success notification appears at the bottom right of the screen confirming the configuration was saved.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-10.png" alt="API Product deployment page showing success notification after deployment"><figcaption></figcaption></figure>

### Automatic Plan Tag Cleanup

When tags are removed from the API Product, any plan tags that are no longer on the product are automatically stripped from affected plans. The cleanup runs for all plans of the product, not just plans with the removed tag. Cleanup is logged: `"Auto-cleaning orphaned tags from plan [plan-id] of API Product [product-id]: [old-tags] -> [new-tags]"`. Expanding product tags does not retroactively add tags to existing plans. Clearing all product tags clears all plan tags on that product's plans.

When an organization-level tag is deleted, the tag is removed from all API Products in all environments of the organization and from all plans of those API Products. The operation is idempotent (safe to retry after partial failure).

### Gateway Runtime Behavior

Gateway instances only index and serve the product when product tags match their configured sharding tags. Within an eligible product, only published or deprecated plans whose plan tags match the gateway are indexed. Tagless plans match any gateway that already matched the product.

| Gateway Configuration | Behavior |
|:----------------------|:---------|
| No sharding tags configured | Gateway retrieves all API Products, plans, and APIs (same as APIs today). |
| One or more sharding tags configured | Gateway only indexes entities whose tags intersect with its configured tags. Within an eligible product, only published or deprecated plans whose plan tags match the gateway are indexed. Tagless plans match any gateway that already matched the product. |

A member API is shard-eligible on a gateway if **either** its own sharding tags match the gateway **or** it has at least one published or deprecated API Product plan indexed on that gateway, where the product's tags match the gateway (tagless product matches all gateways) and the plan's tags are empty (inherits product placement) or match the gateway (subset of product tags). Standalone APIs (not relying on product eligibility) deploy only when their own tags match the gateway.

When an API Product is undeployed or its tags or plans change such that member APIs are no longer eligible, affected APIs are undeployed on that gateway. Product deploy and update events trigger ordered resync and re-evaluation of member APIs.

### Validation and Constraints

Plan tags are validated during plan creation and update operations. Existing plans with invalid tags (created before validation was added) are not automatically corrected.

Users without the API_PRODUCT_DEFINITION:UPDATE permission see the Deployment tab controls as read-only or disabled. Users without the API_PRODUCT_PLAN:CREATE or API_PRODUCT_PLAN:UPDATE permission cannot assign tags to plans.

When you attempt to save sharding tag changes to an API Product using a restricted tag that you are not authorized to deploy to, the system displays an error message and prevents the deployment. The error notification appears at the bottom of the page, indicating that deployment is not allowed on the restricted tag.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-08.png" alt="API Product deployment page showing error message indicating deployment is not allowed on restricted tag"><figcaption></figcaption></figure>

Sharding tag changes to an API Product require explicit re-deployment to take effect on the gateway. The gateway's API Product registry index is rebuilt entirely on each product registration (no incremental updates). Concurrent product registrations are serialized per product ID.

All tag changes on API Products and plans produce audit log entries on the affected resource.
