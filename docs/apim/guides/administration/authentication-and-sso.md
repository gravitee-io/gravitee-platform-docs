---
description: >-
  This article focuses on how to configure SSO and authentication methods for
  accessing the Gravitee platform using Gravitee Access Management, Google,
  Github, Azure AD, and Keycloack
---

# Authentication and SSO

### Introduction

### Defining Organization authentication and access settings

{% @arcade/embed flowId="iVIQA53PE3vtm6hoNo7b" url="https://app.arcade.software/share/iVIQA53PE3vtm6hoNo7b" %}

Gravitee makes it easy to set up and configure your Organization's authentication and access settings. To do this, log-in to your Gravitee API Management UI and select Organization from the left-hand nav. Then, select **Authentication** underneath **Console.** From here, you will be brought to the **Authentication** page. Here, you can:

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
* Edit: select the **Edit Identity provider icon**, and then edit the same values defined during the "[Add an Identity provider](authentication-and-sso.md#adding-editing-and-managing-identity-providers)" flow above
* Delete: select the **Delete Identity provider** icon
