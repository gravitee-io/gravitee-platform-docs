---
description: This article walks through how to use the Gravitee v4 API creation wizard
---

# v4 API creation wizard

{% @arcade/embed flowId="IoH5bZLjSO6ce8UbgMmc" url="https://app.arcade.software/share/IoH5bZLjSO6ce8UbgMmc" fullWidth="true" %}

## Introduction

The v4 API creation wizard makes it easy to create new Gateway APIs from scratch. The API creation wizard is comprised of several steps, each of which requires you to define certain sets of information:

* API details
* Entrypoints
* Endpoints
* Security
* Documentation
* Summary

## Step 1: API details

The API details step is where you can define a name, version number, and description for your API. The name and version number are required, but we also recommend giving your API a description so that it is more easily understood and managed by internal users.

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-03-15 at 12.38.10 PM.png" alt=""><figcaption><p>Step 1: define your Gateway API's basic details.</p></figcaption></figure>

## Step 2: Entrypoints

### Choose your backend exposure method

The first part of the Entrypoints step is to choose how you want to expose your backend. As of today, Gravitee offers two options:

* **Proxy upstream protocol:** use this method if you want to use Gravitee to proxy backend REST APIs, SOAP APIs, WebSocket Server, gRPC, or GraphQL. You will not be able to enforce policies at the message level.
* **Introspect messages from event-driven backend:** use this method if you want to expose backend event brokers, such as Kafka and MQTT.

