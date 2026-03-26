---
description: An overview about Configuring Gravitee Access Management Authentication.
---

# Configuring Gravitee Access Management Authentication

## Overview

In addition to API Management, Gravitee offers a full-fledged Access Management product. While Gravitee works seamlessly with other IAM and IdP providers, many teams prefer to use a single vendor for their APIM and AM needs. This section walks through how to use Gravitee Access Management as a preferred authentication method for your Gravitee platform users.

{% hint style="info" %}
**Necessary prerequisites**

Before you can use Gravitee AM as an authentication provider for Gravitee, you need to create a Gravitee AM security domain and client as described in the [Gravitee Access Management documentation.](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/hbYbONLnkQLHGL1EpwKa/)
{% endhint %}

## Configuration

You can configure Gravitee AM as your Gravitee APIM authentication provider via either the `gravitee.yaml` file or by using the Gravitee APIM UI. Whichever you choose, the configuration is stored in the database. This means that APIM starts using your new configuration as soon as you select the **Save** button (if configuring in the APIM UI) or restart the APIM API (if configuring in the `gravitee.yaml` configuration file). Please see the tabs below to lean more about each approach:

{% tabs %}
{% tab title="Use the gravitee.yaml file" %}
Before configuring the `gravitee.yaml` file, you'll need to access the Gravitee AM client's credentials for authentication configuration. For example:

<figure><img src="../../.gitbook/assets/AM client info.png" alt=""><figcaption><p>Gravitee AM client credentials</p></figcaption></figure>

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

<figure><img src="../../.gitbook/assets/AM client info.png" alt=""><figcaption><p>Gravitee AM client credentials</p></figcaption></figure>

Next, log in to your Gravitee API Management Console and select Organization from the left hand nav. Then, select **Authentication** underneath **Console.** You will be brought to the **Authentication** page where you can:

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

## Test your Gravitee AM configuration

{% hint style="info" %}
**Set up your AM user**

Before being able to log-in via AM, you will need to create users in AM. To do this please refer to the "Set up your first application" documentation within the Gravitee AM documentation.
{% endhint %}

You can easily test your Gravitee AM configuration by logging out of the Management Console, clearing your cookies, and then logging back in. Once on the log in screen, you should see a **Sign in with Gravitee AM** option.

Select this, and enter in your credentials. You should then be met with an approval page. Here, select **Authorize**. You should then be brought to the Management Console.
