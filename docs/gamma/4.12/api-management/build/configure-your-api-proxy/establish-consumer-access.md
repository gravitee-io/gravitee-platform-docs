---
hidden: false
noIndex: false
---

# Establish consumer access

Consumer access controls how external applications discover, subscribe to, and authenticate with your API. This page covers the application model, subscription workflows, and API key management in the Gamma console.

## Applications

An **application** represents an external consumer—a frontend, a microservice, a partner integration, or an AI agent—that wants to call your API. Applications live at the environment level, in **Platform Management**, and are the entity that subscribes to API plans.

### Create an application

1. From the Gamma console, switch to **Platform Management**.
2. Select **Applications**.
3. Select **Register Application**.
4. Under **General**, enter the application details:

| Field           | Description                                                      | Required |
| --------------- | ---------------------------------------------------------------- | -------- |
| **Name**        | A human-readable name to identify the application.               | Yes      |
| **Description** | Freeform text describing the application's purpose.              | Yes      |
| **Domain**      | The domain associated with this application.                     | No       |
| **Groups**      | Assign the application to one or more groups for access control. | No       |

5. Under **Security**, select the application type. The types offered come from the environment's application registration settings; when only one type is enabled, its card is shown selected and cannot be changed.

| Type                   | Description                                                             | Redirect URIs required |
| ---------------------- | ----------------------------------------------------------------------- | :--------------------: |
| **Simple**             | Basic application with an optional client ID. No OAuth grant types.     |           No           |
| **SPA (Browser)**      | Single-page application. Default grant type: Authorization Code.        |           Yes          |
| **Web**                | Server-side web application. Default grant type: Authorization Code.    |           Yes          |
| **Native**             | Mobile or desktop application. Default grant type: Authorization Code.  |           Yes          |
| **Backend-to-Backend** | Machine-to-machine application. Default grant type: Client Credentials. |           No           |

6. For a **Simple** application, optionally set a free-text **Type**, for example `mobile` or `web`, and a **Client ID**. A client ID is required to subscribe to certain plan types, such as OAuth2 and JWT.
7. For OAuth-enabled types—SPA, Web, Native, and Backend-to-Backend—configure grant types and redirect URIs as required.
8. For TLS-based authentication, paste the PEM-encoded certificate into **Client Certificate (PEM Only)**. A client certificate is required to subscribe to certain mTLS plans.
9. Select **Create Application**.

## Subscriptions

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-dfb28969984772b95c88f75e178ebbb4b486ccfd%2Fgamma-api-consumers.png?alt=media" alt="Consumers page showing subscriptions and API key management"><figcaption><p>The Consumers page lists all subscriptions for this API, with filters for status, plan, and API key. Each row shows the subscribing application, plan, security type, status, and creation date.</p></figcaption></figure>

A **subscription** binds an application to a specific **plan** on your API proxy or API product. When a consumer calls an API protected by an API Key, JWT, OAuth2, or mTLS plan, they must hold an active subscription before the Gateway accepts their credentials.

Before you create a subscription, ensure the following:

* At least one plan exists on the target API and is in **Published** status. Plans in **Staging** are not available for subscription.
* The consuming **application** already exists.

### Create a subscription from API Management

Use this path when you configure access from the API owner's perspective—for example, after you create plans on a new API proxy.

1. From the Gamma console sidebar, select **API Management**.
2. From **API Proxies** or **API Products**, open the target **API proxy** or **API product**.
3. In the API detail sidebar, under **Consumer Access**, open **Consumers**.
4. Select **Create subscription**.
5. Under **Select Application**, search for and select the application that consumes the API.
6. Under **Subscription Plan**, select a plan. Only published plans are listed. If the API has no subscribable plan, the field reports that none is available and explains that keyless APIs do not require a subscription.
7. Review the **Subscription Summary**, and then select **Create subscription**.

If the plan requires manual approval, the subscription stays pending until an API owner approves it. Plans configured for automatic validation are active immediately after creation.

{% hint style="info" %}
The subscription creation panel does not accept a custom API key. To issue a subscription with a key value you choose, use a plan with manual validation and enter the value in the **Custom API key** field when you approve the request.
{% endhint %}

### Create a subscription from Platform Management

Use this path when you start from the consumer application—for example, when you onboard a partner team that already has an application registered.

