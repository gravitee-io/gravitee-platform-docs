---
description: >-
  This article walks through how to design and enforce policy flows using the
  legacy v2 Policy Studio.
---

# v2 API Policy Studio

{% hint style="warning" %}
**Legacy version**

The v2 Policy Studio can only be used to design flows for APIs using the v2 API definition. The v2 Policy Studio does not support applying policies at the message level or for pub/sub use cases. If you want to design and enforce policy flows at the message level or for pub/sub use cases, please refer to the [v4 Policy Studio](v4-api-policy-studio.md) documentation.
{% endhint %}

## Introduction

The v2 Policy Studio is broken into the following sections:

* **Design:** Manage all flows associated with your Gateway API
* **Configuration:** Modify settings around flow execution
* **Properties:** Define key-value pairs at the API level. These properties are read-only during the Gateway's execution of an API transaction.
* **Resources:** Configure global resources to support your Gateway API's flows
* **Debug:** Test and troubleshoot your Gateway APIs

{% @arcade/embed flowid="kApsIRtoWrfIFRzd7DQj" url="https://app.arcade.software/share/kApsIRtoWrfIFRzd7DQj" %}

## Design

Flows can be added to existing v2 APIs, which are accessed by selecting **APIs** in the left-hand nav. Next, select the API for which you want to design a flow. You'll be taken to the API's **General** details page. Select **Design** in the left-hand nav.

You're now in the **Design** section of the Policy Studio. Here, you can create flows by adding policies to the request and/or response phases and target them by path, HTTP method(s), or via [Gravitee's Expression Language](../gravitee-expression-language.md). You can create multiple flows, each with different policies and applied to different parts of an API. Flows can also be associated with specific plans or exist at the API-level as shown below:

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-09 at 2.10.06 PM.png" alt=""><figcaption><p>v2 Policy Studio example</p></figcaption></figure>

The sample Gateway API shown above has three plans: Keyless Plan, Premium API Key Plan, and Premium JWT Plan. Flows can be set to target subscribers of any of these three plans, or they can target all users of the API when placed under the **Flows** section, e.g., the Assign Metrics Flow.

### Create a flow and add policies

As an example, let's create a flow that targets all users of the API.

First, find the **Flows** section and select the **+** icon to create a flow. Before adding policies to the flow, you'll need to configure the flow using the **Flow Configuration** module with the options shown below.

<figure><img src="../../.gitbook/assets/v2_flow_config.png" alt=""><figcaption><p>Sample flow configuration</p></figcaption></figure>

* **Name:** Give your flow a descriptive name. If you don't, a name will be automatically generated using the path and methods.
* **Operator path:** For the provided **Path**, apply this flow to requests with a path that **Equals** or **Starts with** the same path.
* **Path:** Define the path to use in conjunction with the **Operator path** to determine if this flow should be applied.
* **Methods:** Define the HTTP methods for which you want the flow to be executed. If you leave this empty, the flow will be executed for every HTTP method, assuming the other conditions are met.
* **Conditions:** Define specific conditions that will trigger flow execution using Gravitee's Expression Language (EL).

Now, it's time to add policies to that flow.

To add a policy to the flow, drag-and-drop the policy that you want to enforce onto either the request or response phase. If you add a policy on the request phase, the policy will be enforced by the Gateway at the time of the request, before a client is given access to the API that they are trying to call. If you add a policy on the response phase, the Gateway will enforce the policy after the request is allowed, but before the response is returned to the client.

Once you've added your policy, you can edit that policy by selecting the policy and using the configuration menu below the flow map. After you configure the policy, select the **checkmark icon**, and then **Save** in the pop-up to save the policy settings.

<figure><img src="../../.gitbook/assets/v2_policy_config.png" alt=""><figcaption><p>Configure a policy</p></figcaption></figure>

Whenever you edit a flow, like when you configure a policy, you'll need to redeploy your API to the Gateway for the changes to take effect. You'll see a bar appear at the top of the flow designer that says **API out of sync, deploy your API.** Select the hyperlinked **deploy your API** text, and you'll be met with a modal that asks you to provide a label to define and describe your deployment. When you are done, select **OK** to deploy/redeploy your API with the new flow and policy.

<figure><img src="../../.gitbook/assets/redeploy_api.png" alt=""><figcaption><p>Redeploy API after configuring flow</p></figcaption></figure>

#### Example: Add a Rate Limit policy

For example, to limit the number of requests that a client can make using the HTTP GET method to five GET requests per second:

1. Create a new flow via the steps above
2. Configure the flow to execute only at the HTTP GET method
3. Find the Rate Limit policy in the policy menu
4. Drag-and-drop the Rate Limit policy onto the request phase
5. Give the rate limit a description
6. Add conditions using the Gravitee EL
7. Enable or disable non-strict mode
8. Enable or disable rate limit response headers in the HTTP response
9. Define a Key that will be used to identify consumers against whom the Rate Limit policy should be enforced. If this is left blank, and rate limit will be applied to any consumer that has subscribed to the API's plan.
10. Set the max requests (static) as 5
11. Set the time duration as 1
12. Set the time unit as SECONDS
13. Select the checkmark icon to save the rate limit settings
14. Click **Save**
15. Select **deploy your API**
16. In the modal, give the deployment a label
17. Select **OK**

