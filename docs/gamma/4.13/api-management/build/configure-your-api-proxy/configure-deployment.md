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

## Assign sharding tags

The **Sharding tags** section lists the tags defined for your organization. To assign them, follow these steps:

1. Select one or more tags. Gateways advertise matching tags, and only those instances load this API definition. Each row in the dropdown shows the tag name and its description.
2. Optional: to unassign a tag, click **Remove** on its chip.
3. Click **Save changes**, or **Discard** to revert.

The **Discard** and **Save changes** buttons appear only once your selection differs from the saved value.

When no tags exist, the page reads **No sharding tags configured**. Sharding tags are managed at the organization level under the Gateway settings.

An assigned tag that no longer appears in the organization list is still shown as a chip, and it's preserved when you save.

Changing sharding tags requires the **API_DEFINITION** permission with the **UPDATE** access level. Without it, the controls are read-only or hidden.

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
