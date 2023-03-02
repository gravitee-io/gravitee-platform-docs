# How to configure a production-ready APIM environment

## Overview

During APIM installation, some default settings are created. While these default settings can be useful for testing your new installation, some of them may not be suitable for a production environment, where security is more of a consideration.

This document gives some tips on important settings to check in APIM when preparing to move to a production environment. APIM includes many other configuration options and every environment is unique. It is recommended that you also read the [APIM Configuration Guide](../getting-started/configuration/configuration/configuration-guide.md) to determine if you have completed all the configuration you need before you can deploy APIM in production.

### Configuring APIM

You can configure APIM settings in various ways — by using the `gravitee.yml` file, the APIM Console settings, and environment and system variables.

When you configure new settings, it is important to understand that one configuration type can override another. The [Configure APIM API](../getting-started/configuration/configuration/rest-apis/installation-guide-rest-apis-configuration.md) page gives a good overview of this topic.

## Step 1: Disable the internal APIs

APIM API and APIM Gateway include internal APIs which are enabled by default. If you do not intend to use them, we recommend you disable them.

Perform the following steps on both the APIM API component and the APIM Gateway component:

1. Open your `gravitee.yml` file.
2.  In the `services:` section, set the `http:` `enabled` value to `false`:

    ```
        services:
          core:
            http:
              enabled: false
              port: 18083
              host: localhost
              authentication:
                # authentication type to be used for the core services
                # - none : to disable authentication
                # - basic : to use basic authentication
                # default is "basic"
                type: basic
                users:
                  admin: adminadmin
    ```

To learn more about the internal APIs, see:

* [Configure the APIM API internal API](../getting-started/configuration/configuration/rest-apis/installation-guide-rest-apis-technical-api.md)
* [Configure the APIM Gateway internal API](../getting-started/configuration/configuration/gateway/installation-guide-gateway-technical-api.md)

## Step 2: Update the default users

Some default users are created for you during installation. It is recommended that you remove any users you do not need.

!!! warning

```
It is also strongly recommended that, regardless of the user management system you put in place, you keep the default **admin** user, so that you can recover APIM in case of issues. Remember to change the default administrator password.
```

Perform the following steps on the APIM API component:

1. Open your `gravitee.yml` file.
2.  In the `security \ providers` section, remove any users you do not need:

    ```
        security:
          # When using an authentication providers, use trustAll mode for TLS connections
          # trustAll: false
          providers:  # authentication providers
            - type: memory
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
    ```
3. Update the default administrator password: ![](../../../images/apim/3.x/how-tos/configure-apim/admin-pwd.png)

To learn more about configuring users, see [Configure authentication](../getting-started/configuration/configuration/authentication/installation-guide-authentication.md).

## Step 3: Update the JWT secret

The JWT secret is used for signing session cookies in the APIM UI components. Any users with this secret can log in to APIM and update their permissions.

Perform the following steps on the APIM API component:

1. Open your `gravitee.yml` file.
2.  In the `jwt` section, update the `secret` value:

    ```
        jwt:
          secret: myJWT4Gr4v1t33_S3cr3t
          # Allows to define the end of validity of the token in seconds (default 604800 = a week)
          #expire-after: 604800
          # Allows to define the end of validity of the token in seconds for email registration (default 86400 = a day)
          #email-registration-expire-after: 86400
          # Allows to define issuer (default gravitee-management-auth)
          #issuer: gravitee-management-auth
          # Allows to define cookie context path (default /)
          #cookie-path: /
          # Allows to define cookie domain (default "")
          #cookie-domain: .gravitee.io
          # Allows to define if cookie secure only (default false)
          #cookie-secure: true
    ```
3. You can also update other values, such as:

* The `expire-after` value, to change the validity period from the default value of one week.
* The `cookie-path` and `cookie-domain` values, to adapt them to your own environment; the values you define must be specific to the domain and path where the API is running and not apply to any another environment (for example, `.gravitee.io` could apply to any domain called `xxx.gravitee.io`, such as `dev.gravitee.io` or `qa.gravitee.io`)

## Step 4: Update the default APIM settings

The most common settings are described below. Not all of these settings need to be changed in every environment.

Perform the following steps in APIM Console:

1. [Log in to APIM Console](../quickstart/quickstart-console-login.md).
2. Click **Settings**.
3. In the **PORTAL** section:
   1. Click **Settings**.
   2. Update the **Company name**.
   3. In the **Management** section of the page:
   4. Update the **Title** of APIM Console to make it more appropriate for your own environment.
   5. Update the **Management URL** to your APIM Console URL. ![](../../../images/apim/3.x/how-tos/configure-apim/portal-management-settings.png)
4. In the **GATEWAY** section:
   1. Click **Sharding Tags**.
   2. In the **Default configuration** section of the page, update th **Entrypoint** field with your APIM API endpoint. You can also update this value [using an environment variable](../getting-started/configuration/configuration/rest-apis/installation-guide-rest-apis-configuration.md#environment-variables). ![](../../../images/apim/3.x/how-tos/configure-apim/gateway-shardingtags-settings.png)
5. Click **API Logging**.
6. Update the maximum logging duration for APIM API logging to avoid flooding. In this example, we have configured a logging duration of 15 minutes: ![](../../../images/apim/3.x/how-tos/configure-apim/gateway-api-logging-settings.png)

!!! note\
The recommended value depends on the type of logging you have enabled: the more information you log, the lower the value needs to be (although the value must be above zero to be taken into account).
