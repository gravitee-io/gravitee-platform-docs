# Configure Plan Deployment with Sharding Tags

## Managing API Product Plans

### Assigning Sharding Tags to Plans

Plan sharding tags refine deployment eligibility within an API Product. Plan tags must be a subset of the product's tags. An empty plan tag set means the plan is eligible on every gateway where the parent product is eligible.

{% hint style="info" %}
**Prerequisites**

* The API Product must have sharding tags assigned. See [Assigning Sharding Tags to API Products](../../configure-and-manage-the-platform/gravitee-gateway/sharding-tags.md#assigning-sharding-tags-to-api-products).
* You must have `API_PRODUCT_PLAN:CREATE` permission (for new plans) or `API_PRODUCT_PLAN:UPDATE` permission (for existing plans).
{% endhint %}

1. Navigate to **API Products → [API Product Name] → Consumers → Plans**.
2. Create a new plan or select an existing plan to edit.
3. On the **General** step, scroll down to the **Deployment** section.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-32.png" alt="Plan configuration page showing deployment section with empty sharding tags dropdown"><figcaption></figcaption></figure>

4. Click the **Sharding tags** dropdown to expand the list of available tags. The dropdown is constrained to the parent API Product's tags. Tags not defined on the product cannot be added to the plan.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-34.png" alt="Plan configuration form with deployment section showing sharding tags dropdown expanded with 'external' selected"><figcaption></figcaption></figure>

5. Select zero or more tags from the dropdown.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-35.png" alt="Plan configuration form showing General section with name field, Description field, Characteristics field, Subscriptions section, and Deployment section"><figcaption></figcaption></figure>

6. Save the plan.

    When tags are removed from the API Product, any plan tags that are no longer on the product are automatically stripped from affected plans. Expanding product tags does not retroactively add tags to existing plans. Clearing all product tags clears all plan tags on that product's plans.

### Viewing Plan Deployment Targets

The **Deploy on** column in the Plans list displays the sharding tags that determine where each plan is deployed.

1. Navigate to **API Products → [API Product Name] → Consumers → Plans**.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-27.png" alt="API Product consumers page showing subscription details with plan information"><figcaption></figcaption></figure>

2. Review the **Deploy on** column for each published plan. For example, a plan may display "shared" to indicate it is deployed to gateways tagged with "shared".

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-28.png" alt="Plans list showing published plan with 'shared' deployment target in the Deploy on column"><figcaption></figcaption></figure>

 If your API Product has multiple plans with different deployment targets, each plan will display its respective tags.

 <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-29.png" alt="Plans list showing two published plans with 'external' and 'internal' deployment targets"><figcaption></figcaption></figure>

 <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-30.png" alt="Plans list showing single published plan with 'shared' deployment target"><figcaption></figcaption></figure>

3. To view which deployment target a subscription uses, select the **Subscriptions** tab and click a subscription. The subscription details page displays the plan information, including the deployment target.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-31.png" alt="Subscription details page showing subscription metadata, API Keys section with key value, and action buttons including Transfer, Pause, Change end date, and Close subscription"><figcaption></figcaption></figure>

## Viewing API Product Sharding Tags

When an API Product contains APIs with sharding tags, you can view which APIs are accessible through each product by navigating to the product's **APIs** page. Each product displays only the APIs that match its assigned sharding tags.

For example, if you navigate to a product with the `external` sharding tag, the APIs page shows only APIs tagged as `external`:

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-24.png" alt="API Product APIs page showing a single API named 'api-c' with context path and version"><figcaption></figcaption></figure>

Similarly, navigating to a product with the `internal` sharding tag displays only APIs tagged as `internal`:

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-25.png" alt="API Product APIs page showing a single API named 'api-a' with context path and version"><figcaption></figcaption></figure>

In the API Products list, the **Sharding Tags** column displays the first tag assigned to each product. When multiple tags are assigned, a badge shows the count of additional tags (e.g., "2 more"). Hovering over the badge displays a tooltip with the comma-separated list of all tags:

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-26.png" alt="API Products list showing product with external and internal sharding tags displayed in tooltip"><figcaption></figcaption></figure>
