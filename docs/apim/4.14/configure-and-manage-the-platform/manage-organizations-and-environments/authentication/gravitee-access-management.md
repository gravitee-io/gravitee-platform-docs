---
description: Gravitee offers Access Management alongside API Management 4.13 for full identity handling. Learn how the two products relate.
metaLinks:
  alternates:
    - gravitee-access-management.md
---

# Gravitee Access Management

## Overview

In addition to API Management, Gravitee offers a full-fledged Access Management product. While Gravitee works seamlessly with other IAM and IdP providers, many teams prefer to use a single vendor for their APIM and AM needs. This section walks through how to use Gravitee Access Management as a preferred authentication method for your Gravitee platform users.

{% hint style="info" %}
**Necessary prerequisites**

Before you can use Gravitee AM as an authentication provider for Gravitee, you need to create a Gravitee AM security domain as described in the [Gravitee Access Management](https://documentation.gravitee.io/am) documentation. Then create an application in that domain as described in [#create-the-application-in-gravitee-am](gravitee-access-management.md#create-the-application-in-gravitee-am "mention").
{% endhint %}

## Create the application in Gravitee AM

APIM signs users in through an application in your Gravitee AM security domain. To create the application, complete the following steps:

1. Log in to the AM Console.
2. At the top of the page, click the button that shows the name of the current security domain.
3. Select the security domain of your APIM users.
4. Open **Applications**.
5. Click the plus icon ![plus icon](../../../.gitbook/assets/plus-icon.png).
6. Click **Web**.
7. Click **Next**.
8. In **Name**, enter a name for the application.
9. In **Redirect URI**, enter the address of your APIM Console without a trailing slash. For example, `https://apim.example.com/console`. APIM sends this address as the redirect URI when a user signs in to the Console.
10. Optional: In **Client ID** and **Client Secret**, enter your own values. AM generates any value that you leave empty.
11. Click **Create**.
12. In the **Copy your Client Secret** dialog, click the copy icon next to **Client Secret**. Keep the secret for the APIM configuration. AM doesn't show it again.
13. Click **OK**.
14. Click **Identity Providers**.
15. Turn on the **Selected** toggle of each identity provider that your APIM users sign in with.
16. Click **SAVE**.
17. Click **Settings**.
18. Click **OAuth 2.0 / OIDC**.
19. On the **Grant Flows** tab, keep **Authorization Code** selected.
20. In the **Public / Confidential** section, select `client_secret_post` in the **Type** list.
21. Click **Scopes**.
22. Click **ADD SCOPES**.
23. In the **Add scope** dialog, select the `openid`, `profile`, and `email` scopes.
24. Click **Add**.
25. Click **SAVE**.

{% hint style="info" %}
The Developer Portal sends the address of its sign-in page as the redirect URI. To show the provider on the Developer Portal too, add that address in the **Redirect URIs** section of the application's **General** settings.
{% endhint %}

When you configure the provider in APIM, use the following values from the application:

* **Client Id** and **Client Secret**: the client ID that the application's **Overview** page shows, and the secret that you copied.
* **Server URL** and **Security domain**: the **Authorization endpoint** on the application's **Endpoints** page is made of the server URL, the security domain, and `/oauth/authorize`. For example, for `https://am.example.com/my-domain/oauth/authorize`, enter `https://am.example.com` in **Server URL** and `my-domain` in **Security domain**.
* **Client Authentication Method**: **Client secret in the request body (`client_secret_post`)**, which matches the **Type** that you selected in AM. A provider that you declare in the `gravitee.yml` file sends the client secret in the request body when it signs a user in.
* **Scopes**: `openid`, `profile`, and `email`. AM returns the user's profile only when the sign-in requests `openid`. The `profile` and `email` scopes carry the claims that the default **User profile mapping** reads. By default, AM refuses a sign-in that requests a scope the application doesn't list.

## Configuration

You can configure Gravitee AM as your Gravitee APIM authentication provider via either the `gravitee.yaml` file or by using the Gravitee APIM UI. Whichever you choose, the configuration is stored in the database. This means that APIM starts using your new configuration as soon as you select the **Save** button (if configuring in the APIM UI) or restart the APIM API (if configuring in the `gravitee.yaml` configuration file). Please see the tabs below to lean more about each approach:

{% tabs %}
{% tab title="Use the gravitee.yaml file" %}
Before configuring the `gravitee.yaml` file, you'll need to access the Gravitee AM client's credentials for authentication configuration. For example:

<figure><img src="../../../.gitbook/assets/AM client info.png" alt="The Client ID and Client Secret fields of an application&#x27;s client information, each with a copy button alongside."><figcaption><p>Gravitee AM client credentials</p></figcaption></figure>

From here, you can configure the `gravitee.yaml` file using those credentials:

```yaml
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

<figure><img src="../../../.gitbook/assets/AM client info.png" alt="The Client ID and Client Secret fields of an application&#x27;s client information, each with a copy button alongside."><figcaption><p>Gravitee AM client credentials</p></figcaption></figure>

Next, log in to your Gravitee API Management Console and select Organization from the left hand nav. Then, select **Authentication** underneath **Console.** You will be brought to the **Authentication** page where you can:

* Enable or disable a log-in form for the API Management Console by toggling **Show login form on Management Console** ON or OFF
* Manage Identity Providers for logging in and registering Gravitee platform users

To add an identity provider, select **+ Add an identity provider.** From here, you will have to select your IdP within the **Provider type** section. Choose **Gravitee AM** as your IdP. From here, you will need to enter in the following information:

* Define **General** settings
  * Name
  * Description
  * **Allow portal authentication to use this identity provider**. Optional, and off by default in the Console-only setup. This setting doesn't control the Console login page. See [How identity providers are scoped](README.md#how-identity-providers-are-scoped).
  * Whether or not to require a public email for authentication
  * Define Group and role mappings: this defines the level to which Platform administrators cam still override mappings. You have two options:
    * Computed only during first user authentication
    * Computed during each user authentication
* Define **Configuration** settings
  * Client Id
  * Client Secret
  * Server URL
  * Security domain
  * Client Authentication Method (optional). Decides how APIM sends its client credentials to the token and introspection endpoints. See [Choose how APIM authenticates to the identity provider](README.md#choose-how-apim-authenticates-to-the-identity-provider).
  * Scopes
  * Authentication button color
* **User profile mapping**: this will be used to define a user's Gravitee user profile based on the values provided by the Identity Provider upon registration:
  * ID
  * First name
  * Last name
  * Email
  * Picture
* **Persisted Claims** (optional): the claims to store on each user at login, for injection into dynamic client registration requests. See [Inject identity provider claims into DCR requests](../inject-identity-provider-claims-into-dcr-requests.md).

When you are done, select **Create.** Then go back to the identity provider list and click the activation toggle on the provider's row, so the **Status** column reads **Activated**. That organization activation is what puts the provider on the Console login page. To show it on the Developer Portal as well, turn **Allow portal authentication to use this identity provider** on, then activate the provider on the **Authentication** page of that environment's settings.
{% endtab %}
{% endtabs %}

## Test your Gravitee AM configuration

{% hint style="info" %}
**Set up your AM user**

Before being able to log-in via AM, you will need to create users in AM. To do this please refer to the "Set up your first application" documentation within the Gravitee AM documentation.
{% endhint %}

You can easily test your Gravitee AM configuration by logging out of the Management Console, clearing your cookies, and then logging back in. Once on the log in screen, you should see a **Sign in with Gravitee AM** option.

Select this, and enter in your credentials. You should then be met with an approval page. Here, select **Authorize**. You should then be brought to the Management Console.
