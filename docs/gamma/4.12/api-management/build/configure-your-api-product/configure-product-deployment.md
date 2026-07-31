---
hidden: false
noIndex: false
---

# Configure product deployment

The **Deployment** tab controls where an API Product runs. You assign sharding tags to the product, and only Gateway instances that advertise a matching tag load it. The tab also surfaces the product's Gateway sync state.

## Prerequisites

Sharding tags are defined once at the organization level and then assigned to individual products. Before you can assign a tag to an API Product, the tag must already exist for your organization.

If no tags are defined, the **Deployment** tab shows **No sharding tags configured** and explains that sharding tags are managed at the organization level under Gateway settings.

{% hint style="info" %}
The Gamma **Settings** page is a placeholder in this release and does not yet manage sharding tags. Organization-level tags must be created outside the Gamma API Management module.
{% endhint %}

## Open the Deployment tab

1. From the Gamma console sidebar, select **API Management**.
2. From the module navigation, select **API Products**.
3. Select the product you want to configure.
4. In the product detail sidebar, under **OPERATIONS**, select **Deployment**.

The page opens on **Deployment Configuration**.

## Assign sharding tags to a product

The **Sharding tags** card lists every organization-level tag as a selectable card with a checkbox. Each card shows the tag name, followed by its description when one is set.

1. Select the checkbox for each tag that matches the Gateway instances you want to run this product on. You can select more than one.
2. Select **Save changes**.

**Save changes** and **Discard** only appear once your selection differs from what is currently saved. **Discard** returns the selection to the saved value without contacting the server.

On success, the console confirms with a **Deployment configuration saved** notification. If the save is rejected, the console shows a **Failed to save changes.** notification and the selection is left as you set it.

A product with no tags selected shows **—** in the **Sharding Tags** column of the API Products list.

{% hint style="info" %}
A tag assigned in the console is only half of the configuration. Each target Gateway must also declare the corresponding tag in its own configuration before it loads the product.
{% endhint %}

### Permissions

To change sharding tags, you need update permission on the product definition. Without it, the tag checkboxes are disabled and the page shows the message **You do not have permission to change sharding tags for this API Product.** The tags themselves remain visible.

## Deployment state

Gamma tracks whether the product definition you see in the console matches what the Gateway has. The state appears in the following two places:

* As a badge directly under the product name in the product detail sidebar header.
* As the **Gateway sync** row on the product **General** page.

The badge has the following meanings:

| Badge           | Meaning                                                            |
| --------------- | ------------------------------------------------------------------ |
| **Synced**      | The product definition matches what was last sent to the Gateway.  |
| **Out of sync** | The product has been modified since the last deployment.           |

When no state is available for the product, the **Gateway sync** row shows **—** and the sidebar header shows no badge at all.

{% hint style="info" %}
The API Product screens do not provide a deploy or redeploy action in this release. A product showing **Out of sync** cannot be redeployed from the product detail pages. Deployment is available through the Management API. See [Manage API products with the Management API](manage-api-products-with-the-management-api.md).
{% endhint %}

## Sharding tags and product plans

A product's tags are the ceiling for its plans' tags. In the plan wizard's **General** step, the **Sharding tags** selector disables any tag that is not part of the parent API Product's tags. As a result, a plan can never be placed on a shard the product itself does not cover. Tags you are not allowed to use are disabled as well.

The **Sharding tags** field only appears in the plan wizard when organization-level tags exist.

## Next steps

* [Manage product APIs](manage-product-apis.md). Attach and detach API proxies from the product.
* [Secure your API proxy](../secure-your-api-proxy.md). Create plans for your product.
