# Rate limiting REST APIs

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

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252Fem9e0beNBbuOdmR8W2Pb%252Fhaley%25201.png%3Falt%3Dmedia%26token%3D9b073f55-35ff-4590-a0bc-de1e1928043b\&width=768\&dpr=4\&quality=100\&sign=39216ae5\&sv=1)

    **Flows vs. policies** Flows are a collection of policies. Flows can be specified for each individual plan, e.g., API Key (SILVER), API Key (GOLD), and API Key (PLATINUM). Alternatively, a common flow can be applied to all plans within the specific API_._

#### Step 2: Add a Quota policy for each user group <a href="#step-2-add-a-quota-policy-for-each-user-group" id="step-2-add-a-quota-policy-for-each-user-group"></a>

Add differentiated Quota policies to each plan per the instructions below.

**Silver Tier plan**

1. Select the **+** icon next to the API Key (SILVER) plan
2.  Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252F6hn1bcFTVlC24qJwAk7Y%252Fhaley%25202.png%3Falt%3Dmedia%26token%3D5f018c15-ef29-4417-9025-c8a38cc57144\&width=768\&dpr=4\&quality=100\&sign=caa194b8\&sv=1)
3. Click **Create**
4.  Select the **+** icon within the request phase section. This lets us use the Quota policy to limit the number of requests Silver Tier members can make to the API per month_._

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FAK0vBFhNk4zWzMq5DCJE%252Fhaley%25203.png%3Falt%3Dmedia%26token%3Df299b2e5-46cf-4fe4-bb1e-006ca092b78e\&width=768\&dpr=4\&quality=100\&sign=672b576b\&sv=1)
5.  Use the search bar or scroll to navigate to the **Quota** policy, then click **Select**

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FxgG4TfgVKR8MAGh4lxwl%252Fhaley%25205.png%3Falt%3Dmedia%26token%3Dadf040e4-1808-4fad-929c-1061808b3070\&width=768\&dpr=4\&quality=100\&sign=2e29cbaa\&sv=1)
6.  Toggle **Add response headers** ON and click **Save**

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252F5Dr6uOEv5m1kmQVgxI5E%252Fhaley%25204.png%3Falt%3Dmedia%26token%3D21675f39-795a-4e47-abaf-dad5f2a03f86\&width=768\&dpr=4\&quality=100\&sign=95be508f\&sv=1)
7.  Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 100 requests per 1 month

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FPIW3igBnvoEcRbduC9Ds%252Fhaley%25206.png%3Falt%3Dmedia%26token%3Da3057830-c7c6-46dd-9d9c-06d5e66ac5a3\&width=768\&dpr=4\&quality=100\&sign=13082174\&sv=1)
8. Click **Add policy**
9.  On the **Policies** page, click **Save**

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252F41P328C4xbFM1XqV5H0F%252Fhaley%25207.png%3Falt%3Dmedia%26token%3D26ad4d3c-7585-4a3e-be06-2a9f3750d7fe\&width=768\&dpr=4\&quality=100\&sign=e9ecb5ed\&sv=1)
10. Click **Deploy API** to redeploy the API and have the changes take effect

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FPv3qMDl4HMVsmdq6KkQA%252Fhaley%25208.png%3Falt%3Dmedia%26token%3Dfc695698-5ced-4572-8e56-a59218fdda57\&width=768\&dpr=4\&quality=100\&sign=91bc61ef\&sv=1)

**Gold Tier plan**

