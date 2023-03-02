# Design your API flows

## Overview

You can use Design Studio to create new API flows for your plans and define policies for each flow. Creating different flows for a plan allows you to apply different policies by path and/or HTTP method.

## Get started with Design Studio

1. link:\{{ _/apim/3.x/apim\_quickstart\_console\_login.html_ | relative\_url \}}\[Log in to APIM Console^].
2. Click **APIs** and select your API in the list.
3. Click **Design**.
4. If your API was created in an earlier version of APIM, migrate it to Design Studio as described in link:\{{ _/apim/3.x/apim\_publisherguide\_design\_studio\_migrate.html_ | relative\_url \}}\[Migrate to Design Studio^].

## Create and configure an API flow

You can create flows at API level or at plan level.

1.  In the **DESIGN** tab, click the **API** tab to design a new API level flow or **PLANS** to create a new plan level flow.

    image:\{% link images/apim/3.x/api-publisher-guide/design-studio/design-studio.png %\}\[Design Studio]
2.  Click the plus icon to add a new flow.

    image:\{% link images/apim/3.x/api-publisher-guide/design-studio/add-plan-flow.png %\}\[]
3.  Double-click the flow to configure its details.

    image:\{% link images/apim/3.x/api-publisher-guide/design-studio/flow-configuration.png %\}\[]

    Configure the following:

    * Name
    * Path details to filter on: the path syntax for the flow in link:\{{ _/apim/3.x/apim\_policies\_overview.html#ant-notation_ | relative\_url \}}\[Ant format^] and whether the path starts with or equals the value entered in **Path**.
    * One or methods to filter on (specify all which apply)
    * One or more conditions to filter on, in link:\{{ _/apim/3.x/apim\_publisherguide\_expression\_language.html_ | relative\_url \}}\[Expression Language format^] — for example, a condition to filter on query parameters called `X-debug` would be written like this: `#request.params['X-debug'] != null`
4. Click **SAVE**.

You can update a flow by clicking it and changing any required values, then clicking the tick icon image:\{% link images/icons/tick-icon.png %\}\[role="icon"] to update the values.

## Additional configuration

You can configure the following additional resources and properties for your API flows.

### Specify Best match for your flow paths

In the **CONFIGURATION** tab, select **Best match** if you want APIM to match your flows from the path that is closest to that defined in the flow definition.

image:\{% link images/apim/3.x/api-publisher-guide/design-studio/configuration-tab.png %\}\[]

Best match flow is chosen if the request matches the flow. A plain text part of the path will take precedence over a path parameter.

It means, reading from left to right, each part of the path is compared, keeping the better matching. Strict equality between part of request path and flow path prevails over a path parameter.

For example, with those flows configured:

* `/test/:id`
* `/test/subtest`

If the request is `/test/55`, the resulting flow will be `/test/:id`. If the request is `/test/subtest`, the resulting flow will be `/test/subtest`.

### Define properties for your API flows

In the **PROPERTIES** tab, specify properties as key-value pairs. You can specify them one by one, or toggle from **Simple** to **Expert** mode and paste property definitions into an editor in format `<key>=<value>`.

You can also configure dynamic properties by clicking **CONFIGURE DYNAMIC PROPERTIES**. Dynamic properties are fetched with a URL on a regular schedule and subsequently updated according to the details you specify.

image:\{% link images/apim/3.x/api-publisher-guide/design-studio/properties-tab.png %\}\[]

When you add new policies to your API flows which include link:\{{ _/apim/3.x/apim\_publisherguide\_expression\_language.html#api_ | relative\_url \}}\[Expression Language^] fields as part of their configuration (such as the dynamic routing policy), you can retrieve and query property values with the `#properties` statement. For more details, see the [???](design-studio-create.md#example) below.

#### Dynamic properties

You can configure dynamic properties, which retrieve properties from a remote server with a URL and update them according to the details you specify.

1. Click **CONFIGURE DYNAMIC PROPERTIES**.
2. Specify the details of the property:
   * `cron` schedule
   * URL
   * request headers and body to include with the call
   * JOLT transformation to perform on the response
3. Toggle on the **Enabled** option.
4. Click the tick icon image:\{% link images/icons/tick-icon.png %\}\[role="icon"] to save your changes.
5.  Click **SAVE**.

    After the first call, the resulting property is added to the list of global properties, where its value is continuously updated according to the `cron` schedule specified.

### Create resources to use in your flows

In the **RESOURCES** tab, create new resources to use in your flows. You can add resources to policies which support them when configuring them for a flow.

image:\{% link images/apim/3.x/api-publisher-guide/design-studio/resources-tab.png %\}\[]

* `Cache` resources can be added to a `Cache` policy
* `Generic OAuth2 Authorization Server` resources can be added to an `OAuth2` policy
* `Gravitee.io AM Authorization Server` resources can be added to an `OAuth2` policy

For example, specify a cache resource as follows:

1.  Click **CACHE**.

    image:\{% link images/apim/3.x/api-publisher-guide/design-studio/cache-resource.png %\}\[]
2. Enter the cache name.
3. Specify the cache properties: time to idle, time to live and max entries on heap.
4. Click the tick icon image:\{% link images/icons/tick-icon.png %\}\[role="icon"].
5. Click **SAVE**.

## Add policies to a flow

You can add as many policies as you want to a flow.

You can find out more about a specific policy by selecting it to view the in-product reference documentation, or you can view the online Policy Reference link:\{{ _/apim/3.x/apim\_policies\_overview.html_ | relative\_url \}}\[here^].

1. Click the **DESIGN** tab.
2.  Click on a plan to expand it.

    image:\{% link images/apim/3.x/api-publisher-guide/design-studio/add-policies-expand-plan.png %\}\[] . From the list on the right, drag the policy to the required phase of the flow.

    image:\{% link images/apim/3.x/api-publisher-guide/design-studio/add-policies-new-policy.png %\}\[] . Specify the details of the policy configuration. If this is a `Cache` or `OAuth2` type policy, you can add the corresponding resources created in \[???]\(#Create resources to use in your flows). . Click **SAVE**.

If you hover over a policy in a flow you can perform various operations on it: drag the policy to another phase of the flow, disable, delete or duplicate the policy.

## Example

In this example, we want our API to query our shop databases to check their stock levels. We will dynamically reroute any API calls containing a shop ID to its associated URL.

The first step is to [define a list of properties](design-studio-create.md#api-properties) for the shops, with each unique shop ID as the key and the URL of the shop as the value.

image::\{% link images/apim/3.x/api-publisher-guide/design-studio/global-properties-list.png %\}\[]

We then configure a dynamic routing policy for the API with a routing rule which builds a new URL dynamically through property matching. The URL is created with a `#properties` statement which matches properties returned by querying the request header containing the shop ID.

image::\{% link images/apim/3.x/api-publisher-guide/design-studio/dynamic-routing-properties.png %\}\[]

If the ID in the request header matches the key of one of the properties, it is replaced with the URL. The dynamic routing policy then reroutes the API call to the URL.

The list of shop IDs and URLs could also be maintained using a dictionary, for example, in organizations where the administrator maintains this information independently of the API creation process or if the list needs to be available to multiple APIs. For more details, see link:\{{ _/apim/3.x/apim\_installguide\_configuration\_dictionaries.html_ | relative\_url \}}\[Configure dictionaries^] in the Configuration Guide.

## Deploy your API and view it in the audit history

When you have finished designing an API, you need to click the **deploy your API** link to deploy your API with your changes.

Each new API deployment has a version associated, for which you can add a description as a label when deploying the API:

image:\{% link images/apim/3.x/api-publisher-guide/design-studio/deploy-label.png %\}\[]

You can use this label to identify the API deployment in the audit trail and in views on the API dashboard:

image:\{% link images/apim/3.x/api-publisher-guide/audit/audit-history.png %\}\[]

The audit history allows you to view the deployment in detail. For more information, see link:\{{ _/apim/3.x/apim\_publisherguide\_audit.html_ | relative\_url \}}\[Audit trail^].
