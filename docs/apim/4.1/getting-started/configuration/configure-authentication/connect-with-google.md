# Connect with Google

### Overview

This page explains how to configure an APIM connection with a Google account.

### Create a Google OAuth client

Before you can connect to APIM with a Google account, you need to create an OAuth client ID.

#### Check access to the Google+ API

Before you begin, you need to create a Google project with access to the Google+ API at [https://console.developers.google.com/](https://console.developers.google.com/).

![Check Google+ API access](https://docs.gravitee.io/images/apim/3.x/installation/authentication/google\_enable\_google+\_api.png)

#### Create a new client

1. Go to [https://console.developers.google.com/](https://console.developers.google.com/).
2.  In your project **Credentials**, click **Create credentials** and select **OAuth client ID**.

    ![Create a new OAuth client](https://docs.gravitee.io/images/apim/3.x/installation/authentication/google\_create\_client.png)
3.  Enter the client details.

    ![Fill the form](https://docs.gravitee.io/images/apim/3.x/installation/authentication/google\_fill\_client\_form.png)

    |   | The `Authorized redirect URIs` value must exactly match the domain hosting APIM Portal. |
    | - | --------------------------------------------------------------------------------------- |

#### Retrieve client credentials

After you create the client, you can retrieve its credentials for authentication configuration.

![Get Client credentials](https://docs.gravitee.io/images/apim/3.x/installation/authentication/google\_client\_credentials.png)

### Configure APIM

#### Configure with `gravitee.yml` or APIM Console

You can configure this provider both in APIM Console and in the `gravitee.yml` configuration file. Whichever you choose, the configuration is stored in the database. This means that APIM starts using your new configuration as soon as you click the **Save** button (if configuring in APIM Console) or restart APIM API (if configuring in the configuration file).

|   | If you configure the provider in the configuration file and then change the values in APIM Console, all changes are overwritten by the values in the configuration file next time you restart APIM API. |
| - | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

**APIM Console configuration**

1. Click **Organization Settings > Authentication**.
2. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png) and select the **Google** icon.
3. If you want to use this provider to log in to APIM Portal, ensure that **Allow portal authentication to use this identity provider** is checked. To use it only for APIM Console, uncheck this option.
4.  Enter the details of the provider, including the credentials created in the AM client.

    ![Gravitee.io - New Google IDP](https://docs.gravitee.io/images/apim/3.x/management-api-configuration-idp/new-google.png)
5. Click **CREATE**.
6. Activate the provider for Portal or Console login, as described in [Activating providers](https://docs.gravitee.io/apim/3.x/apim\_installguide\_authentication.html#activating-providers).

**`gravitee.yml` file configuration**

Update the following section of the file with the Google client credentials.

```
security:
  providers:
    - type: google
      clientId: xxxx-xxx-xxx-xxx
      clientSecret: xxxx-xxx-xxx-xxx
```

### Test the connection

#### Log in to APIM Portal

1.  Click **Sign in with Google**.

    ![Login Form](https://docs.gravitee.io/images/apim/3.x/installation/authentication/google\_login\_form.png)
2.  Choose the Google account.

    ![Login Form](https://docs.gravitee.io/images/apim/3.x/installation/authentication/google\_choose\_google\_account.png)

    You have successfully logged in:

    ![google login success](https://docs.gravitee.io/images/apim/3.x/installation/authentication/google\_login\_success.png)
