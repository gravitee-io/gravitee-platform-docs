# Resources

## Overview

Resources provide a way to define reusable configuration sets.

## Resource types

Gravitee AM currently supports the following resources:

* HTTP Factor
* Infobip 2FA
* SMTP
* Twilio Verify

Click on the tabs below to learn more.

{% tabs %}
{% tab title="HTTP Factor" %}
The HTTP Factor resource uses HTTP requests to send and verify a generated, one time code. It supports Gravitee Expression Language (EL) to configure the resource properties.

<figure><img src="../.gitbook/assets/resource_http 2.png" alt="" width="563"><figcaption><p>Configure an HTTP Factor resource</p></figcaption></figure>

To configure an HTTP Factor resource, you must specify:

* **Resource name:** Create a resource name
* **Base URL:** Enter the base URL to which to send a request. This field supports Gravitee Expression Language.
* **Send Verification Code**
  * **Endpoint:** Enter the resource path. This value will be appended to the base URL, must start with a '/', and supports EL.
  * **HTTP Method:** Select the HTTP method used to call the resource. Available options are **None**, **CONNECT**, **DELETE**, **GET**, **HEAD**, **OPTIONS**, **PATCH**, **POST**, **PUT**, **TRACE**, and **OTHER**.
  * **HTTP Headers:** Enter the HTTP header **Name** and **Value** (supports EL)
  * **Request body:** Enter the HTTP request body with which to call (supports EL)
  * **Response Error Conditions (one of)**
    * **Value:** Enter the condition to be verified following the remote call (e.g., `{#response.status == 400}`). Supports EL.
    * **Exception:** Select the exception sent to the consumer if the condition is true. Available options are limited to **SendChallengeException**.
    * **Message:** Enter the error message if the condition is true (supports EL)
* **Check Verification Code**
  * **Endpoint:** Enter the resource path. This value will be appended to the base URL, must start with a '/', and supports EL.
  * **HTTP Method:** Select the HTTP method used to call the resource. Available options are **None**, **CONNECT**, **DELETE**, **GET**, **HEAD**, **OPTIONS**, **PATCH**, **POST**, **PUT**, **TRACE**, and **OTHER**.
  * **HTTP Headers:** Enter the HTTP header **Name** and **Value** (supports EL)
  * **Request body:** Enter the HTTP request body with which to call (supports EL)
  * **Response Error Conditions (one of)**
    * **Value:** Enter the condition to be verified following the remote call (e.g., `{#response.status == 400}`). Supports EL.
    * **Exception:** Select the exception sent to the consumer if the condition is true. Available options are limited to **InvalidCodeException**.
    * **Message:** Enter the error message if the condition is true (supports EL)
* **HTTP client connect timeout:** Enter the duration (ms) of the HTTP client connection timeout (default 10000 ms)
* **HTTP client max pool size:** Maximum size of the HTTP client connection pool (default 100)
* **Use system proxy:** Toggle ON or OFF
{% endtab %}

{% tab title="Infobip 2FA" %}
The Infobip 2FA resource is used to generate PINs, or passcodes, that can be delivered by SMS, voice, or email.

<figure><img src="../.gitbook/assets/resource_infobip 2.png" alt="" width="563"><figcaption><p>Configure an Infobip 2FA resource</p></figcaption></figure>

To configure an Infobip 2FA resource, you must specify:

* **Resource name:** Create a resource name
* **Application ID:** Enter the 2FA application ID
* **Message ID:** Enter the message template ID that will be sent to the phone number
* **API Key:** Enter the API key
* **API Key Prefix:** Select a value to use for the prefix of the API key. The available options are **Basic**, **App**, **IBSSO**, and **Bearer**.
* **Base URL:** Enter the base URL, including protocol (e.g., https://this-is-my-url.com)
{% endtab %}

{% tab title="SMTP" %}
SMTP is a resource you can use to send email over SMTP. Once you have created your SMTP resource, you can reference it in the [email factor configuration](multi-factor-authentication/managing-factors/email.md).

<figure><img src="../.gitbook/assets/resource_smtp 2.png" alt="" width="563"><figcaption><p>Configure an SMTP resource</p></figcaption></figure>

To configure an SMTP resource, you must specify:

* **Resource name:** Create a resource name
* **Hostname:** Enter the hostname or IP of the SMTP server
* **Port:** Enter the port of the SMTP server
* **From:** Enter the email address of the sender
* **Protocol:** Enter the protocol used to send the email
* **Authentication:** Toggle ON to use authentication
* **Start TLS:** Toggle ON to start TLS
* **SSL Trust:** Enter trusted domains. If set to an asterisk (\*), all hosts are trusted. If set to a whitespace-separated list of hosts, those hosts are trusted (e.g., smtp.gmail.com).
* **SSL Protocols:** Enter a whitespace-separated list of SSL protocols that are enabled for SSL connections (e.g., TLSv1 TLSv1.1)
{% endtab %}

{% tab title="Twilio Verify" %}
The Twilio Verify resource configures a Twilio account to use the `Twilio Verify` service for Multi-factor Authentication. Once you have created your Twilio resource, you can reference it in SMS factor configuration.

<figure><img src="../.gitbook/assets/resource_twilio verify 2.png" alt="" width="563"><figcaption><p>Configure a Twilio Verify resource</p></figcaption></figure>

To configure a Twilio Verify resource, you must specify:

* **Resource name:** Create a resource name
* **Service ID:** Enter the Verification Service ID
* **Account ID:** Enter your Twilio account ID
* **Authentication Token:** Enter the authentication token linked to your account
* **Use system proxy:** Toggle ON or OFF
{% endtab %}
{% endtabs %}

## Create a new resource

1. Log in to AM Console
2. Select **Settings** from the left nav
3. From the Resources section of the inner left nav, select **Services**
4.  Click the plus icon <img src="/broken/files/3KzHhiYUzObdj2EiETbU" alt="" data-size="line"> at the bottom of the page

    <div align="left"><figure><img src="../.gitbook/assets/resource_add.png" alt="" width="563"><figcaption><p>Add a resource</p></figcaption></figure></div>
5.  Select the resource type and click **Next**

    <div align="left"><figure><img src="../.gitbook/assets/resource_select.png" alt="" width="563"><figcaption><p>Create a new HTTP Factor resource</p></figcaption></figure></div>
6.  Enter the resource configuration values (see [Resource Types](resources.md#resource-types)) and click **Create**

    <div align="left"><figure><img src="../.gitbook/assets/resource_configure.png" alt="" width="563"><figcaption><p>Configuration for an HTTP Factor resource</p></figcaption></figure></div>
7.  Your resource is now available for use in AM

    <div align="left"><figure><img src="../.gitbook/assets/resource_available.png" alt="" width="563"><figcaption><p>The newly-created resource is now available</p></figcaption></figure></div>
