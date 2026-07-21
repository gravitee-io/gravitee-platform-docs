---
hidden: false
noIndex: false
---

# Establish consumer access
<!-- GAP-STRUCTURAL: Missing procedural content source -->

Consumer access controls how external applications discover, subscribe to, and authenticate with your API. This page covers the application model, subscription workflows, and API key management in the Gamma console.

## Applications

An **application** represents an external consumer — a frontend, a microservice, a partner integration, or an AI agent — that wants to call your API. Applications are created in the Gamma console and are the entity that subscribes to API plans.

### Create an application

1. From the Gamma console sidebar, select **API Management**.
2. Navigate to **Applications**.
3. Select **Register Application**.
4. Enter the application details:

| Field           | Description                                                      | Required |
| --------------- | ---------------------------------------------------------------- | -------- |
| **Name**        | A human-readable name to identify the application.               | Yes      |
| **Description** | Freeform text describing the application's purpose.              | Yes      |
| **Domain**      | The domain associated with this application.                     | No       |
| **Groups**      | Assign the application to one or more groups for access control. | No       |


5. Select the application type:

| Type                   | Description                                                             | Redirect URIs required |
| ---------------------- | ----------------------------------------------------------------------- | :--------------------: |
| **Simple**             | Basic application with an optional client ID. No OAuth grant types.     |           No           |
| **SPA (Browser)**      | Single-page application. Default grant type: Authorization Code.        |           Yes          |
| **Web**                | Server-side web application. Default grant type: Authorization Code.    |           Yes          |
| **Native**             | Mobile or desktop application. Default grant type: Authorization Code.  |           Yes          |
| **Backend-to-Backend** | Machine-to-machine application. Default grant type: Client Credentials. |           No           |

6. For OAuth-enabled types (SPA, Web, Native, Backend-to-Backend), configure grant types and redirect URIs as required.
7. For TLS-based authentication, upload a client certificate in the TLS settings section.
8. Select **Create** to register the application.

Also, you can create applications from **Platform → Applications** in the console sidebar. Use whichever entry point fits your workflow because subscriptions created from either location grant the same access.

### Application types

## Subscriptions

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-dfb28969984772b95c88f75e178ebbb4b486ccfd%2Fgamma-api-consumers.png?alt=media" alt="Consumers page showing subscriptions and API key management"><figcaption><p>The Consumers page lists all subscriptions for this API, with filters for status, plan, and API key. Each row shows the subscribing application, plan, security type, status, and creation date.</p></figcaption></figure>

A **subscription** binds an application to a specific **plan** on your API proxy (or API product). When a consumer calls an API protected by an API Key, JWT, OAuth2, or mTLS plan, they must hold an active subscription before the Gateway accepts their credentials.

Before creating a subscription, ensure:

* At least one plan exists on the target API and is in **Published** status (plans in **Staging** are not available for subscription).
* The consuming **application** already exists, or you create one as part of the flow below.

### Create a subscription from API Management

Use this path when you are configuring access from the API owner's perspective — for example, after creating plans on a new API proxy.

1. From the Gamma console sidebar, select **API Management**.
2. Open the target **API proxy** (or **API product**) from **API Proxies** or **API Products**.
3. In the API detail sidebar, open **Consumer Access → Consumers**.
4. Select **Create subscription**.
5. Choose the **application** that will consume the API.
6. Choose a **plan** (only published plans are listed).
7. Optionally provide a **custom API key** if the plan type is API Key and you want to specify the key value.
8. Confirm to create the subscription.

If the plan requires manual approval, the subscription stays pending until an API owner approves it. Plans configured for automatic validation are active immediately after creation.

### Create a subscription from Platform / Applications

Use this path when you start from the consumer application — for example, onboarding a partner team that already has an application registered.

1. From the Gamma console sidebar, select **Platform → Applications**.
2. **Create** a new application or open an existing one.
3. On the application detail page, start a new subscription.
4. Select the target **API** (API proxy or API product).
5. Select a **plan**.
6. Subscribe directly from the application.

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

API owners manage subscriptions from the **Consumer Access → Consumers** page on the API (or product) detail view. The following actions are available:

| Action              | From status | Result                                                                                         |
| ------------------- | ----------- | ---------------------------------------------------------------------------------------------- |
| **Approve**         | Pending     | Activates the subscription. Optionally set a custom API key, reason, start date, and end date. |
| **Reject**          | Pending     | Denies the subscription request. Optionally provide a reason.                                  |
| **Pause**           | Accepted    | Temporarily suspends the subscription. The consumer cannot make requests.                      |
| **Resume**          | Paused      | Reactivates a paused subscription.                                                             |
| **Resume (failed)** | Failed      | Reactivates a subscription in a failed consumer state.                                         |
| **Close**           | Any active  | Permanently deactivates the subscription and revokes all credentials.                          |
| **Transfer**        | Accepted    | Transfers the subscription from one plan to another.                                           |
| **Update end date** | Any active  | Sets or changes the subscription expiration date.                                              |

### Subscription origins

Subscriptions track where they were created:

| Origin         | Description                                            |
| -------------- | ------------------------------------------------------ |
| **Management** | Created through the Gamma console UI.                  |
| **Kubernetes** | Created automatically by a Kubernetes custom resource. |

## API key management

For APIs secured with an **API Key** plan, the Gamma console generates and manages API keys for each active subscription.

### API key modes

Each API Key plan operates in one of two key modes:

| Mode          | Description                                                                                                                                                                                                      |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Exclusive** | Each subscription gets its own independent API key. Keys are managed per subscription.                                                                                                                           |
| **Shared**    | All subscriptions under the same application share a single API key. When shared mode is active, per-subscription renew is disabled and a banner indicates that key management happens at the application level. |

### Manage API keys

From the API proxy **Consumer Access → Consumers** page, select a subscription to view its API keys. The key table displays:

| Column                | Description                                               |
| --------------------- | --------------------------------------------------------- |
| **Status**            | Active, revoked, or expired — indicated by a status icon. |
| **Key**               | The API key value (displayed in monospace).               |
| **Created**           | When the key was generated.                               |
| **Revoked / Expired** | When the key was revoked or when it expires.              |

**Available actions:**

| Action         | Description                                                                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Renew**      | Generate a new API key for the subscription. The previous key remains active until explicitly revoked. Not available in shared key mode.                |
| **Revoke**     | Immediately invalidate a specific API key. Takes effect at the Gateway on the next request. The subscription itself remains active if other keys exist. |
| **Set expiry** | Set an expiration date for an API key using the date picker. After the expiry date, the key is automatically invalidated.                               |

{% hint style="info" %}
For APIs secured with **JWT** or **OAuth2** plans, credentials are managed through the application's security settings (client ID / client secret) rather than through subscription-level API keys. For **Keyless** plans, no credential management is needed.
{% endhint %}

## Next steps

* [Apply security policies](apply-security-policies.md) — Add fine-grained policies that run on top of your security plans.
* [Secure your API proxy](../secure-your-api-proxy.md) — Add or change security plans before opening new subscriptions.
* [Manage applications](../../../platform-management/manage-applications.md) — View and manage applications across the platform.
