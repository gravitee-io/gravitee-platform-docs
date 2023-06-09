---
description: >-
  This article walks through how to design and enforce policy flows using the
  legacy v2 Policy Design Studio.
---

# V2 API Policy Design Studio

{% hint style="warning" %}
Legacy version

The v2 Policy Design Studio can only be used to design flows for APIs using the v2 API definition. The v2 Policy Design studio does not support applying policies at the message level or for pub/sub use cases. If you want to design and enforce policy flows at the message level or for pub/sub use cases, please refer to the [v4 Policy Design studio documentation.](v4-api-policy-design-studio.md)
{% endhint %}

{% @arcade/embed flowId="w2EIKB74a9xXG3sXcQVI" url="https://app.arcade.software/share/w2EIKB74a9xXG3sXcQVI" fullWidth="true" %}

## Design a flow with the policy design studio

Flows can be added to existing v2 APIs. So, head to the API list by selecting **APIs** in the left-hand nav. Then, select the API for which you want to design a flow.

You'll be taken to the API's **General** details page. Select **Design** in the left-hand nav.

You're now in the **Design** section of the Policy Design Studio. Here, you can create flows by adding policies on to the request and/or response phases and targeting them by path, HTTP method(s), or using [Gravitee's Expression Language](gravitee-expression-language.md). You can create multiple flows, each with different policies and applied to different parts of your API. Flows can also be associated with specific plans or exist at the API-level as shown below:

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-09 at 2.10.06 PM.png" alt=""><figcaption><p>V2 policy design studio example</p></figcaption></figure>

### Create a flow, and add policies

First, let's create a flow. To do so, find the **Flows** section, and select the **+** icon. This will create your flow. Before adding policies to your flow, you'll need to configure the flow using the **Flow Configuration** module. You can:

* Give your flow a descriptive name. If you don't, a name will be automatically generated using the path and methods.
* Define the Operator Path and the Path.&#x20;
* Define the HTTP methods at/during which you want the flow to be executed. If you leave this empty, the flow will be executed with every HTTP method.
* Define conditions: this enables you to define specific conditions that will trigger flow execution. You will need to use the Gravitee Expression Language here. More information can be found in the [Gravitee Expression language documentation](gravitee-expression-language.md).&#x20;

Now, it's time to add policies to that flow.

To add a policy, find the policy that you want to enforce, and then drag and drop that policy onto either the request or response phase. If you add a policy at the Request phase, the policy will be enforced by the Gateway at the time of the request, before a client is given access to the API that they are trying to call. If you add a policy on the response phase, the Gateway will enforce the policy after the request is allowed, but as/before the response is allowed, depending on the policy enforced.

Once you've added your policy, you can edit that policy by selecting the policy, and using the configuration menu below the flow map. After you configure the policy, select the checkmark icon, and then Save in the pop-up to save the policy settings.

Anytime after you finish configuring a policy, or editing a flow, you'll need to redeploy your API to the Gateway for the changes to take effect. You'll see a bar appear at the top of the flow designer, that says **API out of sync, deploy your API.** Select the hyperlinked deploy your API text, and you'll be met with a pop-up that asks you to provide a label to define and describe your deployment. when you are done, select OK to deploy/redeploy your API with the new flow and policy.

#### Example: add a Rate limit policy

For example, if I wanted to limit the number of requests that a client could make using the HTTP GET method to five GET requests per second, I would:

1. Create a new flow using the steps above
2. Configure the flow to execute only at the HTTP GET method
3. Find the Rate Limit policy in the policy menu
4. Drag n' drop the Rate Limit policy onto the Request phase
5. Give my Rate Limit a description
6. Add any conditions using the Gravitee EL
7. Enable or disable non-strict mode
8. Enable or disable Rate-Limit response headers in the HTTP response
9. Define a Key that will be used to identify consumers against whom the rate limit policy should be enforced. Otherwise, you can leave this blank, and the rate limit will be applied to any consumer that has subscribed to that API's plan.
10. Set the Max requests (static) as 5
11. Set the time duration as 1
12. Set the time unit as SECONDS
13. Select the checkmark icon to save my rate limit settings.
14. Select Save.
15. Select **deploy your API**
16. In the pop-up, give the deployment a label
17. Select **OK**

