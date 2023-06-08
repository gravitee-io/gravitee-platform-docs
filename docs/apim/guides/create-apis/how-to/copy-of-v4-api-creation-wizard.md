# Copy of v4 API creation wizard

## Introduction

The API creation wizard makes it easy to create new Gateway API's from scratch.&#x20;

{% @arcade/embed flowId="gjzRqNfSladxmw4olxSX" url="https://app.arcade.software/share/gjzRqNfSladxmw4olxSX" %}

The API creation wizard is comprised of several steps, each which requires you to define certain sets of information:

* API details
* API architecture
* Entrypoints
* Endpoints
* Security
* Documentation
* Summray

## Step 1: API details

The API details step is where you can define a name, version number, and description for your API. The name and version number are required, but we also recommend giving your API a description so that it is more easily understood and managed by internal users.

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-03-15 at 12.38.10 PM.png" alt=""><figcaption><p>Step 1: define your Gateway API's basic details.</p></figcaption></figure>

## Step 2: Entrypoints

### Choose your backend exposure method

The first part of the Entrypoints step is to choose how you want to expose your backend. As of today, Gravitee offers two options:

* **Proxy upstream protocol:** use this method if you want to use Gravitee to proxy backend REST APIs, SOAP APIs, WebSocket Server, gRPC, or GraphQL. You will not be able to enforce policies at the message level.
* **Introspect messages from event-driven backend:** use this method if you want to expose backend event brokers, such as Kafka and MQTT

