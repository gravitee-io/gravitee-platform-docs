---
description: This article walks through how to administer Organizations and Environments
---

# Organizations and Environments

## Introduction

### Organizations

In Gravitee, **Organizations** reflect a logical part of your company in a way that makes the most for your setup. For example, an organization could be a region or business unit.

In the context of an APIM installation, it is the level at which shared configurations for environments are managed, such as:

* Users
* Roles
* Identity providers
* Notification templates

Gravitee Organizations can include multiple environments.

#### Managing platform access

As a part of Organization administration, Gravitee offers multiple manners of managing and controlling access to the Gravitee platform. This is done by configuring Identity providers and login/registration settings.

{% hint style="info" %}
**This is different from Gravitee Access Management**

This should _not_ be confused with Gravitee Access Management, which is a fully-featured Identity and Access Management solution that is used for controlling access to applications and APIs. To learn more about the Access Management product, please refer to the [Gravitee Access Management documentation](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/hbYbONLnkQLHGL1EpwKa/).
{% endhint %}

### Environments

In Gravitee, **Environments** are flexible and act as the workspace in which users can manage their APIs, applications, and subscriptions. An environment handles its own categories, groups, documentation pages, and quality rules.

Examples of environments:

* Technical environments such as DEV / TEST / PRODUCTION
* Functional environments such as PRIVATE APIS / PUBLIC APIS / PARTNERSHIP

## Defining general Organization settings

{% @arcade/embed flowid="sAy3l769Swk9epGVWCED" url="https://app.arcade.software/share/sAy3l769Swk9epGVWCED" %}

To access your Organization settings, log-in to your Gravitee API Management Console and select **Organization** from the left-hand nav. From here, you can edit all of your Organization settings. To define general organization settings, select **Settings** under **Console.**

You'll be brought the **Settings** page, where you can define:

* **Management settings**:
  * Title of of your Organization
  * The url of your Management Console
  * Whether or not to activate:
    * Support
      * User registration
      * Automatical validation of registration requests
* **Schedulers**: here you can configure how often Gravitee would check for new Tasks or Notifications. When a new task/notification is detected, a small indicator will appear in your user's icon, on the top right-hand side part of the screen. An example of a task is when someone requests access to an API of which the current user is one of the approvers so their task will be either accept or reject access to an API. An example of Notification is when an API owner uses the Messages feature to send a message to all the subscribers of an API.
* **CORS settings**: configure Organization-wide CORS settings. You can configure the following:
  * Allow-origin: the origin parameter specifies a URI that may access the resource. Scheme, domain and port are part of the _same-origin_ definition.
  * Access-Control-Allow-Methods: specifies the method or methods allowed when accessing the resource. This is used in response to a preflight request.
  * Exposed-Headers: used in response to a preflight request to indicate which HTTP headers can be used when making the actual request
  * Max age: how long the response from a pre-flight request can be cached by clients

{% hint style="info" %}
**CORS at the API level**

CORS can also be configured at the API level. To configure CORS at the API level, refer to the [CORS documentation within the API Configuration section](broken-reference).
{% endhint %}

* **SMTP settings**: defines organization-wide emailing settings, which will impact how platform users are notified via email for organization-wide events. To learn more about notifications, refer to the [Notifications](broken-reference) documentation. Within this section, you will define:
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
