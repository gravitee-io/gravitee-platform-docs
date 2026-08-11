---
hidden: false
noIndex: false
description: Define static or dynamic key/value properties that policies read at runtime through the Expression Language. Follow the steps to add and encrypt them.
---

# Configure API properties

The **API Properties** page defines key/value pairs that policies read at runtime through the Expression Language, with the syntax `{#api.properties['key']}`. Properties externalize configuration, for example timeouts, feature flags, and secrets, so you change values without redeploying the API.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **API Properties** in the API proxy sidebar.

<!-- TODO: Screenshot of the API Properties page with defined properties -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-properties-page.png" alt=""><figcaption><p>The API Properties page</p></figcaption></figure>

Once properties exist, the page shows three counters, **Total properties**, **Encrypted**, and `Dynamic (auto-synced)`, above the **Defined properties** table. The table lists each property's **Key**, **Value**, and **Characteristics**, and a search field filters properties by key.

## Add a property

To add a property, follow these steps:

1. Click **Add property**.
2. In the **Add property** panel, enter a **Key**. Keys are unique per API. Reusing an existing key shows the error **A property with this key already exists.**
3. Enter a **Value**.
4. Optional: turn on **Encrypt on save** to store the value encrypted.
5. Click **Add property**.

{% hint style="warning" %}
An encrypted value is encrypted on save and can't be retrieved later. The table shows it as dots, and its **Characteristics** column reads **Encrypted**.
{% endhint %}

## Manage existing properties

The actions menu of each property row offers the following actions:

* **Edit value**. Change the value of an unencrypted property.
* **Encrypt value**. Mark an unencrypted property for encryption. Its badge switches to **Encrypt on save**, and the value is encrypted when the change is saved.
* **Renew encryption**. For an encrypted property, enter a new plaintext value that's re-encrypted on save.
* **Delete**. Remove the property.

A property synced from a dynamic source carries the **Dynamic** badge, and its only action is **Remove (re-added on next sync)**: the next scheduled sync recreates it.

## Import properties in bulk

To import a list of properties, follow these steps:

1. Click **Import**.
2. In the **Import properties** panel, paste the property list in `KEY=value` or `KEY="value"` format, one property per line.
3. Click the import button to merge the list.

The merge behaves differently per existing key:

* A key that already exists unencrypted is overwritten with the imported value.
* A key that already exists encrypted is skipped, and the panel lists it under **Conflicts with existing properties**.

Parsing problems appear under **Errors in properties**, and the import stays disabled until they're fixed.

## Sync properties dynamically

The **Manage dynamically** button opens the **Dynamic properties** screen, which polls an external HTTP endpoint on a cron schedule and refreshes the property list automatically.

The form carries the following main settings:

| Setting                                | Description                                                                                                        |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Enable dynamic properties**          | When enabled, the gateway polls the configured HTTP endpoint on the cron schedule and refreshes the property list. |
| Schedule                               | A cron expression that sets the polling frequency.                                                                 |
| Method and URL                         | The HTTP method (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, or `OPTIONS`) and the endpoint URL to poll.      |
| **Request headers**                    | Headers sent with the poll request.                                                                                |
| **Request body**                       | Body sent with the poll request. Only applicable to the `POST`, `PUT`, and `PATCH` methods.                        |
| **JOLT transformation specification**  | A JOLT spec that transforms the upstream JSON response into `[{"key":"k","value":"v"}]` format.                    |

The form also carries HTTP client options (timeouts, keep-alive, compression, and redirect behavior), proxy settings, and SSL settings for the connection to the polled endpoint.

{% hint style="info" %}
When the API proxy is managed by the Kubernetes operator, the dynamic property settings are read-only.
{% endhint %}

## Verification

To verify a property is working as expected, follow these steps:

1. Add a property, for example `backend.timeout` with the value `5000`.
2. Reference it from a policy configuration field with `{#api.properties['backend.timeout']}`.
3. Deploy the API. The policy resolves the property value at runtime.

<!-- TODO: Screenshot of a policy field referencing an API property -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-properties-el.png" alt=""><figcaption><p>A policy field referencing an API property</p></figcaption></figure>