What you choose here will dictate the kinds of entrypoints and endpoints that you can select later on. For more in-depth information on the exact support that these two methods offer, please [refer to this documentation. ](../#backend-exposure-methods)

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-06-08 at 8.39.02 AM.png" alt=""><figcaption><p>v4 API creation wizard: select how you want your backend service exposed</p></figcaption></figure>

After you choose your method of exposure, select **Select my API architecture,** and you'll be taken to the entrypoint selection screen. Please read the following content to learn more about entrypoint selection and configuration, based on your selected exposure method.

### Proxy upstream protocol entrypoints

If you chose **Proxy upstream protocol**, the entrypoints step will require you to define a context path and decide whether or not you want to enable virtual hosts. The context path is just the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path. Please note that the context path must start with a '/' and can only contain uppercase letters, numbers, dashes or underscores.

If you select :heavy\_check\_mark:**Enable virtual hosts**, you'll have to define the following in addition to your context path:

* **Virtual host:** the host that must be set in the HTTP request to access your entrypoint.
* **Override access: e**nable override on the access URL of your Portal using a virtual host.
  * To enable or disable this, simply toggle **Enable** ON or OFF

To disable virtual hosts, just select **X Disable virtual hosts.**&#x20;

<figure><img src="../../../.gitbook/assets/HTTP proxy entrypoints.gif" alt=""><figcaption><p>HTTP-Proxy entrypoints</p></figcaption></figure>

### Introspect messages from Event-driven backend entrypoints

If you chose **Introspect messages from Event-driven backend,** you get a much different set of entrypoint options:

* **HTTP GET:** allows you to front a chosen backend or data source with a Gateway REST API with support for the HTTP GET request
* **HTTP POST:** allows you to front a chosen backend or data source with a Gateway REST API with support for the HTTP POST request
* **Server-sent Events:** allows you to front a chosen backend or data source with a Gateway SSE API for unidirectional communication between server and client
* **Server-sent Events advanced:** allows you to front a chosen backend or data source with a Gateway SSE API for unidirectional communication between server and client with additional support for Quality of Service (QoS)
* **Webhook**: allows you to front a chosen backend or data source with a Gateway Webhook API. This allows consumers to subscribe to the Gravitee Gateway via Webhook and then retrieve streamed data in real-time from a backend data source, via the Gateway, over the consumer's Webhook callback URL.
* **WebSocket**: allows you to front a chosen backend or data source with a Gateway WebSocket API. This allows for a consumer to retrieve and send streamed events and messages in real-time.

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-06-08 at 8.44.08 AM.png" alt=""><figcaption><p>v4 API creation wizard: event-driven backend entrypoints</p></figcaption></figure>

Once you select your entrypoints from the entrypoints page, there will be further configuration required. The following sections outline the necessary configuration per entrypoint.

#### HTTP GET

#### HTTP POST

#### Webhook

#### WebSocket

#### Server-sent Events

## Step 3: Endpoints

**Gateway endpoints** define the protocol and configuration by which the gateway API will fetch data from, or post data to, the backend API. Your endpoints will be dictated by the API architecture that you selected earlier.&#x20;

### HTTP Proxy endpoints

If you chose the HTTP Proxy option, your endpoint will be an HTTP Proxy. To configure this endpoint, you will be brought to a page where you can:

* **Define your target url:** enter your target url in the **Target url** text field.
* **Define your HTTP options**
  * Choose to either allow or disallow h2c clear text upgrade by toggling **Allow h2c Clear Text Upgrade** ON or OFF.
    * You'll need to select the HTTP protocol version to use. As of now, HTTP/1.1 or HTTP/2 are options.
  * Choose to either enable or disable keep-alive by toggling **Enable keep-alive** ON or OFF
    * If you enable this, you'll need to define a timeout value by entering a numerical value in the **Connect timeout** text field by either typing in a numerical value or using the arrow keys in the text field.
  * Choose to either enable or disable HTTP pipelining by toggling **Enable HTTP pipelining** ON or OFF.&#x20;
    * If you enable this, you'll need to define a read timeout value by entering a numerical value in the **Read timeout** text field by either typing in a numerical value or using the arrow keys in the text field.
  * Choose to either enable or disable compression by toggling **Enable compression (gzip, deflate)** ON or OFF.&#x20;
  * **Configure your idle timeout settings**: defines the maximum time a connection will stay in the pool without being used in milliseconds. Once the timeout has elapsed, the unused connection will be closed, allowing to free the associated resources. To configure this, enter in a numerical value or using the arrow keys in the text field.
  * Choose to follow HTTP redirects or not: toggle **Follow HTTP redirects** ON or OFF.
  * Define the number of max concurrent connections: enter in a numerical value or using the arrow keys in the text field.
  * Choose to propagate client Accept-Encoding header: toggle **Propagate client Accept-Encoding header (no decompression if any)** ON or OFF.
  * Add HTTP headers: select **+ Add HTTP headers** to add headers that the Gateway should add or override before proxying the request to the backend API.
* **Define your Proxy options**
  * **Use proxy:** choose whether or not to use a proxy for client connections. To enable this, toggle Use proxy ON.
    * If you enable Use proxy, you will need to select the Proxy type in the **Proxy type** drop-down. You choose between:
      * HTTP proxy
      * SOCKS4
      * SOCKS5
  * **Use system proxy:** choose to use the proxy configured at system level. If you enable this, you'll need to define the:
    * Proxy host: enter your proxy host in the **Proxy host** text field.
    * Proxy port: enter your proxy port in the **Proxy port** text field.
    * (Optional) Proxy username: enter your proxy username in the **Proxy username** text field.
    * (Optional) Proxy password: enter your proxy password in the **Proxy password** text field.
* **Define your SSL options**
* **Define your Key store**

### **Message-based endpoints**

If youse chose **Message** as your API architecture, you will be able to choose from the following endpoints:

* Endpoint Mock
* MQTT 5.X
* Kafka

Depending on which endpoint you choose, you will need to further define certain sets of endpoint configurations. Please see the tabs below to learn more about endpoint configuration per each available endpoint:&#x20;

## Step 4: Security

The next step in the API creation wizard is Security. The Security stage of the API creation wizard is where you will configure:

* **Plan information**: defines a "plan" that provides the API producer a method to secure, monitor, and transparently communicate details around access
* **Configuration**: define authorization resources, such as Gravitee AM or another OAuth2 resource
* **Limitations**: where you will configure access limitations such as rate limiting and quotas

### Plan information&#x20;

Plans are essentially an access layer around APIs that provide the API producer a method to secure, monitor, and transparently communicate details around access. If you want to learn more about how Plans function in Gravitee, please refer to the [Plans documentation](../../api-exposure-plans-applications-and-subscriptions/plans.md). You will be able to choose between several different plan types:

* **OAuth2**: standard designed to allow a website or application to access resources hosted by other web apps on behalf of a user.
* **JWT**: open standard that defines a compact and URL-safe way to securely transmit information as a JSON object between parties
* **API Key:** the API Gateway will reject calls from consumers that aren't able to pass the right API key in their request
* **Keyless**: this results in no added security via plan configuration. This is considered an "Open" plan.
* **Push plan**: a plan that provides an access layer for the gateway pushing data to consumers. This will be used for subscribers.

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-06-01 at 12.14.02 PM.png" alt=""><figcaption><p>API creation wizard: different Security plan types</p></figcaption></figure>

Depending on which plan you select, the configuration will differ. Please see the expandable sections below to learn more about how to configure each of the different plans.

<details>

<summary>OAuth2 plan</summary>

To configure your OAuth2 plan, select OAuth2 from the **+ Add plan** dropdown. From here, you'll need to define general details, configuration, and restrictions.&#x20;

On the **General** screen, define:

* **Name**
* **Description**
* **Characteristics**
* **Subscription** options: choose whether to auto-validate subscriptions, require a message from consumers during subscription, and/or to present a message to the consumer upon subscription
* **Access control**: here, select any Groups within APIM that you do not want to have access to this API. For more information on Groups, refer to the [Groups documentation](../../administration/#users-and-user-groups).

<img src="../../../.gitbook/assets/image (6).png" alt="" data-size="original">



Once you're done, select Next, and move on to **OAuth2 authentication configuration**. Here, you'll define:

* Your OAuth2 resource in the **OAuth2 resource** field. This should be the resource that you'll use to validate the token.
* Your cache resource in the **Cache resource** field. This should be the cache resource that you will use to store the tokens.
* Whether or not to:&#x20;
  * **Extract an OAuth2 payload**: this will push the token endpoint payload into the oauth.payload context attribute&#x20;
  * **Check scopes**: this will tell your authentication method to check required scopes in order to access the resource&#x20;
    * If you do choose to check scopes, you'll need to define your list of required scopes using the **Required scopes** module.
* Enable or disable strict mode. If you choose **Strict**, scopes will be checked against the exact list you provided in the Requires scopes section,
* Choose whether or not to permit authorization headers to target endpoints&#x20;
* Optionally, you can define additional selection rules. If you are managing multiple plans that share the same type, this will help the plan's selection process. You will need to use the Gravitee Expression Language here. For more information on the Gravitee Expression Language, please refer to the Expression Language documentation.

![](<../../../.gitbook/assets/image (4).png>)

After you're done with the configuration, select Next to define any additional restrictions for the plan. These Restrictions include:

* **Rate limiting**: define the maximum number of requests that an application can make within a defined amount of seconds or minutes. If you choose this, you will need to then:
  * Enable or disable **Non-strict mode:** this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict
  * Enable or disable **Add response headers**
  * Define your rate limit's **Key**
  * Define the **max request count** (this can be a static or dynamic count)
  * Define the **time duration** (i.e. a one second time interval within which to apply the request limitation)
* **Quota**: defines a rate limit over a period of hours, days, or months. If you choose this, you'll need to then define the same settings as you would for rate limiting (see above)
* **Resource filtering**: this allows you to restrict resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These will be defined by path patterns and methods.

![](<../../../.gitbook/assets/image (2).png>)

</details>

<details>

<summary>JWT plan</summary>

If you choose **JWT**, you will need to define general details, authentication configuration, and restrictions.&#x20;

On the **General** screen, define:

* **Name**
* **Description**
* **Characteristics**
* **Subscription** options: choose whether to auto-validate subscriptions, require a message from consumers during subscription, and/or to present a message to the consumer upon subscription
* **Access control**: here, select any Groups within APIM that you do not want to have access to this API. For more information on Groups, refer to the [Groups documentation](../../administration/#users-and-user-groups).

Once you're done with your general details, select **Next**. Then, you'll need to define your JWT authentication configuration. This will require you to:&#x20;

* Choose **Signature**: this will define how your JWT token must be signed. The options are:
  * RSA\_RS256
  * RSA\_RS384
  * RSA\_RS512
  * HMAC\_HS512
  * HMAC\_HS384
  * HMAC\_HS384
* Define your **JWKS resolver:** this will define how your JSON Web Key Set is retrieved.
* Define your Resolver parameter
* Choose to either use or not use a system proxy
* Choose whether or not to extra JWT claims
* Choose whether or not to propagate Authorization headers
* Define the User claim where users can be extracted
* Define the Client Id claim where the client can be extracted
* Define additional selection rules using the Gravitee Expression Language

Once you're done configuring your JWT plan, select **Next**. You'll then define any restrictions associated with this plan. Your options include:

* **Rate limiting**: define the maximum number of requests that an application can make within a defined amount of seconds or minutes. If you choose this, you will need to then:
  * Enable or disable **Non-strict mode:** this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict
  * Enable or disable **Add response headers**
  * Define your rate limit's **Key**
  * Define the **max request count** (this can be a static or dynamic count)
  * Define the **time duration** (i.e. a one second time interval within which to apply the request limitation)
* **Quota**: defines a rate limit over a period of hours, days, or months. If you choose this, you'll need to then define the same settings as you would for rate limiting (see above)
* **Resource filtering**: this allows you to restrict resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These will be defined by path patterns and methods.

![](<../../../.gitbook/assets/image (5).png>)

</details>

## Step 5: Documentation

As of now, the **Documentation** step is not supported for v4 APIs. This will be added with future releases.

## Step 6: Summary

The final step is to review and then create or deploy your API. Creating your API will create the API as a Gravitee artifact, but not deploy it to the Gateway. If you choose Deploy, the API will be created and Deployed to the Gravitee Gateway.

{% hint style="success" %}
Once you create or deploy your API, you are done with the API creation process! At this point, we recommend learning how to further configure your API and how to design and enforce policies that make your APIs more secure, more reliable, more efficient, etc.
{% endhint %}
