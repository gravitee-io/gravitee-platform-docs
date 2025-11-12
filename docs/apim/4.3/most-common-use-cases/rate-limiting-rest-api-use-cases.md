# Rate Limiting REST API Use Cases

## Overview

This tutorial explores various use cases where rate limiting plays a critical role in enhancing the security, performance, and reliability of your REST APIs.

## Prerequisites

Before proceeding with this tutorial, be sure you're familiar with the following:

* **REST APIs:** Visit our [REST API Tutorial ](https://www.gravitee.io/blog/rest-api-tutorial)to review the key elements, methods, and design and architecture constraints of a RESTful architecture.
* **Gravitee policies:** Rules or logic that the Gateway can execute during the request or response of an API call, e.g., to enhance security, ensure reliability, or enable API monetization. See our [Policy Reference](../reference/policy-reference/) documentation to learn more.
* **Gravitee APIs:** Visit [Create APIs](../guides/create-apis/) to learn about Gravitee API creation concepts and [The API Creation Wizard](../guides/create-apis/the-api-creation-wizard/) for step-by-step guides to create APIs using the Gravitee v2 and v4 API definitions.

## Introduction to Gravitee rate limiting

Rate limiting policies limit and/or throttle the number of API requests over a set time period. Rate limits can be enacted as a security measure to prevent abuse and ensure fair usage of the API. They can be applied differently depending on the type of request, consumer authentication status, or usage history.

Gravitee supports three rate-limiting policies:

* **Quota:** Refers to the total amount of resources or actions that a client is allowed to consume over a given period, e.g., 1000 API requests per day. Once the quota is reached, the client may be denied further access until the quota is reset.
* **Rate Limit:** Specifies the number of requests a client can make within a limited time frame, e.g., 100 requests per minute, to control the rate of requests and ensure that the API is not overwhelmed.
* **Spike Arrest:** Similar to rate limiting but helps prevent servers from being overwhelmed by spikes in traffic. It allows a certain number of requests to be processed immediately, but any requests exceeding that limit are delayed or rejected.

In summary, quota limits the total amount of usage over a period, while rate limit controls the rate at which requests can be made within that period. Both are important for managing API usage and ensuring fair access to resources. Spike arrest handles sudden spikes in traffic to ensure the stability and reliability of the API.&#x20;

## Use case: Rate limits based on consumer plan

This use case is an example of how to enforce a rate limiting policy on a Gravitee REST API.

### **Scenario and objective**

A cloud storage service offers an API that developers can use to access and manage the files hosted on its platform. There are three tiers of service, represented by silver, gold, and platinum plans, which correspond to different levels of consumer access. The goal is to facilitate secure, fair usage of the API while providing a differentiated experience through the unique rate-limiting of each tier.

This use case explores enabling different Quota policies for each tier and also applying a Rate Limit policy to all tiers to ensure that consumer requests do not overwhelm the backend server.&#x20;

### **Users**

* **Silver Tier:** The cloud storage service wants to encourage free, limited use of their API. Users subscribed to this plan will be assigned the lowest quota level.
* **Gold Tier:** This plan allows API consumers to call the API more than the free, limited plan. Subscribers will be subject to a higher quota.&#x20;
* **Platinum Tier:** Users subscribed to the paid plan are granted the highest rate limit compared to other tiers. This incentivizes users to upgrade to a premium plan while still ensuring fair usage across all user groups.&#x20;

### Step 1: Add a Quota policy for each user group

For each user group defined above, an individual plan should be established. This example uses the API Key plan.

{% hint style="info" %}
See the [Plans](../guides/api-exposure-plans-applications-and-subscriptions/plans/) documentation for more information.
{% endhint %}

To add a Quota policy to each plan of this API:

1. Select **APIs** from the left nav
2. Select the API to which you are applying policies
3.  Select **Policies** from the inner left nav&#x20;

    <figure><img src="../.gitbook/assets/haley 1.png" alt=""><figcaption></figcaption></figure>

    {% hint style="info" %}
    **Flows vs. policies**\
    Flows are a collection of policies. Flows can be specified for each individual plan, e.g., API Key (SILVER), API Key (GOLD), and API Key (PLATINUM). Alternatively, a common flow can be applied to all plans within the specific API_._
    {% endhint %}

### Step 2: Add a Quota policy for each user group

Add differentiated Quota policies to each plan per the instructions below.

#### Silver Tier plan

1. Select the **+** icon next to the API Key (SILVER) plan&#x20;
2.  Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)&#x20;

    <figure><img src="../.gitbook/assets/haley 2.png" alt=""><figcaption></figcaption></figure>
