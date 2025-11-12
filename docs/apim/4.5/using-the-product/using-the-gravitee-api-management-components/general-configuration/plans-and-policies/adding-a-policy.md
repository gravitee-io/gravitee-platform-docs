# Adding a policy

### Access API

First, we need to open the API in the APIM Console. You may already have it open from the previous part of the Quickstart Guide. If not, simply head back over to the **APIs** homescreen and select the API you created.

<figure><img src="../../../../.gitbook/assets/Screenshot 2023-11-19 at 8.25.21 PM.png" alt=""><figcaption><p>APIs homescreen</p></figcaption></figure>

> * [x] Select **APIs** in the sidebar
> * [x] Select the API you created in Gateway APIs 101

### Policy Studio

Once you're back to your API's **General Info** page, go to the **Policy Studio**.&#x20;

<figure><img src="../../../../.gitbook/assets/Screenshot 2023-11-19 at 8.55.51 PM.png" alt=""><figcaption><p>API General Info page</p></figcaption></figure>

> * [x] Select **Policy Studio** from the inner sidebar

#### Creating a flow

The Policy Studio is a powerful interface for visually designing flows and applying policies to APIs. Remember, flows are a way to group policies and set conditions that determine which API requests trigger the flow.

One way to condition a flow is by plan. Every plan that is added to an API can have its own set of flows.&#x20;

You should see your **Default Keyless (UNSECURED)** plan on the left side of the Policy Studio. Additionally, you should see **Common flows**. Let's add a flow to **Common flows** to ensure our policy applies to all consumers of our API, regardless of the plan they are subscribed to.

<figure><img src="../../../../.gitbook/assets/Screenshot 2023-11-19 at 10.15.20 PM.png" alt=""><figcaption><p>Adding a flow under Common flows</p></figcaption></figure>

> * [x] Select the **+ icon** to the right of **Common flows**
> * [x] Provide a name for the flow and select **Create**

<details>

<summary>Flow conditions</summary>

We are purposefully keeping this flow very simple. However, the conditions that trigger a flow can be fine-tuned beyond assigning the flow to a plan:&#x20;

* **Operator and path:** Use this to trigger a flow based on the path of the API request. The condition is evaluated for every request and the flow is only triggered if it evaluates to `true`.
* **Methods:** Select the HTTP methods this flow applies to.
* **Expression Language Condition:** Use [Gravitee's Expression Language (EL)](docs/apim/4.5/using-the-product/managing-your-apis/gravitee-expression-language.md) to provide a custom condition. The condition is evaluated for every request and the flow is only triggered if it evaluates to `true`.

</details>

#### Adding a policy

Creating a flow opens up the flow editor. This screen will look different based on whether you are working with a traditional or message proxy API. Follow the instructions that match your API's proxy type:

<details>

<summary><strong>Traditional proxy</strong></summary>

The only phases available to traditional proxy APIs are request and response. We will be adding a policy to the response phase.

<img src="../../../../.gitbook/assets/Screenshot 2023-11-19 at 10.28.53 PM.png" alt="Add policy to the response phase of traditional proxy API" data-size="original">

* [x] Select the **+ icon** in the **Response phase**

</details>

<details>

<summary><strong>Message Proxy</strong></summary>

The phases available to message proxy APIs are request, response, publish, and subscribe. The publish and subscribe phases allow the policy to be applied at the message level. We will be adding the policy to the subscribe phase.

<img src="../../../../.gitbook/assets/Screenshot 2023-11-19 at 10.29.28 PM (1).png" alt="Add policy to the subscribe phase of a message proxy API" data-size="original">

* [x] Select the **Event messages** tab in the flow editor
* [x] Select the **+ icon** in the **Subscribe phase**

</details>

{% hint style="info" %}
The next steps are the same for both traditional and message proxy APIs.
{% endhint %}

The previous actions will open up the policy selector. We are going to add an Assign Content policy that allows us to modify the content of the payload before it reaches the API consumer.

<figure><img src="../../../../.gitbook/assets/Screenshot 2023-11-19 at 10.35.55 PM.png" alt=""><figcaption><p>Add an Assign Content policy</p></figcaption></figure>

> * [x] Click Select under the **Assign content** policy

Every policy allows you to provide a **Description** and a **Trigger condition**. Trigger conditions for policies are just like trigger conditions for flows, except these allow you to set independent conditions for each policy.&#x20;

Additionally, every policy has configuration settings specific to it. For the Assign Content policy, we can override the payload of the response or individual message by supplying a string in the **Body content** input box.

<figure><img src="../../../../.gitbook/assets/Screenshot 2023-11-19 at 10.42.39 PM.png" alt=""><figcaption><p>Configure the Assign Content policy</p></figcaption></figure>

> * [x] Type a string in the **Body content** input box
> * [x] Select **Add policy** to add it the flow
> * [x] Select **Save** in the top right of the flow editor

You should now see the Assign Content policy added to the correct phase of the flow.

#### Redeploy an API

After saving, you'll notice a banner appears at the top of the Console that says **This API is out of sync**. This means the changes you made in the Console are saved but have not yet been propagated to the Gateway.&#x20;

To ensure these changes are synced to the Gateway, the API must be redeployed.&#x20;

<figure><img src="../../../../.gitbook/assets/Screenshot 2023-11-19 at 10.50.29 PM.png" alt=""><figcaption><p>Redeploy an API</p></figcaption></figure>

> * [x] Select **Deploy API** in the top right
> * [x] Select **Deploy** in the modal that pops up on the screen

This is an essential concept to understand. API deployment is a syncing mechanism between the Console and Gateway. Changes in the Console must be synced to the Gateway for them to have any impact on the API consumers who send requests to the Gateway.

### Test your policy

Try sending the same request from the first part of the Quickstart Guide.

{% code overflow="wrap" %}
```sh
curl -X GET -i "https://<your-gateway-server>/<your-context-path>"
```
{% endcode %}

{% hint style="success" %}
Regardless of whether it's a traditional or message proxy API, the payload of the response will be set to whatever you provided as the body content of the Assign Content policy.
{% endhint %}
