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

<figure><img src="../../../.gitbook/assets/gamma-api-deployment-configuration.png" alt="The Deployment Configuration page for an API proxy, listing three organization sharding tags as cards with a checkbox, a name, and a description"><figcaption><p>The Deployment Configuration page</p></figcaption></figure>

To edit this page, you need the `API_DEFINITION` permission with Update access. Without it, the tag checkboxes are disabled and the page reads **You do not have permission to change sharding tags for this API.**

## Assign sharding tags

The **Sharding tags** section lists the tags defined for your organization. To assign them, follow these steps:

1. Select one or more tags. Gateways advertise matching tags, and only those instances load this API definition.
2. Click **Save changes**, or **Discard** to revert.

Each organization tag is listed as a card showing its name, its description, and a checkbox. **Save changes** and **Discard** appear only once the selection differs from the saved one.

Tags assigned to the API but no longer defined for the organization aren't listed on the page, and they're kept when you save.

When no tags exist, the page reads **No sharding tags configured**. Sharding tags are managed at the organization level under the Gateway settings.

{% hint style="info" %}
When the API proxy is managed by the Kubernetes operator, the page shows **This API is managed by the Kubernetes operator. Sharding tags can only be changed from its source definition.**
{% endhint %}

## Verification

To verify the deployment configuration is working as expected, follow these steps:

1. Assign a sharding tag that one of your gateway instances advertises, and click **Save changes**.
2. Deploy the API.
3. Send a request through a gateway instance advertising the tag. The request is served. Gateway instances without a matching tag don't load the API definition.

<figure><img src="../../../.gitbook/assets/gamma-api-deployment-tags-saved.png" alt="The Deployment Configuration page after saving, with one sharding tag checked and the API marked Out of sync above an undeployed changes banner"><figcaption><p>A saved sharding tag selection</p></figcaption></figure>
