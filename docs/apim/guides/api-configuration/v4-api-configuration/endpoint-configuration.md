---
description: >-
  This article walks through how to configure endpoints for your Gravitee v4
  APIs
---

# Endpoint configuration

## Introduction

In Gravitee, Gateway Endpoints define the protocol and configuration settings by which the gateway API will fetch data from, or post data to, the backend API.

After you've created your gateway API and selected your Endpoints(s), you can configure them on the API's page. This article walks through that process.&#x20;

## Configure v4 API Endpoints

v4 APIs currently support the following endpoints:

* **Kafka**: enables the Gravitee API Gateway to establish a persistent connection with a Kafka topic as a backend resource or target
* **MQTT 5**: enables the Gravitee API Gateway to establish a persistent connection with a MQTT topic as a backend resource or target
* **RabbitMQ**: enables the Gravitee API Gateway to establish a persistent connection with RabbitMQ as a backend resource or target. This will only work if you are using RabbitMQ and the AMQP 0-9-1 protocol. Because this endpoint supports the AMQP 0-9-1 protocol, it may support other event brokers and message queues that communicate over the AMQP 0-9-1 protocol, however, we do not guarantee or officially support these implementations.
* **Solace**: enables the Gravitee API Gateway to establish a persistent connection with Solace as a backend resource or target
* **Mock**: enables the Gateway to simulate responses from a server for testing API implementations

To access Endpoint configuration, head to the **APIs** page, and select your API. Then under **Endpoints**, select **Backend Services.** Depending on which Endpoint(s) your API utilizes, Endpoint configuration may differ. Please refer to the following sections that cover configuration details for each.&#x20;

## Kafka

The **Kafka** endpoint allows the Gateway to open up a persistent connection and/or call a backend Kafka broker via a Kafka client set up by the Gravitee Gateway. If you chose this endpoint, you will need to configure:

* How the Gateway will interact the broker by instructing the Gravitee Gateway's Kafka client to act as either a producer, a consumer, or both a producer and consumer. Choose either **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:
  * **Use Producer:** tells the Gateway Kafka client to be prepared to produce messages and send them to the Kafka broker that you define as your endpoint
  * **Use Consumer:** tells the Gateway Kafka client to be prepared to consume messages from the Kafka broker that you define as your endpoint
  * **Use Producer and Consumer:** tell the Gateway Kafka client to both **Use Producer** and **Use Consumer**
* **Bootstrap servers:** define the comma-separated list of host/port pairs to use for establishing the initial connection to the Kafka cluster. The client will make use of all servers irrespective of which servers the list designates for bootstrapping - this list only pertains to the initial hosts used to discover the full set of servers.
* **Initial security settings:** you will define more Gravitee Gateway-specific security settings later on, but this is where you define your Kafka-specific authentication flow. Gravitee supports PLAINTEXT, SASL\_PLAINTEXT, SASL\_SSL, and SSL as protocols. Depending on which you choose, you will need to define:
  * **PLAINTEXT:** no further security config necessary.
  * **SASL**
    * **SASL mechanism:** used for client connections. This will be GSSAPI, OAUTHBEARER, PLAIN, SCRAM\_SHA-256, or SCRAM-SHA-512.
    * **SASL JAAS Config:** the JAAS login context parameters for SASL connections in the format used by JAAS configuration files.
  * **SSL**
    * **Truststore:** depending on your truststore type, you will need to define:
      * **PEM with location**
        * Define the **location of your truststore file**.
      * **PEM with certificates**
        * Define the trusted certificates in the format specified by 'ssl.truststore.type'.
      * **JKS with location**
        * Define the **location of your truststore file**.
        * Define the **SSL truststore password** for the truststore file.
      * **JKS with certificates**
        * Define the trusted certificates in the format specified by 'ssl.truststore.type'.
        * Define the **SSL truststore password** for the truststore file.
      * **PKCS12 with location**
        * Define the **location of your truststore file**.
        * Define the **SSL truststore password** for the truststore file.
      * **PKCS12 with certificates**
        * Define the **trusted certificates** in the format specified by 'ssl.truststore.type'.
        * Define the **SSL truststore password** for the truststore file.
    * **Keystore:**
      * **PEM with location**
        * Define the **SSL keystore certificate chain**.
        * Define the location of your keystore file.
      * **PEM with Key**
        * Define the **SSL keystore certificate chain**.
        * Define the **SSL keystore private key** by defining the **Key** and the **Key password**.
      * **JKS with location**
        * Define the **location of your keystore file**.
        * Define the **SSL keystore password** for the keystore file.
      * **JKS with Key**
        * Define the **SSL keystore private key** by defining the **Key** and the **Key password**.
        * Define the **SSL keystore password** for the keystore file.
      * **PKCS12 with location**
        * Define the **location of your keystore file**.
        * Define the **SSL keystore password** for the keystore file.
      * **PKCS12 with Key**
        * Define the **SSL keystore private key** by defining the **Key** and the **Key password**.
        * Define the **SSL keystore password** for the keystore file.
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway Kafka client will rely on for producing messages to your backend Kafka topic/broker. You will need to define:
  * **Topic:** the topic that the broker uses to filter messages for each connected client.