3. Click **Create**
4.  Select the **+** icon within the request phase section. This lets us use the Quota policy to limit the number of requests Silver Tier members can make to the API per month_._&#x20;

    <figure><img src="../.gitbook/assets/haley 3.png" alt=""><figcaption></figcaption></figure>
5.  Use the search bar or scroll to navigate to the **Quota** policy, then click **Select**&#x20;

    <figure><img src="../.gitbook/assets/haley 5.png" alt=""><figcaption></figcaption></figure>
6.  Toggle **Add response headers** ON and click **Save**

    <figure><img src="../.gitbook/assets/haley 4.png" alt=""><figcaption></figcaption></figure>
7.  Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 100 requests per 1 month&#x20;

    <figure><img src="../.gitbook/assets/haley 6.png" alt=""><figcaption></figcaption></figure>
8. Click **Add policy**
9.  On the **Policies** page, click **Save**

    <figure><img src="../.gitbook/assets/haley 7.png" alt=""><figcaption></figcaption></figure>
10. Click **Deploy API** to redeploy the API and have the changes take effect&#x20;

    <figure><img src="../.gitbook/assets/haley 8.png" alt=""><figcaption></figcaption></figure>

#### Gold Tier plan

Follow the steps laid out in [Silver Tier plan](rate-limiting-rest-api-use-cases.md#silver-tier-plan), but enter 1000 for the value of **Max requests (static)**.

#### Platinum Tier plan

Follow the steps laid out in [Silver Tier plan](rate-limiting-rest-api-use-cases.md#silver-tier-plan), but enter 20,000 for the value of **Max requests (static)**.

{% hint style="success" %}
Congratulations! You have successfully added differentiated Quota policies to each of your consumer plans.&#x20;
{% endhint %}

### **Step 3: Add Rate Limit policy via Common flows**

To ensure all API consumers, regardless of their plan, do not overwhelm the API, let's add a rate limiting policy to all user groups via **Common flows**.&#x20;

1. Select the **+** icon next to **Common flows**
2.  Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)&#x20;

    <figure><img src="../.gitbook/assets/haley 9.png" alt=""><figcaption></figcaption></figure>
3. Click **Create**
4.  Select the **+** icon within the request phase section. This lets us use the Rate Limit policy to limit the number of requests any API consumer can make to the API within a short period of time.&#x20;

    <figure><img src="../.gitbook/assets/haley 10.png" alt=""><figcaption></figcaption></figure>
5.  Use the search bar or scroll to navigate to the **Rate Limit** policy, then click **Select**&#x20;

    <figure><img src="../.gitbook/assets/haley 11.png" alt=""><figcaption></figcaption></figure>
6.  Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 5 requests per 1 second&#x20;

    <figure><img src="../.gitbook/assets/haley 12.png" alt=""><figcaption></figcaption></figure>

    {% hint style="info" %}
    The Rate Limit time period is shorter than the Quota time period.
    {% endhint %}
7. Click **Add policy**
8.  On the **Policies** page, click **Save**&#x20;

    <figure><img src="../.gitbook/assets/haley 13.png" alt=""><figcaption></figcaption></figure>
9.  Click **Deploy API** to redeploy the API and have the changes take effect&#x20;

    <figure><img src="../.gitbook/assets/haley 8.png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Congratulations! You have successfully added a Rate Limit policy that applies to all API consumers.
{% endhint %}

### **Step 4: Add Spike Arrest policy via Common flows**

Now, let's mitigate traffic spikes and maintain quality of service for all consumers by adding a Spike Arrest policy to **Common flows**.&#x20;

1. Select the **+** icon next to **Common flows**
2.  Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)&#x20;

    <figure><img src="../.gitbook/assets/haley 9.png" alt=""><figcaption></figcaption></figure>
