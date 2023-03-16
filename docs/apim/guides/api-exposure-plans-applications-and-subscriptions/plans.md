---
description: How to expose your APIs
---

# Plans

### Create a plan

Plans are always created by the API publisher. You can create plans in the management UI as part of the [API creation process](../../user-guide/publisher/create-api.md#create-an-api-from-scratch). You can also create them later with the **Portal > Plans** function as shown below.

{% @arcade/embed flowId="L3b4AWtxtYkNE89ZiR2Y" url="https://app.arcade.software/share/L3b4AWtxtYkNE89ZiR2Y" %}

Creating a plan begins by navigating to your API, selecting **Plans** in the sidebar, and then selecting **Add new plan** in the top right of the page.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.36.23 PM.png" alt=""><figcaption><p>Create a new plan</p></figcaption></figure>

This will take you to the plan creation wizard.&#x20;

Creating a plan is broken down into three main stages:

1. **General**
2. **Secure**&#x20;
3. **Restrictions**

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.37.47 PM.png" alt=""><figcaption><p>Plan creation wizard</p></figcaption></figure>

#### General

In the **General** stage, you enter basic details about your plan. The only requirement for this stage is providing a name for your plan.

The initial section lets you set a name, description, and characteristics for your plan. Characteristics are optional labels you can use to tag your plan. &#x20;

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 12.49.56 PM.png" alt=""><figcaption><p>First step in plan creation</p></figcaption></figure>

The next section in the **General** stage is **Conditions.** Here you can optionally select a page containing the general conditions for use of your plan. If included, these conditions must be accepted by the user to finalize the subscription process. To associate general conditions of use with a plan, you need to specify a markdown page where these conditions are specified.&#x20;

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 12.55.52 PM.png" alt=""><figcaption><p>Selecting general conditions for your plan</p></figcaption></figure>

To create a general conditions plan, navigate to the **Documentation** page and select the plus icon in the bottom right. You must create a markdown page and publish it to use as the general conditions page of your plan.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 12.57.42 PM.png" alt=""><figcaption><p>Creating general conditions for a plan</p></figcaption></figure>

The **Subscriptions** section lets you configure basic settings around a subscription for plans requiring authentication.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.07.37 PM.png" alt=""><figcaption><p>Basic subscription setting</p></figcaption></figure>

Toggling **Auto validate subscription** means you will **** accept any and all subscriptions to a plan without the API publisher's review. These subscriptions can be modified at any time.

You can require all subscription requests from API consumers to include a comment detailing their request. Additionally, with this option enabled, the API publisher can leave a default message explaining what is expected in the API consumer's comment.

The final two sections in the **General** stage are **Deployment** and **Access-Control**.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.10.04 PM.png" alt=""><figcaption><p>Deployment and Access-Control settings</p></figcaption></figure>

The **Deployment** section allows you to selectively deploy the plan to particular APIs using sharding tags which you can learn more about [here](../../getting-started/configuration/configure-sharding-tags-for-your-gravitee-api-gateways.md).

**Access-Control** lets you **** prevent specified groups from accessing this plan. You can learn more about user management and how to configure groups here.

#### Secure

During the **Secure** stage of plan creation, the API publisher selects one of four authentication types to secure their API. You can learn more about how to configure plan security in the following section.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.49.42 PM.png" alt=""><figcaption><p>Select authentication type</p></figcaption></figure>

* **Keyless (public):**  does _not_ require authentication and allows public access to the API. By default, keyless plans offer no security and are most useful for quickly and easily exposing your API to external users and getting their feedback.&#x20;
* **API key:** only allows apps with approved API keys to access your API. This plan type ensures that API keys are valid, are not revoked or expired, and are approved to consume the specific resources associated with your API.
* **JSON web token (JWT):** open method for representing claims securely between two parties. JWT are digitally-signed using HMAC shared keys or RSA public/private key pairs. JWT plans allow you to verify the signature of the JWT and check if the JWT is still valid according to its expiry date.
* **Oauth 2.0:** open standard that apps can use to provide client applications with secure delegated access. OAuth works over HTTPS and authorizes devices, APIs, servers, and applications with access tokens rather than credentials.

#### Restrictions

Restrictions are just policies to regulate access to your APIs. Like any policy, restrictions can also be applied to a plan through the design studio. You can learn more about configuring these particular policies here.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.52.54 PM.png" alt=""><figcaption><p>Configure restrictions</p></figcaption></figure>

* **Rate Limiting:** limit how many HTTP requests an application can make in a specified period of seconds or minutes. This policy is meant to help avoid unmanageable spikes in traffic.
* **Quota:** specifies the number of requests allowed to call an API backend during a specified time interval. The policy is generally used to tier access to APIs based on subscription level.
* **Resource Filtering:** limit access to a subset of API resources

### Configure plan security

The most important part of plan configuration is security. APIM supports the following four authentication types:

* Keyless (public)
* API Key
* JWT
* OAuth 2.0

{% hint style="info" %}
**Policies vs authentication types**

Authentication types are simply policies integrated directly into a plan. Once a plan is created, the authentication type can not be changed. However, you can always add additional security at the API or plan level with policies in the design studio.
{% endhint %}

#### Keyless plan

The Keyless **** authentication type **** does _not_ require authentication and allows public access to the API. By default, keyless plans offer no security and are most useful for quickly and easily exposing your API to external users and getting their feedback. Due to not requiring a subscription and a lack of a consumer identifier token, keyless consumers are set as `unknown application` in the API analytics section.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 1.39.10 PM.png" alt=""><figcaption><p>Keyless authentication type</p></figcaption></figure>

{% hint style="info" %}
**Basic authentication and keyless plans**

You can configure basic authentication for keyless plans, by associating a basic authentication policy with either an LDAP or inline resource. For more details, see [Basic authentication policy](https://docs.gravitee.io/apim/3.x/apim\_policies\_basic\_authentication.html).
{% endhint %}

#### API key plan

The API key authentication type enforces verification of API keys during request processing, allowing only apps with approved API keys to access your APIs. This plan type ensures that API keys are valid, are not revoked or expired, and are approved to consume the specific resources associated with your API.

API key plans offer only a basic level of security, acting more as a unique identifier than a security token. For a higher level of security, see JWT and OAuth 2.0 plans below.

When configuring API key authentication, there are two main options:

* **Propogate API key to upstream API:** toggling this setting on ensures the request to the backend API includes the API key header sent by the API consumer. This is setting is useful for backend APIs that already have integrated API key authentication.
* **Additional selection rule:** this setting allows you to use Gravitee Expression Language (EL) to filter by contextual data (request headers, tokens, attributes, etc.) for plans of the same type. For example, if you have two API key plans, you can set different selection rules on each plan to determine which plan handles each request.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 3.22.29 PM.png" alt=""><figcaption><p>API key plan configuration</p></figcaption></figure>

Typically, API keys are randomly generated for each subscription. However, Gravitee provides two other options for API key generation: custom API key and shared API key. Both of these settings can be enabled at the environment level by selecting **Settings** in the main sidebar and then selecting **Settings** again under the **Portal** group in the nested sidebar.

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 3.49.04 PM.png" alt=""><figcaption><p>API key generation settings</p></figcaption></figure>

{% tabs %}
{% tab title="Custom API key" %}
You can specify a custom API key for an API key plan. This is particularly useful when you want to silently migrate to APIM and have a pre-defined API key. The custom API key must have more than 8 characters, less than 64 characters, and be URL compliant. `^ # % @ \ / ; = ? | ~ , space` are all invalid characters.

When prompted, you can choose to provide your custom API key or let APIM generate one for you by leaving the field empty.

You can provide a custom API key when:

* Creating a subscription

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 3.54.21 PM.png" alt=""><figcaption><p>Manually creating a subscription</p></figcaption></figure>

* Accepting a subscription

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 3.57.18 PM.png" alt=""><figcaption><p>Accepting a subscription</p></figcaption></figure>

* Renewing a subscription

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-15 at 3.58.35 PM.png" alt=""><figcaption><p>Renewing a subscription</p></figcaption></figure>
{% endtab %}

{% tab title="Shared API key" %}
The shared API key mode allows consumers to reuse the same API key across all API subscriptions of an application.&#x20;

With this mode enabled, consumers will be asked on their second subscription to choose between reusing their key across all subscriptions or generating one different API key for each subscription (which is the default mode). This is known as the application API key type.

{% hint style="info" %}
**Shared API key limitations**

For technical reasons, in shared mode, API keys can only be shared across API key plans that belong to distinct gateway APIs. Therefore, if you attempt to subscribe to two API key plans on the same gateway API, no prompt will be made to choose the application API key type and the default mode will be used automatically.
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/shared-api-key-2-portal.png" alt=""><figcaption><p>Subscribing in the developer portal</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Screen Shot 2023-03-16 at 11.44.51 AM.png" alt=""><figcaption><p>Subscribing in the managment UI</p></figcaption></figure>

This choice is _permanent_ for that application and consumers will not be able to switch between application API key types after the initial decision.

When disabling the shared API key mode in environment settings, applications that have already been configured to use a shared key will continue to work this way, but consumers will stop being asked to choose between one mode or the other on their second subscription.

{% hint style="warning" %}
**Missing API key type selection menu?**

Shared API key mode must be enabled in settings before creating an application in order to have this option show up. If you are having issues, the best option is to create a new application and immediately subscribe to two API key plans.
{% endhint %}

Shared API key mode also has an important consequence you should be aware of before enabling. Because the shared API key may be used to call APIs that are owned by another group of API publishers, shared API keys cannot be edited from the API publisher subscription view. So while shared API keys are still readable by API publishers, renewal and revocation of shared API keys cannot be performed by the API publisher when a subscription has been made in shared API key mode.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/shared-api-key-3.png" alt=""><figcaption><p>Shared API key adminstration limitations</p></figcaption></figure>

Instead, it is the responsibility of the application owner to perform such operations, and for this reason, shared API keys can only be revoked from the application owner subscription view in either the management UI or the developer portal.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/shared-api-key-4.png" alt=""><figcaption><p>Manage shared API key in the management UI</p></figcaption></figure>

<figure><img src="https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/shared-api-key-4-portal.png" alt=""><figcaption><p>Manage shared API key in the developer portal</p></figcaption></figure>

{% hint style="info" %}
**Shared API key limitations**

For technical reasons, in shared mode, API keys can only be shared across API key plans that belong to distinct gateway APIs. Therefore, if you attempt to subscribe to two API key plans on the same gateway API, no prompt will be made to choose the application API key type and the default mode will be used automatically.
{% endhint %}
{% endtab %}
{% endtabs %}

#### JSON Web Token (JWT) plan

The JWT authentication type ensures that JWTs issued by third parties are valid. Only applications with approved JWTs can access APIs associated with a JWT plan.

[JSON Web Tokens](https://tools.ietf.org/html/rfc7519) are an open method for representing claims securely between two parties. JWTs are digitally signed using HMAC shared keys or RSA public/private key pairs. JWT plans allow you to verify the signature of the JWT and check if the JWT is still valid according to its expiry date.

JWT defines some [registered claim names](https://tools.ietf.org/html/rfc7519#section-4.1) including subject, issuer, audience, expiration time, and not-before time. In addition to these claims, the inbound JWT payload must include the `client_id` claim (see below) to establish a connection between the JWT and the APIM application subscription.

The policy searches for a client ID in the payload as follows:

* First in the `azp` claim
* Next in the `aud` claim
* Finally in the `client_id` claim

**Add JWT security to a plan**

1. In APIM Console, select your API and click **Portal > Plans**.
2. On the **Secure** page, choose **JWT** as the authorization type.
3.  Specify the public key used to verify the incoming JWT token.

    |   | You can also set the public key in the `gravitee.yml` file. See [JWT policy](https://docs.gravitee.io/apim/3.x/apim\_policies\_jwt.html) for more information. APIM only supports the RSA Public Key format. |
    | - | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

    ![create jwt plan](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/create-jwt-plan.png)

Your API is now JWT secured and consumers must call the API with an `Authorization Bearer :JWT Token:` HTTP header to access the API resources.



#### Oauth 2.0

To configure an OAuth 2.0 plan for an API, you need to:

* create an OAuth 2.0 client resource that represents your OAuth 2.0 authorization server
* create a new plan for it or apply it to an existing plan

**Create and specify an OAuth 2.0 authorization server**

|   | The instructions below explain how to create an OAuth 2.0 resource in Design Studio. For APIs not migrated to Design Studio, you can create resources with the **Design > Resources** menu option. |
| - | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

1. Open your API in APIM Console and click **Design**.
2.  Click the **RESOURCES** tab and create a new **Generic OAuth2 Authorization Server** resource.

    |   | If you use [Gravitee.io Access Management](https://gravitee.io/), we provide a dedicated OAuth 2.0 AM resource. |
    | - | --------------------------------------------------------------------------------------------------------------- |

    ![Gravitee.io - Create OAuth 2.0 resource](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/create-oauth2-resource.png)
3. Enter the **Resource name**.
4. Set the **OAuth 2.0 Authorization server URL**.
5. Set the [Token introspection endpoint](https://tools.ietf.org/html/rfc7662) URI with the correct HTTP method and [scope](https://tools.ietf.org/html/rfc6749#section-3.3) delimiter.
6. Enter the **Scope separator**.
7. If you want to retrieve consented claims about the end user, enter the [UserInfo Endpoint](http://openid.net/specs/openid-connect-core-1\_0.html#UserInfo) URI.
8.  Enter the **Client Id** and **Client Secret** used for token introspection.

    |   | Why do I need this? As defined in [RFC 7662](https://tools.ietf.org/html/rfc7662#section-2.1), to prevent token scanning attacks, the introspection endpoint must also require some form of authorization to access this endpoint, such as client authentication. |
    | - | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
9. Enter any other required information, then click the tick icon ![tick icon](https://docs.gravitee.io/images/icons/tick-icon.png).
10. Click **SAVE** to save the resource.

**Add OAuth 2.0 security to a plan**

|   | If you already have a suitable plan defined, you can add your OAuth2 resource to one of the flows defined for it in Design Studio, by following the steps in [Add policies to a flow](https://docs.gravitee.io/apim/3.x/apim\_publisherguide\_design\_studio\_create.html#flow-policies). |
| - | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

1. In APIM Console, select your API and click **Portal > Plans**.
2. On the **Secure** page, choose **OAuth2** as the authorization type.
3.  Specify the OAuth2 resource name you created and check any [scopes](https://tools.ietf.org/html/rfc6749#section-3.3) to access the API.

    ![create oauth2 plan](https://docs.gravitee.io/images/apim/3.x/api-publisher-guide/plans-subscriptions/create-oauth2-plan.png)

Your API is now OAuth 2.0 secured and consumers must call the API with an `Authorization Bearer :token:` HTTP header to access the API resources.

|   | Any applications wanting to subscribe to an OAuth 2.0 plan must have an existing client with a valid `client_id` registered in the OAuth 2.0 authorization server. The `client_id` will be used to establish a connection between the OAuth 2.0 client and the APIM consumer application. |
| - | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

### Publish a plan

Similar to an API, a plan can also be published. Publishing is one of four stages of a plan: staging, published, deprecated, and closed.

* **Staging** - Generally, this is the first state of a plan. View it as a draft mode. You can configure your plan but it won’t be accessible to users.
* **Published** - Once your plan is ready, you can publish it to let API consumers view and subscribe on the APIM Portal and consume the API through it. A published plan can still be edited.
* **Deprecated** - You can deprecate a plan so it won’t be available on the APIM portal and API Consumers won’t be able to subscribe to it. Existing subscriptions remains so it doesn’t impact your existing API consumers.
* **Closed** - Once a plan is closed, all associated subscriptions are closed too. This can not be undone. API consumers subscribed to this plan won’t be able to use your API.

<figure><img src="https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/6/6333ad2d86aae2ceb0cac422dd9015c75c3e6fb5_2_689x197.png" alt=""><figcaption><p>Four stages of a plan</p></figcaption></figure>

> ![:bulb:](https://emoji.discourse-cdn.com/twitter/bulb.png?v=12) **The Benefits of Deprecation**
>
> ***
>
> Take a moment to try and open the [todo application](http://localhost:3000/). It should no longer be functional as the **Open** plan it depended on was closed. Typically, this is why an API producer would elect to deprecate existing plans. It allows consumers of the API time to migrate without breaking their application while also ensuring new users do not subscribe to the deprecated plan.

Click the **plus icon** in the bottom right to create a new plan. Input a name and description for the new plan similar to ours below. Everything else on the define page can remain blank or use the default option. Scroll down and click **Next**.

[![Screen Shot 2023-02-16 at 4.06.08 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/6/630dc132cdd79e61d430b858cfd956fe3f9937d6\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/6/630dc132cdd79e61d430b858cfd956fe3f9937d6.png)

Select **API Key** from the **authentication type dropdown** and proceed to the next page. At this point, we don’t need any additional restrictions on this plan so just click **Save** on the last page.

[![Screen Shot 2023-02-16 at 4.08.54 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/2/2b7e8cf2f60ed52e56d3b4482490b52ad58344fe\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/2/2b7e8cf2f60ed52e56d3b4482490b52ad58344fe.png)

Excellent, we have our new plan ready to go in the staging area. For now, let’s leave it in the staging area and navigate back to the general page of our Dev Guide API. Deploy the API to sync the recent changes then publish the API using the option in the ![:warning:](https://emoji.discourse-cdn.com/twitter/warning.png?v=12) danger zone ![:warning:](https://emoji.discourse-cdn.com/twitter/warning.png?v=12).

[![Screen Shot 2023-02-16 at 4.12.23 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/a/a798336659267cbe13c706ce651bb14f900d2c03\_2\_690x311.jpeg)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/a/a798336659267cbe13c706ce651bb14f900d2c03.jpeg)

Okay, time to check out the [developer portal](http://localhost:8085/). Use `admin` for the username and password if you’re asked to login. Once there, navigate straight to **Catalog** and then **All APIs** in the submenu to see the published API in all of its glory.

[![Screen Shot 2023-02-16 at 4.25.13 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/8/84b18001a50959dc764d38ee5f714669ac8f4466\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/8/84b18001a50959dc764d38ee5f714669ac8f4466.png)

Click **View API** to see what details about the API are exposed in the portal. From the perspective of the consumer, this acts as the API’s homepage which provides documentation, a method to contact support, issue tracking, reviews from other consumers, and most importantly, a way to subscribe to the API. Click the **Subscribe** button in the top right to get started.

[![Screen Shot 2023-02-16 at 7.59.25 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/0/0fafad3f66ab0cfc124dbff69a1d0b764d2e53b3\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/0/0fafad3f66ab0cfc124dbff69a1d0b764d2e53b3.png)

So where’s our plan with API key authentication we just created? If you remember, we never actually published the plan. Also, those of you with sharp eyes may notice that the **Access URL** shown in the sidebar has a placeholder domain. Let’s return to the management console for a moment to resolve both of these issues.

First, we’ll show you how to modify the default access url of your API. Click on **Organization** in the sidebar of the management console. Next, click on **Sharding tags** in the sidebar under the **Gateway** subheader. This page allows you to modify the default entrypoint of the gateway which is `https://localhost:8082` for this tutorial’s architecture.

> ![:bulb:](https://emoji.discourse-cdn.com/twitter/bulb.png?v=12) **Sharding Tags and Gateway Entrypoint Mappings**
>
> ***
>
> At a high-level, sharding tags are assigned to APIs and Gravitee gateways to provide a method to deploy an API to a subset of gateways. Adding a mapping between these sharding tags and a gateway’s entrypoint url allows the developer portal to intelligently display different entrypoints depending on the API’s sharding tags.
>
> Sharding tags are used to help manage complex distributed architectures. If you want to learn more, we highly recommend reading Gravitee’s very own @nicobalestra’s [blog on the topic](https://www.gravitee.io/blog/manage-complex-environments-sharding-tags).

[![Screen Shot 2023-02-23 at 1.45.18 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/8/8d8cf9a2ba0a7827d0069e7c08fe168982936911\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/8/8d8cf9a2ba0a7827d0069e7c08fe168982936911.png)

Next, let’s publish our plan.

[![Screen Shot 2023-02-16 at 8.02.00 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/7/770659411800cefac6dd0eea8374be2dc06c55ee\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/7/770659411800cefac6dd0eea8374be2dc06c55ee.png)

Publishing a plan is as simple as clicking the **Publish Plan** button, confirming your desire to publish the plan with the modal that appears on your screen, and deploying your API again to synchronize the changes. With that, return to the developer portal and refresh the page to be greeted by the new and improved page shown below.

[![Screen Shot 2023-02-23 at 1.47.48 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/3/3d7ff98275f65dc11d888385427539fa9d31355e\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/3/3d7ff98275f65dc11d888385427539fa9d31355e.png)

Our **API Key Plan** is summarized in the image above: subscriptions require _manual validation_ and authentication is dependent on a _personal key_. Manual validation refers to the fact that the API publisher has elected to manually approve every subscription to this plan as opposed to auto validation. A plan can easily be created or updated to use auto validation by using the **Auto validate subscription** toggle as shown in the image below.

[![Screen Shot 2023-02-16 at 8.08.42 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/a/aa13b67ac923431c0248a972eb739bd23eb769c6\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/a/aa13b67ac923431c0248a972eb739bd23eb769c6.png)

As for the personal key authentication, we’ll double back to that in just a minute. Click **Next** to be greeted by the following roadblock:

[![Screen Shot 2023-02-23 at 1.54.32 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/2/243246689fa0d391138d0f5bb9a6dea8af0b0335\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/2/243246689fa0d391138d0f5bb9a6dea8af0b0335.png)

If this is your first time subscribing to an API plan with authentication enabled, an application may seem like a strange requirement just to access an API. Previously with the keyless plan, anyone on the network had the ability to start sending requests to the API, no application necessary. However, with authentication enabled, it is important for the API producer to be aware of all consumers of the API. If one consumer turns out to be a bad actor engaging in malicious activity, then producers require more granular control to revoke access for that one consumer instead of shutting the API down for all users. Additionally, more advanced authentication methods like OAuth 2.0 require the client to provide information such as a client id when subscribing. These more advanced methods will be detailed in a future tutorial.

So how are subscriptions monitored? Well, through _applications_ of course! Applications and plans go together like developers and repurposing code from stack overflow. Remember, plans are an access layer around APIs that provide the API producer a method to secure, monitor, and transparently communicate details around access. An application allows an API consumer to register and agree to this plan. The result is a successful contract or _subscription_.

So let’s make an application from the developer portal by clicking the aptly named **I want to create an application** link. Provide a name and description for your application and click **Next**.

[![Screen Shot 2023-02-17 at 1.22.30 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/9/9f2c6d954f08482c8bd0512b328f32a834b301e5\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/9/9f2c6d954f08482c8bd0512b328f32a834b301e5.png)

Because we’re using a more basic form of authentication, the only option on the **Security** page is a simple application. Creating a browser, web, native, or backend-to-backend application requires enabling [dynamic client registration](https://docs.gravitee.io/am/current/am\_userguide\_dynamic\_client\_registration.html) as detailed in [the docs](https://docs.gravitee.io/apim/3.x/apim\_consumerguide\_manage\_applications.html#prerequisites).

For this tutorial, leave everything blank and click **Next** again. This will take you to the **Subscription** page where you have the option to request a subscription to any available plans. For now, that is limited to the singular **API Key Plan** tied to the **Dev Guide API**. Click **Subscribe**, add a comment if you’d like, and click **Next** one more time. This should take you to the final page shown below where you can click **Create the App**.

[![Screen Shot 2023-02-17 at 1.31.20 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/5/5f840477110d2da207008673192f828ca8bd8e45\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/5/5f840477110d2da207008673192f828ca8bd8e45.png)

Easy enough. We were able to complete the application and subscription request in one go. So where’s the API key? If we navigate to the **Applications** tab, then the **Subscriptions** tab on the submenu, we can see the subscription is still awaiting approval.

[![Screen Shot 2023-02-17 at 1.34.51 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/6/643caf6873231077f974ba5c90737fb0697eb283\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/6/643caf6873231077f974ba5c90737fb0697eb283.png)

To quickly approve that subscription, return to the management console and click on your profile icon in the top right. Select the **Task** option that appears in the dropdown to navigate to the following page.

[![Screen Shot 2023-02-20 at 1.31.08 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/1/1adb13370733ef8d510f26ba1ae048d9c97fa009\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/1/1adb13370733ef8d510f26ba1ae048d9c97fa009.png)

Next, click **Validate** to be taken taken to the subscription requests page. This provides all the high-level details about any subscription requests including the user and application making the request. Clicking **Accept** returns the modal shown in the image below where you can set an expiration date on the subscription. For our use case, leave that blank and confirm the subscription. An API producer can pause, close, or add an expiration date to a subscription at any time.

[![Screen Shot 2023-02-20 at 1.34.32 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/f/f2825ef1077bdfca97e4e4b35898f830a70255e1\_2\_690x311.jpeg)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/f/f2825ef1077bdfca97e4e4b35898f830a70255e1.jpeg)

The following page is shown after accepting the subscription. Most importantly, the API key to be used for authentication in future requests is shown with the ability to renew, revoke, or set an expiration date on the API key itself, as opposed to on the actual subscription. Generally, it is good practice to rotate the means of authentication on a regular basis instead of providing long-lived access tokens like this static API key.

[![Screen Shot 2023-02-20 at 1.37.27 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/6/6709f0f781e8210ec41bb5f81bb49a9e81234c8f\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/6/6709f0f781e8210ec41bb5f81bb49a9e81234c8f.png)

If you scroll up to the top of the page, you can click on the **Back to subscriptions** link to see a list of all current, pending, paused, and closed subscriptions. Currently, you should only see the subscription we just approved. However, there are a number of filtering mechanisms provided for managing more popular APIs that may include a number of different types of plans.

[![Screen Shot 2023-02-20 at 1.44.34 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/b/bcc7f130fe0f52862ac42ac6a2cd0298d75239b6\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/b/bcc7f130fe0f52862ac42ac6a2cd0298d75239b6.png)

With the subscription approved, we can switch our perspective back to that of the API consumer and return to the developer portal. Refreshing the “Subscriptions” tab under the “Internal Consumer” application shows the accepted subscription. Click anywhere on the row to reveal the API key.

[![Screen Shot 2023-02-20 at 1.49.46 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/2/2c3f030c8cd56d9dd34e5a1f4f21d2cb0c59092b\_2\_690x311.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/2/2c3f030c8cd56d9dd34e5a1f4f21d2cb0c59092b.png)

Excellent! Now we just need a way to pass this API key to our todo application. Feel free to take a look at the source code for the todo app, but essentially, each API call is passing a header with the following key-value pair:

`"X-Gravitee-Api-Key": process.env.REACT_APP_API_KEY`

where `"X-Gravitee-Api-Key"` is the default API key header accepted by the Gravitee gateway. If needed, this header can be customized as [outlined in the docs](https://docs.gravitee.io/apim/3.x/apim\_policies\_apikey.html#gateway).

To successfully authenticate, we need to provide a value for the `REACT_APP_API_KEY` environment variable as it is currently undefined. There are two steps to passing environment variables to our application:

1. Create a `.env` file with the correct key-value pair
2. Modify the docker-compose.yml file to pass the environment variables to individual containers

The first step is easy enough. Simply create a `.env` file in the root directory of the cloned repo then copy and paste this key-value pair:

`REACT_APP_API_KEY="your-api-key-string"`

Next, open the docker-compose file and uncomment lines 55 and 56 to pass the environment variable to the `app-frontend` container.

[![Screen Shot 2023-02-20 at 7.37.00 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/f/fc7b73263405e7a08072858a2e3786913f4fe6bb\_2\_690x260.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/f/fc7b73263405e7a08072858a2e3786913f4fe6bb.png)

Finally, save the files and run `docker-compose up -d` to rebuild and restart the necessary containers. If you return to the [todo application](http://localhost:3000/), you should be greeted by the fruits of your labor: a functioning todo app using API key authentication!

[![Screen Shot 2023-02-20 at 7.40.24 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/2/2646c8286ba91a81a1bf4a2d8463b47218b6c5ac\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/2/2646c8286ba91a81a1bf4a2d8463b47218b6c5ac.png)

### External Exposure <a href="#external-exposure-4" id="external-exposure-4"></a>

The workflow demonstrated in the Internal Exposure section works great for API publishers and API consumers working at the same company. But what if the API publishers wanted to expose APIs to external consumers? This is a common use case when developers are looking to monetize their APIs so let’s dive into the details of how to set this up.

First, open the management console and navigate back to the **Dev Guide API’s** plans. We’re going to quickly create and publish a new plan for external consumers. This plan will use the same API key authentication as our **API Key Plan**, and for now, the will only the change will be to the name and description. Sticking with our history of creative names, we’ll call the new plan **External API Key Plan**. You’re witnessing poetry in motion.

Build the plan in the console and publish it. Your plans page should now look like the following:

[![Screen Shot 2023-02-23 at 2.26.36 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/e/e89e8db222168f6007715ad709766dc1db54928d\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/e/e89e8db222168f6007715ad709766dc1db54928d.png)

Now, in the previous section we simulated internal exposure of our API by using the same admin account for both the API producer and API consumer. However, external exposure necessitates the ability to create new accounts which requires some additional configuration. We’ll walk you through how to set that up.

The ability to create new user accounts has [two requirements](https://docs.gravitee.io/apim/3.x/apim\_consumerguide\_create\_account.html#prerequisites):

1. the “Allow User Registration” option enabled in settings
2. email [SMTP (simple mail transfer protocol) configuration](https://docs.gravitee.io/apim/3.x/apim\_installguide\_rest\_apis\_configuration.html#smtp-configuration)

User registration is already enabled by default, but emailing is disabled since it requires configuring an SMTP email service. To set that up, return to the management console and select **Settings** in the main menu and select **Settings** again under the **Portal** header in the submenu.

[![Screen Shot 2023-02-20 at 10.13.49 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/d/d033d41925c00cd1b56d9934ca774e89d4d118a2\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/d/d033d41925c00cd1b56d9934ca774e89d4d118a2.png)

Here, you can customize a number of aspects of the developer portal, but notice the warning at the top of the page. It essentially says the configuration file takes precedence. For example, if you scroll to the bottom of that page, you will see the SMTP settings, but the option to enable emailing is greyed out due to the previously mentioned configuration file.

[![Screen Shot 2023-02-20 at 10.11.35 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/a/abe13454c6d7c6a968428f085632edd92d44276c\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/a/abe13454c6d7c6a968428f085632edd92d44276c.png)

This configuration file is known as the `gravitee.yml` file. It is one of [three ways to configure settings for your APIM environment](https://docs.gravitee.io/apim/3.x/apim\_installguide\_rest\_apis\_configuration.html#overview): environment variables, system properties, and `gravitee.yml`, in order of precedence. We will be overriding these settings using environment variables, but first, we want to show you where in our docker installation the `gravitee.yml` file for APIM lives.

Open **Docker Desktop**, click on the `gio_apim_management_api` container, and switch to the **Terminal** tab. The `gravitee.yml` file lives in the `config` directory as shown in the image below. If you use the `cat` command to print the contents of the file, you will be able to search for and see the default SMTP settings.

> ![:bulb:](https://emoji.discourse-cdn.com/twitter/bulb.png?v=12) The gateway component has a separate `gravitee.yml` file.

[![Screen Shot 2023-02-22 at 11.43.42 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/f/f9048fa605cb73e34636e17358268f1f4e4e0193\_2\_690x261.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/f/f9048fa605cb73e34636e17358268f1f4e4e0193.png)\
[![Screen Shot 2023-02-20 at 10.38.06 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/1/18291fe9b031f5d3becfdc0c6750eeffc1f4b96d\_2\_690x277.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/1/18291fe9b031f5d3becfdc0c6750eeffc1f4b96d.png)

Rather than modify this file directly, we’re going to stick with our theme of using environment variables. Environment variables have precedence over the other two configuration types and allow us to define them in the same `.env` file we created earlier.

> ![:bulb:](https://emoji.discourse-cdn.com/twitter/bulb.png?v=12) **Gravitee Environment Variable Syntax**
>
> ***
>
> Unlike our `REACT_APP_API_KEY` environment variable which was injected into our todo application, these environment variables are being used to modify Gravitee specific configurations. You must ensure you use the correct syntax for each property:
>
> * Each level of indentation in the `gravitee.yml` file needs to be seperated by an underscore. For example, this inside a `gravitee.yml` file
>
> ***
>
> ```
> management:
>    Mongodb:
>       dbname: myDatabase
> ```
>
> ***
>
> **becomes** `gravitee_management_mongodb_dbname=myDatabase`
>
> * Some properties are case-sensitive and cannot be written in uppercase (for example, `gravitee_security_providers_0_tokenIntrospectionEndpoint`). Therefore, we advise you to define all Gravitee environment variables in lowercase.
> * In some systems, hyphens are not allowed in variable names. For example, you may need to write `gravitee_policy_api-key_header` as `gravitee_policy_apikey_header`.

Open the `.env` file created in the Internal Exposure section and add the following environment variables:

```
gravitee_email_enabled=true
gravitee_email_host=fqdn-smtp-service-provider.com
gravitee_email_username=your-email@your-email-host.com
gravitee_email_password=your-password
gravitee_email_from=your-email@your-email-host.com
```

where `fqdn-smtp-service-provider` (fqdn = fully qualified domain name) and `your-email-host` is dependent on the email service you would like to use (e.g. Gmail, Yahoo, etc.). For Gmail, they have several options as [detailed here](https://support.google.com/a/answer/176600?hl=en). The rest should be self-explanatory; however, if you are using two-factor authentication with Gmail, then you need to [generate an application password](https://security.google.com/settings/security/apppasswords). This password will be used in place of your standard account password for the `gravitee_email_password` environment variable.

Similar to before, once you’ve input your email information, you need to make sure the environment variables are passed to the `management_api` container. Open the `docker-compose.yml` file again and uncomment lines 141 and 142. Finally, save the files and run `docker-compose up -d` to rebuild and restart the necessary containers one more time.

[![Screen Shot 2023-02-20 at 11.09.46 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/5/5e88cbd9ab8cc9e67bcb48cf9e780cbdfbb3368a\_2\_690x322.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/5/5e88cbd9ab8cc9e67bcb48cf9e780cbdfbb3368a.png)

After you give the containers a chance to restart, you should be able to return to the management console to see your updated settings. You also now have the option to enable auth and TLS in the management console which is recommended.

[![Screen Shot 2023-02-20 at 11.15.11 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/9/96bc69d764fee7a570e2bb2b238424769d72ce1a\_2\_690x149.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/9/96bc69d764fee7a570e2bb2b238424769d72ce1a.png)

Alright, let’s test these new settings by attempting to create a new user. We recommend [opening the developer portal](http://localhost:8085/) in an incognito window to avoid being automatically signed out of the admin account being used in the management console. In the new incognito window, click **Sign in** then **Sign up**. Enter a name and functioning email.

[![Screen Shot 2023-02-20 at 11.27.01 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/4/423e485a2a5abd1477b326d9f795408e556dbe08\_2\_370x500.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/4/423e485a2a5abd1477b326d9f795408e556dbe08.png)

If all goes smoothly, you should get a registration confirmation and an email to the address you provided. Open the email and click on the link. Make sure the link opens in the incognito tab; otherwise, it will just open the developer portal with the admin account signed in.

You will taken to a page to finalize your account and add a password. By default, the password must meet the following requirements:

* 8 to 32 characters
* no more than 2 consecutive equal characters
* min 1 special characters (@ & # …)
* min 1 upper case character

> ![:bulb:](https://emoji.discourse-cdn.com/twitter/bulb.png?v=12) **Password Customization**
>
> ***
>
> Password requirements can be modified by changing the regex pattern under **User Management Configuration** in the `gravitee.yml` file or by using environment variables. Additionally, you can provide [custom UI errors](https://docs.gravitee.io/am/current/am\_userguide\_user\_management\_password\_policy.html#custom\_ui\_errors) for future new users by modifying the sign up and register HTML templates.

Once you finish creating your password, you should be able to sign in without issue. The newly created external user will also be immediately visible in the admin’s management console. Leave the incognito window and return to the standard window where you are singed in as an admin in the management console. In the sidebar menu, you can reach your organization settings by clicking on **Organization** at the bottom. Once there, navigate to the **Users** tab in the sidebar. Here you will see a list of all current users tied to the organization. As an admin, you can click on any user for more details and to apply administrative policies. Additionally, admins can pre-register users by clicking the **Add user** button in the top right.

[![Screen Shot 2023-02-23 at 1.55.44 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/7/712b65b5d81ff0459a41a4f2f76487611d5ce4f8\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/7/712b65b5d81ff0459a41a4f2f76487611d5ce4f8.png)

Next, click on **Applications** in the sidebar. Interestingly, you should see a new application called **Default application** which is owned by the user you just created.

[![Screen Shot 2023-02-21 at 12.26.03 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/1/186f0300a51db63b3fece375675232e15e40486e\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/1/186f0300a51db63b3fece375675232e15e40486e.png)

So why did the new user not have to create a first application like the admin? In order to allow new users to quickly move forward with API consumption, the default settings are every new user automatically has a default application created. This can be easily disabled through the aforementioned three configuration options.

To follow the wisdom of Gravitee’s creators and take advantage of this default setting meant to promote speed of API consumption, let’s quickly have our external user subscribe to the **Dev Guide API**. Return to the developer portal in the incognito tab and navigate to the **Dev Guide API** inside the catalog. Once there, we will subscribe to **External API Key Plan** just like we did previously with our internal consumer and the original **API Key Plan**. Complete and submit the subscription request.

[![Screen Shot 2023-02-23 at 2.34.45 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/5/5f399e12252a024dce57d56ce7b14e823e43eb03\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/5/5f399e12252a024dce57d56ce7b14e823e43eb03.png)

To approve this subscription, leave the incognito tab and return to the management console with the admin signed in. From there, navigate to the **Task** page shown under the profile dropdown in the top right. And just like before, validate this subscription request.

With the new subscription approved, let’s update the todo application to use the API key tied to the **External API Key Plan**. This will be at the bottom of the page as shown below.

[![Screen Shot 2023-02-23 at 2.52.09 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/b/b86752223c9815e7ead90f7ce97c5adbc104b12e\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/b/b86752223c9815e7ead90f7ce97c5adbc104b12e.png)

Copy the key and return to the `.env` file in the root of the cloned repo and update `REACT_APP_API_KEY` environment variable. Once again, save the files and run `docker-compose up -d` to rebuild and restart the necessary containers. Give the containers at least a minute to fully start back up. You can test the functionality by trying to create a new task in the [todo app](http://localhost:3000/). It should function exactly as it did before.

Once completed, you can return to the subscriptions page to see both active subscriptions.

[![Screen Shot 2023-02-23 at 2.36.58 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/f/f8bf594a92c21554196b989893ec2a3fae5f1aa5\_2\_690x312.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/f/f8bf594a92c21554196b989893ec2a3fae5f1aa5.png)

With this API now being used by to external consumers, we may want to consider using some additional policies to restrict how the API is used. We’ll do this by adding some policies to the **External API Key Plan** instead of directly to the API so the internal consumers are not impacted.

To illustrate a potential issue an we want to protect against, open the todo app and create a todo with the following text:

> Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry’s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

Your result should look similar to the image below.\


[![Screen Shot 2023-02-22 at 4.03.05 PM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/3/36c8b88099909c1f7ab1855e548370e56c638f5d\_2\_690x334.png)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/3/36c8b88099909c1f7ab1855e548370e56c638f5d.png)

Clearly, multi-line todos are causing some issues with the UI. This is an issue your internal users are aware of and know to avoid, but there is no way to ensure all external users are notified and comply with this restricted usage of the API. Your first thought is probably to update the UI, but let’s pretend that is not an option. Perhaps our hypothetical frontend developer does not have an immediate solution or is away vacationing deep in the Alps. To handle this, we’re going to create a new flow to restrict how much content external users can pass in a POST request to our todo application.

Click **Design** at the top of the page to access the Design Studio. If you completed Part 3 of the dev guide, you should see the API-level flow that implements rate limiting. Click on the empty flow beneath the **External API Key Plan**.

[![Screen Shot 2023-02-23 at 2.45.10 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/d/d4f4664da294aa531a556e0463a5ef1bf19e76fe\_2\_690x312.jpeg)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/d/d4f4664da294aa531a556e0463a5ef1bf19e76fe.jpeg)

Next, provide the flow a name and restrict it to the POST method. Then drag and drop the **Request Content Limit** policy from the sidebar into the **Request** part of the flow as shown below. In the policy settings, set the **Limit** to 175 then save and redeploy the API.

> ![:bulb:](https://emoji.discourse-cdn.com/twitter/bulb.png?v=12) **Request Content Limit Units**
>
> ***
>
> The limit specified for this policy is in number of octets (an octet is synonymous with a byte on most architectures). However, if your payload is text and is encoded using UTF-8 like this example, then you can assume each character is equal to one octet.

[![Screen Shot 2023-02-23 at 2.46.45 AM](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/optimized/2X/1/1b28aac714f87f5f81c5a0990f5acb7b9c8b83f4\_2\_690x312.jpeg)](https://europe1.discourse-cdn.com/business20/uploads/graviteeforum/original/2X/1/1b28aac714f87f5f81c5a0990f5acb7b9c8b83f4.jpeg)

Finally, return to the todo app and attempt to create a new todo with the same lorem ipsum block of text. You should receive an alert with a **HTTP 413 Content Too Large** response status code. Congrats! As a quick final note, flows can be paused be paused in the UI by hovering over the flow in the sidebar, clicking the toggle, saving, and redeploying the API.

Bravo. Both the internal and external consumers now have access to the API with different restrictions and authentication. However, it is worth noting that both types of consumer would likely be at a loss on how to actually use the API since we do not provide any API documentation. This is something we will be diving into deeper in a future tutorial as we explore things like Gravitee’s API designer that has the capability to generate documentation automatically. Additionally, we will be working with Gravitee’s access management offering to implement more advanced authentication with protocols like Oauth2.0 in the coming tutorials.

As always, please provide any feedback or requests you may have with a comment below!
