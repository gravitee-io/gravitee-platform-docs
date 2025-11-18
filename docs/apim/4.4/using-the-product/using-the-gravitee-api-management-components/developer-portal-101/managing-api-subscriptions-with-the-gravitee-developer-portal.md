# Managing API subscriptions with the Gravitee Developer Portal

## Managing subscriptions

It's time to resume our previous role as an API publisher. Let's return to the APIM Console to manage the subscription request we just submitted. It should have come through as a new **Task**.

<figure><img src="../../../../4.0/.gitbook/assets/DP_view (1).png" alt=""><figcaption><p>View your tasks in the Console</p></figcaption></figure>

> * [x] Select your profile in the top right
> * [x] Select **Task** from the drop-down menu

This will bring you to a list of all your current tasks, which should consist of a subscription request from the application to your API you just created.

<figure><img src="../../../../4.0/.gitbook/assets/DP_list (1).png" alt=""><figcaption><p>A list of your tasks in the Console</p></figcaption></figure>

> * [x] Click Validate under the subscription request

This will not immediately validate the request, but instead navigate you to the part of the Console where you can validate the subscription.

{% hint style="info" %}
This was essentially a shortcut to our API's subscription screen. You can always navigate here by selecting your API, selecting **Plans** from the inner sidebar, and then selecting the **Subscriptions** tab.
{% endhint %}

Here, you can see all the metadata (e.g., user, application, plan, etc.) for the request and decide on an action. Once you validate, you will have additional options for managing the subscription.

<figure><img src="../../../../4.0/.gitbook/assets/DP_sub val (1).png" alt=""><figcaption><p>Subscription validation screen</p></figcaption></figure>

> * [x] Click **Validate subscription**
> * [x] Leave the defaults and click **Validate** in the modal

The subscription is now active! However, as the API publisher, you have a number of different options for managing this subscription:

* **Transfer:** Move the subscription to a different plan
* **Pause:** Temporarily suspend the subscription. Be careful with this, because the consumer's API requests will fail when their subscription is paused.
* **Change end date:** Change or set the expiration date on the provisioned API keys.
* **Close:** Permanently end the subscription. The API consumer will need to subscribe again to have access to this API.

At the bottom of the screen, you will see the API key that has been randomly generated and provisioned for this user. APIM allows you to customize this behavior, including providing your own API key and allowing the API consumer to share API keys between subscriptions.

For now, simply copy that API key to your clipboard.

<figure><img src="../../../../4.0/.gitbook/assets/DP_management (1).png" alt=""><figcaption><p>Subscription management</p></figcaption></figure>

> * [x] Select the **Copy to clipboard** icon next to the API key
