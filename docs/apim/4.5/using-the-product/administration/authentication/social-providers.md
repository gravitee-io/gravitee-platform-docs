# Configuring authentication with Social Providers

## Overview

The following sections describe how to configure:

* [GitHub authentication](social-providers.md#github-authentication)
* [Google authentication](social-providers.md#google-authentication)

## GitHub authentication

Gravitee supports GitHub authentication. This section describes how to:

* [Create a GitHub OAuth application](social-providers.md#create-a-github-oauth-application)
* [Retrieve your OAuth2 credentials](social-providers.md#retrieve-your-oauth2-credentials)
* [Configure the Gravitee APIM and GitHub connection](social-providers.md#configure-github-authentication-in-gravitee)
* [Test your GitHub authentication flow](social-providers.md#test-your-new-github-authentication-flow)

### Create a GitHub OAuth application

A GitHub OAuth application is a type of OAuth 2.0 application that allows users to authenticate and authorize access to their GitHub account without sharing their login credentials with third-party services. You can also use this application to manage and control access to other tools and services that support GitHub as an IdP and authentication provider, such as Gravitee.

Before you can set up GitHub as an authentication provider for Gravitee APIM, you'll need to create a GitHub OAuth application that you can link to Gravitee APIM. To do so, follow these steps:

1. Log in to your GitHub account, go to **Settings**, then **Developer Settings**
2. Select **OAuth Apps**
3.  Select **Register an application**

    <figure><img src="../../../../../../.gitbook/assets/github_register_new_app (1).png" alt=""><figcaption><p>Register an application in GitHub</p></figcaption></figure>
4.  Enter in your Gravitee details in the **Register a new OAuth application** section. Please note that the Authorization callback URL must match the domain hosting Gravitee APIM. When you're done, select **Register application.**

    <figure><img src="../../../../../../.gitbook/assets/github_fill_app_form (1).png" alt=""><figcaption><p>Register Gravitee details in GitHub</p></figcaption></figure>

### Retrieve your OAuth2 credentials

After you've registered Gravitee, you'll need to retrieve the GitHub OAUth2 credentials that you'll need to give to Gravitee APIM. To do so, follow these steps:

1. In your GitHub settings, select **OAuth Apps**
2. Find your Gravitee OAuth app

From here, you should be able to see your Client ID and Client secret.

<figure><img src="../../../../../../.gitbook/assets/github_oauth_credentials (1).png" alt=""><figcaption><p>GitHub Oauth credentials</p></figcaption></figure>

### Configure GitHub authentication in Gravitee

Once you're done creating your GitHub OAuth application, you can configure your settings in Gravitee. You can do this either via the Gravitee APIM UI or the `gravitee.yaml` file. Either way, the configuration is stored in the database. This means that APIM starts using your new configuration as soon as you select **Save** (if configuring in APIM Console) or restart the APIM API (if configuring in the configuration file). Please see the tabs below to see how to configure GitHub authentication via the APIM UI and the `gravitee.yaml` file.

{% hint style="warning" %}
**Values can be overwritten**

If you configure the provider in the configuration file and then change the values in APIM Console, all changes are overwritten by the values in the configuration file next time you restart APIM API.
{% endhint %}

{% tabs %}
{% tab title="gravitee.yaml file" %}
Configuring GitHub authentication via the `gravitee.yaml` file is easy. Simply update the following section of the `gravitee.yaml` file with your GitHub OAuth2 app credentials that [you retrieved above](social-providers.md#retrieve-your-oauth2-credentials).

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

Gravitee supports Google authentication. This section describes how to:

* [Create a Google OAuth client](social-providers.md#create-a-google-oauth-client)
* [Configure the Gravitee APIM and Google connection](social-providers.md#configure-gravitee-apim-and-google-connection)
* [Test your Google authentication flow](social-providers.md#test-your-new-google-authentication-flow)

### Create a Google OAuth client

In order to connect Google and Gravitee APIM, you'll need to create a Google OAuth client ID. To do so, follow these steps:

1.  First, create a Google project with access to the Google+ API. [Do this here](https://console.developers.google.com/).

    <figure><img src="../../../../../../.gitbook/assets/google_enable_google+_api (1).png" alt=""><figcaption><p>Create a Google project with access to the Google + API</p></figcaption></figure>
2. Now, it's time to create a client. Access [https://console.developers.google.com/](https://console.developers.google.com/), and access your project **Credentials.** Select **Create.**
3.  Select OAuth client ID from the **Create credentials** drop-down.

    <figure><img src="../../../../../../.gitbook/assets/google_create_client (1).png" alt=""><figcaption><p>Create your OAuth client ID</p></figcaption></figure>
4.  Enter in your client details. These will be your Gravitee APIM details. The **Authorized redirect URIs** value _must match_ the domain hosting your Gravitee APIM Portal.

    <figure><img src="../../../../../images/apim/3.x/installation/authentication/google_fill_client_form (1).png" alt=""><figcaption><p>Enter in your Gravitee details when creating a Client ID</p></figcaption></figure>
5. Select **Create**.
6.  Retrieve the new **Client ID** and **Client secret**.

    <figure><img src="../../../../../../.gitbook/assets/google_client_credentials (1).png" alt=""><figcaption><p>Google Client ID and Client secret.</p></figcaption></figure>

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