At this point, the Rate Limit policy has been applied at five requests per second on the HTTP GET request.

## Configure flow mode

Gravitee offers two flow modes: **default** and **best match**. If you keep the flow mode as default, execution of each flow is determined independently based on the **Operator path** defined in the flow itself (see [documentation above](v2-api-policy-studio.md#create-a-flow-and-add-policies)). Default mode allows for the execution of multiple flows.

However, if you select best match, the Gateway will choose a single flow with the closest match to the path of the API request. A plain text part of the path will take precedence over a path parameter, which means, reading from left to right, each part of the path is compared and the best matching is kept. Strict equality between part of the request path and the flow path prevails over a path parameter.

For example, with these flows configured:

* `/test/:id`
* `/test/subtest`

If the request is `/test/55`, the resulting flow will be `/test/:id`. If the request is `/test/subtest`, the resulting flow will be `/test/subtest`.

To modify the flow mode, select the **Configuration** tab and change the **Flow Mode** to either **DEFAULT** or **BEST\_MATCH** using the **Flow Mode** drop-down.

<figure><img src="../../.gitbook/assets/Configure flow mode.png" alt=""><figcaption><p>v2 Policy Studio: Configure flow mode</p></figcaption></figure>

## API properties

Properties allow you to define key-value pairs at the Gateway API level. These properties are read-only during the Gateway's execution of an API transaction and can be accessed using Gravitee's Expression Language (EL) with the `#properties` statement inside of the flows.

API properties are set and configured in the **Properties** tab. You can specify properties one by one, or toggle from **Simple** to **Expert** mode and paste property definitions into an editor in the format `<key>=<value>`.

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-12 at 7.11.41 AM.png" alt=""><figcaption><p>API properties expert format</p></figcaption></figure>

### Encryption

You can easily encrypt API properties by enabling the **Encrypted** toggle next to the property. The value will remain unencrypted and editable until you save your changes. Once you select **Save**, you can no longer edit, modify, or view the value.

{% hint style="danger" %}
Encrypted values can still be used by API policies (under the **Design** tab) and **APIM Gateway will automatically decrypt these values**. Pay special attention to how you use encrypted data in policies.
{% endhint %}

Before using encryption, you’ll need to reset the secret key. The method of encryption used for API properties is based on the default secret key in the `gravitee.yml` config file which you must override to ensure proper security.

{% code title="gravitee.yml" %}
```yaml
# Encrypt API properties using this secret:
api:
  properties:
    encryption:
         secret: vvLJ4Q8Khvv9tm2tIPdkGEdmgKUruAL6
 to provide the best security available.
```
{% endcode %}

{% hint style="warning" %}
The secret must be **32 bytes in length.**
{% endhint %}

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-12 at 7.45.12 AM.png" alt=""><figcaption><p>Encrypted API property</p></figcaption></figure>

### **Dynamic properties**

You can also configure dynamic properties by clicking **CONFIGURE DYNAMIC PROPERTIES**. Dynamic properties are fetched from a remote server on a regular schedule and subsequently updated according to the details you specify.

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-12 at 7.15.36 AM.png" alt=""><figcaption><p>Dynamic properties configuration screen</p></figcaption></figure>

To configure dynamic properties:

1. In the **Properties** tab, select **CONFIGURE DYNAMIC PROPERTIES**
2. Specify the details of the property:
   * `cron` schedule
   * HTTP method(s)
   * URL
   * Request headers and body to include with the call
   * JOLT transformation to perform on the response
3. Toggle **Enabled** ON
4. Select the tick icon ![tick icon](https://docs.gravitee.io/images/icons/tick-icon.png) to save your changes
5. Select **SAVE**

After the first call, the resulting property is added to the list of global properties, where its value is continuously updated according to the `cron` schedule specified.

### Example

In this example, we want our Gateway API to query our shop databases to check their stock levels. We will dynamically reroute any API call containing a shop ID to its associated URL.

The first step is to define a list of properties for the shops, with each unique shop ID as the key and the URL of the shop as the value.

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-12 at 7.20.12 AM.png" alt=""><figcaption><p>Add API properties</p></figcaption></figure>

We then configure a dynamic routing policy for the API with a routing rule which builds a new URL dynamically through property matching. The URL is created with a `#properties` statement which matches properties returned by querying the request header containing the shop ID.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/design-studio/dynamic-routing-properties.png" alt=""><figcaption><p>Add dynamic routing policy based on API property</p></figcaption></figure>

If the ID in the request header matches the key of one of the properties, it is replaced with the URL. The dynamic routing policy then reroutes the API call to the URL.

{% hint style="info" %}
**Dictionaries vs API properties**

The list of shop IDs and URLs could also be maintained using a dictionary, for example, in organizations where the administrator maintains this information independently of the API creation process or if the list needs to be available to multiple APIs. For more details, see "configure dictionaries" in the Configuration Guide.
{% endhint %}

## Resources

Some policies support the addition of resources, which can be used for actions such as authentication and schema registry validation. Policies supporting resources include:

* **Cache policy**: Specify a cache resource via the Cache or Cache Redis resources
* **OAuth2 policy**: Specify a Generic OAuth2 Authorization Server resource or a Gravitee AM Authorization Server resource
* **OpenID Connect - UserInfo:** Specify a Keycloak Adapter resource to use Keycloak as your OpenID Connect resource
* **Serialization & deserialization policies**: Specify your Confluent Schema Registry to retrieve serialization and deserialization schemas from a Confluent Schema registry
  * Avro <> JSON policy
* **HTTP signature policies**: Specify your HTTP Authentication Provider resource
* **Basic authentication:** Specify an LDAP Authentication Provider resource and/or an Inline Authentication Provider resource to authenticate users in memory

<figure><img src="../../.gitbook/assets/Confluent schema registry.png" alt=""><figcaption><p>Resources: Confluent Schema Registry</p></figcaption></figure>

After you create these resources, you will be able to reference them when designing policies in the **Design** tab.

{% hint style="info" %}
Global resources are globally available to all flows associated with the Gateway API. However, they will not be available to other Gateway APIs.
{% endhint %}

## Debug mode

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, Debug mode is an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../overview/ee-vs-oss/README.md)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

{% hint style="info" %}
**Debug mode limitations**

Debug mode does not work for v4 APIs. To take advantage of Debug mode, create and use APIs via the Gravitee v2 API definition.

Debug mode also does not support testing the following policies and features:

* **Rate Limit & quota policies**
* **Spike arrest**
* **Cache:** Cache policy is not testable via Debug mode with in-memory cache since it is created and destroyed with the API
* **IPFiltering:** As calls are emitted by the Gateway itself, you are not able to emulate a call from another IP via Debug mode (IP used to issue requests is 127.0.0.1)
* **Health-check**
* **Virtual hosts:** The first host is always selected
* **Encrypted properties** - For security reasons, you are not able to clear encrypted properties in Debug mode (e.g., this could impact use in a condition)
{% endhint %}

Debug mode is a tool for troubleshooting your Gateway APIs running on Gravitee API Management. It provides detailed information about the behavior of each policy in your flows, as well as the overall execution order at runtime. With Debug mode, you can:

* Understand which policies are triggered by a specific request (including platform-level policies)
* Visualize which policies are executed or skipped (conditional policy)
* Understand the order of execution of your policies
* Trace transformations and changes made to headers, body, and execution context
* Easily troubleshoot and root-cause errors, misbehaviors, or performance issues

To debug your flows:

1. Select the **Debug** tab
2. Define the HTTP method, path, headers, and request bodies for the debug request
3. Select **Send**

Gravitee will initiate a test request, and then you will be presented with a timeline that shows the order of your flows and policies.

<figure><img src="../../.gitbook/assets/Debug mode timeline.png" alt=""><figcaption><p>Debug mode timeline</p></figcaption></figure>

### Understanding different indicators for policies

Gravitee Debug mode uses different indicators to indicate the status of policies:

* **Executed**: The policy has been executed properly
* **Skipped:** The policy contains a condition that has not been fulfilled. Refer to the input/output inspector for more details on the evaluation of the condition.
* **Error:** An error occurred during policy execution. Refer to the input/output inspector for more details on the error.

Select a specific policy in the timeline to access additional information regarding the input/output of the policy:

* Header
* Context attributes
* Body

The inspector relies on 3 colors to indicate the nature of changes:

* **Green:** Indicates an addition
* **Orange:** Indicates an edit
* **Red:** Indicates a deletion

### Understanding the timeline

The order in which the policies appear in the timeline reflects the exact order in which they have been executed by the Gateway at runtime.

Note that this order may differ from the order in which policies were placed in the Policy Studio during the design phase due to a performance optimization applied at runtime on the policy chain.

The Gateway always executes policies interacting with the HTTP header part of the request (onRequest, onResponse) before policies interacting with the body part of the request (onRequestContent, onResponseContent). A policy may appear twice in the timeline if it interacts with both the header and body of the request.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/design-studio/debug-mode/debug-mode-policy-chain.png" alt=""><figcaption></figcaption></figure>

### **Navigating the timeline**

You can scroll through the list of policies via the timeline. You can also quickly access a specific policy by selecting it in the **quick access** timeline.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/design-studio/debug-mode/debug-mode-timeline.png" alt=""><figcaption><p>Navigating debug timeline</p></figcaption></figure>

Select **Request Input** or **Request Output** to view the global transformation on the request and the difference between what has been received by the Gateway and what has been sent to the backend.

Select **Response Input** or **Response Output** to view the global transformation on the response and the difference between what has been received from the backend and what has been sent back to the client app.
