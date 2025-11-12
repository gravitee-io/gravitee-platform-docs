---
description: This article walks through how to administer Organizations and Environments
---

# Administering organizations and environments

### Introduction

Gravitee offers simple methods for managing Organizations and Environments. In this article, we will cover:

* Defining general Organization settings
* Configuring Authentication settings (Identity Providers) for accessing the Gravitee API Management platform
* Setting up notification templates
* Connecting Gravitee API Management to Gravitee Cockpit for advanced Environment Management

### Defining general Organization settings

To access your Organization settings, log-in to your Gravitee API Management Console and select **Organization** from the left-hand nav. From here, you can edit all of your Organization settings. To define general organization settings, select **Settings** under **Console.**

You'll be brought the **Settings** page, where you can define:

* **Management settings**:
  * Title of of your Organization
  * The url of your Management Console
  * Whether or not to activate:
    * Support
      * User registration
      * Automatic validation of registration requests
* **Schedulers**: here you can configure how often Gravitee would check for new Tasks or Notifications. When a new task/notification is detected, a small indicator will appear in your user's icon, on the top right-hand side part of the screen. An example of a task is when someone requests access to an API of which the current user is one of the approvers so their task will be either accept or reject access to an API. An example of Notification is when an API owner uses the Messages feature to send a message to all the subscribers of an API.
* **CORS settings**: configure Organization-wide CORS settings. You can configure the following:
  * Allow-origin: the origin parameter specifies a URI that may access the resource. Scheme, domain and port are part of the _same-origin_ definition.
  * Access-Control-Allow-Methods: specifies the method or methods allowed when accessing the resource. This is used in response to a preflight request.
  * Exposed-Headers: used in response to a preflight request to indicate which HTTP headers can be used when making the actual request
  * Max age: how long the response from a pre-flight request can be cached by clients

{% hint style="info" %}
**CORS at the API level**

CORS can also be configured at the API level. To configure CORS at the API level, refer to the [CORS documentation within the API Configuration section](docs/apim/4.2/guides/api-configuration/v2-api-configuration/general-proxy-settings.md#configure-cors).
{% endhint %}

* **SMTP settings**: defines organization-wide emailing settings, which will impact how platform users are notified via email for organization-wide events. To learn more about notifications, refer to the [Notifications](docs/apim/4.2/getting-started/configuration/notifications.md) documentation. Within this section, you will define:
  * Whether or not you will enable emailing
  * Host
  * Port
  * Username
  * Password
  * Protocol
  * Subject line content
  * "From" email address
  * Mail properties
    * Whether or not to enable authentication
    * Whether or not to enable Start TLS
    * SSL Trust
