# Configure the Kafka Gateway and Client

## Overview

Before you can use Gravitee to proxy in a Kafka cluster, you need to configure the Gravitee Kafka Gateway and a Kafka client. This article describes how to:

* [Configure the Kafka Gateway](configure-the-kafka-gateway-and-client.md#configure-the-kafka-gateway)
* [Configure a Kafka client](configure-the-kafka-gateway-and-client.md#configure-the-kafka-client)
* [Produce and consume messages](configure-the-kafka-gateway-and-client.md#produce-and-consume-messages)

## Configure the Kafka Gateway

{% hint style="info" %}
Running the Kafka Gateway requires an Enterprise license with the Kafka Gateway feature included. This does not come by default with a Universe license; it must be purchased separately from Gravitee.
{% endhint %}

To run the Kafka Gateway, enable the Gateway server in `gravitee.yml`.  The full example of the configuration is defined [below](configure-the-kafka-gateway-and-client.md#appendix-full-gateway-configuration). The baseline required configuration is:

```yaml
# Gateway Kafka server
kafka:
  enabled: true

  routingMode: host # default is host. Only host is supported for now.
  # Routing Host Mode
  routingHostMode:
    brokerPrefix: "broker-" # default is broker-
    domainSeparator: "-" # Used to separate broker's name from api & defaultDomain. Default is '-'

    # The default domain where the Kafka APIs are exposed. ex: `myapi` will be exposed as `myapi.mycompany.org`
    defaultDomain: "mycompany.org" # Should set according to the public wildcard DNS/Certificate. Default is empty
    defaultPort: 9092 # Default public port for Kafka APIs. Default is 9092
```

### Bootstrap server domain

* The Gateway runs multiple APIs on different **domains**. The Kafka client will connect to the API using the bootstrap server `{apiHost}.{defaultDomain}:{defaultPort}` , where `{apiHost}` is host prefix defined for each API.

<figure><img src="../.gitbook/assets/image (3).png" alt="" width="555"><figcaption><p>The Kafka client routes to the correct API through the gateway using SNI routing.</p></figcaption></figure>

* To route to the correct API, the Gateway uses [SNI routing](https://en.wikipedia.org/wiki/Server_Name_Indication), which is part of the TLS protocol. Consequently, all client connections **must** happen over TLS (with at least `security.protocol=SSL` set in the Kafka client configuration).
* The client **must** trust the certificate provided by the Gateway. To handle the variable host in the proxy bootstrap server URL, you will likely need to request a wildcard SAN to use as the certificate presented by the Gateway.
* Using the default configuration, you will ideally need a wildcard DNS entry, so that you don't need a new DNS entry for every API. In this example, the DNS and wildcard certificate should be for `*.mycompany.org`.

<details>

<summary>What if I have restrictions on the domains I can use?</summary>

If you have restrictions on the domain names you can use for APIs, you can override the default hostname by updating the Gateway configuration. For example, instead of `{apiHost}.{defaultDomain}`  as the hostname, you can set the pattern to `my-bootstrap-{apiHost}.mycompany.org` by configuring the variables below:

```yaml
# Gateway Kafka server
kafka:
  enabled: true

  routingMode: host # default is host. Only host is supported for now.
  # Routing Host Mode
  routingHostMode:
    brokerPrefix: "broker-" # default is broker-
    domainSeparator: "-" # Used to separate broker's name from api & defaultDomain. Default is '-'

    # The default domain where the Kafka APIs are exposed. ex: `myapi` will be exposed as `myapi.mycompany.org`
    defaultDomain: "mycompany.org" # Should set according to the public wildcard DNS/Certificate. Default is empty
    defaultPort: 9092 # Default public port for Kafka APIs. Default is 9092
    
    # Customize the host domain.
    # {apiHost} is a placeholder that will be replaced at runtime, when the API is deployed, by the API Host Prefix.
    bootstrapDomainPattern: "my-bootstrap-{apiHost}.mycompany.org"
```

Then, for two APIs, the client will connect to, e.g., `my-bootstrap-api1.mycompany.org:9092` and `my-bootstrap-api2.mycompany.org:9092`, as opposed to the default of `api1.mycompany.org:9092` and `api2.mycompany.org:9092`.

</details>

### Broker mapping

After the Kafka client connects to the API, the Gateway (acting as the bootstrap server) returns the list of brokers in the upstream cluster.&#x20;

<figure><img src="../.gitbook/assets/image (1) (2).png" alt="" width="563"><figcaption><p>The proxy obtains the list of brokers from the upstream cluster.</p></figcaption></figure>

To properly provide the client with the list of brokers and the associated metadata about topics and partitions on those brokers, the Gateway creates a one-to-one mapping between the brokers in the upstream cluster and the brokers seen by the client.

<figure><img src="../.gitbook/assets/image (3) (2).png" alt="" width="563"><figcaption><p>The gateway returns the list of brokers back to the client, rewritten to use the gateway hostname.</p></figcaption></figure>

The mapping combines the `brokerPrefix`, `brokerSeparator`, and `defaultDomain` variables, along with the API host prefix. The Kafka client must be able to route to `{brokerPrefix}-{brokerId}-{apiHost}.{defaultDomain}`, for as many brokers as there are in the Kafka cluster. Again, a wildcard DNS entry is the preferred way to do this.

<details>

<summary>What if I have restrictions on the domains I can use?</summary>

If you have restrictions on the domain names you can use for APIs, then, as [above](configure-the-kafka-gateway-and-client.md#what-if-i-have-restrictions-on-the-domains-i-can-use), you can override the broker domain pattern. The configuration will then be as follows (with `brokerDomainPattern` being the relevant option):

```yaml
# Gateway Kafka server
kafka:
  enabled: true

  routingMode: host # default is host. Only host is supported for now.
  # Routing Host Mode
  routingHostMode:
    brokerPrefix: "broker-" # default is broker-
    domainSeparator: "-" # Used to separate broker's name from api & defaultDomain. Default is '-'

    # The default domain where the Kafka APIs are exposed. ex: `myapi` will be exposed as `myapi.mycompany.org`
    defaultDomain: "mycompany.org" # Should set according to the public wildcard DNS/Certificate. Default is empty
    defaultPort: 9092 # Default public port for Kafka APIs. Default is 9092
    
    # Customize the host domain.
    # {apiHost} is a placeholder that will be replaced at runtime, when the API is deployed, by the API Host Prefix.
    # {brokerId} is a placeholder that stand for the broker id
    bootstrapDomainPattern: "my-bootstrap-{apiHost}.mycompany.org"
    brokerDomainPattern: "{apiHost}-broker-{brokerId}-test.mycompany.org"
```

With this, if there are three brokers in the upstream cluster, the client must be able to route to `api1-broker-0-test.mycompany.org`,  `api1-broker-0-test.mycompany.org`, and `api1-broker-0-test.mycompany.org`, along with `my-bootstrap-api1.mycompany.org`.

</details>

<details>

<summary>What if I don't have a valid DNS entry?</summary>

If you do not have a valid DNS entry for your Gateway because, for example, you're running the Gateway on `localhost`, then you may need to update your `/etc/hosts` file.&#x20;

If you are running the Gateway locally in Docker, and setting the `defaultDomain` to `kafka.local`, you can update your `/etc/hosts` file with the following entries:

```
127.0.0.1    localhost kafka.local api1.kafka.local
::1          localhost broker-0-api1.kafka.local broker-1-api1.kafka.local broker-2-api1.kafka.local
127.0.0.1    localhost broker-0-api1.kafka.local broker-1-api1.kafka.local broker-2-api1.kafka.local
```

To add more APIs, you will need to add another API host to the first line and two more entries for each API to the IPs `::1` and `127.0.0.1`. With two APIs, this becomes:

```
127.0.0.1    localhost kafka.local api1.kafka.local api2.kafka.local
::1          localhost broker-0-api1.kafka.local broker-1-api1.kafka.local broker-2-api1.kafka.local
127.0.0.1    localhost broker-0-api1.kafka.local broker-1-api1.kafka.local broker-2-api1.kafka.local
::1          localhost broker-0-api2.kafka.local broker-1-api2.kafka.local broker-2-api2.kafka.local
127.0.0.1    localhost broker-0-api2.kafka.local broker-1-api2.kafka.local broker-2-api2.kafka.local
```

</details>

### Defining the default entrypoint configuration

By default, clients talk to Kafka APIs by setting the bootstrap server as `{apiHost}.{defaultDomain}:{defaultPort}`. This is set in `gravitee.yml`, but for convenience, when developing APIs in the UI, you can set the default values appended to the hostname. You can also leave this value blank and respecify the full hostname in the API.

To configure the APIM Console to use the Kafka domain and port values for your Organization:

1. Log in to your APIM Console.
2. Select **Organization** from the bottom of the left nav.
3. Select **Entrypoints & Sharding Tags** from the left nav.
4.  In the **Entrypoint Configuration** section, confirm that the **Default Kafka domain** and **Default Kafka port** values match those of your Kafka API.\


    <figure><img src="../.gitbook/assets/00 kafka.png" alt=""><figcaption></figcaption></figure>

    This value is then displayed on the entrypoint page of your APIs.\


    <figure><img src="../.gitbook/assets/00 kafka 1.png" alt=""><figcaption></figcaption></figure>

## Configure the Kafka client

To use the Kafka Gateway, you use a regular Kafka client. There are many implementations of the Kafka client, and you can use any client that supports the full Kafka protocol.

{% hint style="info" %}
As of the 4.6.0 release, the Kafka Gateway requires the Kafka client to be version 3.0 or above.
{% endhint %}

The default client to talk to Kafka is packaged within the Kafka binary and is based on Java. The prerequisite for using this client is a JRE. See the [Java documentation](https://www.java.com/en/) for more information on how to install a JRE.

1. Download Kafka. Gravitee Kafka Gateway is compatible with the source code or either binary download of each supported Kafka release. For more information about downloading Kafka, go to [Kafka's download page](https://kafka.apache.org/downloads).
2. Store the downloaded file structure in a secure place. The root folder will be your working directory when calling your Kafka API.

The client is now ready to use, but to produce and consume messages you must create a `.properties` file in the root folder as described below.

{% hint style="info" %}
At this point, you can begin creating and deploying APIs to the Gravitee Kafka Gateway.
{% endhint %}

## Produce and consume messages

You can use the Kafka Gateway and client to call your [Kafka API](create-kafka-apis.md) and, as a primary use case, produce or consume messages. You can also proxy requests to create and manage topics, update partitions, and manage consumer groups.

### Prerequisites

The following prerequisites must be met before you can produce and consume Kafka messages:

* You must have an active subscription to a published API [plan](../expose-apis/plans/) belonging to your Gravitee Kafka API.&#x20;
* If you are subscribing to an OAuth2 or JWT plan, your application must reference the same client ID that you use for authorization.&#x20;

{% hint style="info" %}
When using [Gravitee Access Management (AM)](https://documentation.gravitee.io/am) as the authorization server, the client ID is generated when you create a Gravitee AM Authorization Server resource. To access this resource, you must also create an application in Gravitee Access Management.&#x20;
{% endhint %}

For plan, application, subscription, and resource information, see the following:

* For information on how to create and manage plans, see [Plans](plans.md).
* To learn how to create an application for a Gravitee plan, see [Applications](applications.md).
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


    <div align="left"><figure><img src="../.gitbook/assets/00 kafka 2.png" alt="" width="563"><figcaption></figcaption></figure></div>
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
    brokerPrefix: "broker-" # default is broker-
    domainSeparator: "-" # Used to separate broker's name from api & defaultDomain. Default is '-'

    # The default domain where the Kafka APIs are exposed. ex: `myapi` will be exposed as `myapi.mycompany.org`
    defaultDomain: "mycompany.org" # Should set according to the public wildcard DNS/Certificate. Default is empty
    defaultPort: 9092 # Default public port for Kafka APIs. Default is 9092

    # If necessary, customize the host domain.
    # {apiHost} is a placeholder that will be replaced at runtime, when the API is deployed, by the API Host Prefix.
    # {brokerId} is a placeholder that stand for the broker id
    bootstrapDomainPattern: "my-bootstrap-{apiHost}.mycompany.org"
    brokerDomainPattern: "{apiHost}-broker-{brokerId}-test.mycompany.org"

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