1. From the Gamma console, switch to **Platform Management**, and then select **Applications**.
2. Open the application, and then select **Subscriptions** from the application sidebar.
3. Select **Create a subscription**.
4. Search for the target **API or API Product** by name and select it.
5. Select a plan to subscribe to.
6. The API key mode choice is permanent. If this is the application's first API Key subscription, choose one of the following modes:
    * **API Key**. A new API key is generated for each subscription.
    * **Shared API Key**. Every subscription uses the same API key.
7. If the plan requires a comment, enter a **Subscription message** for the API owner.
8. Select **Create subscription**.

The resulting subscription is the same as one created from the API Management Consumers page; both paths issue credentials and enforce the selected plan at the Gateway.

### Subscription lifecycle

Every subscription moves through a defined set of statuses:

| Status       | Description                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------------------- |
| **Pending**  | The subscription has been requested but not yet approved. Only appears when the plan uses manual validation.      |
| **Accepted** | The subscription is active. Credentials are valid and the consumer can call the API.                              |
| **Paused**   | The subscription is temporarily suspended. The consumer cannot call the API, but the subscription can be resumed. |
| **Resumed**  | The subscription has been reactivated after being paused. Equivalent to Accepted.                                 |
| **Rejected** | The API owner denied the subscription request. No credentials are issued.                                         |
| **Closed**   | The subscription is permanently deactivated. All associated credentials are revoked.                              |

**Subscription consumer statuses** track the runtime connection state:

| Consumer status | Description                                              |
| --------------- | -------------------------------------------------------- |
| **Started**     | The consumer is actively connected and sending requests. |
| **Stopped**     | The consumer has disconnected or is idle.                |
| **Failure**     | The consumer connection is in a failed state.            |

### Subscription actions

API owners manage subscriptions from the **Consumers** page under **Consumer Access** on the API or product detail view. Open a subscription to see the actions available for its current status:

| Action                   | Available when                       | Result                                                                                                   |
| ------------------------ | ------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| **Approve**              | Status is Pending                    | Activates the subscription. Optionally set a starting date, ending date, custom API key, and message.    |
| **Reject**               | Status is Pending                    | Denies the subscription request. A reason is required.                                                   |
| **Transfer**             | Status is Accepted                   | Moves the subscription to another plan that uses the same security type.                                 |
| **Change end date**      | Status is Accepted or Paused         | Sets or clears the subscription expiration date.                                                         |
| **Pause**                | Status is Accepted                   | Temporarily suspends the subscription. The consumer cannot make requests.                                |
| **Resume**               | Status is Paused                     | Reactivates a paused subscription.                                                                       |
| **Resume after failure** | Consumer status is Failure           | Reactivates a subscription whose consumer connection failed.                                             |
| **Close subscription**   | Status is Pending, Accepted, or Paused | Permanently closes the subscription and invalidates all associated API keys.                            |

The pause, resume, and close actions are confirmed inline on the subscription page rather than in a dialog.

{% hint style="info" %}
A subscription whose origin is **Kubernetes** cannot be modified from the console. The subscription page shows a notice instead of the action buttons; change the Kubernetes custom resource instead.
{% endhint %}

### Review and approve subscription requests

When a plan uses manual validation, every subscription request lands in **Pending** status and waits for an API owner. The **Consumers** page shows a **Pending** count alongside the total and accepted counts.

1. Under **Consumer Access**, open **Consumers** on the API proxy or API product.
2. Select the pending subscription to open its detail page.
3. To approve it, select **Approve** and complete the **Approve Subscription** dialog. All fields are optional; leave them blank to use the defaults.

| Field                     | Description                                                                                                                    |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Starting date**         | The date the subscription becomes valid. Defaults to the approval time.                                                        |
| **Ending date**           | The date the subscription expires. Cannot be earlier than the starting date.                                                   |
| **Custom API key**        | API Key plans only. Leave blank to autogenerate a key. If provided, the value must be 8–64 alphanumeric characters.            |
| **Message to subscriber** | A message returned to the consumer with the decision.                                                                          |

4. Select **Approve**. The status changes to **Accepted**, the processed and starting timestamps are stamped, and for API Key plans the key is issued.
5. To deny the request instead, select **Reject**, enter a **Reason**, and select **Reject**. The reason is mandatory—the confirmation button stays disabled until you enter one.

### Be notified of subscription events

The **Consumers** page does not announce a new request, so if you rely on manual validation, configure notifications to learn when one arrives. Notifications are configured per API proxy:

1. Open the API proxy.
2. In the API detail sidebar, under **General**, open **Notifications**.
3. Add a notification, choose a channel, and then select the events to send.

