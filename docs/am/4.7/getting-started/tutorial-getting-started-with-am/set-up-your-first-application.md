---
description: Installation guide for Set Up Your First Application.
---

# Set Up Your First Application

## Overview

This section walks you through creating your first application. For more detailed instructions, see the [Guides section.](../../guides/prologue.md)

In this example, we will:

* Create a security domain for the application
* Create a new web application
* Create a new identity provider and associate it with the application
* Test the application

## Create a security domain

A _security domain_ is a series of security policies that apply to a set of applications that all share common security mechanisms for authentication, authorization, and identity management.

{% hint style="info" %}
You only need to create a new security domain for an application when you do not have a suitable domain configured already. You can find a list of security domains in your user menu.
{% endhint %}

### Create a domain with AM Console

1. Login to AM Console.
2.  From the user menu at the top right, click **Create domain**.

    <figure><img src="https://docs.gravitee.io/images/am/current/quickstart-create-domain.png" alt=""><figcaption><p>Create a security domain</p></figcaption></figure>
3.  Give your security domain a **Name** and a **Description** and click **CREATE**.

    <figure><img src="https://docs.gravitee.io/images/am/current/quickstart-create-domain2.png" alt=""><figcaption><p>Define your security domain</p></figcaption></figure>
4.  Select the **click here** link on the banner to enable the domain.

    <figure><img src="https://docs.gravitee.io/images/am/current/quickstart-enable-domain.png" alt=""><figcaption><p>Banner to enable domain</p></figcaption></figure>

### Create a domain with AM API

{% code overflow="wrap" %}
```sh
# create domain
$ curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d '{"name":"My First Security Domain","description":"My First Security Domain description"}' \
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains

# enable domain
$ curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X PATCH \
     -d '{"enabled": true}' \
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains/:domainId
```
{% endcode %}

## Create an application

Before you can work with AM Gateway, you must create an _application_. The application will provide the necessary information (such as the client ID and client Secret) for authentication and authorization. The application can be a native mobile app, a single page front-end web application or a regular web application that executes on a server.

In this example, we will create a regular web application.

1. Click **Applications**.
2. In the Applications page, click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
3.  Choose a **Web** application type.

    <figure><img src="https://docs.gravitee.io/images/am/current/quickstart-create-application.png" alt=""><figcaption><p>Select application type</p></figcaption></figure>
4. Click the **Next** button.
5.  Give your application a **Name** and a **Redirect URI** (with HTTPS scheme and non-localhost) and click the **Create** button.

    <figure><img src="https://docs.gravitee.io/images/am/current/quickstart-create-application2.png" alt=""><figcaption><p>Application settings</p></figcaption></figure>

{% hint style="info" %}
This application will be used by end users, so we need to bind them with an identity provider.
{% endhint %}

## Create an identity provider

An _identity provider_ (IdP) is usually a service used to authenticate and communicate authorization and user information. It can be a social provider like Facebook, Google, or Twitter, an enterprise provider such as Active Directory, or a custom provider such as a database.

In this example, we will create an In-memory identity provider with an inline user configuration.

1. Click **Settings > Providers**.
2. In the Identity Providers page, click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
3.  Choose **Inline** and click **Next**.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-idp-type.png" alt=""><figcaption><p>IdP selection</p></figcaption></figure>
4.  Give your identity provider a **Name** and enter the user details, then click **Create**.

    {% code overflow="wrap" %}
    ```sh
    curl -H "Authorization: Bearer :accessToken" \
        -H "Content-Type:application/json;charset=UTF-8" \
        -X POST \
        -d '{
            "external": false,
            "type": "inline-am-idp",
            "configuration": "{\"users\":[{\"firstname\":\"John\",\"lastname\":\"Doe\",\"username\":\"johndoe\",\"password\":\"johndoepassword\"}]}",
            "name": "Inline IdP"
            }' \
        http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains/:securityDomainPath/identities
    ```
    {% endcode %}

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-create-idp.png" alt=""><figcaption><p>Configure your IdP</p></figcaption></figure>
5. Click **Applications** and select your web application. 
6.  In the **Identity Providers** tab, select **Inline identity provider** and click **SAVE**.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-client-idp.png" alt=""><figcaption><p>Select IdP for application</p></figcaption></figure>

## Test your identity provider with OAuth2

You can now test your identity provider by requesting a token, as described in[ ID Token in the next section.](get-user-profile-information.md#id-token)

## Initiate the login flow

In the case of a **Web Application**, **Single Page Application** or **Native Application**, you can decide also to redirect your end users to an AM login page:

1. Click **Applications** and select your web application.
2. In the **Overview** tab, get to the **Initiate the Login flow** section and copy the given URL

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-client-initiate-the-login-flow.png" alt=""><figcaption><p>Copy redirect URL</p></figcaption></figure>

You will be redirected to the Login page where you can enter the credentials configured in the Identity Provider.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-client-login-page.png" alt=""><figcaption><p>Login page for IdP</p></figcaption></figure>

Once logged in you will be redirected to the configured `redirect_uri` with the correct parameters regarding your OAuth2 configuration.

To fine-grain tune your application, you can check in detail the [User Guide.](../../guides/prologue.md)