Follow the steps laid out in [Silver Tier plan](https://documentation.gravitee.io/apim/v/4.3/most-common-use-cases/rate-limiting-rest-api-use-cases#silver-tier-plan), but enter 1000 for the value of **Max requests (static)**.

**Platinum Tier plan**

Follow the steps laid out in [Silver Tier plan](https://documentation.gravitee.io/apim/v/4.3/most-common-use-cases/rate-limiting-rest-api-use-cases#silver-tier-plan), but enter 20,000 for the value of **Max requests (static)**.

Congratulations! You have successfully added differentiated Quota policies to each of your consumer plans.

#### **Step 3: Add Rate Limit policy via Common flows** <a href="#step-3-add-rate-limit-policy-via-common-flows" id="step-3-add-rate-limit-policy-via-common-flows"></a>

To ensure all API consumers, regardless of their plan, do not overwhelm the API, let's add a rate limiting policy to all user groups via **Common flows**.

1. Select the **+** icon next to **Common flows**
2.  Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FZeNUV6RB9ZbCNY0fJAQw%252Fhaley%25209.png%3Falt%3Dmedia%26token%3Db2a198f6-1c34-43eb-91d6-3e0143e667bf\&width=768\&dpr=4\&quality=100\&sign=e25e6239\&sv=1)
3. Click **Create**
4.  Select the **+** icon within the request phase section. This lets us use the Rate Limit policy to limit the number of requests any API consumer can make to the API within a short period of time.

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FyJGQ3MEIXSWlm2ju1vdC%252Fhaley%252010.png%3Falt%3Dmedia%26token%3Df38a6cae-a949-4dae-a9cd-d5435bc3a102\&width=768\&dpr=4\&quality=100\&sign=1dc7296e\&sv=1)
5.  Use the search bar or scroll to navigate to the **Rate Limit** policy, then click **Select**

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FZB7WdoZ0pVYxc9TEnyBv%252Fhaley%252011.png%3Falt%3Dmedia%26token%3Dfa7d2355-4166-4539-a824-67613fa453d9\&width=768\&dpr=4\&quality=100\&sign=c1c33eab\&sv=1)
6.  Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 5 requests per 1 second

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252F3WISSqQUHlUuZPPSMYFy%252Fhaley%252012.png%3Falt%3Dmedia%26token%3D57a52b61-4bcd-4747-91fe-f5172c25353b\&width=768\&dpr=4\&quality=100\&sign=af50590a\&sv=1)

    The Rate Limit time period is shorter than the Quota time period.
7. Click **Add policy**
8.  On the **Policies** page, click **Save**

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FzBUMHuvVlmLlTJQ0EMbG%252Fhaley%252013.png%3Falt%3Dmedia%26token%3Db51bbefa-a01a-4d22-926c-0d5d82ee4917\&width=768\&dpr=4\&quality=100\&sign=3ae8c711\&sv=1)
9.  Click **Deploy API** to redeploy the API and have the changes take effect

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FPv3qMDl4HMVsmdq6KkQA%252Fhaley%25208.png%3Falt%3Dmedia%26token%3Dfc695698-5ced-4572-8e56-a59218fdda57\&width=768\&dpr=4\&quality=100\&sign=91bc61ef\&sv=1)

Congratulations! You have successfully added a Rate Limit policy that applies to all API consumers.

#### **Step 4: Add Spike Arrest policy via Common flows** <a href="#step-4-add-spike-arrest-policy-via-common-flows" id="step-4-add-spike-arrest-policy-via-common-flows"></a>

Now, let's mitigate traffic spikes and maintain quality of service for all consumers by adding a Spike Arrest policy to **Common flows**.

1. Select the **+** icon next to **Common flows**
2.  Modify the flow name, operator, path, methods, and conditions as desired (leaving name and path blank will apply default values)

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FZeNUV6RB9ZbCNY0fJAQw%252Fhaley%25209.png%3Falt%3Dmedia%26token%3Db2a198f6-1c34-43eb-91d6-3e0143e667bf\&width=768\&dpr=4\&quality=100\&sign=e25e6239\&sv=1)
3. Click **Create**
4.  Select the **+** icon within the request phase section to use the Spike Arrest policy to limit sudden spikes in traffic. Configured as a **Common flow**, the Spike Arrest policy applies to all API consumers.

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FdqZCKAJ3WFS2RhQn6vOF%252Fhaley%252015.png%3Falt%3Dmedia%26token%3Dbd580a8e-2160-40ce-a787-5828bf0145ce\&width=768\&dpr=4\&quality=100\&sign=2c5acfa7\&sv=1)
5.  Use the search bar or scroll to navigate to the **Rate Limit** policy, then click **Select**

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252F1RaOBSxIpOU60rZ0fxdf%252Fhaley%252014.png%3Falt%3Dmedia%26token%3D303ed0ee-c17b-43a5-98f0-8710f7a84a56\&width=768\&dpr=4\&quality=100\&sign=9efa3fca\&sv=1)
6.  Enter values for **Max requests (static)**_,_ **Time duration**, and **Time unit**, e.g., 100 requests per 1 second

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252Fk2RZ7pgXCbESAi6gCVm3%252Fhaley%252016.png%3Falt%3Dmedia%26token%3Df6e660e9-00a0-48d9-86a9-f8f0449085ed\&width=768\&dpr=4\&quality=100\&sign=d76cb845\&sv=1)
7. Click **Add policy**
8.  On the **Policies** page, click **Save**

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FpPGbjT18VDrfE1og7eJg%252Fhaley%252017.png%3Falt%3Dmedia%26token%3De2409479-bfa5-451a-916f-90236b0782d1\&width=768\&dpr=4\&quality=100\&sign=75c86a0\&sv=1)
9.  Click **Deploy API** to redeploy the API and have the changes take effect

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FPv3qMDl4HMVsmdq6KkQA%252Fhaley%25208.png%3Falt%3Dmedia%26token%3Dfc695698-5ced-4572-8e56-a59218fdda57\&width=768\&dpr=4\&quality=100\&sign=91bc61ef\&sv=1)