Three channels are available: **Console**, **Email**, and **Webhook**.

The subscription events correspond to the statuses and actions described above:

| Event                        | Corresponds to                                                       |
| ---------------------------- | ---------------------------------------------------------------------- |
| **New Subscription**         | A consumer requests a subscription. Enable this one for manual validation. |
| **Subscription Accepted**    | The **Approve** action.                                              |
| **Subscription Rejected**    | The **Reject** action.                                               |
| **Subscription Paused**      | The **Pause** action.                                                |
| **Subscription Resumed**     | The **Resume** action.                                               |
| **Subscription Closed**      | The **Close subscription** action.                                   |
| **Subscription Transferred** | The **Transfer** action.                                             |
| **Subscription Failed**      | The consumer status changing to **Failure**.                         |

Three further events cover API key changes: **API-Key Renewed**, **API-Key Revoked**, and **API-Key Expired**.

### Transfer a subscription to another plan

A transfer moves an accepted subscription onto a different plan without closing it or re-issuing credentials. This is useful when a consumer moves from a trial tier to a paid tier that enforces different rate limits or quotas.

1. Under **Consumer Access**, open the accepted subscription from **Consumers**.
2. Select **Transfer**.
3. In the **Transfer Subscription** dialog, open **New plan**, and then select the target plan.
4. Select **Transfer**.

The **New plan** list contains only published plans on the same API proxy or API product that use the same security type as the current plan. The current plan itself is excluded. When no such plan exists, the dialog reports that no compatible plans are available for transfer.

After a transfer the subscription keeps its status, its identifier, and its existing API keys—only the plan changes.

### Filter subscriptions

The **Consumers** page on an API proxy or API product provides the following filters:

| Filter      | Behavior                                                                                     |
| ----------- | ---------------------------------------------------------------------------------------------- |
| **Status**  | Multi-select over Pending, Accepted, Rejected, Closed, Paused, and Resumed. Defaults to all.  |
| **Plan**    | Multi-select over the published plans on the API. Defaults to all.                            |
| **API Key** | Free-text search that matches a subscription by the key value it was issued.                  |

A **Reset** control appears next to the filters once any of them is set.

An application's own **Subscriptions** page filters the same way, but by **API** rather than by plan. It opens pre-filtered to the Accepted, Paused, Pending, and Resumed statuses, so closed and rejected subscriptions are hidden. Select **Reset filters** to return to that default. Expand **Subscription status details** on that page for an inline description of each status.

### Subscription origins

Subscriptions track where they were created:

| Origin         | Description                                            |
| -------------- | ------------------------------------------------------ |
| **Management** | Created through the Gamma console UI.                  |
| **Kubernetes** | Created automatically by a Kubernetes custom resource. |

## API key management

For APIs secured with an **API Key** plan, the Gamma console generates and manages API keys for each active subscription.

### API key modes

Each application operates in one of two key modes, chosen the first time it subscribes to an API Key plan:

| Mode          | Description                                                                                                                                                                                                      |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Exclusive** | Each subscription gets its own independent API key. Keys are managed per subscription. The mode selector labels this option **API Key**.                                                                          |
| **Shared**    | All subscriptions under the same application share a single API key. When shared mode is active, per-subscription renew is disabled and a banner indicates that key management happens at the application level. |

### Manage API keys

From the API proxy **Consumers** page under **Consumer Access**, select a subscription to view its API keys. The key table displays the following columns:

| Column                | Description                                               |
| --------------------- | --------------------------------------------------------- |
| **Status**            | Active, revoked, or expired—indicated by a status icon.   |
| **Key**               | The API key value, displayed in monospace.                |
| **Created**           | When the key was generated.                               |
| **Revoked / Expired** | When the key was revoked or when it expires.              |

The following actions are available:

| Action             | Description                                                                                                                                                            |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Renew**          | Generate a new API key for the subscription. The previous key is scheduled to expire two hours later, so consumers have a window to switch. This action is not available in shared key mode. |
| **Copy key**       | Copy the key value to the clipboard.                                                                                                                                    |
| **Revoke key**     | Immediately invalidate a specific API key. The subscription itself remains active, and any other keys it holds keep working.                                            |
| **Set expiry date** | Set a date on which the key is automatically invalidated.                                                                                                              |

Renew is offered only while the subscription is accepted. The per-row actions apply only to keys that are still active: once a key is revoked or expired, its row shows no actions.

