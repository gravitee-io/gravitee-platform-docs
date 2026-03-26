---
description: >-
  This article focuses on how to configure SSO and authentication methods for
  accessing the Gravitee platform using Gravitee Access Management, Google,
  Github, Azure AD, and Keycloak
---

# Authentication

## Introduction

Gravitee API Management (APIM) natively support several types of authentication methods to allow users to securely access APIM:

* Authentication providers (such as in-memory, LDAP and databases)
* Social providers (such as GitHub and Google)
* A custom OAuth2/OpenID authorization server

In this article, we will walk through how to configure each by using the `gravitee.yaml` file and the Gravitee API Management Console.

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
      password-encoding-algo: bcrypt
      users:
        - user:
          username: user
          #firstname:
          #lastname:
          # Passwords are encoded using BCrypt
          # Password value: password
          password: $2a$10$9kjw/SH9gucCId3Lnt6EmuFreUAcXSZgpvAYuW2ISv7hSOhHRH1AO
          roles: ORGANIZATION:USER,ENVIRONMENT:USER
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

If you use bcrypt to hash passwords, you can generate new passwords with the [htpasswd](https://httpd.apache.org/docs/current/en/programs/htpasswd.html) command line, as shown in the following example (where `new_password` is your new password):

```
htpasswd -bnBC 10 "" new_password | tr -d ':\n'
```

## LDAP authentication

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

## APIM data source authentication

APIM allows users to connect using an APIM data source. This is required if you want to add and register users via self-registration.

To activate this provider, all you need to do is declare it in the `gravitee.yaml` file. All data source information is then retrieved from the Management Repository configuration.

```
security:
  providers:
    - type: gravitee
```

## Gravitee Access Management Authentication

In addition to API Management, Gravitee offers a fully-fledged Access Management product. While Gravitee works seamlessly with other IAM and IdP providers, many teams prefer to use a single vendor for their APIM and AM needs. This section walks through how to use Gravitee Access Management as a preferred authentication method for your Gravitee platform users.

{% hint style="info" %}
**Necessary prerequisites**

Before you can use Gravitee AM as an authentication provider for Gravitee, you need to create a Gravitee AM security domain and client. To do so, please refer to the [Gravitee Access Management documentation.](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/hbYbONLnkQLHGL1EpwKa/)
{% endhint %}

You can configure Gravitee AM as your Gravitee APIM authentication provider via either the `gravitee.yaml` file or by using the Gravitee APIM UI. Whichever you choose, the configuration is stored in the database. This means that APIM starts using your new configuration as soon as you select the **Save** button (if configuring in the APIM UI) or restart the APIM API (if configuring in the `gravitee.yaml` configuration file). Please see the tabs below to lean more about each approach:

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
{% endtab %}

{% tab title="Use the Gravitee API Management Console" %}
Before configuring authentication via the Gravitee APIM UI, you'll need to access the Gravitee AM client's credentials for authentication configuration. For example:

<figure><img src="../../.gitbook/assets/AM client info.png" alt=""><figcaption><p>Gravitee AM client credentials</p></figcaption></figure>

From here, you'll need to log-in to your Gravitee API Management Console and select Organization from the left-hand nav. Then, select **Authentication** underneath **Console.** From here, you will be brought to the **Authentication** page. Here, you can:

* Enable or disable a log-in form for the API Management Console by toggling **Show login form on Management Console** ON or OFF
* Manage Identity Providers for logging in and registering Gravitee platform users

To add an identity provider, select **+ Add an identity provider.** From here, you will have to select your IdP within the **Provider type** section. Choose **Gravitee AM** as your IdP. From here, you will need to enter in the following information:

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

You can easily test your Gravitee AM configuration by logging out of the Management Console, clearing your cookies, and then logging back in. Once on the log in screen, you should see a **Sign in with Gravitee AM** option.

Select this, and enter in your credentials. You should then be met with an approval page. Here, select **Authorize**. You should then be brought to the Management Console.

## GitHub authentication

Gravitee supports GitHub authentication. In this section, we will cover:

* Creating a GitHub OAuth application
* Configuring the Gravitee APIM and GitHub connection
* Testing your GitHub authentication flow

### Create a GitHub OAuth application

A GitHub OAuth application is a type of OAuth 2.0 application that allows users to authenticate and authorize access to their GitHub account without sharing their login credentials with third-party services. You can also use this application to manage and control access to other tools and services that support GitHub as an IdP and authentication provider, such as Gravitee.

Before you can set up GitHub as an authentication provider for Gravitee APIM, you'll need to create a GitHub OAuth application that you can link to Gravitee APIM. To do so, follow these steps:

1. Log in to your GitHub account, go to **Settings**, then **Developer Settings**
2. Select **OAuth Apps**
3.  Select **Register an application**

    <figure><img src="../../.gitbook/assets/github_register_new_app.png" alt=""><figcaption><p>Register an application in GitHub</p></figcaption></figure>
4.  Enter in your Gravitee details in the **Register a new OAuth application** section. Please note that the Authorization callback URL must match the domain hosting Gravitee APIM. When you're done, select **Register application.**

    <figure><img src="../../.gitbook/assets/github_fill_app_form.png" alt=""><figcaption><p>Register Gravitee details in GitHub</p></figcaption></figure>

#### Retrieve your OAuth2 credentials

After you've registered Gravitee, you'll need to retrieve the GitHub OAUth2 credentials that you'll need to give to Gravitee APIM. To do so, follow these steps:

1. In your GitHub settings, select **OAuth Apps**
2. Find your Gravitee OAuth app

From here, you should be able to see your Client ID and Client secret.

<figure><img src="../../.gitbook/assets/github_oauth_credentials.png" alt=""><figcaption><p>GitHub Oauth credentials</p></figcaption></figure>

### Configure GitHub authentication in Gravitee

Once you're done creating your GitHub OAuth application, you can configure your settings in Gravitee. You can do this either via the Gravitee APIM UI or the `gravitee.yaml` file. Either way, the configuration is stored in the database. This means that APIM starts using your new configuration as soon as you select **Save** (if configuring in APIM Console) or restart the APIM API (if configuring in the configuration file). Please see the tabs below to see how to configure GitHub authentication via the APIM UI and the `gravitee.yaml` file.

{% hint style="warning" %}
**Values can be overwritten**

If you configure the provider in the configuration file and then change the values in APIM Console, all changes are overwritten by the values in the configuration file next time you restart APIM API.
{% endhint %}

{% tabs %}
{% tab title="gravitee.yaml file" %}
Configuring GitHub authentication via the `gravitee.yaml` file is easy. Simply update the following section of the `gravitee.yaml` file with your GitHub OAuth2 app credentials that [you retrieved above](authentication.md#retrieve-your-oauth2-credentials).

```
security:
  providers:
    - type: github
      clientId: xxxx-xxx-xxx-xxx
      clientSecret: xxxx-xxx-xxx-xxx
```

\
After this, you just need to restart the Gravitee APIM API, and you should be good to go.
{% endtab %}

{% tab title="APIM UI" %}
To configure GitHub authentication using the APIM UI, follow these steps:

1. Log-in to the Gravitee APIM UI, and select **Organization** from the left-hand nav.
2. Under **Console,** select **Authentication.**
3. Select **+ Add an identity provider.**
4. On the **Create a new identity provider** page, select Github as your **Provider type.** Then you will need to:
   * Define **General** settings
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

When you are done, select **Create.** Then, go back to the IdP page, and toggle **Activate Identity Provider** ON for your new IdP.
{% endtab %}
{% endtabs %}

### Test your new GitHub authentication flow

You can easily test your GitHub configuration by logging out of the Management Console, clearing your cookies, and then logging back in. Once on the log in screen, you should see a **Sign in with GitHub** option.

Select this, and enter in your credentials. You should then be met with an **Authorize Gravitee** page. Here, select **Authorize**. You should then be brought to the Gravitee API Management Console.

## Google authentication

Gravitee supports GitHub authentication. In this section, we will cover:

* Creating a Google OAuth client
* Configuring the Gravitee APIM and Google connection
* Testing your Google authentication flow

### Create a Google OAuth client

In order to connect Google and Gravitee APIM, you'll need to create a Google OAuth client ID. To do so, follow these steps:

1.  First, create a Google project with access to the Google+ API. [Do this here](https://console.developers.google.com/).

    <figure><img src="../../.gitbook/assets/google_enable_google+_api.png" alt=""><figcaption><p>Create a Google project with access to the Google + API</p></figcaption></figure>
2. Now, it's time to create a client. Access [https://console.developers.google.com/](https://console.developers.google.com/), and access your project **Credentials.** Select **Create.**
3.  Select OAuth client ID from the **Create credentials** drop-down.

    <figure><img src="../../.gitbook/assets/google_create_client.png" alt=""><figcaption><p>Create your OAuth client ID</p></figcaption></figure>
4.  Enter in your client details. These will be your Gravitee APIM details. The **Authorized redirect URIs** value _must match_ the domain hosting your Gravitee APIM Portal.

    <figure><img src="../../.gitbook/assets/google_fill_client_form_gravitee_details.png" alt=""><figcaption><p>Enter in your Gravitee details when creating a Client ID</p></figcaption></figure>
5. Select **Create**.
6.  Retrieve the new **Client ID** and **Client secret**.&#x20;

    <figure><img src="../../.gitbook/assets/google_client_credentials.png" alt=""><figcaption><p>Google Client ID and Client secret.</p></figcaption></figure>

### Configure Gravitee APIM and Google connection

Once you're done creating your Google OAuth client, you can configure your settings in Gravitee. You can do this either via the Gravitee APIM UI or the `gravitee.yaml` file. Either way, the configuration is stored in the database. This means that APIM starts using your new configuration as soon as you select **Save** (if configuring in APIM Console) or restart the APIM API (if configuring in the configuration file). Please see the tabs below to see how to configure Google authentication via the APIM UI and the `gravitee.yaml` file.

{% hint style="warning" %}
**Values can be overwritten**

If you configure the provider in the configuration file and then change the values in APIM Console, all changes are overwritten by the values in the configuration file next time you restart APIM API.
{% endhint %}

{% tabs %}
{% tab title="gravitee.yaml file" %}
Configuring Google authentication via the gravitee.yaml file is easy. simply update the following section of the file with the Google client credentials.

```
security:
  providers:
    - type: google
      clientId: xxxx-xxx-xxx-xxx
      clientSecret: xxxx-xxx-xxx-xxx
```

\
Once you're done, just restart the APIM API.
{% endtab %}

{% tab title="APIM UI" %}
To configure Google authentication using the APIM UI, follow these steps:

1. Log-in to the Gravitee APIM UI, and select **Organization** from the left-hand nav.
2. Under **Console,** select **Authentication.**
3. Select **+ Add an identity provider.**
4. On the **Create a new identity provider** page, select Google as your **Provider type.** Then you will need to:
   * Define **General** settings
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

When you are done, select **Create.** Then, go back to the IdP page, and toggle **Activate Identity Provider** ON for your new IdP.
{% endtab %}
{% endtabs %}

### Test your new Google authentication flow

You can easily test your Google configuration by logging out of the Management Console, clearing your cookies, and then logging back in. Once on the log in screen, you should see a **Sign in with Google** option.

Select this, and choose your Google account that you want to use for authentication. You should then be brought to the Gravitee API Management Console.

## OpenID Connect authentication

OpenID Connect is an authentication protocol built on top of the OAuth 2.0 framework that provides identity verification capabilities for web and mobile applications. It enables users to authenticate with an identity provider and obtain an identity token, which can be used to access protected resources on a web application.

\
Gravitee offers support for OpenID Connect authentication. In this section, we will walk through general OpenID Connect authentication set up. To see a more in-depth example, we've also included a section that covers how to [set up Keycloak as your OpenId Connect authentication method.](authentication.md#example-openid-connect-authentication-keycloak)

Before you can configure your OpenID Connect IdP in Gravitee, you will need to:

* Create your OpenID Connect client
* Retrieve the following information for your client:
  * Client ID
  * Client Secret
  * Token endpoint
  * Token introspection Endpoint (optional)
  * Authorize Endpoint
  * UserInfo Endpoint
  * UserInfo Logout Endpoint (optional)
* (Optional) Decide:
  * Scopes
  * Authentication button color
* Decide proper user profile mappings:
  * ID
  * First name (optional)
  * Last name (optional)
  * Email (optional)
  * Picture (optional)

Once you've done the above, you can use either the `gavitee.yaml` file or the API Management Console to set up your OpenID Connect authentication. Please see the tabs below that walk through general set up directions for OpenID Connect authentication:

{% tabs %}
{% tab title="gravitee.yaml file" %}
To configure an OpenID Connect authentication provider using the `gravitee.yaml` configuration file, you'll need to update to the file with your client information. You'll need to enter in this information where we have **(enter in client information)** called out in the code block. Depending on your client, this information will be different. To see a real-life example, check out the [Configure Keycloak authentication](authentication.md#example-keycloak-authentication) section below.

{% code overflow="wrap" lineNumbers="true" %}
```
security:
  providers:
    - type: (enter in client information)
      id: (enter in client information; not required if not present and the type will be used)
      clientId: (enter in client information)
      clientSecret: (enter in client information)
      tokenIntrospectionEndpoint: (enter in client information)
      tokenEndpoint: (enter in client information)
      authorizeEndpoint: (enter in client information)
      userInfoEndpoint: (enter in client information)
      userLogoutEndpoint: (enter in client information)
      color: "(enter in client information)"
      syncMappings: false
      scopes:
        - (enter in client information)
      userMapping:
        id: (enter in client information)
        email: (enter in client information)
        lastname: (enter in client information)
        firstname: (enter in client information)
        picture: (enter in client information)
      groupMapping:
        - condition: (enter in client information)
          groups:
            - (enter in client information) 1
            - (enter in client information) 2
      roleMapping:
        - condition: (enter in client information)
          roles:
            - (enter in client information)
            - (enter in client information)                  #applied to the DEFAULT environment
            - (enter in client information)          #applied to the DEFAULT environment
            - (enter in client information) #applied to environment whose id is <ENVIRONMENT_ID>
```
{% endcode %}
{% endtab %}

{% tab title="APIM UI" %}
To configure OpenID Connect authentication using the APIM UI, follow these steps:

1. Log-in to the Gravitee APIM UI, and select **Organization** from the left-hand nav.
2. Under **Console,** select **Authentication.**
3. Select **+ Add an identity provider.**
4. On the **Create a new identity provider** page, select OpenID Connect as your **Provider type.** Then you will need to:
   * Define **General** settings
     * Name
     * Description (optional)
     * Whether or not to allow portal authentication to use this provider
     * Whether or not to require a public email for authentication
     * Define Group and role mappings: this defines the level to which Platform administrators cam still override mappings. You have two options:
       * Computed only during first user authentication
       * Computed during each user authentication
   * Define **Configuration** settings
     * Client Id
     * Client Secret
     * Token Endpoint
     * Token Introspection Endpoint (optional)
     * Authorize Endpoint
     * UserInfo Endpoint
     * UserInfo Logout Endpoint (optional)
     * Scopes (optional)
     * Authentication button color (optional)
   * **User profile mapping**: this will be used to define a user's Gravitee user profile based on the values provided by the Identity Provider upon registration:
     * ID
     * First name (optional)
     * Last name (optional)
     * Email (optional)
     * Picture (optional)

When you are done, select **Create.** Then, go back to the IdP page, and toggle **Activate Identity Provider** ON for your new IdP.
{% endtab %}
{% endtabs %}

#### If you're using a custom PKI

When using custom a Public Key Infrastructure (PKI) for your OAuth2 authentication provider, you may have to specify the certificate authority chain of your provider in APIM. To do this, you can either:

*   Export an environment variable for your current session. For example:

    ```
    export JAVA_OPTS="
      -Djavax.net.ssl.trustStore=/opt/graviteeio-management-api/security/truststore.jks
      -Djavax.net.ssl.trustStorePassword=<MYPWD>"
    ```
*   Add an environment variable to your Docker compose file to ensure that this configuration persists across settings. For example:

    {% code overflow="wrap" lineNumbers="true" %}
    ```
    local_managementapi:
        extends:
          file: common.yml
          service: managementapi
        ports:
          - "8005:8083"
        volumes:
          - ./conf/ssl/truststore.jks:/opt/graviteeio-management-api/security/truststore.jks:ro
          - ./logs/management-api:/home/gravitee/logs
        links:
          - "local_mongodb:demo-mongodb"
          - "local_elasticsearch:demo-elasticsearch"
        environment:
          - JAVA_OPTS=-Djavax.net.ssl.trustStore=/opt/graviteeio-management-api/security/truststore.jks -Djavax.net.ssl.trustStorePassword=<MYPWD>
          - gravitee_management_mongodb_uri=mongodb://demo-mongodb:27017/gravitee?serverSelectionTimeoutMS=5000&connectTimeoutMS=5000&socketTimeoutMS=5000
          - gravitee_analytics_elasticsearch_endpoints_0=http://demo-elasticsearch:9200
    ```
    {% endcode %}

## Keycloak authentication

To better illustrate how the OpenID Connect configuration works (and to assist users who are using Keycloak as their authentication provider, this section walks through how to set up Keycloak as an OpenID Connect authentication provider.

### Create a Keycloak client

Before you can connect to the Gravitee portal using Keycloak, you need to create a new client. To do so, follow these steps:

1.  Log-in to Keycloak and create a new client.

    <figure><img src="../../.gitbook/assets/keycloak_create_client.png" alt=""><figcaption><p>Add a Gravitee client in Keycloak</p></figcaption></figure>
2.  Enter in your client details for Gravitee. The `Valid Redirect URIs` value must exactly match the domain which is hosting APIM Portal.

    <figure><img src="../../.gitbook/assets/keycloak_configure_client.png" alt=""><figcaption><p>Enter Gravitee client details in Keycloak</p></figcaption></figure>
3.  Once you're done and create the client, retrieve the client credentials that you will need to give to Gravitee.&#x20;

    <figure><img src="../../.gitbook/assets/keycloak_client_credentials.png" alt=""><figcaption><p>Keycloak client credentials that will need to be given to Gravitee</p></figcaption></figure>

#### Create and configure Keycloak Client scope

1. In your realm, go to the `Client scopes` page.
2.  Set a special gravitee-client-groups [Scope](https://oauth.net/2/scope/) that will contain users' roles.

    ![Keycloak console - Create scope](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_mng-01-client\_scopes-roles\_add\_client\_scope.png)
3.  In the new client scope, set a mapper with Claim name "groups".

    ![Keycloak console - Add mapper to scope](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_mng-02-client\_scopes-mapper.png)
4. In your realm, go to the `Client` page, and select your Client.
5.  Add the new configured scope in the `Client Scopes` tab.

    ![Keycloak console - Add scope to client](https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak\_mng-03-client-add\_scope.png)

#### Create Keycloak Client roles

Optionally, you can configure Keycloak client roles. These roles can be defined later in Gravitee either via the `gravitee.yaml` file or the Gravitee APIM UI. To configure Client roles in Keycloak, follow these steps:

1.  In your client, create roles as needed by organization.

    <figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak_mng-04-client-add_roles.png" alt=""><figcaption><p>Add roles in Keycloak</p></figcaption></figure>
2. To then configure Keycloak users with appropriate roles, select **Role Mappings**, and then define roles as appropriate.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/installation/authentication/keycloak_mng-roles-05-users-add_user_client_roles.png" alt=""><figcaption><p>Define role mappings</p></figcaption></figure>

Gravitee role mapping uses Spring Expression Language ([SpEL](https://docs.spring.io/spring-framework/docs/3.0.x/reference/expressions.html)) for writing conditions. The only available object in context is #profile set from [userInfoEndpoint](https://www.oauth.com/oauth2-servers/signing-in-with-google/verifying-the-user-info/). For example:

```
security:
  providers:
    - type: oidc
      ...
      roleMapping:
        - condition: "{(#jsonPath(#profile, '$.groups') matches 'gravitee-admin' )}"
          roles:
            - "ORGANIZATION:ADMIN"
            - "ENVIRONMENT:ADMIN"

```

### Configure Keycloak authentication in Gravitee

Once you're done creating your Keycloak client, you can configure your settings in Gravitee. You can do this either via the Gravitee APIM UI or the `gravitee.yaml` file. Either way, the configuration is stored in the database. This means that APIM starts using your new configuration as soon as you select **Save** (if configuring in APIM Console) or restart the APIM API (if configuring in the configuration file). Please see the tabs below to see how to configure Keycloak authentication via the APIM UI and the `gravitee.yaml` file.

{% tabs %}
{% tab title="gravitee.yaml" %}
To configure Keycloak as an OpenID Connect authentication provider using the `gravitee.yaml` configuration file, you'll need to update to the file with your Keycloak client information as shown below:

{% code overflow="wrap" lineNumbers="true" %}
```
security:
  providers:
    - type: oidc
      id: keycloak # not required if not present, the type is used
      clientId: gravitee
      clientSecret: 3aea136c-f056-49a8-80f4-a6ea521b0c94
      tokenIntrospectionEndpoint: http://localhost:8080/auth/realms/master/protocol/openid-connect/token/introspect
      tokenEndpoint: http://localhost:8080/auth/realms/master/protocol/openid-connect/token
      authorizeEndpoint: http://localhost:8080/auth/realms/master/protocol/openid-connect/auth
      userInfoEndpoint: http://localhost:8080/auth/realms/master/protocol/openid-connect/userinfo
      userLogoutEndpoint: http://localhost:8080/auth/realms/master/protocol/openid-connect/logout
      color: "#0076b4"
      syncMappings: false
      scopes:
        - openid
        - profile
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
{% endcode %}
{% endtab %}

{% tab title="APIM UI" %}
To configure OpenID Connect authentication using the APIM UI, follow these steps:

1. Log-in to the Gravitee APIM UI, and select **Organization** from the left-hand nav.
2. Under **Console,** select **Authentication.**
3. Select **+ Add an identity provider.**
4. On the **Create a new identity provider** page, select OpenID Connect as your **Provider type.** Then you will need to:
   * Define **General** settings
     * Name
     * Description (optional)
     * Whether or not to allow portal authentication to use this provider
     * Whether or not to require a public email for authentication
     * Define Group and role mappings: this defines the level to which Platform administrators cam still override mappings. You have two options:
       * Computed only during first user authentication
       * Computed during each user authentication
   * Define **Configuration** settings
     * Client Id
     * Client Secret
     * Token Endpoint
     * Token Introspection Endpoint (optional)
     * Authorize Endpoint
     * UserInfo Endpoint
     * UserInfo Logout Endpoint (optional)
     * Scopes (optional)
     * Authentication button color (optional)
   * **User profile mapping**: this will be used to define a user's Gravitee user profile based on the values provided by the Identity Provider upon registration:
     * ID
     * First name (optional)
     * Last name (optional)
     * Email (optional)
     * Picture (optional)

When you are done, select **Create.** Then, go back to the IdP page, and toggle **Activate Identity Provider** ON for your new IdP.
{% endtab %}
{% endtabs %}

### Test your Keycloak authentication

You can easily test your Keycloak configuration by logging out of the Management Console, clearing your cookies, and then logging back in. Once on the login screen, you should see a **Sign in with Keycloak** option.

Then, enter in your Keycloak credentials. After this, you should be successfully logged in.

1. This example uses bcrypt to hash passwords.
2. Define the password.
3. Here, you can define information, passwords, roles, etc. for specific user types, such as user or admin.
4. Define the roles.

[^1]: insert memory here.
