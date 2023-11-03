# Single Sign On

## Introduction

With Single Sign On you are able to configure your own authentication method for signing in to Cockpit. This will allow many benefits, such as:

* Your users to sign in with an already familiar account and credentials
* You can use an authentication method that meets your information security assessments
* You will have greater influence to centrally remove users accounts and hence remove their possibility to sign in to Cockpit

{% hint style="info" %}
Single Sign On is an enterprise feature. Want to know more about the full Gravitee Enterprise offering? [Reach out to our commercial team](https://www.gravitee.io/contact-us-cockpit).
{% endhint %}

## How it works

Single Sign On allows you to set up an identity trust federation with your organizations Identity Provider using the standard OAuth 2.0 and OpenID Connect. This means you can connect directly to your Gravitee Access Management, Okta, Ping, Azure AD, Keycloak or any Identity provider that support OAuth 2.0 and OpenID Connect.

From an end user perspective, they will choose to sign in with single sign on option on the main sign in page of Cockpit. They will then be presented a page where they are asked to provide their organization email. Based on the email provided by the user, they will be redirected to your chosen authentication method to either sign in or to have an single sign on experience if the user is already authenticated.

<figure><img src="../.gitbook/assets/image (2).png" alt="" width="375"><figcaption><p>Sign in screen of Cockpit where single sign in users should click on "Sign in with your company SSO" option.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (3).png" alt="" width="375"><figcaption><p>Single Sign On screen where user should provide their email in order to be redirected to organization IdP.</p></figcaption></figure>

## How to configure



{% hint style="info" %}
It is recommended to keep a non Single Sign On user as Account Primary Owner so you always have a way of recovering the Cockpit Account. Only the Account Primary Owner can configure Single Sign On.
{% endhint %}

Step 1. Navigate to Account Settings menu, choose Single Sign On and click on Configure.

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption><p>Single Sign On option is found on Account Settings menu.</p></figcaption></figure>

Step 2. The first section to configure is the domain realm. The domain realm value is the domain that will be used to identify how to authenticate users when they enter their email on the sign in screen.

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption><p>Section where you should add the domain realm, i.e the email domain that users should provide in order to be redirected correctly.</p></figcaption></figure>

Step 3. Create an Oauth client in your IdP that supports the Authorization Code Flow.

{% hint style="info" %}
If you are using Gravitee Access Management, you can follow the guide [here](https://documentation.gravitee.io/am/guides/applications) on how to configure an OAuth client Application.
{% endhint %}

Step 4. Enter the details of your Oauth client in the "Set up Oauth/ OpenID Connect configuration" section.

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption><p>Section where you should add details of the OAuth client configured in your IdP</p></figcaption></figure>

Step 5. Make sure you allow Oauth scopes openid, profile and email in your OAuth client. Its needed for Cockpit to receive all user attributes (claims) to create the user profile.

Step 6. Once you feel comfortable with the configuration. Click on "Create Redirect URI".

<figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption><p>Section where you need to consent that you allow scopes openid, profile and email in your OAuth client.</p></figcaption></figure>

Step 7. Now you will be presented with a new screen which shows the generated redirect uri. This is the endpoint that your IdP will send back users from once they have succesfully authenticated. Copy this value and update the redirect uri on the OAutht client in your IdP

<figure><img src="../.gitbook/assets/image (10).png" alt=""><figcaption><p>Section where you will receive generated redirect uri that you need to update your OAuth Client in your IdP with</p></figcaption></figure>

You will now see the Single Sign On screen but with an Identity Provider created and enabled. Your users can now sign in to Cockpit with Single Sign On.

<figure><img src="../.gitbook/assets/image (13).png" alt=""><figcaption><p>Single Sign On with an Identity Provider successfully created.</p></figcaption></figure>