* **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway Kafka client will rely on for consuming messages from your backend Kafka topic/broker. You will need to define:
  * **Topic:** the topic(s) from which your Gravitee Gateway client will consume messages.
  * **Encode message Id:** Toggle this ON or OFF to encode message IDs in base64.
  * **Auto offset reset:** Use the **Auto offset reset** drop-down menu to configure what happens when there is no initial offset in Kafka, or if the current offset no longer exists on the server:
    * **Earliest:** automatically reset the offset to the earliest offset.
    * **Latest:** automatically reset the offset to the latest offset.
    * **None:** throw an exception to the consumer if no previous offset is found for the consumer's group.
    * **Anything else:** throw an exception to the consumer.

## MQTT 5

The **MQTT 5.X** endpoint allows the Gateway to open up a persistent connection and/or call a backend MQTT broker, as long as that broker is running on MQTT 5.x, via an MQTT client set up by the Gravitee Gateway. If you chose this endpoint, you will need to configure:

* How the Gateway will interact the broker by instructing the Gravitee Gateway's MQTT client to act as either a producer, a consumer, or both a producer and consumer. Choose either **Use Consumer**, **Use Producer**, or **Use Consumer and Producer** from the drop-down menu to do one of the following:
  * **Use Producer:** tells the Gateway MQTT client to be prepared to produce messages and send them to the MQTT broker that you define as your endpoint.
  * **Use Consumer:** tells the Gateway MQTT client to be prepared to consume messages from the MQTT broker that you define as your endpoint.
  * **Use Producer and Consumer**: tell the Gateway MQTT client to both **Use Producer** and **Use Consumer**.
* **Server host:** define the serverHost for the MQTT broker that you are using as your endpoint.
* **Server port:** define the serverPort for the MQTT broker that you are using as your endpoint.
* **Reconnect attempts:** specify an integer number of reconnect attemps that the Gateway will initiate if the Gateway MQTT client disconnects from the MQTT broker. The maximum is 10.
* **Session expiry interval:** defines the period of time that the broker stores the session information of that particular MQTT client. When the session expiry interval is set to **0** or the CONNECT packet does not contain an expiry value, the session information is immediately removed from the broker when the client network connection closes.
* **Clean start:** toggle **Clean start** ON or OFF to enable or disable the **cleanStart** tag. This tag causes the MQTT broker to discard any previous session data and the Gateway MQTT client to connect with a fresh session.
* **Initial security settings:** you will define more Gravitee Gateway-specific security settings later on, but this is where you define your MQTT-specific authentication flow. Gravitee supports username and password using TLS. You will need to define:
  * Username
  * Password
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway MQTT client will rely on for producing messages to your backend MQTT topic/broker. You will need to specify:
  * **Topic:** the UTF-8 string that the broker uses to filter messages for each connected client. The topic consists of one or more topic levels. Each topic level is separated by a forward slash (topic level separator).
  * **Retain settings:** whether the retain flag must be set for every published message by toggling **Retained** ON or OFF. If enabled, the broker stores the last retained message.
  * **Message expiry interval:** defines the period of time that the broker stores the PUBLISH message for any matching subscribers that are not currently connected. When no message expiry interval is set, the broker must store the message for matching subscribers indefinitely. When the "retained=true" option is set on the PUBLISH message, this interval also defines how long a message is retained on a topic.
  * **Response topic:** represents the topics on which the responses from the message receivers are expected.
* **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway MQTT client will rely on for consuming messages from your backend MQTT topic/broker. You must define the **Topic** from which the Gateway MQTT client will consume messages.

## Solace

If you choose the Solace endpoint, the Gravitee Gateway will be able to create an API that exposes Solace resources and event APIs via your chosen Gravitee Entrypoint(s). You will need to configure:

* Url: your Soalce broker's url
* VPN name
* **Producer settings** (if you chose **Use Producer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway MQTT client will rely on for producing messages to your backend MQTT topic/broker. You will need to specify:
  * **Topic:** the UTF-8 string that the broker uses to filter messages for each connected client. The topic consists of one or more topic levels. Each topic level is separated by a forward slash (topic level separator).
  * **Retain settings:** whether the retain flag must be set for every published message by toggling **Retained** ON or OFF. If enabled, the broker stores the last retained message.
  * **Message expiry interval:** defines the period of time that the broker stores the PUBLISH message for any matching subscribers that are not currently connected. When no message expiry interval is set, the broker must store the message for matching subscribers indefinitely. When the "retained=true" option is set on the PUBLISH message, this interval also defines how long a message is retained on a topic.
  * **Response topic:** represents the topics on which the responses from the message receivers are expected.
* **Consumer settings** (if you chose **Use Consumer** or **Use Producer and Consumer**): define the settings that the Gravitee Gateway MQTT client will rely on for consuming messages from your backend MQTT topic/broker. You must define the **Topic** from which the Gateway MQTT client will consume message
* **Security settings**:
  * Toggle Authentication configuration ON or OFF. If you toggle this OFF, you will have no further configuration necessary. If you toggle this ON, you will need to:
    * Define the username used for authentication
    * Define the password used for authentication

## Mock

The Endpoint Mock endpoint allows you to mock a backend service to emulate the behavior of a typical HTTP server and test processes. If you chose this endpoint, you will need to configure:

* **Interval between messages publication:** defines, in milliseconds, the interval between published messages. The default is 1000.
* **Content of published messages:** defines the content of the message body that will be streamed. The default is "mock message".
* **Count of published messages:** defines, as an integer, the maximum number of published messages that are streamed as a part of the mocking. If left unspecified, there will be no limit.
