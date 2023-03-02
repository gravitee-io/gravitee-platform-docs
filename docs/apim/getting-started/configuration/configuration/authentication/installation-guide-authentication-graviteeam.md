# Overview

This page explains how to configure APIM authentication using the
[Gravitee.io Access
Management^](https://www.gravitee.io/products/access-management)
product.

The examples below are based on Access Management 2.x (2.0.4 or above).

# Create a new client in Access Management

Before you can connect to APIM using Access Management (AM), you need to
create a new client.

See link:{{ */am/current/am\_quickstart\_app\_setup.html* |
relative\_url }}\[Set up your first application^\] in the AM
documentation for guidance on setting up your first security domain and
client application.

The `Valid Redirect URIs` value must exactly match the domain hosting
APIM Portal.

## Retrieve client credentials

After you create the client, you can retrieve its credentials for
authentication configuration.

image::{% link
images/apim/3.x/installation/authentication/graviteeam\_client\_credentials.png
%}\[Get client credentials\]

# Configure APIM

You can configure this provider both in APIM Console and in the
`gravitee.yml` configuration file. Whichever you choose, the
configuration is stored in the database. This means that APIM starts
using your new configuration as soon as you click the **Save** button
(if configuring in APIM Console) or restart APIM API (if configuring in
the configuration file).

If you configure the provider in the configuration file and then change
the values in APIM Console, all changes are overwritten by the values in
the configuration file next time you restart APIM API.

# APIM Console configuration

1.  Click **Organization Settings &gt; Authentication**.

2.  Click the plus icon image:{% link images/icons/plus-icon.png
    %}\[role="icon"\] and select the **Gravitee.io AM** icon.

3.  If you want to use this provider to log in to APIM Portal, ensure
    that **Allow portal authentication to use this identity provider**
    is checked. To use it only for APIM Console, uncheck this option.

4.  Enter the details of the provider, including the credentials created
    in the AM client.

    image::{% link
    images/apim/3.x/management-api-configuration-idp/new-am.png
    %}\[Gravitee.io - New Gravitee.io AM IDP\] . Click **CREATE**. .
    Activate the provider for Portal or Console login, as described in
    link:{{
    */apim/3.x/apim\_installguide\_authentication.html#activating-providers*
    | relative\_url }}\[Activating providers^\].

# `gravitee.yml` file configuration

Update the following section of the file with the AM client credentials.

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

# Test the configuration

## Create a user in AM

See link:{{ */am/current/am\_quickstart\_app\_setup.html* |
relative\_url }}\[Set up your first application^\] for guidance on
setting up your new AM user.

APIM requires an `email` profile to enable portal authentication. If you
create an Inline identity provider in AM, you need to specify an email
address in the **Username** field.

image::{% link
images/apim/3.x/installation/authentication/graviteeam\_create\_user.png
%}\[\]

## Log in to APIM Portal

1.  Click **Sign in with Gravitee.io AM**.

    image::{% link
    images/apim/3.x/installation/authentication/graviteeam\_login\_form.png
    %}\[\]

2.  Enter your user credentials and click **LOG IN**.

    image::{% link
    images/apim/3.x/installation/authentication/graviteeam\_login\_form2.png
    %}\[\]

3.  Click **AUTHORIZE** on the approval page.

    image::{% link
    images/apim/3.x/installation/authentication/graviteeam\_login\_form3.png
    %}\[\]

    You have successfully logged in:

    image::{% link
    images/apim/3.x/installation/authentication/graviteeam\_login\_success.png
    %}\[\]
