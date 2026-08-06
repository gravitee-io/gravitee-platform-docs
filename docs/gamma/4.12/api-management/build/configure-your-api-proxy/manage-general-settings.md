---
description: >-
  Edit the name, version, metadata, and images of an API proxy, and control its
  runtime state from the General page.
hidden: false
noIndex: false
---

# Manage general settings

The **General** page groups the identity fields, images, metadata, definition actions, and lifecycle actions of an API proxy.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **General** in the API proxy sidebar.

<!-- TODO: Screenshot of the General page of an API proxy -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-general-page.png" alt=""><figcaption><p>The General page of an API proxy</p></figcaption></figure>

{% hint style="info" %}
When the API proxy is managed by the Kubernetes operator, the page shows the banner **This API is managed by the Kubernetes operator. Configuration changes must be made in your Kubernetes manifests.** and every field is read-only.
{% endhint %}

## Edit the identity fields

The main card carries the following fields. Editing any of them reveals the **Discard** and **Save changes** buttons at the top of the page.

| Field           | Description                                                                                          |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| **Name**        | The display name of the API proxy. Required.                                                          |
| **Version**     | The version string of the API proxy, up to 32 characters. Required.                                   |
| **Description** | A free-text description of what the API proxy does.                                                   |
| **Labels**      | Free-form tags. Type a label and press Enter to add it.                                               |
| **Categories**  | Categories defined for the environment. Select one or more from the list.                             |

The **Allow in API Products** switch sits under the identity fields. When enabled, this API can be bundled into API Products for grouped consumer access. See [API product configuration reference](../configure-your-api-product/api-product-configuration-reference.md).

## Manage the API images

The **Images** panel holds two images:

* **Picture**. The avatar of the API proxy, also shown in the API proxy sidebar header.
* **Background**. The background image of the API proxy.

Both accept PNG, JPG, and SVG files up to 500 KB.

## Review the API details

The **Details** panel is read-only and lists **Owner**, **Created**, **Updated**, **Visibility**, **Lifecycle**, and **Status**.

## Export, import, or duplicate the API

An action strip under the identity fields carries the definition-level actions:

| Button        | Behavior                                                                                       |
| ------------- | ---------------------------------------------------------------------------------------------- |
| **Export**    | Opens the **Export API** panel to download the API definition.                                 |
| **Import**    | Opens the **Import API Definition** panel to replace the configuration of this API proxy from a definition file. |
| **Duplicate** | Opens the **Duplicate API** panel to create a copy of this API proxy.                          |
| **Promote**   | Not available in this release. The button is always disabled.                                  |

The **Import** and **Duplicate** buttons are disabled when the API proxy is managed by the Kubernetes operator.

## Start or stop the API

The **API Events** card alters the runtime state of the API on the gateway:

* **Stop API**. Shown while the API is started. The gateway stops accepting requests. Subscriptions are preserved.
* **Start API**. Shown while the API is stopped. Starts the API and makes it available on all connected gateways.

## Delete the API

The **Delete this API** action in the **API Events** card permanently removes the API, all plans, subscriptions, and analytics data.

The action is unavailable in the following two cases:

* The API is started. Stop it first.
* The API lifecycle is `PUBLISHED`.

In both cases the card reads **A running or published API cannot be deleted.**

To delete the API, follow these steps:

1. Click **Delete this API**.
2. In the **Delete API permanently?** dialog, type the name of the API to confirm.
3. Click **Delete permanently**.

{% hint style="warning" %}
Deletion is permanent. The dialog deletes the API along with all plans, subscriptions, and analytics data, and the action can't be undone.
{% endhint %}

## Verification

To verify the general settings are working as expected, follow these steps:

1. Edit the **Description** field.
2. Click **Save changes**.
3. Reload the page. The **Description** field shows the new text, and the **Updated** row of the **Details** panel shows the current date.

<!-- TODO: Screenshot of the Details panel showing the refreshed Updated timestamp -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-general-updated.png" alt=""><figcaption><p>The Details panel after a save</p></figcaption></figure>
