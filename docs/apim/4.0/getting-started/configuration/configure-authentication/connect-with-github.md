# Connect with GitHub

### Overview

This page explains how to configure an APIM Portal connection with a [GitHub](https://github.com/) account.

|   | GitHub authentication requires users to use a public email address to connect to the portal. |
| - | -------------------------------------------------------------------------------------------- |

### Create a GitHub OAuth application

Before you can connect to APIM Portal using a GitHub account, you need to create a GitHub application to link to APIM.

#### Create a new GitHub application

1. Go to [https://github.com/settings/developers](https://github.com/settings/developers).
2. Click **OAuth Apps**.
3.  Click **Register an application**.

    ![Register a new GitHub OAuth apps](https://docs.gravitee.io/images/apim/3.x/installation/authentication/github\_register\_new\_app.png)
4.  Enter the application details.

    ![Fill the form](https://docs.gravitee.io/images/apim/3.x/installation/authentication/github\_fill\_app\_form.png)

    |   | The `Authorization callback URL` must exactly match the domain hosting APIM Portal. |
    | - | ----------------------------------------------------------------------------------- |
5. Click **Register application**.

#### Retrieve the OAuth2 credentials

After you create the GitHub application, you can retrieve the OAuth2 client ID and secret.

![Get Oauth2 credentials](https://docs.gravitee.io/images/apim/3.x/installation/authentication/github\_oauth\_credentials.png)

### Configure APIM

#### Configure with `gravitee.yml` or APIM Console

You can configure this provider both in APIM Console and in the `gravitee.yml` configuration file. Whichever you choose, the configuration is stored in the database. This means that APIM starts using your new configuration as soon as you click the **Save** button (if configuring in APIM Console) or restart APIM API (if configuring in the configuration file).

|   | If you configure the provider in the configuration file and then change the values in APIM Console, all changes are overwritten by the values in the configuration file next time you restart APIM API. |
| - | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

**APIM Console configuration**

1. Click **Organization Settings > Authentication**.
2. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png) and select the **GitHub** icon.
3. If you want to use this provider to log in to APIM Portal, ensure that **Allow portal authentication to use this identity provider** is checked. To use it only for APIM Console, uncheck this option.
4.  Enter the details of the provider, including the OAuth2 credentials created in the GitHub OAuth app.

    ![Gravitee.io - New Github IDP](https://docs.gravitee.io/images/apim/3.x/management-api-configuration-idp/new-github.png)
5. Click **CREATE**.
6. Activate the provider for Portal or Console login, as described in [Activating providers](https://docs.gravitee.io/apim/3.x/apim\_installguide\_authentication.html#activating-providers).

**`gravitee.yml` file configuration**

Update the following section of the file with the GitHub OAuth2 app credentials.

```
security:
  providers:
    - type: github
      clientId: xxxx-xxx-xxx-xxx
      clientSecret: xxxx-xxx-xxx-xxx
```

### Test the connection

#### Log in to APIM Portal

1.  Click **Sign in with GitHub**.

    ![Login Form](https://docs.gravitee.io/images/apim/3.x/installation/authentication/github\_login\_form.png)
2.  Allow access to the user account.

    ![Login Form](https://docs.gravitee.io/images/apim/3.x/installation/authentication/github\_access\_account.png)

    You have successfully logged in:

    ![Here we are !](https://docs.gravitee.io/images/apim/3.x/installation/authentication/github\_login\_success.png)
