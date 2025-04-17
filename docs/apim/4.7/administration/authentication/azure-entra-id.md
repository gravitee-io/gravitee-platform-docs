# Azure Entra ID

## Overview

This article aims to provide information on how to setup APIM authentication in the APIM Console UI to be able to use Azure Entra ID (formerly known as Azure AD) as an IDP.

{% hint style="info" %}
These instructions currently only cover authentication, not the role mappings.
{% endhint %}

{% hint style="info" %}
For documentation about securing your APIs with OAuth2 and Entra ID, see the documentation about the [JWT Plan](../../expose-apis/plans/jwt.md).
{% endhint %}

## Prerequisites:

* Azure Entra ID subscription
* An Application Registered in Entra ID to represent Gravitee APIM console
* A running Gravitee APIM installations with access to Entra ID.
* A User who can access the domain in Entra ID.

## Application Creation (example) in Entra ID (minimum setup):

First, you'll need to create an application in Entra ID. Here is an example of steps to create that application:

* In the Entra ID menu, click **App registrations**
* Click **New Registration**
  * Pick a name for your application ex: "gravitee-client-local"
  * Select who can use or access the API:
  * Pick what applies to your context (use the default "Accounts in this organizational directory only (\<yourdomain> only - Single tenant) for example)
  * edit the Redirect URI to map with your API Management console URL
    * ex: [http://localhost:8084](http://localhost:8084) for a local deployment of APIM
* Click **Register**
* Enter you application details by clicking on it
  * copy the Application (client) ID from the Overview page . This will be used to identify your application when configuring APIM Authentication (this looks like a UUID)

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/vknINzxKjIORrO3PPJCQhI89.png" alt=""><figcaption></figcaption></figure>

* Generate a client secret
  * Click on the Certificate & Secrets
  * Click on New client secret
    * Enter a description
    * Enter an expiration
    * Click Add
  * copy the Value (not the Secret ID): This will be used in to authenticate your Gravitee APIM application when checking token and authentication of users.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/lu-VXbcFoZUJOcnAbiVAmOb9.png" alt=""><figcaption></figcaption></figure>

At this point, you are ready to configure the Authentication in Gravitee APIM Console.

## Instructions using Azure v1 endpoints:

First, you'll need to retrieve your endpoint configuration within Azure Entra ID. To do so, follow these steps:

* Log in to your Azure Portal
* Enter the "Microsoft Entra ID" service
* Go to App Registrations
* Click on Endpoints

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/4_VGG-R9ILX5w7ombyNvQnZb.png" alt=""><figcaption></figcaption></figure>

* It will give you the list open endpoints for your calls. This will be helpful for our configuration. Provide a copy of that list.
  * Note: The hidden part is your tenant ID. You can replace those values by "common" in all the URL below as well.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/9QDH_3f1LptEvDLnKy0N1veC.png" alt=""><figcaption></figcaption></figure>

* Use the OpenID Connect Metadata document link (ends with /openid-configuration). A page will open with your OpenID configuration. You'll use the endpoint on that list to configure Gravitee.

### Configure APIM Azure Entra ID Authentication

Next, you'll need to configure authentication on the Gravitee side. Follow these steps:

* Log into the APIM Console as a user with the ADMIN role
* Go to Organization>Authentication
* Click **Add an identity provider**
* Select **OpenID Connect.** Configure as follows:
  * General section
    * Give a Name and a Description to that OIDC Identity Provider
    * Check the "Allow portal authentication to use this identity provider" option
    * Check the "A public email is required to be able to authenticate"
    * Check "Computed during each user authentication"

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/pYGrG6-7PMAv7pETkO5KSLGb.png" alt=""><figcaption></figcaption></figure>

* Configuration
  * clientid: the client ID of \<your application representing Gravitee>
  * client secret: the client secret of \<your application representing Gravitee>
* Edit the fields in the different section according to the endpoints found in your Entra ID configuration.
  * You have to use the following endpoints for Azure v1 (you can replace "common" by the value in your own configuration but "common" should work as well):
    * Token Endpoint: [https://login.microsoftonline.com/common/oauth2/token](https://login.microsoftonline.com/common/oauth2/token)
    * Token Introspect Endpoint: Azure Entra ID doesn't provide any Introspect endpoint - leave it empty
    * Authorize Endpoint: [https://login.microsoftonline.com/common/oauth2/authorize](https://login.microsoftonline.com/common/oauth2/authorize)
    * UserInfo Endpoint: [https://login.microsoftonline.com/common/openid/userinfo](https://login.microsoftonline.com/common/openid/userinfo)
    * UserInfo Logout Endpoint: [https://login.microsoftonline.com/common/oauth2/logout](https://login.microsoftonline.com/common/oauth2/logout)
    * Scopes: openid
    * Authentication button color: Your color of choice

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/ibNH9Gp72TkE7WDe8BYZc2m2.png" alt=""><figcaption></figcaption></figure>

* User profile mapping
  * ID: sub
  * First Name: name
  * Last Name: name
  * Email: upn (this one is tricky, if you leave at a value like email, or anything that is not part of the token provided by Azure , it will fail and likely won't give you any error message.
  * Picture: picture (likely a warning in the logs)
* Save your Identity provider

{% hint style="success" %}
At this point, the IdP should be set up. Feel free to follow the remaining steps to test authentication.
{% endhint %}

### Use your new Identity Provider

Now, let's test your new Identity provider. Follow these steps:

* Log to APIM console

{% hint style="info" %}
**Reset your cache**

It is recommended to reset the cache of your browser so to avoid the use of a previous token or misconfiguration.
{% endhint %}

* You should now see Azure AD as an option on the login screen

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/preload/oiNtu7QGGkPPEHhmKSlppWFI.png" alt=""><figcaption></figcaption></figure>

* Click on the button and follow the steps to login (might include MFA, etc…)
* Once logged in, you'll have restricted access to APIM Console
* You'll need to logout and log again with an ADMIN user, go to Organization > Users and set the correct rights to the newly added user attached to Azure AD.
