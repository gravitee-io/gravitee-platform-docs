---
description: An overview about rate limiting rest api use cases.
---

# Rate Limiting REST API Use Cases

### Overview <a href="#overview" id="overview"></a>

This tutorial explores various use cases where rate limiting plays a critical role in enhancing the security, performance, and reliability of your REST APIs.

### Prerequisites <a href="#prerequisites" id="prerequisites"></a>

Before proceeding with this tutorial, be sure you're familiar with the following:

* **REST APIs:** Visit our [REST API Tutorial ](https://www.gravitee.io/blog/rest-api-tutorial)to review the key elements, methods, and design and architecture constraints of a RESTful architecture.
* **Gravitee policies:** Rules or logic that the Gateway can execute during the request or response of an API call, e.g., to enhance security, ensure reliability, or enable API monetization. See our [Policy Reference](https://documentation.gravitee.io/apim/v/4.3/reference/policy-reference) documentation to learn more.
* **Gravitee APIs:** Visit [Create APIs](https://documentation.gravitee.io/apim/v/4.3/guides/create-apis) to learn about Gravitee API creation concepts and [The API Creation Wizard](https://documentation.gravitee.io/apim/v/4.3/guides/create-apis/the-api-creation-wizard) for step-by-step guides to create APIs using the Gravitee v2 and v4 API definitions.

### Introduction to Gravitee rate limiting <a href="#introduction-to-gravitee-rate-limiting" id="introduction-to-gravitee-rate-limiting"></a>

Rate limiting policies limit and/or throttle the number of API requests over a set time period. Rate limits can be enacted as a security measure to prevent abuse and ensure fair usage of the API. They can be applied differently depending on the type of request, consumer authentication status, or usage history.

Gravitee supports three rate-limiting policies:

* **Quota:** Refers to the total amount of resources or actions that a client is allowed to consume over a given period, e.g., 1000 API requests per day. Once the quota is reached, the client may be denied further access until the quota is reset.
* **Rate Limit:** Specifies the number of requests a client can make within a limited time frame, e.g., 100 requests per minute, to control the rate of requests and ensure that the API is not overwhelmed.
* **Spike Arrest:** Similar to rate limiting but helps prevent servers from being overwhelmed by spikes in traffic. It allows a certain number of requests to be processed immediately, but any requests exceeding that limit are delayed or rejected.

In summary, quota limits the total amount of usage over a period, while rate limit controls the rate at which requests can be made within that period. Both are important for managing API usage and ensuring fair access to resources. Spike arrest handles sudden spikes in traffic to ensure the stability and reliability of the API.

### Use case: Rate limits based on consumer plan <a href="#use-case-rate-limits-based-on-consumer-plan" id="use-case-rate-limits-based-on-consumer-plan"></a>

This use case is an example of how to enforce a rate limiting policy on a Gravitee REST API.

#### **Scenario and objective** <a href="#scenario-and-objective" id="scenario-and-objective"></a>

A cloud storage service offers an API that developers can use to access and manage the files hosted on its platform. There are three tiers of service, represented by silver, gold, and platinum plans, which correspond to different levels of consumer access. The goal is to facilitate secure, fair usage of the API while providing a differentiated experience through the unique rate-limiting of each tier.

This use case explores enabling different Quota policies for each tier and also applying a Rate Limit policy to all tiers to ensure that consumer requests do not overwhelm the backend server.

#### **Users** <a href="#users" id="users"></a>

* **Silver Tier:** The cloud storage service wants to encourage free, limited use of their API. Users subscribed to this plan will be assigned the lowest quota level.
* **Gold Tier:** This plan allows API consumers to call the API more than the free, limited plan. Subscribers will be subject to a higher quota.
* **Platinum Tier:** Users subscribed to the paid plan are granted the highest rate limit compared to other tiers. This incentivizes users to upgrade to a premium plan while still ensuring fair usage across all user groups.

#### Step 1: Add a Quota policy for each user group <a href="#step-1-add-a-quota-policy-for-each-user-group" id="step-1-add-a-quota-policy-for-each-user-group"></a>

For each user group defined above, an individual plan should be established. This example uses the API Key plan.

See the [Plans](https://documentation.gravitee.io/apim/v/4.3/guides/api-exposure-plans-applications-and-subscriptions/plans) documentation for more information.

To add a Quota policy to each plan of this API:

1. Select **APIs** from the left nav
2. Select the API to which you are applying policies
3.  Select **Policies** from the inner left nav

    **Flows vs. policies** Flows are a collection of policies. Flows can be specified for each individual plan, e.g., API Key (SILVER), API Key (GOLD), and API Key (PLATINUM). Alternatively, a common flow can be applied to all plans within the specific AP&#x49;_._

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

#### Step 2: Add a Quota policy for each user group <a href="#step-2-add-a-quota-policy-for-each-user-group" id="step-2-add-a-quota-policy-for-each-user-group"></a>

Add differentiated Quota policies to each plan per the instructions below.

**Silver Tier plan**

1. Select the **+** icon next to the API Key (SILVER) plan
2. Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

3. Click **Create**
4. Select the **+** icon within the request phase section. This lets us use the Quota policy to limit the number of requests Silver Tier members can make to the API per mont&#x68;_._

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

5. Use the search bar or scroll to navigate to the **Quota** policy, then click **Select**.

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

6. Toggle **Add response headers** ON and click **Save**.

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

7. Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 100 requests per 1 month

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

8. Click **Add policy**
9. On the **Policies** page, click **Save**

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

10. Click **Deploy API** to redeploy the API and have the changes take effect

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

**Gold Tier plan**

Follow the steps laid out in [Silver Tier plan](https://documentation.gravitee.io/apim/v/4.3/most-common-use-cases/rate-limiting-rest-api-use-cases#silver-tier-plan), but enter 1000 for the value of **Max requests (static)**.

**Platinum Tier plan**

Follow the steps laid out in [Silver Tier plan](https://documentation.gravitee.io/apim/v/4.3/most-common-use-cases/rate-limiting-rest-api-use-cases#silver-tier-plan), but enter 20,000 for the value of **Max requests (static)**.

Congratulations! You have successfully added differentiated Quota policies to each of your consumer plans.

#### **Step 3: Add Rate Limit policy via Common flows** <a href="#step-3-add-rate-limit-policy-via-common-flows" id="step-3-add-rate-limit-policy-via-common-flows"></a>

To ensure all API consumers, regardless of their plan, do not overwhelm the API, let's add a rate limiting policy to all user groups via **Common flows**.

1. Select the **+** icon next to **Common flows**
2. Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

3. Click **Create**
4. Select the **+** icon within the request phase section. This lets us use the Rate Limit policy to limit the number of requests any API consumer can make to the API within a short period of time.

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

5. Use the search bar or scroll to navigate to the **Rate Limit** policy, then click **Select**

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

6.  Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 5 requests per 1 second

    The Rate Limit time period is shorter than the Quota time period.

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

7. Click **Add policy**
8. On the **Policies** page, click **Save**

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

9. Click **Deploy API** to redeploy the API and have the changes take effect

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

#### **Step 4: Add Spike Arrest policy via Common flows** <a href="#step-4-add-spike-arrest-policy-via-common-flows" id="step-4-add-spike-arrest-policy-via-common-flows"></a>

Now, let's mitigate traffic spikes and maintain quality of service for all consumers by adding a Spike Arrest policy to **Common flows**.

1. Select the **+** icon next to **Common flows**
2. Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

3. Click **Create**
4. Select the **+** icon within the request phase section to use the Spike Arrest policy to limit sudden spikes in traffic. Configured as a **Common flow**, the Spike Arrest policy applies to all API consumers.

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

5. Use the search bar or scroll to navigate to the **Rate Limit** policy, then click **Select**

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

6. Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 100 requests per 1 second

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

7. Click **Add policy**
8. On the **Policies** page, click **Save**

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

9. Click **Deploy API** to redeploy the API and have the changes take effect

Congratulations! You have successfully added a Spike Arrest policy that applies to all API consumers.

### Short cut to add select rate limiting policies <a href="#short-cut-to-add-select-rate-limiting-policies" id="short-cut-to-add-select-rate-limiting-policies"></a>

Rate limiting policies can also be added during [Step 4: Security](https://documentation.gravitee.io/apim/v/4.3/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard#step-4-security) of the [API creation process](https://documentation.gravitee.io/apim/v/4.3/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard). Let's demonstrate this by adding three API Key plans.

1. Complete steps 1-3 of the [v4 API creation wizard](https://documentation.gravitee.io/apim/v/4.3/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard)
2.  At step 4, click **Add plan**

    All created APIs will include a **Default Keyless (UNSECURED)** plan. You may modify or delete this plan.

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

3. Click **API Key**
4. Enter a plan **Name**, **Description** (optional), and modify **Subscriptions** and **Access-Control** (optional)

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

5. Click **Next**, then optionally propagate the API Key to upstream API or add a selectional rule

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

6. Click **Next** to add Quota and/or Rate Limit policies

The Spike Arrest policy cannot be added during the API creation process.

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

7. Toggle Rate Limiting and/or Quota ON to configure rate limiting policies for the plan

Rate limiting policies added during the API creation process will applied to the request phase.

8. Configure the plan:

* Enter a **Key** to specify the consumer group against which the policy will be applied (leave blank to use the default plan/subscription pair)
* Enter values for **Max requests (static)**, **Time duration**, and **Time unit** intended for that consumer group

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

9. Click **Add plan**
10. Add additional plans or select **Validate my plans** to continue with the API creation process

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
