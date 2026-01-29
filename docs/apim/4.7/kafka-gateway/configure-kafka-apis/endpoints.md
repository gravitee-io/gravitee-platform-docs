---
description: An overview about endpoints.
---

# Endpoints

## Overview

Endpoints define the protocol and configuration settings by which the Gateway API will fetch data from, or post data to, the backend API. Kafka APIs can only have one endpoint group and one endpoint per endpoint group. The **Endpoints** section allows you to modify your Kafka endpoint group and/or Kafka endpoint.

<figure><img src="../../.gitbook/assets/A 11 endpoint (1).png" alt=""><figcaption></figcaption></figure>

## Edit the endpoint group

Gravitee automatically assigns the endpoint group of a Kafka API the name **Default Broker group**. To edit the endpoint group, click the **Edit** button with the pencil icon.

By selecting the **General** tab, you can change the name of your Kafka endpoint group.

<figure><img src="../../.gitbook/assets/A 11 endpoint3 (1).png" alt=""><figcaption></figcaption></figure>

By selecting the **Configuration** tab, you can edit the security settings of your Kafka endpoint group.

<figure><img src="../../.gitbook/assets/A 11 endpoint4 (1).png" alt=""><figcaption></figcaption></figure>

Gravitee Kafka APIs support **PLAINTEXT**, **SASL\_PLAINTEXT**, **SASL\_SSL**, or **SSL** as the security protocol. Select one of these from the drop-down menu and configure the associated settings to define your Kafka authentication flow:

* **PLAINTEXT:** No further security configuration is necessary.
* **SASL\_PLAINTEXT:** Choose NON&#x45;**,** GSSAPI, OAUTHBEARER, OAUTHBEARER\_TOKEN, PLAIN, SCRAM\_SHA-256, or SCRAM-SHA-512
  * **NONE:** No further security config necessary.
  * **AWS\_MSK\_IAM:** Enter the JAAS login context parameters.
  * **GSSAPI:** Enter the JAAS login context parameters.
  * **OAUTHBEARER:** Enter the OAuth token URL, client ID, client secret, and scopes to request when issuing a new token.
  * **OAUTHBEARER\_TOKEN:** Provide your custom token value.
  * **PLAIN:** Enter the username and password to connect to the broker.
  * **SCRAM\_SHA256:** Enter the username and password to connect to the broker.
  * **SCRAM\_SHA512:** Enter the username and password to connect to the broker.
*   **SSL:** Choose whether to enable host name verification, then use the drop-down menu to configure a truststore type

    * **None**
    * **JKS with content:** Enter binary content as base64 and the truststore password.
    * **JKS with path:** Enter the truststore file path and password.
    * **PKCS#12 / PFX with content:** Enter binary content as base64 and the truststore password.
    * **PKCS#12 / PFX with path:** Enter the truststore file path and password.
    * **PEM with content:** Enter binary content as base64 and the truststore password.
    * **PEM with path:** Enter the truststore file path and password.

    and a keystore type

    * **None**
    * **JKS with content:** Enter the keystore password, the key's alias, the key password, and the binary content as base64.
    * **JKS with path:** Enter the keystore password, the key's alias, the key password, and the keystore file path.
    * **PKCS#12 / PFX with content:** Enter the keystore password, the key's alias, the key password, and the binary content as base64.
    * **PKCS#12 / PFX with path:** Enter the keystore password, the key's alias, the key password, and the keystore file path.
    * **PEM with content:** Enter the certificate and private key.
    * **PEM with path:** Enter the certificate path and private key path.
* **SASL\_SSL:** Configure for both **SASL\_PLAINTEXT** and **SSL**.

## Edit the endpoint

Gravitee automatically assigns your Kafka API endpoint the name **Default Broker**. To edit the endpoint, click the pencil icon under ACTIONS.

By selecting the **General** tab, you can edit your endpoint name and the list of bootstrap servers.

<figure><img src="../../.gitbook/assets/A 11 endpoint1 (1).png" alt=""><figcaption></figcaption></figure>

By default, the endpoint inherits its configuration settings from the endpoint group to which it belongs. By selecting the **Configuration** tab, you can choose to disable that setting change the security configuration.

<figure><img src="../../.gitbook/assets/A 11 endpoint2 (1).png" alt=""><figcaption></figcaption></figure>
