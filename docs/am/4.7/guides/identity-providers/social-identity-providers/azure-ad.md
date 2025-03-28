# Azure AD

## Overview

You can authenticate users with Azure Active Directory. Before you begin, you need to sign up for an [Azure account](https://azure.microsoft.com/en-us/free/?ref=microsoft.com\&utm_source=microsoft.com\&utm_medium=docs\&utm_campaign=visualstudio) and [Set up a tenant](https://azure.microsoft.com/en-us/free/?ref=microsoft.com\&utm_source=microsoft.com\&utm_medium=docs\&utm_campaign=visualstudio).

## Steps

To connect your application to Azure AD, you will:

* Register a new application in Azure AD
* Create an Azure AD identity provider in Gravitee AM
* Set up the connection in Azure AD
* Test the connection

## Register a new application in Azure AD

[Register an application with the Microsoft identity platform](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app).

1. Sign in to the [Azure portal](https://portal.azure.com/).
2. If you have access to multiple tenants, use the **Directory + subscription** filter in the top menu to select the tenant for which you want to register an application.
3. Search for and select Azure Active Directory.
4. Under **Manage**, select **App registrations**, then **New registration**.
5. Enter a Name for your application.
6. Specify who can use the application.
7. Do not enter anything for **Redirect URI** at this point, you will be able to configure one in the next section (note that this field is optional).
8. Click **Register** to complete the initial app registration. Azure will generate an Application ID. We need to create a new client secret.
9. Select your application in **App registrations** in the Azure portal.
10. Select **Certificates & secrets > New client secret**.
11. Add a description for your client secret.
12. Select a duration.
13. Click **Add**.

{% hint style="info" %}
Record the client secret value for later use, as it is not displayed again after you leave this page.
{% endhint %}

## Create an Azure AD identity provider

1. Log in to AM Console.
2. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
3. Choose the **Azure AD** identity provider type and click **Next**.

{% hint style="info" %}
Ensure you have the generated Client ID and Client Secret from the Azure AD application to hand.
{% endhint %}

4. Give your identity provider a name.
5. Enter the Azure Tenant ID of your application.
6. Enter your Azure application ID and Client Secret.
7.  Click **Create**.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-azure-ad.png" alt=""><figcaption><p>Create Azure AD IdP</p></figcaption></figure>

{% hint style="info" %}
On the right of the screen under **1. Configure the Redirect URI**, copy the value of the URL. You will need to update it in your Azure AD application settings.
{% endhint %}

## Set up the connection

1. Go to your Azure AD application settings and click **Add a Redirect URI** from your application overview page.
2. Enter the value of the Redirect URI created in the previous step and click **Save**.

## Test the connection

You can test the Azure AD connection using a web application created in AM.

1.  i.e.In AM Console, click **Applications** and select your social identity provider.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select Azure AD IdP</p></figcaption></figure>
2.  Call the Login Page (i.e. `/oauth/authorize` endpoint). If the connection is working you will see the **Sign in with …​** button.

    If the button is not visible, there may be a problem the identity provider settings. Check the AM Gateway log for more information.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-login.png" alt=""><figcaption><p>Sign in options</p></figcaption></figure>
