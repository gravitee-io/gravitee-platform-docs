---
hidden: false
noIndex: false
description: Subscribe an application to an LLM Proxy or MCP Proxy plan and issue the credential the AI Gateway checks. Follow the steps to provision and revoke consumer access.
---

# Manage subscriptions

A subscription binds one application to one plan on an LLM Proxy or MCP Proxy. The plan's security type decides which credential the consumer presents to the AI Gateway, and the subscription is where you read the value to hand over. For an API Key plan, approving the subscription is what generates the key.

## Before you begin

A subscription needs a published plan and an application that carries the identity the plan checks.

**Publish the plan.** The subscription form lists only plans in **Published** status. When you add a plan to an LLM Proxy, it's published as part of the same action. When you add a plan to an MCP Proxy, it stays in **Staging** until you publish it:

1. Open the MCP Proxy.
2. Under **Consumer Access**, select **Plans**.
3. Open the actions menu on the plan row.
4. Select **Publish**.

**Deploy the proxy.** Publishing a plan leaves the proxy out of sync with the AI Gateway. A banner then appears on the proxy pages reporting that the change isn't live. Select **Deploy** in that banner to push it to the AI Gateway.

**Register the application.** Applications live under **Platform Management**. See [Manage applications](../../platform-management/manage-applications.md). Some plan types need more than a name on the application:

* A **JWT** or **OAuth 2.0** plan needs a client ID on the application. Without one, the subscription is refused with a message stating that a `client_id` is required.
* An **mTLS** plan needs a client certificate on the application. Without one, the subscription is refused.

Keyless plans carry no credential, so consumers of a keyless plan don't subscribe at all.

## Create a subscription

You can open access to a consumer directly, without waiting for the consumer to request it.

1. Open the LLM Proxy or MCP Proxy.
2. Under **Consumer Access**, select **Consumers**.
3. Select **Create subscription**.
4. Under **Select Application**, type part of the application name, and then select the application from the results.
5. Under **Subscription Plan**, select a plan. The list holds the published, non-keyless plans on this proxy. When the proxy has none, the field reports that no subscribable plan exists and explains that keyless plans need no subscription.
6. Review **Subscription Summary**, and then select **Create subscription**.

Where the new subscription lands depends on the plan:

| Plan validation | Result |
| --------------- | ------ |
| Manual | The subscription is created in **Pending** status and waits for your decision. Plans you create on an LLM Proxy always use manual validation. |
| Automatic | The subscription is accepted as soon as it's created, and an API Key plan issues its key in the same step. On an MCP Proxy plan, **Auto validate subscription** sets this. It's off by default, and it's forced on for a keyless plan. |

<!-- TODO: Screenshot of the Consumers page on an LLM Proxy, showing the subscriptions table and the Create subscription button -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-412-aim-consumers.png" alt=""><figcaption><p>The Consumers page lists the applications subscribed to this proxy's plans.</p></figcaption></figure>

## Approve or reject a request

The **Consumers** page lists the pending, accepted, and paused subscriptions on the proxy, with a column each for the application, the plan, the status, and the creation date. Rejected and closed subscriptions drop off this list.

1. Under **Consumer Access**, select **Consumers**.
2. Select the application name on the subscription row.
3. Select **Approve** to grant access, or **Reject** to deny it. Both buttons appear only while the subscription is pending.

Both actions show a confirmation message and refresh the subscription. Approving moves the subscription to **Accepted** and stamps the activation time on the **Subscription details** card. For an API Key plan, approving also generates the key.

The console sends no start date, end date, or custom key value with the approval. The subscription starts at the moment you approve it and runs until you close it.

## Find the credential issued to a consumer

Open a subscription from the **Consumers** page to read its **Credentials** card. What the card holds depends on the plan's security type.

| Plan type | Available on | Credentials card |
| --------- | ------------ | ---------------- |
| **API Key** | LLM Proxy, MCP Proxy | How the consumer sends the key, plus each key value with a copy control. A revoked key is badged **Revoked**. While the subscription holds no key, the card states that the key is generated when the subscription is accepted. |
| **JWT** | LLM Proxy | The client ID the subscription was created with. |
| **OAuth 2.0** | LLM Proxy | The client ID the subscription was created with. |
| **OAuth 2.0 (Gravitee AM)** | MCP Proxy | A pointer to the subscribing application, where the credentials for the Gravitee Access Management integration are held. |
| **mTLS** | LLM Proxy | The client certificate the subscription was created with. |

For an API Key plan, the card also states where the AI Gateway reads the key, which follows the delivery mode chosen on the plan:

| Delivery mode | What the consumer sends |
| ------------- | ----------------------- |
| **Authorization: Bearer** | `Authorization: Bearer <api-key>`. The AI Gateway reads the key from that header only. |
| **Custom header** | The header named on the plan. The AI Gateway falls back to the `api-key` query parameter when that header is absent. |
| **Query parameter** | The `api-key` query parameter. The AI Gateway reads the key from that parameter only. |

<!-- TODO: Screenshot of a subscription detail page showing the Subscription details card and the Credentials card with an issued API key -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-412-aim-subscription-credentials.png" alt=""><figcaption><p>The Credentials card holds the key or client identity issued to the consumer.</p></figcaption></figure>

## Close a subscription

Closing ends a consumer's access to the proxy. The actions on a subscription cover pending and accepted subscriptions only, so a closed subscription can't be reopened from this page.

1. Under **Consumer Access**, select **Consumers**.
2. Select the application name on an accepted subscription.
3. Select **Close subscription**.
4. Confirm in the dialog.

Closing an accepted subscription revokes the API keys attached to it, and the subscription leaves the **Consumers** list. To deny access before you ever grant it, reject the pending request instead.

## Next steps

* [Publish your LLM Proxy](publish-your-llm-proxy.md). Deploy an LLM Proxy so consumers can send prompts to its context path.
* [Manage applications](../../platform-management/manage-applications.md). Register and maintain the applications that subscribe to your plans.
* [Expose your agent with the A2A Proxy](../build/expose-agent-with-a2a-proxy.md). Open an A2A Proxy to a client.
