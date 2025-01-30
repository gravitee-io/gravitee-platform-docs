# Configure the Kafka Gateway and Client

## Overview

Before you can use Gravitee to proxy n Kafka clusters, you need to configure the Gravitee Kafka Gateway and a Kafka client. This article describes how to:

* [Configure the Kafka Gateway](configure-the-kafka-gateway-and-client.md#configure-the-kafka-gateway)
* [Configure a Kafka client](configure-the-kafka-gateway-and-client.md#configure-the-kafka-client)
* [Produce and consume messages](configure-the-kafka-gateway-and-client.md#produce-and-consume-messages)

## Configure the Kafka Gateway

{% hint style="info" %}
Running the Kafka Gateway requires an Enterprise license with the Kafka Gateway feature included. This does not come by default with a Universe license; it must be purcahsed separately from Gravitee.
{% endhint %}

To run the Kafka Gateway, you enable the gateway server in \`gravitee.yml\`.  The full example of the configuration is defined below. The baseline required configuration is simply:

```yaml
# Gateway Kafka server
kafka:
  enabled: true

  routingMode: host # default is host. Only host is supported for now.
  # Routing Host Mode
  routingHostMode:
    brokerPrefix: broker- # default is broker-
    domainSeparator: - # Used to separate broker's name from api & defaultDomain. Default is '-'

    # The default domain where the Kafka APIs are exposed. ex: `myapi` will be exposed as `myapi.mycompany.org`
    defaultDomain: mycompany.org # Should set according to the public wildcard DNS/Certificate. Default is empty
    defaultPort: 9092 # Default public port for Kafka APIs. Default is 9092
```

The gateway domain is used as the core domain of the bootstrap server for client requests. Each Kafka API will use a different host prefix. Your client must trust the certificate provided by the gateway, and as there is a variable host in the proxy bootstrap server URL, you likely need to request a wildcard SAN for the certificate presented by the gateway.

{% hint style="info" %}
SNI routing is **required** to run the Kafka Gateway. As the gateway can run multiple Kafka APIs simultaneously, this is how the gateway determines which API proxy is the intended target of the client request. As SNI is part of the TLS protocol, the gateway **must** present a certificate that is trusted by the client.
{% endhint %}

### Defining the Default Entrypoint Configuration

By default, clients talk to Kafka APIs by setting the bootstrap server as `{api-specific-prefix}.{gateway-hostname}:9092`. This is set in `gravitee.yml`, but for convenience, when developing APIs in the UI, you can set the default values appended to the hostname. You can also leave this value blank and respecify the full hostname in the API.

In order to configure the APIM Console to use the Kafka domain and port values for your Organization:

1. Log in to your APIM Console.
2. Select **Organization** from the bottom of the left nav.
3. Select **Entrypoints & Sharding Tags** from the left nav.
4.  In the **Entrypoint Configuration** section, confirm that the **Default Kafka domain** and **Default Kafka port** values match those of your Kafka API.\


    <figure><img src="../.gitbook/assets/1 KG 1.png" alt=""><figcaption></figcaption></figure>

    This value then shows in the entrypoint page for your APIs.\


    <figure><img src="../.gitbook/assets/1 KG 2.png" alt=""><figcaption></figcaption></figure>

## Configure the Kafka client

To use the Kafka Gateway, you use a regular Kafka client. There are many implementations of the Kafka client, and you can use any client that supports the full Kafka protocol.

{% hint style="info" %}
As of the 4.6.0 release, the Kafka Gateway requires the Kafka client to be version 3.0 or above.
{% endhint %}

The default client to talk to Kafka is packaged within the Kafka binary and is based on Java. To use this client, as a prerequisite, you will need to install a JRE. See the [Java documentation](https://www.java.com/en/) for more information.

1. Download Kafka. Gravitee Kafka Gateway is compatible with the source code or either binary download of each supported Kafka release. For more information about downloading Kafka, go to [Kafka's download page](https://kafka.apache.org/downloads).
2. Store the downloaded file structure in a secure place. The root folder will be your working directory when calling your Kafka API.

The client is now ready to use, but to produce and consume messages you must create a `.properties` file in the root folder as described below.

{% hint style="info" %}
At this point, you can begin creating and deploying APIs to the Gravitee Kafka Gateway.
{% endhint %}

## Produce and consume messages

You can use the Kafka Gateway and client to call your [Kafka API](create-kafka-apis.md) and, as a primary use case, produce or consume messages. Note that you can also proxy requests to create and manage topics, update partitions, and manage consumer groups.

### Prerequisites

The following prerequisites must be met before you can produce and consume Kafka messages:

* You must have an active subscription to a published API [plan](../expose-apis/plans/) belonging to your Gravitee Kafka API.&#x20;
* If you are subscribing to an OAuth2 or JWT plan, your application must reference the same client ID that you use for authorization.&#x20;

{% hint style="info" %}
When using [Gravitee Access Management (AM)](https://documentation.gravitee.io/am) as the authorization server, the client ID is generated when you create a Gravitee AM Authorization Server resource. To access this resource, you must also create an application in Gravitee Access Management.&#x20;
{% endhint %}

For plan, application, subscription, and resource information, see the following:

* For information on how to create and manage plans, see [Plans](plans.md).
* To learn how to create an application to a Gravitee plan, see [Applications](applications.md).
* For more information on how subscriptions work in Gravitee, see [Subscriptions](subscriptions.md).
* To learn how to create a resource, see [Resources](../policies/resources.md).

### Example

The following example provides a template for how to produce and consume messages using the Kafka Gateway, Kafka client, and the prerequisites mentioned above.&#x20;

1. In the top-level folder of your Kafka download, create an empty `.properties` file named `connect.properties`.
2. Go to the Developer Portal and find your API.
3. After selecting your API, click on the **My Subscriptions** tab.
4.  Copy the script in the **Review Kafka Properties** section and paste it into your `connect.properties` file.\


    <div align="left"><figure><img src="../.gitbook/assets/1 pc 2.png" alt="" width="563"><figcaption></figcaption></figure></div>
5.  Copy either the produce or consume commands from the **Calling the API** section.\


    <div align="left"><figure><img src="../.gitbook/assets/1 pc 4.png" alt="" width="563"><figcaption></figcaption></figure></div>
6. In a terminal, change your working directory to the top-level folder of your Kafka download.
7. Paste and execute the commands you copied to produce or consume messages.

## Appendix: Full Gateway Configuration

Here is a reference for the full server configuration of the Kafka Gateway.

```yaml
# Gateway Kafka server
kafka:
  enabled: false

  routingMode: host # default is host. Only host is supported for now.
  # Routing Host Mode
  routingHostMode:
    brokerPrefix: broker- # default is broker-
    domainSeparator: - # Used to separate broker's name from api & defaultDomain. Default is '-'

  # The default domain where the Kafka APIs are exposed. ex: `myapi` will be exposed as `myapi.mycompany.org`
   defaultDomain: mycompany.org # Should set according to the public wildcard DNS/Certificate. Default is empty
   defaultPort: 9092 # Default public port for Kafka APIs. Default is 9092

  # API-Key plan security configuration
  # These are the SASL mechanisms that API key plans support.
  api-key:
    securityMechanisms: PLAIN, SCRAM-SHA-256, SCRAM-SHA-512

  # Kafka Network settings
  port: 9092
  host: 0.0.0.0
  idleTimeout: 0
  tcpKeepAlive: true
  instances: 0
  requestTimeout: 35_000 # default is 35_000 ms

  # TCP REQUIRES TLS to be set up properly
  secured: true
  ssl:
    # TCP REQUIRES SNI to be setup to match APIs
    sni: true
    clientAuth: none # Supports none, request, required
    tlsProtocols: TLSv1.2, TLSv1.3
    tlsCiphers: TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA
    keystore:
      type: jks # Supports jks, pem, pkcs12, self-signed
      path: ${gravitee.home}/security/keystore.jks # A path is required if certificate's type is jks or pkcs12
      certificates: # Certificates are required if keystore's type is pem
        - cert: ${gravitee.home}/security/mycompany.org.pem
          key: ${gravitee.home}/security/mycompany.org.key
        - cert: ${gravitee.home}/security/mycompany.com.pem
          key: ${gravitee.home}/security/mycompany.com.key
      password: secret
      watch: true # Watch for any updates on the keystore and reload it. Default is true.
    truststore:
      type: jks # Supports jks, pem, pkcs12, pem-folder (for the latter watch supports added/updated/removed files)
      path: ${gravitee.home}/security/truststore.jks
      password: secret
      watch: true # Watch for any updates on the keystore/pem and reload it. Default is true.
    openssl: false # Used to rely on OpenSSL Engine instead of default JDK SSL Engine

  haproxy: # Support for https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt
    proxyProtocol: false
    proxyProtocolTimeout: 10000
```
