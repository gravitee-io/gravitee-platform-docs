# Configuring API Product Deployment with Sharding Tags

## Creating API Product Deployment Configuration

Navigate to **API Products → [Product Name] → Deployment** to assign sharding tags to an API Product. The Deployment tab controls where the product is deployed by selecting one or more organization sharding tags.

The **Sharding Tags** multi-select dropdown lists all organization-level tags in the format `[tag name] - [tag description]`. Select the tags that match the target gateway instances.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-01.png" alt="API deployment configuration page showing sharding tags dropdown with 'shared' tag selected"><figcaption></figcaption></figure>

When you save the configuration, the system validates that the current user is allowed to assign the selected tags. Unrestricted tags are available to all users. Group-restricted tags are only available to members of those groups. The configuration is persisted to the API Product definition, and a success message confirms the save.

Saving tags marks the product out of sync until the **Deploy** action is run. An "out of sync" banner appears at the top of the page indicating that the configuration has changed and requires synchronization.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-02.png" alt="API Product deployment configuration page showing empty sharding tags dropdown with out of sync warning banner"><figcaption></figcaption></figure>

If you attempt to select a group-restricted tag for which you are not a member, the system displays an error message indicating that deployment is not allowed on that tag.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-03.png" alt="API Product deployment page showing sharding tags dropdown with 'restricted-tag-api1-not-a-member' selected and an error message indicating deployment is not allowed on this tag"><figcaption></figcaption></figure>

Use the **Deploy API Product** button in the out of sync banner to synchronize the updated product (including its tags and published plans) to gateway instances. When you click the button, a confirmation dialog appears.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-05.png" alt="Deploy API Product confirmation dialog with cancel and deploy buttons"><figcaption></figcaption></figure>

The Deploy action is available to users with the **API_PRODUCT_DEFINITION:UPDATE** permission. Verifying deployment (license and compatibility check) requires the **API_PRODUCT_DEFINITION:READ** permission.

After deployment, gateway instances index the product only when the product's tags intersect with the gateway's configured sharding tags. Gateway logs show whether the product is indexed or skipped with a tag mismatch debug message.

You can select multiple sharding tags from the dropdown to deploy the product to multiple gateway groups.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-12.png" alt="Deployment configuration page showing sharding tags dropdown expanded with external, internal, and shared options all selected"><figcaption></figcaption></figure>

Users with read-only definition access see the sharding tags selector disabled. Buttons, tabs, and actions are hidden or disabled for users without the required permission.

### Field Reference

| Field | Description | Example |
|:------|:------------|:--------|
| **Sharding Tags** | Multi-select dropdown of organization-level sharding tags. Dictates where the API Product is deployed. | `eu`, `us-west` |

### Gateway Runtime Behavior

Gateway instances filter API Products and plans based on sharding tags:

| Gateway Configuration | Behavior |
|:----------------------|:---------|
| No sharding tags configured | Gateway retrieves all API Products, plans, and APIs. |
| One or more sharding tags configured | Gateway only indexes entities whose tags intersect with its configured tags. Within an eligible product, only published or deprecated plans whose plan tags match the gateway are indexed. Tagless plans match any gateway that already matched the product. |

### Member API Deployment Eligibility

A member API is shard-eligible on a gateway if either:

* Its own sharding tags match the gateway, or
* It has at least one published or deprecated API Product plan indexed on that gateway, where:
    * The product's tags match the gateway (tagless product matches all tagless gateways), and
    * The plan's tags are empty (inherits product placement) or match the gateway (subset of product tags).

Standalone APIs (not relying on product eligibility) are unchanged: they deploy only when their own tags match the gateway.

When an API Product is undeployed or its tags or plans change such that member APIs are no longer eligible, affected APIs are undeployed on that gateway. Product deploy and update events trigger ordered resync and re-evaluation of member APIs.

### Tag Change Effects

* **Product tags are the ceiling for plan tags.** Plan tags must be a subset of product tags. You cannot deploy a plan to a shard that the product itself does not cover.
* **Tagless product vs tagless plan.** A product with no tags is eligible on all tagless gateways (when deployed). A plan with no tags is eligible on all gateways where its parent product is eligible.
* **Saving tags ≠ deploying.** Updating tags on the Deployment tab marks the product out of sync until Deploy is run. An "out of sync" banner does not mean the product is undeployed on gateways.
* **Narrowing product tags auto-cleans plans.** Removing a tag from the product removes that tag from any plan that still had it. Widening product tags does not retroactively add tags to existing plans.
* **Organization tag deletion is cascading.** Deleting a tag removes it from all API Products and their plans in all environments.

All tag changes on API Products and plans produce audit log entries on the affected resource.

{% hint style="info" %}
Gateway tag configuration is required. Console tag assignment alone is not enough — each target gateway must declare the corresponding tag key in its configuration.
{% endhint %}
