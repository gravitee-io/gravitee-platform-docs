---
hidden: false
noIndex: false
description: Create, edit, publish, deprecate, and close the plans that control how consumers authenticate to an A2A Proxy. Follow the steps to manage plans from the Gamma console.
---

# Manage A2A Proxy plans

Each A2A Proxy detail view includes a **Plans** page under **Consumers**. Plans define the access policies and security requirements that consumers of the proxy must satisfy. A consumer subscribes to a published plan, and the gateway authenticates each call against that plan.

The A2A Proxy wizard creates and publishes a default plan when you create the proxy. Use the **Plans** page to add plans, and to edit, publish, deprecate, or close them.

## Open the Plans page

1. In the Gamma console, open **Agent Management**.
2. Under **Secure**, select **A2A Proxies**.
3. Select your A2A Proxy.
4. Under **Consumers**, select **Plans**.

<figure><img src="../../.gitbook/assets/gamma-a2a-proxy-plans.png" alt="The Plans page of an A2A Proxy with the Staging, Published, Deprecated, and Closed status cards, the Published card selected, and Plans selected under Consumers in the proxy sidebar"><figcaption><p>The Plans page</p></figcaption></figure>

## Read the plan list

Four cards, **Staging**, **Published**, **Deprecated**, and **Closed**, show how many plans are in each status. Select a card to list the plans in that status. When you open the page, the **Published** card is selected, or the first card that holds a plan when no plan is published.

The table lists one row per plan, with the following columns:

| Column       | Description                                                                                                                                  |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Name**     | The name of the plan, next to the icon of its security type.                                                                                 |
| **Security** | The security type: **Keyless**, **API Key**, **JWT**, **OAuth2**, or **mTLS**. |
| **Created**  | The creation date of the plan.                                                                                                               |
| **Status**   | **Staging**, **Published**, **Deprecated**, or **Closed**.                                                                                   |

Each row of a plan that isn't closed ends with an actions menu. The menu offers **Edit** for any plan that isn't closed, **Publish** for a staging plan, **Deprecate** for a published plan, and **Close** for a staging, published, or deprecated plan. The table shows 10 plans per page by default. On the **Published** card, drag a plan by its handle to change the order of the published plans.

Plans created outside Gamma, for example in the API Management console, are listed too when they use one of the five security types. Plans that use any other security type, and push plans, aren't listed.

## Plan lifecycle

A plan moves through the following statuses:

* **Staging**. Every plan starts in staging when you create it, and stays there until you publish it. Consumers can't subscribe to a staging plan.
* **Published**. Consumers can subscribe to the plan.
* **Deprecated**. The plan isn't available on the Developer Portal anymore, and consumers can't subscribe to it. Existing subscriptions are maintained.
* **Closed**. Every subscription on the plan is terminated, and the plan can't be reopened or edited.

## Create a plan

To create a plan, follow these steps:

1. Click **Create plan**, and then select a security type: **Keyless**, **API Key**, **JWT**, **OAuth2**, or **mTLS**. The **Create plan** page opens.
2. In the **General** step, enter a **Name** of up to 50 characters. The name is shown to consumers subscribing to the proxy. To approve subscription requests without a manual review, turn on **Auto validate subscription**. Click **Next**.
3. In the **Configure** step, complete the settings of the security type, and then click **Next**. A **Keyless** plan has no **Configure** step. To choose between several plans of the same type, open **Additional selection rule**, and then enter an expression in **Selection rule**.
4. Optional: In the **Restrictions** step, turn on **Rate limiting**, **Quota**, or both, and then set the limits. You set restrictions only when you create a plan. Click **Next**.
5. In the **Review** step, check the plan settings, and then click **Create plan**.

The plan is created in staging, and the **Staging** card opens. A subscription request waits for your approval unless you turned on **Auto validate subscription**.

### Configure an API Key plan

Choose how consumers send their API key:

* **Authorization: Bearer**. The consumer sends `Authorization: Bearer <api-key>`. This is the recommended mode, and the default.
* **Custom header**. The consumer sends the key in the request header you enter in **Header name**. The header name is required.
* **Query parameter**. The consumer appends the key as the `api-key` URL query parameter. This mode isn't recommended.

Turn on **Propagate key to upstream** to forward the API key to the backend service after validation.

### Configure a JWT plan

To configure a JWT plan, follow these steps:

1. Select the **Signature algorithm**: **RS256**, **RS384**, **RS512**, **HS256**, **HS384**, or **HS512**.
2. Select the **Public key resolver**: **JWKS URL**, **Given key (PEM, single key)**, or **Gateway keys (configured globally)**.
3. For **JWKS URL**, enter the **JWKS URL** that the gateway fetches the signing keys from. For **Given key**, paste the **Public key (PEM)**. **Gateway keys** needs no value.

