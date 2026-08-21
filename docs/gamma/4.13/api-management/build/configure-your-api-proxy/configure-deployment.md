---
hidden: false
noIndex: false
description: Choose which API Gateway instances load an API definition by assigning sharding tags. Follow the steps on the Deployment Configuration page.
---

# Configure deployment

The **Deployment Configuration** page controls where this API is deployed on the gateway mesh. Only gateway instances advertising matching sharding tags load this API definition.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **Deployment** in the API proxy sidebar.
4. Click **Configuration**.

<!-- TODO: Screenshot of the Deployment Configuration page with sharding tags -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-deployment-configuration.png" alt=""><figcaption><p>The Deployment Configuration page</p></figcaption></figure>

Editing this page requires the API_DEFINITION permission with Update access. Without it, the sharding tag picker is disabled and reads **You do not have permission to change sharding tags for this API.**

## Assign sharding tags

The **Sharding tags** section lists the tags defined for your organization. To assign them, follow these steps:

1. Select one or more tags. Gateways advertise matching tags, and only those instances load this API definition.
2. Click **Save changes**, or **Discard** to revert.

The **Sharding tags** field reads **Select tags…** until you make a selection. If no entry matches your search, the list reads **No matching tags**. Optional: remove a tag by clicking **Remove {tag name}** on its chip before you save. **Save changes** and **Discard** appear only once the selection differs from the saved one.

Tags already assigned to the API but no longer listed for the organization are still shown as chips, and they're kept when you save.

When no tags exist, the page reads **No sharding tags configured**. Sharding tags are managed at the organization level under the Gateway settings.

If the API definition can't be read, the page reads **Failed to load sharding tags. Please try again.** instead of showing an editable picker.

{% hint style="info" %}
When the API proxy is managed by the Kubernetes operator, the page shows **This API is managed by the Kubernetes operator. Sharding tags can only be changed from its source definition.**
{% endhint %}

## Verification

To verify the deployment configuration is working as expected, follow these steps:

1. Assign a sharding tag that one of your gateway instances advertises, and click **Save changes**.
2. Deploy the API.
3. Send a request through a gateway instance advertising the tag. The request is served. Gateway instances without a matching tag don't load the API definition.

<!-- TODO: Screenshot of the saved sharding tag selection -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-deployment-tags-saved.png" alt=""><figcaption><p>A saved sharding tag selection</p></figcaption></figure>
