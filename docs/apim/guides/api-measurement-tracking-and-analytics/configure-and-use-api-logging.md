---
description: Learn how to configure and use API logging.
---

# Configure and Use API Logging

### Introduction

Logging refers to the process of recording and monitoring API requests, responses, and related events. It enables developers and administrators to track API usage, monitor performance, and troubleshoot issues by collecting and analyzing data such as timestamps, endpoints, response times, and error messages.

Gravitee enables you to configure and view logs for your APIs. In this article, we will walk through how to configure logging in the API Management UI.

### Configure logging at the API and Gateway levels

{% @arcade/embed flowId="nifDyFJpS1oFPpGfCwqu" url="https://app.arcade.software/share/nifDyFJpS1oFPpGfCwqu" %}

An API's logs will be visible at the level of the individual API. This is viewed under an APIs **Analytics** by selecting **Logs.**\


<figure><img src="../../.gitbook/assets/Access API logs.gif" alt=""><figcaption><p>Access an API's logs</p></figcaption></figure>

If logging isn't enabled for your API, you will need to enable it manually. You can enable logging at the both the Gateway and the API levels.&#x20;

#### Configure logging at the API level

To first enable logging at the API level, select **Configure the logging** at the top of your APIs logs page. You'll be brought to the **Logging configuration** page. To enable logging, toggle **Enable logging** ON.&#x20;

Once you've enabled logging, you can further define how logging works in Gravitee by defining the **Logging mode, Content Mode, Scope Mode,** and any **Conditions**. Please see the tabs below to learn more about each.

{% tabs %}
{% tab title="Logging Mode" %}
**Logging Mode** allows you to define which stakeholders are logged. You'll have three options:

* **Client only**: this options enables logging for HTTP request headers and payload details for interactions between only the client and gateway
* **Proxy only**: this option enables logging for HTTP request headers and payload details for interactions solely between the gateway and your backend resource
* **Client & proxy**: this options logs HTTP request headers and payload content for both of the above

{% hint style="info" %}
You choose for logs to only capture headers and/or payload details in the **Content Mode** settings. Please see the next tab for more details.
{% endhint %}
{% endtab %}

{% tab title="Content Mode" %}
Content Mode defines which kinds of content are captured in logs. You can choose for logs to capture:

* **Headers only**
* **Payload details only**
* **Headers and Payloads**
{% endtab %}

{% tab title="Scope Mode" %}
**Scope Mode** defines which interactions that logs capture. You have three options:

* **Request only**: this tells the Gateway to only capture logs for request content
* **Response only**: this tells the Gateway to only capture logs for the response content
* **Request & Response**: this tells the Gateway to capture logs for both request content and response content
{% endtab %}
{% endtabs %}

After you've configured settings for **Logging mode, Content Mode,** and **Scope Mode,** you can optionally define conditions for your logging in the **Conditions** text field. You can set conditions around:

* application or plan
* request header or query parameter
* HTTP method
* request IP address
* duration
* end date

Conditions are set using the Gravitee expression language.

#### Configure logging at the Gateway level

You can also configure logging permissions and settings at the Gateway level. To do this, select Settings in the far left-hand nav. Then, within the Settings menu, select **API Logging** underneath the **Gateway** section of your settings. From here, you can choose to enable:

* Auditing API Logging consultation
* The display of end user information in your API logging (this is useful for when you are using OAuth2 or JWT plans)
* Generation of API logging as audit events (API\_LOGGING\_ENABLED, API\_LOGGING\_DISABLED, API\_LOGGING\_UPDATED)

You can also define the maximum duration (in ms) for the activation of logging mode by entering in a numerical value in the **Maximum duration** text field.

