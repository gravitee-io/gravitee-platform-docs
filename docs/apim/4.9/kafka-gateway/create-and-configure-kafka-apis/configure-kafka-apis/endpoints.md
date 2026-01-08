---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings the Gateway API uses to fetch data from or post data to the backend API. Kafka APIs can have one endpoint group with a single endpoint. The **Endpoints** section lets you modify your Kafka endpoint group and Kafka endpoint.

<figure><img src="../../../.gitbook/assets/sample-kafka-api-endpoint.png" alt=""><figcaption></figcaption></figure>

## Security protocols&#x20;

Gravitee Kafka APIs support **PLAINTEXT**, **SASL\_PLAINTEXT**, **SASL\_SSL**, or **SSL** as the security protocol to connect to the Kafka cluster.

### SASL mechanisms

In addition to [Kafka's](https://kafka.apache.org/documentation/#security_overview) standard mechanisms, Gravitee supports:

* **NONE**: A stub mechanism that falls back to `PLAINTEXT` protocol.
* **OAUTHBEARER\_TOKEN**: A mechanism that defines a fixed token or a dynamic token from [Gravitee Expression Language](../../../gravitee-expression-language.md).
*   **DELEGATE\_TO\_BROKER**: Authentication is delegated to the Kafka broker.

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p>When using <code>DELEGATE_TO_BROKER</code>, the supported mechanisms available to the client are <code>PLAIN</code> and <code>AWS_IAM_MSK</code>. The <code>AWS_MSK_IAM</code> mechanism requires you to host the Kafka Gateway on AWS. Otherwise, authentication fails.</p></div>

## Edit the endpoint group

Gravitee assigns each Kafka API endpoint group the default name **Default Broker group.** To edit the endpoint group, complete the following steps:&#x20;

1.  Click the **Edit** button with the pencil icon to edit the endpoint group.

    <figure><img src="../../../.gitbook/assets/edit-button-endpoint-group.png" alt=""><figcaption></figcaption></figure>
2.  Select the **General** tab to change the name of your Kafka endpoint group.

    <figure><img src="../../../.gitbook/assets/image (165).png" alt=""><figcaption></figcaption></figure>
3.  Select the **Configuration** tab to edit the security settings of your Kafka endpoint group.

    <figure><img src="../../../.gitbook/assets/select-configuration-tab-endpoint-group.png" alt=""><figcaption></figcaption></figure>
4.  Select one of the security protocols from the drop-down menu, and then configure the associated settings to define your Kafka authentication flow.

    <figure><img src="../../../.gitbook/assets/supported-endpoint-security-protocol.png" alt=""><figcaption></figcaption></figure>

* **PLAINTEXT:** No further security configuration is necessary.
* **SASL\_PLAINTEXT:** Choose NON&#x45;**,** GSSAPI, OAUTHBEARER, OAUTHBEARER\_TOKEN, PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, or DELEGATE\_TO\_BROKER.
  * **NONE:** No additional security configuration required.
  * **AWS\_MSK\_IAM:** Enter the JAAS login context parameters.
  * **GSSAPI:** Enter the JAAS login context parameters.
  * **OAUTHBEARER:** Enter the OAuth token URL, client ID, client secret, and the scopes to request when issuing a new token.
  * **OAUTHBEARER\_TOKEN:** Provide your custom token value.
  * **PLAIN:** Enter the username and password to connect to the broker.
  * **SCRAM-SHA-256:** Enter the username and password to connect to the broker.
  * **SCRAM-SHA-512:** Enter the username and password to connect to the broker.
  * **DELEGATE\_TO\_BROKER:** No additional security configuration required.
* **SSL:** Choose whether to enable host name verification, and then use the drop-down menu to configure a truststore type.
  * **None**
  * **JKS with content:** Enter binary content as base64 and the truststore password.
  * **JKS with path:** Enter the truststore file path and password.
  * **PKCS#12 / PFX with content:** Enter binary content as base64 and the truststore password.
  * **PKCS#12 / PFX with path:** Enter the truststore file path and password.
  * **PEM with content:** Enter binary content as base64 and the truststore password.
  * **PEM with path:** Enter the truststore file path and password and the keystore type.
* **SASL\_SSL:** Configure both SASL authentication and SSL encryption, choose a **SASL** mechanism from the options listed under **SASL\_PLAINTEXT**, and then configure **SSL** settings as described in the **SSL** section.

## Edit the endpoint

Gravitee automatically assigns your Kafka API endpoint the name **Default Broker**.&#x20;

1.  Click the pencil icon under **ACTIONS** to edit the endpoint.

    <figure><img src="../../../.gitbook/assets/actions-edit-icon-button.png" alt=""><figcaption></figcaption></figure>
2.  Select the **General** tab to edit your endpoint name and the list of bootstrap servers.

    <figure><img src="../../../.gitbook/assets/select-the-general-tab.png" alt=""><figcaption></figcaption></figure>
3.  By default, endpoints inherit configuration settings from their endpoint group. To override these settings, select the **Configuration** tab and configure custom security settings.

    <figure><img src="../../../.gitbook/assets/ovveride-endpoints-configuration.png" alt=""><figcaption></figcaption></figure>