Congratulations! You have successfully added a Spike Arrest policy that applies to all API consumers.

### Short cut to add select rate limiting policies <a href="#short-cut-to-add-select-rate-limiting-policies" id="short-cut-to-add-select-rate-limiting-policies"></a>

Rate limiting policies can also be added during [Step 4: Security](https://documentation.gravitee.io/apim/v/4.3/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard#step-4-security) of the [API creation process](https://documentation.gravitee.io/apim/v/4.3/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard). Let's demonstrate this by adding three API Key plans.

1. Complete steps 1-3 of the [v4 API creation wizard](https://documentation.gravitee.io/apim/v/4.3/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard)
2.  At step 4, click **Add plan**

    All created APIs will include a **Default Keyless (UNSECURED)** plan. You may modify or delete this plan.

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FMfgO84fsN13plQDpn09J%252Fhaley%252018.png%3Falt%3Dmedia%26token%3D9c5e35a1-714b-47a3-b09b-27e34f209e15\&width=768\&dpr=4\&quality=100\&sign=7809cac4\&sv=1)
3. Click **API Key**
4.  Enter a plan **Name**, **Description** (optional), and modify **Subscriptions** and **Access-Control** (optional)

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FRC2fAvg3gDnQ2ckyBcOY%252Fhaley%252019.png%3Falt%3Dmedia%26token%3D73313c33-a176-4285-b695-0f4b2fb0ebc0\&width=768\&dpr=4\&quality=100\&sign=5b026c7a\&sv=1)
5.  Click **Next**, then optionally propagate the API Key to upstream API or add a selectional rule

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252F9kQbKuaJPWsEeqeNaPPA%252Fhaley%252020.png%3Falt%3Dmedia%26token%3Db3e2e92c-7296-4f00-aabd-824070618a9c\&width=768\&dpr=4\&quality=100\&sign=732005bc\&sv=1)
6.  Click **Next** to add Quota and/or Rate Limit policies

    The Spike Arrest policy cannot be added during the API creation process.

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FCKMevFzQmziO01WRnsuK%252Fhaley%252021.png%3Falt%3Dmedia%26token%3Df7db78dd-f879-42da-8783-7dd2e56c26b9\&width=768\&dpr=4\&quality=100\&sign=8f6c0d5e\&sv=1)
7.  Toggle Rate Limiting and/or Quota ON to configure rate limiting policies for the plan

    Rate limiting policies added during the API creation process will applied to the request phase.
8.  Configure the plan:

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252FZtUnwf9mGEF2jZeqLKpd%252Fhaley%252022.png%3Falt%3Dmedia%26token%3D7706dcbd-713d-4a51-9aa4-3c83a2f6cb07\&width=768\&dpr=4\&quality=100\&sign=d8b3f8d3\&sv=1)

    * Enter a **Key** to specify the consumer group against which the policy will be applied (leave blank to use the default plan/subscription pair)
    * Enter values for **Max requests (static)**, **Time duration**, and **Time unit** intended for that consumer group
9. Click **Add plan**
10. Add additional plans or select **Validate my plans** to continue with the API creation process

    ![](https://documentation.gravitee.io/\~gitbook/image?url=https%3A%2F%2F4260319747-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FlGMAxnYO3Z9dU9bQfplr%252Fuploads%252F4IfISv3DlOWJO91CD7X4%252Fhaley%252023.png%3Falt%3Dmedia%26token%3D520ce6f5-c97a-4a7c-a5b3-4c625da80da9\&width=768\&dpr=4\&quality=100\&sign=72bf0215\&sv=1)
