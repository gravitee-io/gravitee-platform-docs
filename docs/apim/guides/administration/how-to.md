---
description: This article walks through how to administer Organizations and Environments
---

# Administering organizations and environments

### Introduction

Gravitee offers simple methods for managing Organizations and Environments. In this article, we will cover:

* Defining general Organization settings
* Configuring Authentication settings (Identity Providers) for accessing the Gravitee API Management platform&#x20;
* Setting up notification templates
* Connecting Gravitee API Management to Gravitee Cockpit for advanced Environment Management

### Defining general Organization settings

{% @arcade/embed flowId="sAy3l769Swk9epGVWCED" url="https://app.arcade.software/share/sAy3l769Swk9epGVWCED" %}

To access your Organization settings, log-in to your Gravitee API Management UI and select **Organization** from the left-hand nav. From here, you can edit all of your Organization settings. To define general organization settings, select **Settings** under **Console.**&#x20;

You'll be brought the **Settings** page, where you can define:

* **Management settings**:
  * Title of of your Organization
  * The url of your Management UI
  * Whether or not to activate:
    * Support
      * User registration
      * Automatical validation of registration requests
* **Theme settings**: this is where you can alter the visual theme of your Management UI for your Organization. You can upload a custom logo and loader.
* **Schedulers**:&#x20;
* **CORS settings**: configure Organization-wide CORS settings. You can configure the following:
  * Allow-origin: the origin parameter specifies a URI that may access the resource. Scheme, domain and port are part of the _same-origin_ definition.
  * Access-Control-Allow-Methods: specifies the method or methods allowed when accessing the resource. This is used in response to a preflight request.
  * Exposed-Headers: used in response to a preflight request to indicate which HTTP headers can be used when making the actual request
  * Max age: how long the response from a pre-flight request can be cached by clients

{% hint style="info" %}
**CORS at the API level**

CORS can also be configured at the API level. To configure CORS at the API level, refer to the [CORS documentation within the API Configuration section](../api-configuration/configure-cors.md#configure-cors).&#x20;
{% endhint %}

* **SMTP settings**: defines organization-wide emailing settings, which will impact how platform users are notified via email for organization-wide events. To learn more about notifications, refer to the [Configure Notifications](../../getting-started/configuration/notifications.md) documentation. Within this section, you will define:
  * Whether or not you will enable emailing
  * Host
  * Port
  * Username
  * PAssword
  * Protocol
  * Subject line content
  * "From" email address
  * Mail properties
    * Whether or not to enable authentication
    * Whether or not to enable Start TLS
    * SSL Trust

### Defining Organization authentication and access settings

You can also configure your Organization's authentication and access settings. To do this, log-in to your Gravitee API Management UI and select Organization from the left-hand nav. Then, select **Authentication** underneath **Console.** From here, you will be brought to the **Authentication** page. Here, you can:

* Enable or disable a log-in form for the API Management UI by toggling **Show login form on management console** ON or OFF
* Manage Identity Providers for logging in and registering Gravitee platform users

#### Adding, editing, and managing identity providers

Gravitee supports the following Identity Providers for registering and logging in Gravitee platform users:&#x20;

* [Gravitee Access Management](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/hbYbONLnkQLHGL1EpwKa/) (AM)
* OpenID Connect
* Google
* Github

To add an identity provider, select **+ Add an identity provider.**  From here, you will have to select your IdP within the **Provider type** section. You will define certain settings and configurations depending on the Identity provider(s) that you select. Please refer to the tabs below to learn more about what you must and/or can define per supported IdP:

{% hint style="info" %}
While many organizations will use multiple IdP providers, we recommend exploring Gravitee Access Management for your broader IdP and IAM needs, as it allows you to consolidate your APIM solution with your IdP and IAM solution.
{% endhint %}

{% tabs %}
{% tab title="Gravitee Access Management" %}
* Define **General** settings
  * Name
  * Description
  * Whether or not to allow portal authentication to use this provider
  * Whether or not to require a public email for authentication
  * Define Group and role mappings: this defines the level to which Platform administrators cam still override mappings. You have two options:
    * Computed only during first user authentication
    * Computed during each user authentication
* Define **Configuration** settings
  * Client Id
  * Client Secret
  * Server URL
  * Security domain
  * Scopes
  * Authentication button color
* **User profile mapping**: this will be used to define a user's Gravitee user profile based on the values provided by the Identity Provider upon registration:
  * ID
  * First name
  * Last name
  * Email
  * Picture
  *
{% endtab %}

{% tab title="OpenID Connect" %}
* Define **General** settings
  * Name
  * Description
  * Whether or not to allow portal authentication to use this provider
  * Whether or not to require a public email for authentication
  * Define Group and role mappings: this defines the level to which Platform administrators cam still override mappings. You have two options:
    * Computed only during first user authentication
    * Computed during each user authentication
* Define **Configuration** settings
  * Client Id
  * Client Secret
  * Token Endpoint
  * Token Introspection Endpoint
  * Authorize Endpoint
  * UserInfo Endpoint
  * UserInfo Logout Endpoint
  * Scopes
  * Authentication button color
* **User profile mapping**: this will be used to define a user's Gravitee user profile based on the values provided by the Identity Provider upon registration:
  * ID
  * First name
  * Last name
  * Email
  * Picture
{% endtab %}

{% tab title="Google" %}
Define **General** settings

* Name
* Description
* Whether or not to allow portal authentication to use this provider
* Whether or not to require a public email for authentication
* Define Group and role mappings: this defines the level to which Platform administrators cam still override mappings. You have two options:
  * Computed only during first user authentication
  * Computed during each user authentication
* **Configuration**
  * Client Id
  * Client Secret
{% endtab %}

{% tab title="GitHub" %}
Define **General** settings

* Name
* Description
* Whether or not to allow portal authentication to use this provider
* Whether or not to require a public email for authentication
* Define Group and role mappings: this defines the level to which Platform administrators cam still override mappings. You have two options:
  * Computed only during first user authentication
  * Computed during each user authentication
* **Configuration**
  * Client Id
  * Client Secret
{% endtab %}
{% endtabs %}

When you are done setting up your Identity provider, select **Create.**&#x20;

Once Identity providers have been added, you are able to easily activate, edit, and delete them within the **Identity Providers** section of the **Authentication** page. You can do so by:

* Activate: toggle the **Activate Identity provider** ON or OFF
* Edit: select the **Edit Identity provider icon**, and then edit the same values defined during the "[Add an Identity provider](how-to.md#adding-editing-and-managing-identity-providers)" flow above
* Delete: select the **Delete Identity provider** icon