3. Click **Create**
4.  Select the **+** icon within the request phase section to use the Spike Arrest policy to limit sudden spikes in traffic. Configured as a **Common flow**, the Spike Arrest policy applies to all API consumers.&#x20;

    <figure><img src="../.gitbook/assets/haley 15.png" alt=""><figcaption></figcaption></figure>
5.  Use the search bar or scroll to navigate to the **Rate Limit** policy, then click **Select**&#x20;

    <figure><img src="../.gitbook/assets/haley 14.png" alt=""><figcaption></figcaption></figure>
6.  Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 100 requests per 1 second&#x20;

    <figure><img src="../.gitbook/assets/haley 16.png" alt=""><figcaption></figcaption></figure>
7. Click **Add policy**
8.  On the **Policies** page, click **Save**&#x20;

    <figure><img src="../.gitbook/assets/haley 17.png" alt=""><figcaption></figcaption></figure>
9.  Click **Deploy API** to redeploy the API and have the changes take effect&#x20;

    <figure><img src="../.gitbook/assets/haley 8.png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Congratulations! You have successfully added a Spike Arrest policy that applies to all API consumers.
{% endhint %}

## Short cut to add select rate limiting policies

Rate limiting policies can also be added during [Step 4: Security](docs/apim/4.3/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md#step-4-security) of the [API creation process](docs/apim/4.3/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md). Let's demonstrate this by adding three API Key plans.&#x20;

1. Complete steps 1-3 of the [v4 API creation wizard](docs/apim/4.3/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md)
2.  At step 4, click **Add plan**&#x20;

    {% hint style="info" %}
    All created APIs will include a **Default Keyless (UNSECURED)** plan. You may modify or delete this plan.
    {% endhint %}



    <figure><img src="../.gitbook/assets/haley 18.png" alt=""><figcaption></figcaption></figure>
3. Click **API Key**
4.  Enter a plan **Name**, **Description** (optional), and modify **Subscriptions** and **Access-Control** (optional)&#x20;

    <figure><img src="../.gitbook/assets/haley 19.png" alt=""><figcaption></figcaption></figure>
5.  Click **Next**, then optionally propagate the API Key to upstream API or add a selectional rule&#x20;

    <figure><img src="../.gitbook/assets/haley 20.png" alt=""><figcaption></figcaption></figure>
6.  Click **Next** to add Quota and/or Rate Limit policies&#x20;

    {% hint style="info" %}
    The Spike Arrest policy cannot be added during the API creation process.
    {% endhint %}



    <figure><img src="../.gitbook/assets/haley 21.png" alt=""><figcaption></figcaption></figure>


7.  Toggle Rate Limiting and/or Quota ON to configure rate limiting policies for the plan

    {% hint style="info" %}
    Rate limiting policies added during the API creation process will applied to the request phase.&#x20;
    {% endhint %}
8.  Configure the plan:

    <figure><img src="../.gitbook/assets/haley 22.png" alt=""><figcaption></figcaption></figure>

    * Enter a **Key** to specify the consumer group against which the policy will be applied (leave blank to use the default plan/subscription pair)
    * Enter values for **Max requests (static)**, **Time duration**, and **Time unit** intended for that consumer group
9. Click **Add plan**
10. Add additional plans or select **Validate my plans** to continue with the API creation process&#x20;

    <figure><img src="../.gitbook/assets/haley 23.png" alt=""><figcaption></figcaption></figure>