The same key table is available from the application, under **Applications** in **Platform Management**, on the application's **Subscriptions** page. There, key values are masked and the row actions are grouped under a menu, but **Renew**, **Revoke**, and **Expire** behave identically.

### Reuse a custom API key

When custom API key reuse is enabled for the environment, a key value that belongs to a revoked or expired key can be assigned to a new subscription instead of being rejected as a duplicate. This lets a consumer keep a key value it has already distributed when its subscription is replaced.

#### Enable reuse

Reuse depends on two environment settings. Both are disabled by default, so reuse does nothing until you turn them on:

| Setting                                         | Purpose                                                                                                                       |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `plan.security.apikey.allowCustom.enabled`      | Permits a key value to be supplied at all. While this is disabled, any approval that carries a **Custom API key** is rejected. |
| `plan.security.apikey.allowCustomReuse.enabled` | Permits an inactive key value to be reactivated rather than rejected as a duplicate.                                          |

The Gamma 4.12 console does not expose either setting. Read and write them through the Management API at environment scope. The endpoint accepts `POST` rather than `PUT`.

{% hint style="warning" %}
`POST` replaces the entire settings object. Any setting missing from your request body is deleted from the environment and reverts to its built-in default, so posting only the two flags resets every other environment setting. Always start from the current settings, change only the two fields, and post the whole object back.
{% endhint %}

**1. Retrieve the current settings.** Save the response to a file rather than editing it by hand from the terminal:

```bash
curl -s -u "admin:admin" \
  "http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/settings" \
  -o settings.json
```

**2. Change the two fields.** Both live under `plan.security`, each as an object with an `enabled` boolean:

```json
{
  "plan": {
    "security": {
      "customApiKey": { "enabled": true },
      "customApiKeyReuse": { "enabled": true }
    }
  }
}
```

The block above is an excerpt. `settings.json` holds the full settings object—`plan.security` also carries the `keyless`, `apikey`, `sharedApiKey`, `oauth2`, `jwt`, and `mtls` entries, alongside many other top-level blocks. Keep all of them.

Editing in place with `jq` avoids dropping anything:

```bash
jq '.plan.security.customApiKey.enabled = true |
    .plan.security.customApiKeyReuse.enabled = true' \
  settings.json > settings-updated.json
```

**3. Post the complete object back** to the same path:

```bash
curl -s -u "admin:admin" -X POST \
  -H "Content-Type: application/json" \
  --data @settings-updated.json \
  "http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/settings"
```

A successful call returns `200` with the saved settings. Re-run the `GET` to confirm both flags are `true`.

{% hint style="info" %}
The stored parameter keys and the settings payload use different names for the same two flags. The parameters are `allowCustom` and `allowCustomReuse`. The matching payload fields are `customApiKey` and `customApiKeyReuse`.
{% endhint %}

The **Custom API key** field appears in the **Approve Subscription** dialog for every API Key plan, whether or not these settings are enabled. When they are disabled, the field accepts input and the approval then fails.

#### Reuse eligibility

| Key state | Can be reused |
| --------- | ------------- |
| Revoked   | Yes           |
| Expired   | Yes           |
| Paused    | No            |
| Active    | No            |

A paused key still belongs to an active subscription, so it is never eligible for reuse.

To reuse a value, copy it from the inactive key, and then enter it in the **Custom API key** field when you approve the new pending subscription. The new subscription must belong to the same application and the same API proxy or API product as the original key.

Gamma reactivates the existing key record rather than creating a second one for the same value. The new subscription is added to the key, its expiration is aligned with the new subscription's end date, and the earlier subscription link is retained for audit history.

Approval fails with an error stating that the API key already exists in any of the following cases:

* Reuse is not enabled.
* The value belongs to a key that is still active or paused.
* The key belongs to a different application or API.

{% hint style="warning" %}
Always assign unique key values where you can. Reuse of an API key value across multiple clients or environments increases risk, because exposing that key compromises every endpoint that accepts it.
{% endhint %}

{% hint style="info" %}
For APIs secured with **JWT** or **OAuth2** plans, credentials are managed through the application's security settings—the client ID and client secret—rather than through subscription-level API keys. For **Keyless** plans, no credential management is needed.
{% endhint %}

## Next steps

* [Apply security policies](apply-security-policies.md). Add fine-grained policies that run on top of your security plans.
* [Secure your API proxy](../secure-your-api-proxy.md). Add or change security plans before opening new subscriptions.
* [Manage applications](../../../platform-management/manage-applications.md). View and manage applications across the platform.
