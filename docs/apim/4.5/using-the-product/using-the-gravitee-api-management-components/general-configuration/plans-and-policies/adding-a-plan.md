---
description: Configuration and usage guide for adding a plan.
---

# Adding a plan

From the Policy Studio, go to the **Plans** page.

<figure><img src="../../../../.gitbook/assets/plans_policy studio (1).png" alt=""><figcaption><p>Policy Studio</p></figcaption></figure>

> * [x] Select **Plans** from the inner sidebar

From here, we can manage all the plans and subscriptions for this API. Currently, the only plan you should see is the **Default Keyless (UNSECURED)** plan that was added by default when creating the API.

This plan is currently in the published state. Plans can be in one of four states: staging, published, deprecated, or closed.

<figure><img src="../../../../.gitbook/assets/image (1).png" alt=""><figcaption><p>Four stages of a plan</p></figcaption></figure>

<details>

<summary>Plan stages explained</summary>

**Staging:** This is the first stage of a plan, when the plan is in draft mode. You can configure your plan, but it won’t be accessible to users.

**Published:** Once your plan is ready, you can publish it to let API consumers view and subscribe to it on the APIM Portal, then consume the API through it. A published plan can still be edited.

**Deprecated (optional state):** You can deprecate a plan so it won’t be available on the APIM Portal and API consumers won’t be able to subscribe to it. Existing subscriptions remain, so deprecation doesn’t impact your existing API consumers.

**Closed:** Once a plan is closed, all associated subscriptions are closed. This cannot be undone. API consumers subscribed to the plan won’t be able to use your API.

</details>

Let's go ahead and add API security with an API key plan:

<figure><img src="../../../../.gitbook/assets/plans_api plans (1).png" alt=""><figcaption><p>API Plans page</p></figcaption></figure>

> * [x] Select **+ Add new plan** in the top right
> * [x] Select **API Key** from the drop-down menu

This opens the **General** page of the plan creation wizard. The only required configuration is to provide the plan with a name.

<figure><img src="../../../../.gitbook/assets/plans_wizard (1).png" alt=""><figcaption><p>General page of plan creation wizard</p></figcaption></figure>

> * [x] Provide a **Name** for the plan
> * [x] Scroll down to the bottom of the page and click **Next**

The next step is to configure the security settings specific to the plan type you selected. For our API key plan, we will just keep the defaults.

<figure><img src="../../../../.gitbook/assets/plans_security (1).png" alt=""><figcaption><p>Security configuration page of plan creation wizard</p></figcaption></figure>

> * [x] Leave the defaults and click **Next**

Finally, you have the option to add restriction policies directly to the plan as part of the creation process.

<figure><img src="../../../../.gitbook/assets/plans_restrictions (1).png" alt=""><figcaption><p>Restrictions page of the plan creation wizard</p></figcaption></figure>

> * [x] Leave the defaults and click **Create**

This will create the plan in the **Staging** state. To make it available to API consumers, we need to publish it.

<figure><img src="../../../../.gitbook/assets/plans_publish (1).png" alt=""><figcaption><p>Publish the API key plan</p></figcaption></figure>

> * [x] Select the **publish icon** to the far right of the plan
> * [x] Select **Publish** in the modal that pops up on the screen

This will change the API key plan's state from staging to published.

To ensure our new API key plan can't be bypassed, we need to close the keyless plan and then sync all the changes we've made to the Gateway.

<figure><img src="../../../../.gitbook/assets/plans_closing (1).png" alt=""><figcaption><p>Closing the keyless plan</p></figcaption></figure>

> * [x] Select the **delete icon** to the far right of the keyless plan
> * [x] Confirm the delete by typing in the name of the plan and then clicking **Yes, close this plan**
> * [x] Sync these changes to the Gateway by clicking **Deploy API** in the banner

## Test the plan

One more time, try sending the same request from the first part of the Quickstart Guide.

{% code overflow="wrap" %}
```sh
curl -X GET -i "https://<your-gateway-server>/<your-context-path>"
```
{% endcode %}

{% hint style="success" %}
The request will be denied with an HTTP **`401 Unauthorized`** error response status code.
{% endhint %}

The error response confirms the keyless plan was removed and all requests are now routed to the API key plan. We will need to subscribe to the API key plan and pass the proper authorization token with each request to continue to use the API.

## Next steps

You should now be starting to grasp the power, versatility, and scope of the Gravitee APIM platform.

For the final part of the Quickstart Guide, we will be diving into the Developer Portal to show how API publishers can expose and catalog their APIs, and how API consumers can create applications and subscribe to APIs in a catalog.