At this point, the Rate Limit policy has been applied at five requests per second on the HTTP GET request.

## Configure flow mode

Gravitee offers two flow modes: **default** and **best match**. If you keep the flow mode as default, your flow will be selected and executed based on the operator defined in the flow itself (see documentation above). If you choose best match, Gravitee will choose the flow that is associated to the closest matching path.

When using **best match** mode, a best match flow is chosen if the request matches the flow. A plain text part of the path will take precedence over a path parameter.

This means, reading from left to right, each part of the path is compared, keeping the better matching. Strict equality between part of the request path and the flow path prevails over a path parameter.

For example, with these flows configured:

* `/test/:id`
* `/test/subtest`

If the request is `/test/55`, the resulting flow will be `/test/:id`. If the request is `/test/subtest`, the resulting flow will be `/test/subtest`.

To make this change, select the **Configuration** tab, and change the **Flow Mode** to either **DEFAULT** or **BEST\_MATCH** using the **Flow Mode** drop-down.&#x20;

<figure><img src="../../.gitbook/assets/Configure flow mode.png" alt=""><figcaption><p>v2 Policy Design studio: Configure flow mode</p></figcaption></figure>

## Define API properties for your API flows

If you want to retrieve and query property values with certain API calls as a part of your flow, you can configure that in the **Properties** tab. Here, you can specify properties as key-value pairs. You can specify them one by one, or toggle from **Simple** to **Expert** mode and paste property definitions into an editor in format `<key>=<value>`.

You can also configure dynamic properties by clicking **CONFIGURE DYNAMIC PROPERTIES**. Dynamic properties are fetched with a URL on a regular schedule and subsequently updated according to the details you specify.

<figure><img src="../../.gitbook/assets/API properties.png" alt=""><figcaption><p>v2 Policy Design studio: API properties</p></figcaption></figure>

