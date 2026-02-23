---
description: An overview about rate limit rest apis.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/how-to-guides/use-case-tutorials/rate-limit-rest-apis
---

# Rate Limit REST APIs

## Rate Limit REST APIs

### Overview <a href="#overview" id="overview"></a>

This tutorial explores various use cases where rate limiting plays a critical role in enhancing the security, performance, and reliability of your REST APIs.

### Prerequisites <a href="#prerequisites" id="prerequisites"></a>

Before proceeding with this tutorial, be sure you're familiar with the following:

* **REST APIs:** Review the key elements, methods, and design and architecture constraints of a RESTful architecture.
* **Gravitee** [**policies**](https://documentation.gravitee.io/apim/create-and-configure-apis/apply-policies/policy-reference)**:** Rules or logic that the Gateway can execute during the request or response of an API call, e.g., to enhance security, ensure reliability, or enable API monetization.
* **Gravitee APIs:** Refer to our API creation wizards for step-by-step guides to create APIs using the Gravitee [v2](https://documentation.gravitee.io/apim/create-and-configure-apis/create-apis/v2-api-creation-wizard) and [v4](https://documentation.gravitee.io/apim/create-and-configure-apis/create-apis/v4-api-creation-wizard) API definitions.

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

To add a Quota policy to each plan of this API:

1. Select **APIs** from the left nav
2. Select the API to which you are applying policies
3.  Select **Policies** from the inner left nav

    **Flows vs. policies** Flows are a collection of policies. Flows can be specified for each individual plan, e.g., API Key (SILVER), API Key (GOLD), and API Key (PLATINUM). Alternatively, a common flow can be applied to all plans within the specific AP&#x49;_._<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FzTwpSpNLpG63ETrhWuan%2Fimage.png?alt=media&#x26;token=876eb41e-41d6-4360-9ea5-d5aa3dfbdcd0" alt=""><figcaption></figcaption></figure>

#### Step 2: Add a Quota policy for each user group <a href="#step-2-add-a-quota-policy-for-each-user-group" id="step-2-add-a-quota-policy-for-each-user-group"></a>

Add differentiated Quota policies to each plan per the instructions below.

**Silver Tier plan**

1. Select the **+** icon next to the API Key (SILVER) plan
2. Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-1312b1d661b3f7a8da1fe4a6368a267625d1655b%2Fhaley%202.png?alt=media" alt=""><figcaption></figcaption></figure>

3. Click **Create**
4. Select the **+** icon within the request phase section. This lets us use the Quota policy to limit the number of requests Silver Tier members can make to the API per mont&#x68;_._

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-670c05af7a02d06fb8af38810fc139f1fac711ff%2Fhaley%203.png?alt=media" alt=""><figcaption></figcaption></figure>

5. Use the search bar or scroll to navigate to the **Quota** policy, then click **Select**.

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-9e3203c3c466e73ac0d4493191d092c8680b18a1%2Fimage%20(29)%20(2).png?alt=media" alt=""><figcaption></figcaption></figure>

6.  Toggle **Add response headers** ON and click **Save**.<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FLWTq2qWhYb0AtHu1YzSR%2Fimage.png?alt=media&#x26;token=d1a95f95-d33a-45da-bff6-6f91a5a41cec" alt=""><figcaption></figcaption></figure>
7.  Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 100 requests per 1 month<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2F6V9NXRY6IU34SHTsy3oZ%2Fimage.png?alt=media&#x26;token=46603f68-1a0e-4060-b59b-82cbcc8b589b" alt=""><figcaption></figcaption></figure>
8. Click **Add policy**
9.  On the **Policies** page, click **Save**<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FXs1S9rTPYHVepNrJ9mRp%2Fimage.png?alt=media&#x26;token=cf53b66f-c4aa-4e3b-a648-031cc0a995b5" alt=""><figcaption></figcaption></figure>
10. Click **Deploy API** to redeploy the API and have the changes take effect<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FgWUyLXyPbw4WvJpzp0Fy%2Fimage.png?alt=media&#x26;token=8b340ae1-a8a2-42cc-9051-b0b182c058a6" alt=""><figcaption></figcaption></figure>

**Gold Tier plan**

Follow the steps laid out in the Silver Tier Plan, but enter 1000 for the value of **Max requests (static)**.

**Platinum Tier plan**

Follow the steps laid out in the Silver Tier Plan, but enter 20,000 for the value of **Max requests (static)**.

Congratulations! You have successfully added differentiated Quota policies to each of your consumer plans.

#### **Step 3: Add Rate Limit policy via Common flows** <a href="#step-3-add-rate-limit-policy-via-common-flows" id="step-3-add-rate-limit-policy-via-common-flows"></a>

To ensure all API consumers, regardless of their plan, do not overwhelm the API, let's add a rate limiting policy to all user groups via **Common flows**.

1. Select the **+** icon next to **Common flows**
2.  Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FRKSU4nYr0vVP9SnH5LRo%2Fimage.png?alt=media&#x26;token=c1f4294b-666c-458c-abbb-5e047a6ba006" alt=""><figcaption></figcaption></figure>
3. Click **Create**
4.  Select the **+** icon within the request phase section. This lets us use the Rate Limit policy to limit the number of requests any API consumer can make to the API within a short period of time.<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fc9xT1RXe9JVbcY9aoZEK%2Fimage.png?alt=media&#x26;token=198ef0d1-33bc-4bc7-bb08-0632534eb0f3" alt=""><figcaption></figcaption></figure>
5.  Use the search bar or scroll to navigate to the **Rate Limit** policy, then click **Select**<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FF4FCSpa4deO5XlRbFcRn%2Fimage.png?alt=media&#x26;token=f4d9588e-b91c-45e2-a63a-b1cd8a468e9c" alt=""><figcaption></figcaption></figure>
6.  Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 5 requests per 1 second

    The Rate Limit time period is shorter than the Quota time period.<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FBqKZm4NeBJk34TxuWfOF%2Fimage.png?alt=media&#x26;token=14e08d76-56b1-4938-a57f-592cb43e32b9" alt=""><figcaption></figcaption></figure>
7. Click **Add policy**
8. On the **Policies** page, click **Save**

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-16ffecd61d3613a42abc7830927af52e051fc6e5%2Fimage%20(38)%20(2).png?alt=media" alt=""><figcaption></figcaption></figure>

9.  Click **Deploy API** to redeploy the API and have the changes take effect<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fn4o22TkEofvaOY2K648b%2Fimage.png?alt=media&#x26;token=8ef6892e-8e78-44c5-9da1-f46687ffd73b" alt=""><figcaption></figcaption></figure>

#### **Step 4: Add Spike Arrest policy via Common flows** <a href="#step-4-add-spike-arrest-policy-via-common-flows" id="step-4-add-spike-arrest-policy-via-common-flows"></a>

Now, let's mitigate traffic spikes and maintain quality of service for all consumers by adding a Spike Arrest policy to **Common flows**.

1. Select the **+** icon next to **Common flows**
2.  Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FLuvN8iUpUBS8kfF54LCC%2Fimage.png?alt=media&#x26;token=b6d4968a-42ba-425a-bdf8-fa2557a8f15e" alt=""><figcaption></figcaption></figure>
3. Click **Create**
4. Select the **+** icon within the request phase section to use the Spike Arrest policy to limit sudden spikes in traffic. Configured as a **Common flow**, the Spike Arrest policy applies to all API consumers.

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-8bb2143a797f7367491583ff389460572ca85690%2Fimage%20(41)%20(1).png?alt=media" alt=""><figcaption></figcaption></figure>

5. Use the search bar or scroll to navigate to the **Rate Limit** policy, then click **Select**

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-2f9e09d0474c91274b871084a86a8a2b13647ce8%2Fimage%20(42)%20(1).png?alt=media" alt=""><figcaption></figcaption></figure>

6. Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 100 requests per 1 second

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-4b3986dcda3b374c874963e690675a31a0c24685%2Fimage%20(43)%20(1).png?alt=media" alt=""><figcaption></figcaption></figure>

7. Click **Add policy**
8. On the **Policies** page, click **Save**

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-b98ee50c333b6dc332ffc392904d2bfed4656700%2Fimage%20(44)%20(1).png?alt=media" alt=""><figcaption></figcaption></figure>

9. Click **Deploy API** to redeploy the API and have the changes take effect

Congratulations! You have successfully added a Spike Arrest policy that applies to all API consumers.

### Shortcut to add select rate limiting policies <a href="#short-cut-to-add-select-rate-limiting-policies" id="short-cut-to-add-select-rate-limiting-policies"></a>

Rate limiting policies can also be added during the API creation process. Let's demonstrate this by adding three API Key plans.

1. Complete the steps of the API creation wizard until it gets to the part about plans
2. In the plans section, click **Add plan**. All created APIs will include a **Default Keyless (UNSECURED)** plan. You may modify or delete this plan.

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-b2b33c37abf22200acc9c041d4b918620ec48711%2Fimage%20(45)%20(2).png?alt=media" alt=""><figcaption></figcaption></figure>

3. Click **API Key**
4.  Enter a plan **Name**, **Description** (optional), and modify **Subscriptions** and **Access-Control** (optional)<br>

    <figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2FK6d9TxcxYr3bkpMPYmvp%2Fimage.png?alt=media&#x26;token=111878f3-f305-4fb4-9439-81308238dcdc" alt=""><figcaption></figcaption></figure>
5. Click **Next**, then optionally propagate the API Key to upstream API or add a selectional rule

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-5da9a9bb92f0618146a369dec17c4ae913393a20%2Fimage%20(47)%20(2).png?alt=media" alt=""><figcaption></figcaption></figure>

6. Click **Next** to add Quota and/or Rate Limit policies

The Spike Arrest policy cannot be added during the API creation process.

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-1d04759e347df3bed374fa6f9ff34b73075edc4b%2Fimage%20(48)%20(2).png?alt=media" alt=""><figcaption></figcaption></figure>

7. Toggle Rate Limiting and/or Quota ON to configure rate limiting policies for the plan

Rate limiting policies added during the API creation process will applied to the request phase.

8. Configure the plan:

* Enter a **Key** to specify the consumer group against which the policy will be applied (leave blank to use the default plan/subscription pair)
* Enter values for **Max requests (static)**, **Time duration**, and **Time unit** intended for that consumer group

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-f8fe6f36275d8a3933b783b6192409d9be6ff7cb%2Fimage%20(49)%20(2).png?alt=media" alt=""><figcaption></figcaption></figure>

9. Click **Add plan**
10. Add additional plans or select **Validate my plans** to continue with the API creation process

<figure><img src="https://128066588-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FbGmDEarvnV52XdcOiV8o%2Fuploads%2Fgit-blob-e086a0e9625ede6f6b3f59ab68d4678267480362%2Fimage%20(50)%20(2).png?alt=media" alt=""><figcaption></figcaption></figure>