### Configure an OAuth2 plan

An OAuth2 plan validates tokens with an OAuth2 resource declared on the proxy. Declare the resource on the **Resources** page first. See [Configure resources for your proxies](../configure-resources-for-your-proxies.md).

<figure><img src="../../.gitbook/assets/gamma-a2a-proxy-create-plan-oauth2.png" alt="The Configure OAuth 2.0 step of the Create plan page, with the OAuth2 resource field filled from the declared resource selected under Declared on this proxy, and the Extract payload and Check required scopes switches"><figcaption><p>The OAuth 2.0 configuration step</p></figcaption></figure>

To configure an OAuth2 plan, follow these steps:

1. In **OAuth2 resource**, enter the name of a resource declared on the proxy, or select one of the names listed under **Declared on this proxy**. The list includes every enabled resource of the proxy, so select one that is an OAuth2 resource. The field also accepts an Expression Language expression, which is resolved on each request.
2. Optional: turn on **Extract payload** to forward the token payload to the upstream agent.
3. Optional: turn on **Check required scopes**, and then add at least one scope under **Required scopes**. Press Enter or a comma to add a scope.

When the proxy declares no resource, the step shows **This proxy declares no resources**, with a **Manage resources** link to the **Resources** page. Creating the plan is refused until you declare a resource or enter an expression.

The name must match a resource that is declared and enabled on the proxy, both when you create the plan and when you publish it. If the resource is removed or disabled in between, publishing is refused until you restore it. An expression is resolved at request time instead, so a mistake in one surfaces only when a request reaches the gateway.

### Configure an mTLS plan

An mTLS plan has no settings of its own. Clients present an X.509 certificate during the TLS handshake. Configure the trusted certificate authorities and the certificate validation rules in the gateway-level TLS settings.

## Edit a plan

To edit a plan that isn't closed, click its name, or open its actions menu and click **Edit**. Change the settings, and then click **Save changes**. The **Edit plan** page has no **Restrictions** step, and the security type of a plan can't be changed. To use another type, create a new plan.

## Publish a plan

To publish a plan, open the actions menu of a staging plan, and then click **Publish**. A message confirms **Published** followed by the plan name, and the plan moves to the **Published** card.

Publishing is refused in the following cases, and the message shows the reason:

* The plan isn't in staging.
* The plan is an OAuth2 plan that names a resource the proxy doesn't declare.
* The plan is a Keyless plan, and the proxy already has a published or deprecated Keyless plan.

## Deprecate a plan

To deprecate a plan, follow these steps:

1. Open the actions menu of a published plan, and then click **Deprecate**.
2. In the **Deprecate plan?** dialog, click **Deprecate plan**.

A message confirms **Deprecated** followed by the plan name, and the plan moves to the **Deprecated** card.

## Close a plan

Closing a plan terminates every subscription on it, and can't be undone. To close a plan, follow these steps:

1. Open the actions menu of the plan, and then click **Close**.
2. In the **Close plan?** dialog, click **Close plan**.

A message confirms **Closed** followed by the plan name, and the plan moves to the **Closed** card. Subscriptions that were already closed or rejected are left as they are. To restore access, create a new plan, and ask the consumers to subscribe again.

## Deploy the change

Publishing or closing a plan marks the proxy out of sync. Creating, renaming, or deprecating a plan doesn't. The proxy shows the **This API is out of sync** banner until you deploy it. Click **Deploy** on the banner, optionally enter a **Deployment label**, and then click **Deploy** in the **Deploy your API** dialog.

## Verification

To verify a plan is available to consumers, follow these steps:

1. Create a plan of any type except Keyless, publish it, and then deploy the proxy.
2. Under **Consumers**, select **Subscriptions**, and then click **Create subscription**.
3. Open the **Subscription Plan** list. The plan is listed. For the steps to complete the subscription, see [Manage subscriptions](../../publish/manage-subscriptions.md).

The gateway applies a deployment within a few seconds. If a call still uses the previous plans right after you deploy, wait a moment and try again.

## Next steps

* [Manage subscriptions](../../publish/manage-subscriptions.md). Create, approve, reject, and close the subscriptions to your plans.
* [Configure resources for your proxies](../configure-resources-for-your-proxies.md). Declare the OAuth2 resource that an OAuth2 plan references.
* [Expose your agent with the A2A Proxy](../expose-agent-with-a2a-proxy.md). Choose the security type of the default plan when you create the proxy.
