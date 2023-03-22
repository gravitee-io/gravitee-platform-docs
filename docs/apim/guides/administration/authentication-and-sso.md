---
description: >-
  This article focuses on how to configure SSO and authentication methods for
  accessing the Gravitee platform using Gravitee Access Management, Google,
  Github, Azure AD, and Keycloack
---

# Authentication and SSO

## Introduction

Gravitee API Management (APIM) natively support several types of authentication methods to allow users to securely access APIM:

* Authentication providers (such as in-memory, LDAP and databases)
* Social providers (such as GitHub and Google)
* A custom OAuth2 / OpenID authorization server

In this article, we will walk through how to configure each by using the `gravitee.yaml` file and the Gravitee API Management UI.

{% @arcade/embed flowId="iVIQA53PE3vtm6hoNo7b" url="https://app.arcade.software/share/iVIQA53PE3vtm6hoNo7b" %}

## Configure in-memory users

This example shows a basic in-memory implementation, providing a simple and convenient way to declare advanced users of APIM, such as administrator users. To do this, you could configure the `gravitee.yaml` file as such:

<pre><code># Authentication and identity sources
# Users can have following roles (authorities):
#  USER: Can access portal and be a member of an API
#  API_PUBLISHER: Can create and manage APIs
#  API_CONSUMER: Can create and manage Applications
#  ADMIN: Can manage global system
security:
  # When using an authentication providers, use trustAll mode for TLS connections
  # trustAll: false
  providers:  # authentication providers
    - type: <a data-footnote-ref href="#user-content-fn-1">memory</a>
      # allow search results to display the user email. Be careful, It may be contrary to the user privacy.
#      allow-email-in-search-results: true
      # password encoding/hashing algorithm. One of:
      # - bcrypt : passwords are hashed with bcrypt (supports only $2a$ algorithm)
      # - none : passwords are not hashed/encrypted
      # default value is bcrypt
      password-encoding-algo: <a data-footnote-ref href="#user-content-fn-2">bcrypt</a>
      users:
        - user:
          username: <a data-footnote-ref href="#user-content-fn-3">user</a>
          #firstname:
          #lastname:
          # Passwords are encoded using BCrypt
          # Password value: password
          password: <a data-footnote-ref href="#user-content-fn-4">$2a$10$9kjw/SH9gucCId3Lnt6EmuFreUAcXSZgpvAYuW2ISv7hSOhHRH1AO</a>
          roles: <a data-footnote-ref href="#user-content-fn-5">ORGANIZATION:USER,ENVIRONMENT:USER</a>
          # Useful to receive notifications
          #email:
        - user:
          username: admin
          #firstname:
          #lastname:
          # Password value: admin
          password: $2a$10$Ihk05VSds5rUSgMdsMVi9OKMIx2yUvMz7y9VP3rJmQeizZLrhLMyq
          roles: ORGANIZATION:ADMIN,ENVIRONMENT:ADMIN
          #email:
        - user:
          username: api1
          #firstname:
          #lastname:
          # Password value: api1
          password: $2a$10$iXdXO4wAYdhx2LOwijsp7.PsoAZQ05zEdHxbriIYCbtyo.y32LTji
          # You can declare multiple roles using comma separator
          roles: ORGANIZATION:USER,ENVIRONMENT:API_PUBLISHER
          #email:
        - user:
          username: application1
          #firstname:
          #lastname:
          # Password value: application1
          password: $2a$10$2gtKPYRB9zaVaPcn5RBx/.3T.7SeZoDGs9GKqbo9G64fKyXFR1He.
          roles: ORGANIZATION:USER,ENVIRONMENT:USER
          #email:

</code></pre>

### Generate a new password

