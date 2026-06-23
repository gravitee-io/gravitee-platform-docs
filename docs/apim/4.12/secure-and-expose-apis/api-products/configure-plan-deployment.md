# Configure Plan Deployment

## Managing API product plans

### Assigning sharding tags to plans

Navigate to **API Product → Consumers → Plans** and select a plan to edit. Plan sharding tags are configured on the **General** step under the **Deployment** section.

1. Scroll down to the **Deployment** section on the General step. The **Sharding tags** dropdown is initially empty.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-05.png" alt="Plan configuration form showing deployment section with empty sharding tags dropdown"><figcaption></figcaption></figure>

2. Click the **Sharding tags** dropdown to view available tags. The dropdown is constrained to the intersection of the parent API Product's tags and the user's allowed tags. Tags outside this intersection are not shown or are disabled.

3. Select one or more tags from the dropdown. In the example shown, the `external` tag is selected.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-06.png" alt="Plan deployment section showing sharding tags dropdown with 'external' tag selected from available options"><figcaption></figcaption></figure>

4. Click **Save** to persist the plan tags.

Plan tags must be a subset of the API Product's tags. Tags not defined on the product cannot be added to the plan. An empty plan tag set means the plan is eligible on every gateway where the parent product is eligible. Buttons, tabs, and actions are hidden or disabled for users without the `API_PRODUCT_PLAN:CREATE` or `API_PRODUCT_PLAN:UPDATE` permission.

| Field | Description | Example |
|:------|:------------|:--------|
| **Sharding tags** | Multi-select dropdown of tags from the parent API Product that control plan deployment placement. Constrained to the intersection of API Product tags and user's allowed tags. | `external` |

### Automatic Plan Tag Cleanup

When tags are removed from an API Product, any plan tags that are no longer on the product are automatically stripped from affected plans. Expanding product tags does not retroactively add tags to existing plans. Clearing all product tags clears all plan tags on that product's plans.

**Validation error when plan tags do not match product tags:**

```
Plan tags mismatch the tags defined by the API Product
```

Details include the plan's tags and the API Product's tags for troubleshooting.

### Gateway Runtime Behavior

Sharding tags on API Products and plans follow the same filtering rules as APIs:

| Gateway Configuration | Behavior |
|:----------------------|:---------|
| No sharding tags configured | Gateway retrieves all API Products, plans, and APIs. |
| One or more sharding tags configured | Gateway only indexes entities whose tags intersect with its configured tags. Within an eligible product, only published or deprecated plans whose plan tags match the gateway are indexed. Tagless plans match any gateway that already matched the product. |

A member API is shard-eligible on a gateway if either its own sharding tags match the gateway, or it has at least one published or deprecated API Product plan indexed on that gateway, where the product's tags match the gateway (tagless product matches all gateways), and the plan's tags are empty (inherits product placement) or match the gateway (subset of product tags). Standalone APIs (not relying on product eligibility) deploy only when their own tags match the gateway.

When an API Product is undeployed or its tags or plans change such that member APIs are no longer eligible, affected APIs are undeployed on that gateway. Product deploy and update events trigger ordered resync and re-evaluation of member APIs.

### Viewing Sharding Tags in the API Products List

The API Products table includes a **Sharding Tags** column that displays sharding tag information for each product. The column shows the first tag name assigned to the product. If the product has multiple tags, a badge appears next to the first tag displaying the count of additional tags (e.g., `+2 more`). Hovering over this badge reveals a tooltip listing all assigned tags in a comma-separated format.

<figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-08.png" alt="API Products list showing product with external sharding tag and expandable tag tooltip displaying additional tags"><figcaption></figcaption></figure>

If a product has no sharding tags assigned, the **Sharding Tags** column remains empty for that product.

### Viewing Plan Tags in the Plan List

1. In the API Product left navigation, select **Consumers**.
2. Select the **Plans** tab to view the list of plans associated with the API Product.
3. In the plans table, locate the **Deploy on** column. This column displays the deployment tags assigned to each plan.

    <figure><img src="../../.gitbook/assets/apim-api-product-sharding-tags-step-07.png" alt="Plans list showing a published plan with 'shared' deployment tag in the Deploy on column"><figcaption></figcaption></figure>

Plans with deployment tags will show the tag values (e.g., `shared`) in the **Deploy on** column. Multiple tags are displayed comma-separated.

### Organization Tag Deletion

Deleting an organization-level tag removes it from all API Products and their plans in all environments. The cascade removal is performed sequentially. If the process is interrupted (e.g., product updated but plan cleanup incomplete), re-running the deletion will complete the cleanup. However, there is no rollback mechanism if a partial failure occurs.

