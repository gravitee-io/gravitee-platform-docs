---
description: Guide to configuring JWT Security with APIM.
---

# Configure JWT Security with APIM

### Overview <a href="#overview" id="overview"></a>

This tutorial will quickly showcase how to apply JSON web token (JWT) security to APIs using Gravitee API Management (APIM) and a third-party identity provider (IdP). This tutorial will focus on APIM-specific configuration and provide generic instructions in regards to IdP setup.

{% hint style="info" %}
**JWT deep dive**

For a much deeper dive on this topic that includes IdP setup and configuration, [check out this blog](https://www.gravitee.io/blog/secure-apis-with-jwt-tokens) on JWT authentication using Gravitee Access Management as the IdP.
{% endhint %}

### Prerequisites <a href="#prerequisites-3" id="prerequisites-3"></a>

To participate in this tutorial, you must have an instance of APIM 4.0 or later up and running. You can check out our [extensive installation guides](https://documentation.gravitee.io/apim/v/4.3/getting-started/install-and-upgrade-guides) to learn the different ways you can get started with Gravitee.

Additionally, the following guide assumes the client application has already been configured to use a third-party IdP. Once the application has received an access token from the IdP in the form of a JWT, a properly configured APIM Gateway can validate the signature before granting the user of the application access to protected resources.

### Gravitee Gateway APIs <a href="#gravitee-gateway-apis-4" id="gravitee-gateway-apis-4"></a>

The first step is to create a Gateway API. A Gateway API is simply an API deployed on the Gravitee Gateway by an API publisher and is what API consumers will call or subscribe to in order to retrieve data, functionality, etc. from the publisher’s backend APIs. Backend APIs are the data source or functionality that you want to proxy with the Gateway.

In the Console UI, select the Gateway API you want to secure with a JWT plan.

<figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

Alternatively, if you haven’t created a Gateway API yet, you can learn [how to create a Gateway API here](https://documentation.gravitee.io/apim/v/4.3/guides/create-apis). For now, be sure to leave the **Default Keyless (UNSECURED)** plan as we’ll be configuring the plan separately.

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

Save and deploy the API when you’re finished.

This guide assumes you are testing. If you’re creating a Gateway API that proxies sensitive information, do not start the API until you have secured it with a plan.

### Plans <a href="#plans-5" id="plans-5"></a>

Next, we need to secure the Gateway API with a JWT plan. A plan provides a service and access layer on top of your APIs for consumer applications. A plan specifies access limits, subscription validation modes, and other configurations to tailor it to a specific application. The most important part of plan configuration is selecting the security type. APIM supports the following four security types:

* Keyless (public)
* API Key
* OAuth 2.0
* JWT

All Gateway APIs require at least one published plan to deploy the API to the Gateway.

#### Create and Publish a JWT Plan <a href="#create-and-publish-a-jwt-plan-6" id="create-and-publish-a-jwt-plan-6"></a>

In the APIM Console UI, open the Gateway API you want to secure with a JWT plan. You should see a screen similar to the following:

<figure><img src="../../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>

In the sidebar, select **Plans**, and then select **+Add new plan** in the top right of the screen. In the dropdown that appears, select **JWT**.

<figure><img src="../../.gitbook/assets/image (3) (1).png" alt=""><figcaption></figcaption></figure>

Provide your plan a name, and then scroll down and toggle on **Auto validate subscription** so we don’t have to manually validate subscription requests later in the tutorial. Scroll down and select **Next**.

<figure><img src="../../.gitbook/assets/image (4) (1).png" alt=""><figcaption></figcaption></figure>

On the security page, select the **Signature** that your IdP uses to encrypt your access tokens.

<figure><img src="../../.gitbook/assets/image (5) (1).png" alt=""><figcaption></figcaption></figure>

Next, you need to tell the Gravitee Gateway where it can retrieve the JSON web key set (JWKS) to validate the signature with a public key. Typically, in a production setup, you want to use JWKS URL as it is more secure and eliminates the need to update the resolver when you rotate keys.

A JWKS URL must be provided by your IdP of choice. Copy the endpoint and return to APIM’s Console UI. Under **JWKS resolver**, select **JWKS\_URL** and then paste the endpoint in the **JWKS\_URL** input box.

<figure><img src="../../.gitbook/assets/image (6) (1).png" alt=""><figcaption></figcaption></figure>

Scroll down and also toggle on **Extract JWT Claims**. This essentially makes all the claims associated with the token available through Gravitee’s Expression Language (EL). This is useful for configuring additional policies such as Role-based Access Control.

For this quick tutorial, everything else can be left as default. Scroll to the bottom of the page and select **Next** to be taken to the **Restrictions** page where you can add rate limiting, quotas, or resource filtering as part of the plan creation process. If desired, these restrictions can also be added later in the Policy Studio.

We won’t be adding any restrictions to the consumption of this API so simply select **Create** on the Restrictions page.

<figure><img src="../../.gitbook/assets/image (7) (1).png" alt=""><figcaption></figcaption></figure>

After creating a plan, it’s initially in the first of the four stages of a plan: staging, published, deprecated, and closed.

* **Staging**: This is the first stage of a plan. View it as a draft mode. You can configure your plan, but it won’t be accessible to users.
* **Published**: Once your plan is ready, you can publish it to let API consumers view and subscribe on the APIM Developer Portal and consume the API through it. A published plan can still be edited.
* **Deprecated**: You can deprecate a plan so that it won’t be available on the APIM Developer Portal and API Consumers won’t be able to subscribe to it. Existing subscriptions remain, so it doesn’t impact your existing API consumers.
* **Closed**: Once a plan is closed, all associated subscriptions are closed too. This cannot be undone. API consumers subscribed to this plan won’t be able to use your API.

<figure><img src="../../.gitbook/assets/image (8) (1).png" alt=""><figcaption></figcaption></figure>

Publish your plan by selecting the publish icon on your plan as shown below.

<figure><img src="../../.gitbook/assets/image (9) (1).png" alt=""><figcaption></figcaption></figure>

At this point, it is likely you have both a Keyless and a JWT plan published. Please delete any Keyless plans to ensure the JWT plan can not be bypassed. Select the **X** icon and then follow the prompts in the modal to delete the Keyless plan as shown below:

<figure><img src="../../.gitbook/assets/image (18) (1).png" alt=""><figcaption></figcaption></figure>

### Redeploying your API <a href="#redeploying-your-api-7" id="redeploying-your-api-7"></a>

As you make modifications to your Gateway API in the Console UI, you will see an orange banner appear that states your API is out of sync. This is because changes you make in the Console UI are not actually synced to the Gateway until you manually redeploy it. Once ready, select **Deploy API** in the banner and then **Deploy** in the subsequent modal to sync your latest changes to the Gravitee Gateway.

<figure><img src="../../.gitbook/assets/image (19) (1).png" alt=""><figcaption></figcaption></figure>

### Subscribe to the JWT Plan <a href="#subscribe-to-the-jwt-plan-8" id="subscribe-to-the-jwt-plan-8"></a>

APIM uses the subscription to decide whether to accept or deny an incoming request. Subscriptions are created when an API consumer uses a registered Gravitee application to create a subscription request to a published plan, and an API publisher either manually or automatically validates the subscription. So now that we have created a plan as an API producer, we need to subscribe as an API consumer.

#### Publish API <a href="#publish-api-9" id="publish-api-9"></a>

First, ensure your API is visible in the developer portal by selecting **General** in the Console UI sidebar and scrolling down to the bottom. In the **Danger Zone**, the API must be published which grants visibility to all members of your API (members are managed under User and group access). Additionally, you can make your API public which makes it visible to anybody who has access to your Developer Portal.

<figure><img src="../../.gitbook/assets/image (20) (1).png" alt=""><figcaption></figcaption></figure>

#### Access Developer Portal <a href="#access-developer-portal-10" id="access-developer-portal-10"></a>

With that completed, let’s head to the Developer Portal by selecting the Developer’s Portal link in the top navigation bar of the Console UI. The Developer Portal is a web application that acts as a centralized API catalog for internal/external API consumers to discover, find, and subscribe to APIs that are developed, managed, and deployed by API publishers.

**Accessing the Developer Portal**

If you do not see a link in your deployment of APIM, please reference the respective installation docs to see how it’s deployed. For example, with default docker installation, you can access the Developer Portal at `localhost:8085` in your browser.

<figure><img src="../../.gitbook/assets/image (21) (1).png" alt=""><figcaption></figcaption></figure>

#### Create an Application <a href="#create-an-application-11" id="create-an-application-11"></a>

Before subscribing, we need to create a Gravitee application with the same `client_id` as the application you create with your IdP. This is because the Gravitee Gateway will validate the JWT signature and validate the JWT contains a valid `client_id`. A valid `client_id` means there is a Gravitee application with an approved subscription to the JWT plan and has a `client_id` matching the `client_id` in the JWT itself.

**Dynamic Client Registration**

For the sake of this demo, we will be creating a Simple application in the Developer Portal that allows API consumers to define their own `client_id`. However, this is not secure and should not be used outside of testing. Therefore, Gravitee allows you to disable Simple applications and [use dynamic client registration (DCR) to create advanced applications](https://documentation.gravitee.io/apim/v/4.3/guides/api-exposure-plans-applications-and-subscriptions/applications#dcr-application-configuration). DCR essentially allows Gravitee to outsource the issuer and management of application credentials to a third party IdP, allowing for additional configuration options and compatibility with various OIDC features provided by the IdP.

In the Developer Portal, select **Applications** in the top navigation bar and then select **+ Create an app** in the top right of the screen.

<figure><img src="../../.gitbook/assets/image (22) (1).png" alt=""><figcaption></figcaption></figure>

Provide a name and description then select **Next**. On the security screen, select a Simple application and provide a `client_id` that matches the `client_id` of your IdP’s application. For example, in Okta, you can find your `client_id` right next to the name of your application.

<figure><img src="../../.gitbook/assets/image (23) (1).png" alt=""><figcaption></figcaption></figure>

After providing the `client_id`, select **Next**.

<figure><img src="../../.gitbook/assets/image (24) (1).png" alt=""><figcaption></figcaption></figure>

On the **Subscription** page, you can directly search for your Gateway API and see the available plans. Search for your API, select **Subscribe**, and then select **Next**.

<figure><img src="../../.gitbook/assets/image (63).png" alt=""><figcaption></figcaption></figure>

Finally, you can see an overview of your new Gravitee application. After careful review, select **Create the App** to create your application.

<figure><img src="../../.gitbook/assets/image (64).png" alt=""><figcaption></figcaption></figure>

Bravo! Since your JWT plan has auto-validation enabled, your application is now approved to send requests through Gravitee’s Gateway to access the protected resources. To test, include the `Authorization: Bearer <your_jwt_token_here>` HTTP header with your request to the Gateway:

```
curl -H "Authorization: Bearer your_jwt_here" https://your-gateway-domain/gateway-api-context
```