When you add new policies to your API flows which include [Expression Language](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_expression\_language.html#api) fields as part of their configuration (such as the dynamic routing policy), you can retrieve and query property values with the `#properties` statement. For more details, see the [Example](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_design\_studio\_create.html#example) below.

### **Example: Dynamic properties**

For example, let's configure dynamic properties that will retrieve properties from a remote server with a URL and update them according to the details you specify. To do so, follow these steps:

1. In the **Properties** tab, select **CONFIGURE DYNAMIC PROPERTIES**.
2. Specify the details of the property:
   * `cron` schedule
   * URL
   * request headers and body to include with the call
   * JOLT transformation to perform on the response
3. Toggle **Enabled** ON.
4. Select the tick icon ![tick icon](https://docs.gravitee.io/images/icons/tick-icon.png) to save your changes.
5. Select **SAVE**.

After the first call, the resulting property is added to the list of global properties, where its value is continuously updated according to the `cron` schedule specified.\


## Add resources to your flows

Some policies support the addition of resources, which can be used for actions such as authentication and schema registry validation. Some of these policies include:

* **Cache policy**: if you using this policy, you can specify a cache resource via the **Cache** or **Cache Redis** resources
* **OAuth2 policy**: if using this policy, you can specify a **Generic OAuth2 Authorization Server** resource, a **Gravitee AM Authorization Server** resource
* **OpenID Connect - UserInfo:** if using this policy, you can specify a Keycloak Adapter resource to use Keycloack as your OpenID Connect resource.
* **Serialization & Deserialization policies**: if using the below policies, you can specify your Confluent Schema Registry. It will be used to retrieve serialization and deserialization schemas from a Confluent Schema registry
  * **JSON to Avro policy**
  * **Avro to JSON policy**
  * **JSON to Protobuf policy policy**
  * **Protobuf to JSON policy**
  * **Avro to Protobuf policy**
  * **Protobuf to Avro policy**
* **HTTP signature policies**: if using this policy, you can specify your **HTTP Authentication Provider** resource
* **Basic authentication:** if using this policy, you can specify an **LDAP Authentication Provider** resource and/or an **Inline Authentication Provider** resource to authenticate users in memory.

<figure><img src="../../.gitbook/assets/Confluent schema registry.png" alt=""><figcaption><p>Resources: Confluent Schema Registry</p></figcaption></figure>



After you create these resources, you will be able to reference them when designing policies in the **Design** tab.

## Debug mode

{% hint style="info" %}
**Debug mode limitations**

As of now, Debug mode will not work for v4 APIs. This will be delivered in a future release, but, for now, if you want to use Debug mode, you will need to create and use  APIs using the Gravitee v2 API definition.

Debug mode also does not support testing the following policies and features:

* **Rate Limit & quota policies**
* **Spike arrest**
* **Cache** - cache policy will not be testable through debug mode with in memory cache since it is created and destroyed with the api
* **IPFiltering** - Since calls are emited by the gateway itself, you will not be able to emulate a call from another IP with the debug mode (IP used to issue requests is 127.0.0.1)
* **Health-check**
* **Virtual hosts** - the first host is always selected
* **Encrypted properties** - For security reasons, you won’t be able to clear encrypted properties in debug mode (it could have an impact if you want to use them in a condition for example).
{% endhint %}

Debug mode is a tool for troubleshooting your API proxies running on Gravitee API Management. It provides detailed information about the behavior of each policy in your flows, as well as the overall execution order at runtime. With debug mode, you can:

* Understand which policies are triggered by a specific request (including Platform-level policies)
* Vizualise which policies are executed or skipped (conditional policy)
* Understand the order of execution of your policies
* Trace transformations and changes made to headers, body, and execution context
* Easily troubleshoot and find the root cause of errors, misbehaviors, or performance issues.

To debug your flows:

1. Select the Debug tab
2. Define your HTTP method, path, headers, response bodies for which flows and policies should be executed
3. Select **Send**

Gravitee will initiate a test request, and then you will be presented with a timeline that shows the order of your flows and policies.

<figure><img src="../../.gitbook/assets/Debug mode timeline.png" alt=""><figcaption><p>Debug mode timeline</p></figcaption></figure>

### Understanding different indicators for policies

Gravitee Debug mode uses different indicators to indicate the status of policies:&#x20;

* **executed** - the policy has been executed properly
* **skipped** - the policy contains a condition that has not been fulfilled. Refer to the input/output inspector for more details on the evaluation of the condition.
* **error** - an error occurred during policy execution. Refer to the input/output inspector for more details on the error.

By selecting a specific policy in the timeline, you have access to additional information regarding the input/output of the policy:

* header
* context attributes
* body

The inspector relies on 3 colors to indicate the nature of changes:

* **green** color indicates an addition
* **orange** color indicates a edit
* **red** color indicates a deletion

### Understanding and navigating the timeline

The order in which the policies appear in the timeline reflects the exact order in which they have been executed by the gateway at runtime.

Note that this order **may** differ from the order in which policies where placed in the Policy Studio during the design phase.

This is due to a performance optimization applied at runtime on the policy chain. The gateway always executes policies interacting with the HTTP Header part of the request (onRequest, onResponse) before policies interacting with the body part of the request (onRequestContent, onResponseContent).

Also, a policy may appear twice in the timeline if it interacts with both the head and the body part of the request.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/design-studio/debug-mode/debug-mode-policy-chain.png" alt=""><figcaption></figcaption></figure>

#### **Navigating the timeline**

You can scroll through the list of policies via the timeline. You can also quickly access a specific policy by selecting it in the quick access timeline.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/design-studio/debug-mode/debug-mode-timeline.png" alt=""><figcaption></figcaption></figure>

By selecting **Request Input** or **Request Output**, you can view the global transformation on your request and the difference between what has been received by the gateway and what has been sent to your backend.

By selecting **Response Input** or **Response Output**, you can view the global transformation on your response and the difference between what has been received from the backend and what has been sent back to your client app.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/design-studio/try-it/try-it-example.png" alt=""><figcaption></figcaption></figure>



\