What you choose will dictate the kinds of entrypoints and endpoints that you can select later on. For more in-depth information on the exact support that these two methods offer, please [refer to this documentation. ](../README.md#backend-exposure-methods)

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-06-08 at 8.39.02 AM.png" alt=""><figcaption><p>v4 API creation wizard: select how you want your backend service exposed</p></figcaption></figure>

After you choose your method of exposure, select **Select my API architecture,** and you'll be taken to the entrypoint selection screen. Please read the following content to learn more about entrypoint selection and configuration, based on your selected exposure method.

### Entrypoint options for the "Proxy upstream protocol" method

If you chose **Proxy upstream protocol**, the Entrypoints step will require you to define a context path and decide whether or not you want to enable virtual hosts. The context path is the URL of your API. Please note that the context path must start with a '/' and can only contain uppercase letters, numbers, dashes or underscores.

If you select :heavy\_check\_mark:**Enable virtual hosts**, you'll have to define the following in addition to your context path:

* **Virtual host:** the host that must be set in the HTTP request to access your entrypoint.
* **Override access:** override the access URL of your Portal using a virtual host.
  * To enable or disable this, toggle **Enable** ON or OFF.

To disable virtual hosts, select **X Disable virtual hosts**.&#x20;

<figure><img src="../../../.gitbook/assets/HTTP proxy entrypoints.gif" alt=""><figcaption><p>HTTP-Proxy entrypoints</p></figcaption></figure>

### Entrypoint options for the "Introspect messages from Event-driven backend" method

If you chose **Introspect messages from Event-driven backend,** you get a much different set of entrypoint options:

* **HTTP GET:** allows you to front a chosen backend or data source with a Gateway REST API with support for the HTTP GET request.
* **HTTP POST:** allows you to front a chosen backend or data source with a Gateway REST API with support for the HTTP POST request.
* **Server-sent Events:** allows you to front a chosen backend or data source with a Gateway SSE API for unidirectional communication between server and client.
* **Webhook**: allows you to front a chosen backend or data source with a Gateway Webhook API. This allows consumers to subscribe to the Gravitee Gateway via Webhook and then retrieve streamed data in real-time from a backend data source, via the Gateway, over the consumer's Webhook callback URL.
* **WebSocket**: allows you to front a chosen backend or data source with a Gateway WebSocket API. This allows a consumer to retrieve and send streamed events and messages in real-time.

<figure><img src="../../../.gitbook/assets/Screen Shot 2023-06-08 at 8.44.08 AM.png" alt=""><figcaption><p>v4 API creation wizard: event-driven backend entrypoints</p></figcaption></figure>

Once you select your entrypoints from the entrypoints page, there will be further configuration required. The following sections outline the necessary configuration per entrypoint.

<details>

<summary>Server-sent Events</summary>

If you choose **SSE** as an entrypoint, you will be brought to a page where you can configure:

* **Context path:** the URL of your API. For example, if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
* **Virtual hosts:** enabling virtual hosts requires you to define your **virtual host** and optionally enable **override access**.
* **SSE characteristics and permissions:**
  * **Heartbeat intervals:** define the interval in which heartbeats are sent to the client by entering a numeric value into the **Define the interval in which heartbeats** **are sent to client** text field or by using the arrow keys. Intervals must be greater or equal to 2000ms. Each heartbeat will be sent as empty comment `''`.
  * Choose to allow or disallow sending message metadata to the client as SSE comments by toggling **Allow sending messages metadata to client as SSE comments** ON or OFF.
  * Choose to allow or disallow sending message headers to the client as SSE comments by toggling **Allow sending messages headers to client as SSE comments** ON or OFF.

</details>

<details>

<summary>Webhook</summary>

If you choose **Webhook** as an entrypoint, you will be brought to a page where you can configure:

* **HTTP Options**
  * **Connect timeout:** the maximum time, in milliseconds, to connect to the webhook. Either enter a numeric value or use the arrows to the right of the text field.
  * **Read timeout:** the maximum time, in milliseconds, allotted for the webhook to complete the request (including response). Either enter a numeric value or use the arrows to the right of the text field.
  * **Idle timeout:** the maximum time, in milliseconds, a connection will stay in the pool without being used. Once this time has elapsed, the unused connection will be closed, freeing the associated resources. Either enter a numeric value or use the arrows to the right of the text field.
* **Proxy options**
  * Choose whether to use a proxy for client connections by toggling **Use proxy** ON or OFF. If enabled, you will need to select from the proxy types in the **Proxy type** drop-down:
    * HTTP proxy
    * SOCKS4
    * SOCKS5
  * Choose whether to use the proxy configured at system level by toggling **Use system proxy** ON or OFF. If enabled, you will need to define:
    * Proxy host: enter your proxy host in the **Proxy host** text field.
    * Proxy port: enter your proxy port in the **Proxy port** text field.
    * (Optional) Proxy username: enter your proxy username in the **Proxy username** text field.
    * (Optional) Proxy password: enter your proxy password in the **Proxy password** text field.

**SOCKS proxy**\
A SOCKS proxy is a type of proxy server that uses the SOCKS protocol to tunnel traffic through an intermediary server.

</details>

<details>

<summary>WebSocket</summary>

If you chose **WebSocket** as an entrypoint, you will be brought to a page where you can configure:

* **The context path:** the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path.
* **Enabling virtual hosts**
  * This will then require you to define your **Virtual host** and optionally enable **override access.**
* **WebSocket configuration**
  * **Publisher configuration:** choose to either enable or disable the publication capability. By disabling it, you assume that the application will never be able to publish any message. To do this, toggle **Enable the publication capability** ON or OFF.
  * **Subscriber configuration:** choose to enable or disable the subscription capability. By disabling it, you assume that the application will never receive any message. To do this, toggle **Enable the subscription capability** ON or OFF.

</details>

<details>

<summary>HTTP POST</summary>

If you chose **HTTP POST** as an entrypoint, you will be brought to a page where you can configure:

* **The context path:** the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path.
* **Enabling virtual hosts**
  * This will then require you to define your **Virtual host** and optionally enable **override access.**
* **HTTP POST permissions:** here, you can choose to allow add request Headers to the generated message. To do this toggle, **Allow add request Headers to the generated message** ON or OFF**.**

</details>

<details>

<summary>HTTP GET</summary>

If you chose **HTTP GET** as an entrypoint, you will be brought to a page where you can configure:

* **The context path:** the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]` then `[/myAPI]` is the context path.
* Enabling virtual hosts
  * This will then require you to define your **Virtual host** and optionally enable **override access.**
* Your HTTP GET characteristics
  * **Limit messages count:** this defines the maximum number of messages to retrieve via HTTP GET. Default is 500. To set a custom limit, enter in your limit as a numerical value in the **Limit messages count** text field.
  * **Limit messages duration:** this defines the maximum duration in milliseconds to wait to retrieve the expected number of messages (See Limit messages count). The effective number of retrieved messages could be less than expected it maximum duration is reached. To set a custom limit, enter in your limit as a numerical value in the **Limit messages count** text field.
  * **HTTP GET permissions:** you can define whether or not to Allow sending messages headers to client in payload or Allow sending messages metadata to client in payload.&#x20;
    * To allow or disallow these actions, toggle either **Allow sending messages headers to client in payload** or **Allow sending messages metadata to client in payload** to either ON or OFF.&#x20;

</details>

## Step 3: Endpoints

**Gateway endpoints** define the protocol and configuration by which the Gateway API will fetch data from or post data to the backend API. Your endpoints will be dictated by the API architecture that you selected earlier.&#x20;

### HTTP Proxy endpoints

If you chose the HTTP Proxy option, your endpoint will be an HTTP Proxy. To configure this endpoint, you will be brought to a page where you can:

* **Define your target URL:** enter your target URL in the **Target URL** text field.
* **Define your HTTP options:**
  * Choose to either allow or disallow h2c clear text upgrade by toggling **Allow h2c Clear Text Upgrade** ON or OFF.
    * You'll need to select the HTTP protocol version to use. HTTP/1.1 and HTTP/2 are supported.
  * Choose to either enable or disable keep-alive by toggling **Enable keep-alive** ON or OFF.
    * If enabled, you'll need to define a numeric timeout value in the **Connect timeout** text field by either entering a numerical value or using the arrow keys.
  * Choose to either enable or disable HTTP pipelining by toggling **Enable HTTP pipelining** ON or OFF.&#x20;
    * If enabled, you'll need to define a numeric timeout value in the **Read timeout** text field by either entering a numerical value or using the arrow keys.
  * Choose to either enable or disable compression by toggling **Enable compression (gzip, deflate)** ON or OFF.&#x20;
  * **Configure your idle timeout settings**: define, in milliseconds, the maximum time a connection will stay in the pool without being used by entering a numeric value or using the arrow keys in the text field. Once the specified time has elapsed, the unused connection will be closed, freeing the associated resources.
  * Choose whether to follow HTTP redirects by toggling **Follow HTTP redirects** ON or OFF.
  * Define the number of max concurrent connections by entering a numeric value or using the arrow keys in the text field.
  * Choose to propagate client Accept-Encoding header by toggling **Propagate client Accept-Encoding header (no decompression if any)** ON or OFF.
  * Select **+ Add HTTP headers** to add headers that the Gateway should add or override before proxying the request to the backend API.
* **Define your Proxy options:**
  * Choose whether to use a proxy for client connections by toggling **Use proxy** ON of OFF.
    * If enabled, you will need to select from the proxy types in the **Proxy type** drop-down:
      * HTTP proxy
      * SOCKS4
      * SOCKS5
  * **Use system proxy:** choose whether to use the proxy configured at system level. If enabled, you'll need to define the following:
    * Proxy host: enter your proxy host in the **Proxy host** text field.
    * Proxy port: enter your proxy port in the **Proxy port** text field.
    * (Optional) Proxy username: enter your proxy username in the **Proxy username** text field.
    * (Optional) Proxy password: enter your proxy password in the **Proxy password** text field.
* **Define your SSL options**
* **Define your Key store**

### **Introspect messages from event-driven backend endpoints**

If youse chose **Introspect messages from event-driven backend** as your exposure method, you will be able to choose from the following endpoints:

* Endpoint Mock
* MQTT 5.X
* Kafka

Depending on which endpoint you choose, you will need to further define certain sets of endpoint configurations. Please see the expandable sections below to learn more about the endpoint configuration of each available endpoint.&#x20;

<details>

<summary>Endpoint Mock</summary>

The Endpoint Mock endpoint allows you to mock a backend service to emulate the behavior of a typical HTTP server and test processes. If you choose this endpoint, you will need to configure:

* **Interval between messages publication:** this defines the interval between published messages (in ms); the default is 1000
* **Content of published messages:** this defines the content of the message body that will be streamed; the default is "mock message"
* **Count of published messages:** this defines the specific limit of published messages as an integer that you want streamed as a part of the mocking; if not specified, there will be no limit

</details>

<details>

<summary>MQTT 5.X</summary>

The **MQTT 5.X** endpoint allows the Gateway to open up a persistent connection and/or call a backend MQTT broker, as long as that broker is running on MQTT 5.x. This is done by the Gravitee Gateway setting up an MQTT client. If you choose this endpoint, you will need to configure:

* **How the Gateway will interact the broker:** you can tell the Gravitee Gateway's MQTT client to act as either a producer, a consumer, or both a producer and consumer. To do this, choose either **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu. Here is an explanation of what each option will result in:
  * **Use Producer**: tells the Gateway MQTT client to be prepared to produce messages and send them to the MQTT broker that you will define as your endpoint
  * **Use Consumer**: tells the Gateway MQTT client to be prepared to consume messages from the MQTT broker that you will define as your endpoint
  * **Use Producer and Consumer**: tell the Gateway MQTT client to do both of the above
* **Define the Server host**: define the serverHost for the MQTT broker that you are using as your endpoint
* **Define the Server port**: define the serverPort for the MQTT broker that you are using as your endpoint
* **Define Reconnect attempts:** this sets the number of reconnect attempts that the Gateway will initiate if there is any kind of disconnecton between the Gateway MQTT client and the MQTT broker; the maximum is 10
* **Session expiry interval: t**his interval defines the period of time that the broker stores the session information of that particular MQTT client. When the session expiry interval is set to **0** or the CONNECT packet does not contain an expiry value, the session information is immediately removed from the broker as soon as the network connection of the client closes.
* **Enable or disable Clean start:** toggle **Clean start** ON or OFF to enable the **cleanStart** tag. This tag tells the MQTT broker to discard any previous session data and the Gateway MQTT client will start with a fresh session upon connection
* **Define initial security settings:** you will define more Gravitee Gateway-specific security settings later on, but this is where you will define your MQTT-specific authentication flow. Gravitee supports username and password using TLS. You will need to define:
  * Username
  * Password
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer** earlier on): this is where you define the settings that the Gravitee Gateway MQTT client will rely on for producing messages to your backend MQTT topic/broker. You will need to define:
  * Topic: the UTF-8 string that the broker uses to filter messages for each connected client. The topic consists of one or more topic levels. Each topic level is separated by a forward slash (topic level separator).&#x20;
  * **Retain settings**: define if the retain flag must be set for every published messages. The broker stores the last retained message. To define this, toggle **Retained** ON or OFF.
  * **Message expiry interval:** defines the period of time that the broker stores the PUBLISH message for any matching subscribers that are not currently connected. When no message expiry interval is set, the broker must store the message for matching subscribers indefinitely. When the retained=true option is set on the PUBLISH message, this interval also defines how long a message is retained on a topic.
  * **Response topic**: represents the topics on which the responses from the receivers of the message are expected
* **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer** earlier on): this is where you define the settings that the Gravitee Gateway MQTT client will rely on for consuming messages from your backend MQTT topic/broker. You will just need to define the **Topic** from which the Gateway MQTT client will consume messages.

</details>

<details>

<summary>Kafka</summary>

The **Kafka** endpoint allows the Gateway to open up a persistent connection and/or call a backend Kafka broker. This is done by the Gravitee Gateway setting up a Kafka client. If you choose this endpoint, you will need to configure:

* **How the Gateway will interact the broker:** you can tell the Gravitee Gateway's Kafka client to act as either a producer, a consumer, or both a producer and consumer. To do this, choose either **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu. Here is an explanation of what each option will result in:
  * **Use Producer**: tells the Gateway Kafka client to be prepared to produce messages and send them to the Kafka broker that you will define as your endpoint
  * **Use Consumer**: tells the Gateway Kafka client to be prepared to consume messages from the Kafka broker that you will define as your endpoint
  * **Use Producer and Consumer**: tell the Gateway Kafka client to do both of the above
* **Define the Bootstrap servers**: defines the list of host/port pairs, separated by a comma, to use for establishing the initial connection to the Kafka cluster. The client will make use of all servers irrespective of which servers are specified here for bootstrapping—this list only impacts the initial hosts used to discover the full set of servers.
* **Define initial security settings:** you will define more Gravitee Gateway-specific security settings later on, but this is where you will define your Kafka-specific authentication flow. Gravitee supports PLAINTEXT, SASL\_PLAINTEXT, SASL\_SSL, and SSL as protocols. Depending on which you choose, you will need to define:
  * **PLAINTEXT**: no further security config necessary
  * **SASL**
    * **SASL mechanism** used for client connections; this will either be GSSAPI, OAUTHBEARER, PLAIN, SCRAM\_SHA-256, or SCRAM-SHA-512
    * **SASL JAAS Config**: the JAAS login context parameters for SASL connections in the format used by JAAS configuration files.
  * **SASL\_SSL**
    * **SASL mechanism** used for client connections; this will either be GSSAPI, OAUTHBEARER, PLAIN, SCRAM\_SHA-256, or SCRAM-SHA-512
    * **SASL JAAS Config**: the JAAS login context parameters for SASL connections in the format used by JAAS configuration files.
      * SSL Configuration
        * **Truststore**: depending on your Truststore type, you will need to define:
          * **PEM with location**
            * Define the **location of your truststore file**
          * **PEM with certificates**
            * Define the trusted certificates in the format specified by 'ssl.truststore.type'
          * **JKS with location**
            * Define the **location of your truststore file**
            * Define the **SSL truststore password** for the truststore file
          * **JKS with certificates**
            * Define the trusted certificates in the format specified by 'ssl.truststore.type'
            * Define the **SSL truststore password** for the truststore file
          * **PKCS12 with location**
            * Define the **location of your truststore file**
            * Define the **SSL truststore password** for the truststore file
          * **PKCS12 with certificates**
            * Define the **trusted certificates** in the format specified by 'ssl.truststore.type'
            * Define the **SSL truststore password** for the truststore file
          * Keystore:
            * **PEM with location**
              * Define the **SSL keystore certificate chain**
              * Define the location of your keystore file
            * **PEM with Key**
              * **SSL keystore certificate chain**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
            * **JKS with location**
              * Define the **location of your keystore file**
              * Define the **SSL keystore password** for the keystore file
            * **JKS with Key**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
              * Define the **SSL keystore password** for the keystore file
            * **PKCS12 with location**
              * Define the **location of your keystore file**
              * Define the **SSL keystore password** for the keystore file
            * **PKCS12 with Key**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
              * Define the **SSL keystore password** for the keystore file
    * **SSL**
      * SSL Configuration
        * **Truststore**: depending on your Truststore type, you will need to define:
          * **PEM with location**
            * Define the **location of your truststore file**
          * **PEM with certificates**
            * Define the trusted certificates in the format specified by 'ssl.truststore.type'
          * **JKS with location**
            * Define the **location of your truststore file**
            * Define the **SSL truststore password** for the truststore file
          * **JKS with certificates**
            * Define the trusted certificates in the format specified by 'ssl.truststore.type'
            * Define the **SSL truststore password** for the truststore file
          * **PKCS12 with location**
            * Define the **location of your truststore file**
            * Define the **SSL truststore password** for the truststore file
          * **PKCS12 with certificates**
            * Define the **trusted certificates** in the format specified by 'ssl.truststore.type'
            * Define the **SSL truststore password** for the truststore file
          * Keystore:
            * **PEM with location**
              * Define the **SSL keystore certificate chain**
              * Define the location of your keystore file
            * **PEM with Key**
              * **SSL keystore certificate chain**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
            * **JKS with location**
              * Define the **location of your keystore file**
              * Define the **SSL keystore password** for the keystore file
            * **JKS with Key**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
              * Define the **SSL keystore password** for the keystore file
            * **PKCS12 with location**
              * Define the **location of your keystore file**
              * Define the **SSL keystore password** for the keystore file
            * **PKCS12 with Key**
              * Define the **SSL keystore private key** by defining the **Key** and the **Key password**
              * Define the **SSL keystore password** for the keystore file
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer** earlier on): this is where you define the settings that the Gravitee Gateway Kafka client will rely on for producing messages to your backend Kafka topic/broker. You will need to define:
  * **Topic**: the topic that the broker uses to filter messages for each connected client.
*   **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer** earlier on): this is where you define the settings that the Gravitee Gateway Kafka client will rely on for consuming messages from your backend Kafka topic/broker.&#x20;

    You will need to define:

    * **Topic**: the topic(s) from which your Gravitee Gateway client will consume messages
    * **Encode message Id:** Toggle this ON or OFF to allow encoding message ids in base64
    * **Auto offset reset:** You can use the **Auto offset reset** drop down to configure what happens when there is no itial offset in Kafka, or if the current offset does not exist on the server anymore. You have multiple options:
      * **Earliest**: automatically reset the offset to the earliest offset
      * **Latest**: automatically reset the offset to the latest offset
      * **None**: throw exception to the consumer if no previous offset is found for the consumer's group
      * **Anything else:** throw exception to the consumer.

</details>

## Step 4: Security

Next in the API creation wizard is the Security step, where you will configure:

* **Plan information**: define a plan that provides the API producer with a method to secure, monitor, and transparently communicate details around access.
* **Configuration**: define authorization resources, such as Gravitee AM or another OAuth2 resource.
* **Limitations**: define access limitations, such as rate limiting and quotas.

### Plan information&#x20;

A plan is essentially an access layer around an API that provides the API producer with a method to secure, monitor, and transparently communicate details around access. If you want to learn more about how plans function in Gravitee, please refer to the [plans documentation](../../api-exposure-plans-applications-and-subscriptions/plans.md). You will be able to choose between several different plan types:

* **OAuth2**: a standard designed to allow a website or application to access resources hosted by other web apps on behalf of a user.
* **JWT**: an open standard that defines a compact and URL-safe way to securely transmit information as a JSON object between parties.
* **API Key:** a plan where the API Gateway will reject calls from consumers that aren't able to pass the right API key in their request.
* **Keyless**: a plan that results in no added security via plan configuration. This is considered an "Open" plan.
* **Push plan**: a plan that provides an access layer for the Gateway pushing data to consumers. This is used for subscribers.

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
* **Access control**: here, select any Groups within APIM that you do not want to have access to this API. For more information on Groups, refer to the [Groups documentation](../../administration/README.md#users-and-user-groups).

<img src="../../../.gitbook/assets/image.png" alt="" data-size="original">



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

![](<../../../.gitbook/assets/image (1).png>)

After you're done with the configuration, select Next to define any additional restrictions for the plan. These Restrictions include:

* **Rate limiting**: define the maximum number of requests that an application can make within a defined amount of seconds or minutes. If you choose this, you will need to then:
  * Enable or disable **Non-strict mode:** this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict
  * Enable or disable **Add response headers**
  * Define your rate limit's **Key**
  * Define the **max request count** (this can be a static or dynamic count)
  * Define the **time duration** (i.e. a one-second time interval within which to apply the request limitation)
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
* **Access control**: here, select any Groups within APIM that you do not want to have access to this API. For more information on Groups, refer to the [Groups documentation](../../administration/README.md#users-and-user-groups).

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
  * Define the **time duration** (i.e. a one-second time interval within which to apply the request limitation)
* **Quota**: defines a rate limit over a period of hours, days, or months. If you choose this, you'll need to then define the same settings as you would for rate limiting (see above)
* **Resource filtering**: this allows you to restrict resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These will be defined by path patterns and methods.

![](<../../../.gitbook/assets/image (2) (1).png>)

</details>

<details>

<summary>API key</summary>

If you choose API key, you'll define general settings, API key authentication configuration, and restrictions.

On the General page, define:

* **Name**
* **Description**
* **Characteristics**
* **Subscription** options: choose whether to auto-validate subscriptions, require a message from consumers during subscription, and/or to present a message to the consumer upon subscription
* **Access control**: here, select any Groups within APIM that you do not want to have access to this API. For more information on Groups, refer to the [Groups documentation](../../administration/README.md#users-and-user-groups).

After you're done, select **Next**, and you'll be taken to the **API key authentication** configuration page. Here, you need to:

* Choose whether or not to propagate your API key to upstream APIs
* Define any additional selection rules using the Gravitee Expression language

Once you're done, select **Next,** and you'll be taken to the **Restriction** page. Here, you'll define any additional restrictions that you want to be associated with your plan, Your options include:one-second

* **Rate limiting**: define the maximum number of requests that an application can make within a defined amount of seconds or minutes. If you choose this, you will need to then:
  * Enable or disable **Non-strict mode:** this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict
  * Enable or disable **Add response headers**
  * Define your rate limit's **Key**
  * Define the **max request count** (this can be a static or dynamic count)
  * Define the **time duration** (i.e. a one second time interval within which to apply the request limitation)
* **Quota**: defines a rate limit over a period of hours, days, or months. If you choose this, you'll need to then define the same settings as you would for rate limiting (see above)
* **Resource filtering**: this allows you to restrict resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These will be defined by path patterns and methods.

</details>

<details>

<summary>Keyless plan</summary>

If you select Keyless, you will need to only define general details and restrictions, as there is no authentication to configure (unlike OAuth2, JWT, and API key).

On the General page, define:

* **Name**
* **Description**
* **Characteristics**
* **Subscription** options: choose whether to auto-validate subscriptions, require a message from consumers during subscription, and/or to present a message to the consumer upon subscription
* **Access control**: here, select any Groups within APIM that you do not want to have access to this API. For more information on Groups, refer to the [Groups documentation](../../administration/README.md#users-and-user-groups).

After you're done, select **Next,** and you'll be taken to the **Restriction** page. This is where you can define any additional restrictions that you want to be associated with your plan. your options include:

* **Rate limiting**: define the maximum number of requests that an application can make within a defined amount of seconds or minutes. If you choose this, you will need to then:
  * Enable or disable **Non-strict mode:** this enables rate limiting to be applied in an asynchronous manner, which results in the distributed counter value not being strict
  * Enable or disable **Add response headers**
  * Define your rate limit's **Key**
  * Define the **max request count** (this can be a static or dynamic count)
  * Define the **time duration** (i.e. a one-second time interval within which to apply the request limitation)
* **Quota**: defines a rate limit over a period of hours, days, or months. If you choose this, you'll need to then define the same settings as you would for rate limiting (see above)
* **Resource filtering**: this allows you to restrict resources based on defined whitelist/allowed and/or blacklist/disallowed settings. These will be defined by path patterns and methods.

</details>

## Step 5: Documentation

he Documentation step is not supported for v4 APIs. This will be added in future releases.

## Step 6: Summary

The final step is to review and then create or deploy your API. Creating your API will create the API as a Gravitee artifact, but not deploy it to the Gateway. If you choose Deploy, the API will be created and deployed to the Gravitee Gateway.

{% hint style="success" %}
Once you create or deploy your API, you are done with the API creation process! At this point, we recommend learning how to further configure your API, and how to design and enforce policies that make your API more secure, reliable, efficient, etc.
{% endhint %}
