---
description: An overview about microsoft entra id.
---

# Microsoft Entra ID

## Overview

This article provides information about setting up APIM authentication in the APIM Console UI to use Microsoft Entra ID (formerly known as Azure AD) as an IDP.

{% hint style="info" %}
For documentation about securing your APIs with OAuth2 and Entra ID, see the documentation on the [JWT Plan](../../../../4.10/secure-and-expose-apis/plans/jwt.md).
{% endhint %}

## Prerequisites

* Microsoft Entra ID subscription
* An administrator who can access the domain in Entra ID
* An Application Registration in Entra ID to allow Gravitee to integrate with Entra ID and retrieve user profiles
* A Gravitee APIM installation with network access to Entra ID

## Task Overview

1. [Create an Application Registration in Entra ID](microsoft-entra-id.md#task-1-create-an-application-registration-in-entra-id)
2. [Obtain the needed URLs from Entra ID](microsoft-entra-id.md#task-2-obtain-the-urls-for-the-gravitee-identity-provider)
3. [Configure Gravitee APIM Identity Provider configuration](microsoft-entra-id.md#task-3-configure-apim-entra-id-authentication)
4. [Test your Identity Provider](microsoft-entra-id.md#task-4-test-your-identity-provider)

### Task 1: Create an Application Registration in Entra ID

1. Create an application in Entra ID. Complete the following steps to fulfill the minimum setup requirements:
   1. In the Azure Portal, search or click **App registrations**.
   2. Click **New Registration**.
   3. Type a name for your application. For example, "gravitee-client-local".
   4. Select who can use or access the API.
   5. **Supported account types:** Choose an option that applies to your context. For example, Accounts in this organizational directory only (\<your\_domain> only - Single tenant).
   6. Modify the **Redirect URI** to map to your APIM Console URL. For example, for a local deployment of APIM: `http://localhost:8084`, or for a Gravitee Cloud customer: `https://prod.apim.console.<tenant>.gravitee.cloud`.
   7. Click **Register** to create the App Registration.
2. Obtain the Application (client) ID. For example, "6f9d31e7-802b".<img src="https://images.gitbook.com/__img/dpr=2,width=1168,onerror=redirect,format=auto,signature=-1460685375/https%3A%2F%2Fslabstatic.com%2Fprod%2Fuploads%2F6lql0jy7%2Fposts%2Fimages%2Fpreload%2FvknINzxKjIORrO3PPJCQhI89.png" alt="" data-size="original">
3. Generate a client secret. To generate a client secret, complete the following steps:
   1. Click **Add a certificate or secret**
   2. Click on New client secret.
   3. Enter a Description.
   4. Specify the Expires value.
   5. Click **Add**.
   6. Copy the Value (not the Secret ID). This is used by APIM to authenticate with Entra ID when checking the tokens and authentication of users logging into Gravitee.![](<../../../../4.10/.gitbook/assets/image (231).png>)
4. Configure the **API permissions** to allow Gravitee to read the user **email**, **openid**, and **profile** details.

<figure><img src="../../../../4.10/.gitbook/assets/image (230).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
The `profile` scope is a permission request that grants access to a wider range of user profile information, including the `given_name` and `family_name` claims.
{% endhint %}

{% hint style="success" %}
You can now progress to the next task and add a new Identity Provider to Gravitee APIM.
{% endhint %}

### Task 2: Obtain the needed URLs from Entra ID

Retrieve your endpoint configuration within Entra ID.&#x20;

1. To retrieve your endpoint configuration, go to the **App Registrations** page, and then click the **Endpoints** menu item. You should see a complete list of available **Endpoints**.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/4_VGG-R9ILX5w7ombyNvQnZb.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../../4.10/.gitbook/assets/image (234).png" alt=""><figcaption></figcaption></figure>

2. Copy the **OpenID Connect metadata document** link. For example, [https://login.microsoftonline.com/common/.well-known/openid-configuration](https://login.microsoftonline.com/b7389665-58df-4f4c-a3a3-ed5adf0aafd8/v2.0/.well-known/openid-configuration).
3. Open the **OpenID Connect metadata document** link in a browser. This link contains the following URLs, which you need to use in the Gravitee Identity Provider configuration wizard:
   * `token_endpoint`: [https://login.microsoftonline.com/common/oauth2/token](https://login.microsoftonline.com/common/oauth2/token)
   * `authorization_endpoint`: [https://login.microsoftonline.com/common/oauth2/authorize](https://login.microsoftonline.com/common/oauth2/authorize)
   * `userinfo_endpoint`: [https://login.microsoftonline.com/common/openid/userinfo](https://login.microsoftonline.com/common/openid/userinfo)
   * `end_session_endpoint`: [https://login.microsoftonline.com/common/oauth2/logout](https://login.microsoftonline.com/common/oauth2/logout)

### Task 3: Configure Gravitee APIM Identity Provider configuration

1. Log in to the APIM Console as a user with the ADMIN role.
2. From the Dashboard, click **Organization**.
3. From the Organization menu, click **Authentication**.
4. Navigate to **Identity Providers**, and then click **+ Add an identity provider**.
5. Select **OpenID Connect**.
6. In the **General** section, add the following information:
   1. In the **Name** field, type the name of your Identity Provider.
   2. (Optional) Type a description for your Identity Provider.
   3. Enable the **Allow portal authentication to use this identity provider** option.
   4. Enable the **A public email is required to be able to authenticate** option.
7. In the **Group and role mappings** sub-section, select the **Computed during each user authentication** option.

<figure><img src="../../../../4.10/.gitbook/assets/image (235).png" alt=""><figcaption></figcaption></figure>

#### Configure the Microsoft Entra ID

<figure><img src="../../../../4.10/.gitbook/assets/image (233).png" alt=""><figcaption></figcaption></figure>

8. In the **Client Id** field, enter your Microsoft Application Registration Client ID.
9.  In the **Client Secret** field, enter your Client Secret.

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>You can include your Tenant ID in your Endpoint URLs. To include your Tenant ID, replace <code>common</code> with your Tenant ID.</p></div>
10. In the **Token Endpoint** field, enter the following endpoint: [`https://login.microsoftonline.com/common/oauth2/token`](https://login.microsoftonline.com/common/oauth2/token).
11. For the **Token Introspect Endpoint**, leave this field blank. Microsoft Entra ID does not provide an Introspective endpoint.
12. In the **Authorization Endpoint** field, enter the following endpoint: [`https://login.microsoftonline.com/common/oauth2/authorize`](https://login.microsoftonline.com/common/oauth2/authorize).
13. In the **UserInfo Endpoint** field, enter the following endpoint: [`https://login.microsoftonline.com/common/openid/userinfo`](https://login.microsoftonline.com/common/openid/userinfo).
14. In the **UserInfo Logout Endpoint** field, enter the following endpoint: [`https://login.microsoftonline.com/common/oauth2/logout`](https://login.microsoftonline.com/common/oauth2/logout).
15. In the **Scopes** field, add `openid` `email` and `profile`.
16. In the **Authentication button color** field, specify your color preferences in the following form: `#RRGGBB`.

#### User profile mapping

<figure><img src="../../../../4.10/.gitbook/assets/image (232).png" alt=""><figcaption></figcaption></figure>

17. In the **ID** field, enter `sub` .
18. In the **First name** field, enter `given_name`.
19. In the **Last name** field, enter `family_name`.
20. In the **Email** field, enter `email`.
21. In the **Picture** field, leave this blank.  Because Entra ID does not provide this claim, providing any value here may cause an error.
22. Click on **Create**.

{% hint style="info" icon="spider-black-widow" %}
If you specify an invalid value, such as a claim that does not exist in the supplied token, Microsoft ID fails and does not provide you with any error message.
{% endhint %}

{% hint style="success" %}
The Identity Provider setup is now complete. You can follow the remaining steps to test authentication.
{% endhint %}

### Task 4: Test your Identity Provider

{% hint style="warning" %}
To avoid the use of a previous token or misconfiguration, reset the cache of your browser.
{% endhint %}

1. Sign in to your Gravitee APIM Console. You should now see Entra ID as an option.
2. Click the button, and then follow the steps to sign in. Once you sign in, you have default (USER) access.

<figure><img src="../../../../4.10/.gitbook/assets/image (238).png" alt=""><figcaption></figcaption></figure>

## **Additional Configuration**

### **Permissions, groups and roles**

You can manually customize permissions, groups, and roles for new users, or use the automatic Roles and Groups Mapping feature. Click this link for more information about [Roles and Groups Mappings](../../../../4.10/configure-and-manage-the-platform/manage-organizations-and-environments/authentication/roles-and-groups-mapping.md).

### **Groups Mapping**

Gravitee APIM can be configured to request the user's groups from an UserInfo endpoint of the OAuth2 server, but Entra ID may not be configured to provide this information through the UserInfo endpoint.

To obtain user groups, your Entra ID Administrator must choose to customize the tokens by mapping the Groups claim. More information can be found on the Microsoft site at [Add group claims to tokens for SAML applications using SSO configuration](https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-fed-group-claims#add-group-claims-to-tokens-for-saml-applications-using-sso-configuration).​

Once the token includes the required `groups` claim, you can check if the user is a member of a group. For example, `{#jsonPath(#profile, '$.groups[0]').contains('your-group-objectID')}`.