If you use [bcrypt](https://en.wikipedia.org/wiki/Bcrypt) to hash passwords, you can generate new passwords with the [htpasswd](https://httpd.apache.org/docs/current/en/programs/htpasswd.html) command line, as shown in the following example (where `new_password` is your new password):

```
htpasswd -bnBC 10 "" new_password | tr -d ':\n'
```

## Authenticate users via LDAP

There are many ways to configure users via LDAP. To illustrate the basic concepts, here is an example configuration using the `gravitee.yaml` file:

```
# ===================================================================
# LDAP SECURITY PROPERTIES
#
# This sample file declared one ldap authentication source
# ===================================================================
security:
  type: basic
  providers:
    - type: ldap
      context:
        username: "uid=admin,ou=system"
        password: "secret"
        url: "ldap://localhost:389/dc=gravitee,dc=io"
        base: "c=io,o=gravitee"
      authentication:
        user:
          base: "ou=people"
          filter: "uid={0}"
        group:
          base: "o=authorization groups"
          filter: "member={0}"
          role:
            attribute: "cn"
            mapper: {
              GRAVITEE-CONSUMERS: API_CONSUMER,
              GRAVITEE-PUBLISHERS: API_PUBLISHER,
              GRAVITEE-ADMINS: ADMIN,
              GRAVITEE-USERS: USER
            }
      lookup:
        user:
          base: "ou=people"
          filter: "(&(objectClass=myObjectClass)(|(cn=*{0}*)(uid={0})))"
```

## Authenticate users via an APIM data source

APIM allows users to connect using an APIM data source. This is required if you want to add and register users via self-registration.

To activate this provider, all you need to do is declare it in the `gravitee.yaml` file. All data source information is then retrieved from the Management Repository configuration.

```
security:
  providers:
    - type: gravitee
```

## Authenticate users via Gravitee Access Management

In addition to API Management, Gravitee offers a fully-fledged Access Management product. While Gravitee works seamlessly with other IAM and IdP providers, many teams prefer to use a single vednor for their APIM and AM needs. This section walk through how to use Gravitee Access Management as a preferred authentication method for your Gravitee platform users.

{% hint style="info" %}
**Necessary prerequisites**

&#x20;**** Before you can use Gravitee AM as an authentication provider for Gravitee, you need to create a Gravitee AM security domain and client. To do so, please refer to the [Gravitee Access Management documentation.](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/hbYbONLnkQLHGL1EpwKa/)
{% endhint %}

You can configure Gravitee AM as your Gravitee APIM authentication provider via either the `gravitee.yaml` file or by using the Gravitee APIM UI. Whichever you choose, the configuration is stored in the database. This means that APIM starts using your new configuration as soon as you select the **Save** button (if configuring in the APIM UI) or restart the APIM API (if configuring in the `gravitee.yaml` configuration file). Please see the tabs below to lean more about each approach:&#x20;

{% tabs %}
{% tab title="Use the gravitee.yaml file" %}
Before configuring the `gravitee.yaml` file, you'll need to access the Gravitee AM client's credentials for authentication configuration. For example:

<figure><img src="../../.gitbook/assets/AM client info.png" alt=""><figcaption><p>Gravitee AM client credentials</p></figcaption></figure>

From here, you can configure the gravitee.yaml file using those credentials:

```
security:
  providers:
    - type: graviteeio_am
      clientId: xxxx-xxx-xxx-xxx
      clientSecret: xxxx-xxx-xxx-xxx
      serverURL: https://gravitee.io/am
      domain: gravitee
      color: "#3C3C3C"
      syncMappings: false
      scopes:
        - openid
        - email
      userMapping:
        id: sub
        email: email
        lastname: family_name
        firstname: given_name
        picture: picture
      groupMapping:
        - condition: "{#jsonPath(#profile, '$.identity_provider_id') == 'PARTNERS' && #jsonPath(#profile, '$.job_id') != 'API_MANAGER'}"
          groups:
            - Group 1
            - Group 2
      roleMapping:
        - condition: "{#jsonPath(#profile, '$.job_id') != 'API_MANAGER'}"
          roles:
            - "ORGANIZATION:USER"
            - "ENVIRONMENT:API_CONSUMER"                  #applied to the DEFAULT environment
            - "ENVIRONMENT:DEFAULT:API_CONSUMER"          #applied to the DEFAULT environment
            - "ENVIRONMENT:<ENVIRONMENT_ID>:API_CONSUMER" #applied to environment whose id is <ENVIRONMENT_ID>
```

\

{% endtab %}

{% tab title="Use the Gravitee API Management UI" %}
Before configuring authentication via the Gravitee APIM UI, you'll need to access the Gravitee AM client's credentials for authentication configuration. For example:

<figure><img src="../../.gitbook/assets/AM client info.png" alt=""><figcaption><p>Gravitee AM client credentials</p></figcaption></figure>

From here, you'll need to log-in to your Gravitee API Management UI and select Organization from the left-hand nav. Then, select **Authentication** underneath **Console.** From here, you will be brought to the **Authentication** page. Here, you can:

* Enable or disable a log-in form for the API Management UI by toggling **Show login form on management console** ON or OFF
* Manage Identity Providers for logging in and registering Gravitee platform users

To add an identity provider, select **+ Add an identity provider.**  From here, you will have to select your IdP within the **Provider type** section. Choose **Gravitee AM** as your IdP. From here, you will need to enter in the following information:

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

When you are done, select **Create.** Then, go back to the IdP page, and toggle **Activate Identity Provider** ON for your new IdP.
{% endtab %}
{% endtabs %}

### Test your Gravitee AM configuration

{% hint style="info" %}
**Set up your AM user**

Before being able to log-in via AM, you will need to create users in AM. To do this please refer to the "Set up your first application" documentation within the Gravitee AM documentation.
{% endhint %}

You can easily test your Gravitee AM configuration by logging out of the Management UI, clearing your cookies, and then logging back in. Once on the log in screen, you should see a **Sign in with Gravitee.io AM** option.

Select this, and enter in your credentials. You should then be met with an approval page. Here, select **Authorize**. You should then be brought to the Management UI.&#x20;

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

[^1]: insert memory here.

[^2]: This example uses bcrypt to hash passwords.

[^3]: Here, you can define information, passwords, roles, etc. for specific user types, such as user or admin.

[^4]: Define the password.

[^5]: Define the roles.
