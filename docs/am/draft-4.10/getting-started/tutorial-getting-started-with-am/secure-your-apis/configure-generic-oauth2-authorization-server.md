# Configure Generic OAuth2 Authorization Server

## Overview

Once you've added the OAuth2 policy to your API, you will need to configure it with an authorization server resource. To configure the Generic OAuth2 Authorization Server resource, follow the steps below.

{% hint style="info" %}
The `clientId` used for the resource configuration must match the `clientId` of the application in APIM.
{% endhint %}

## Configuration

The following instructions assume that the OAuth server is a Gravitee AM Gateway, but other solutions are supported.

1. Log in to APIM Management Console.
2. Click **APIs** in the left sidebar.
3. Select the API you want to add the resource to.
4. Click **Resources** in the inner left sidebar.
5.  Select the **Generic OAuth2 Authorization Server** resource:&#x20;

    <figure><img src="../../../.gitbook/assets/oauth2 resources generic.png" alt=""><figcaption></figcaption></figure>
6.  In the CREATE RESOURCE form, enter the **Resource name** that will be used to link this resource to an OAuth 2 plan:&#x20;

    <figure><img src="../../../.gitbook/assets/resource name 2.png" alt=""><figcaption></figcaption></figure>
7.  Specify the base URL to reach the OAuth2 server. It must be the longest common path between the introspection URL and the user info endpoint URL:&#x20;

    <figure><img src="../../../.gitbook/assets/server url 2.png" alt=""><figcaption></figcaption></figure>
8.  Enter the introspection endpoint used to validate the AccessToken:&#x20;

    <figure><img src="../../../.gitbook/assets/token introspection.png" alt=""><figcaption></figcaption></figure>
9.  If you toggle **System proxy** ON, the resource will use the proxy settings defined in the APIM Gateway's `gravitee.yaml` file:&#x20;

    <figure><img src="../../../.gitbook/assets/use system proxy.png" alt=""><figcaption></figcaption></figure>
10. Enter the HTTP method used to request the introspection endpoint:&#x20;

    <figure><img src="../../../.gitbook/assets/introspection method.png" alt=""><figcaption></figcaption></figure>
11. Enter the path at which the user information will be requested:&#x20;

    <figure><img src="../../../.gitbook/assets/user endpoint.png" alt=""><figcaption></figcaption></figure>
12. Enter the HTTP method used to request the user info endpoint:&#x20;

    <figure><img src="../../../.gitbook/assets/userinfo method.png" alt=""><figcaption></figcaption></figure>
13. Specify the client credentials to authorize access to the introspect endpoint in AM:&#x20;

    <figure><img src="../../../.gitbook/assets/client credentials 2.png" alt=""><figcaption></figcaption></figure>
14. Toggle **Use HTTP header for client authorization** ON to specify that the client credentials are sent to the authorization server using the **Basic** scheme:&#x20;

    <figure><img src="../../../.gitbook/assets/use http header for client auth.png" alt=""><figcaption></figcaption></figure>
15. The OAuth2 server accepts 3 different options for providing the `access_token` to the introspection endpoint. AM expects the `access_token` to be provided through the token parameter of a POST form:  &#x20;

    <figure><img src="../../../.gitbook/assets/access token.png" alt=""><figcaption></figcaption></figure>
16. Specify the claim that contains the user identifier (AM provides this information through the `sub` claim by default):&#x20;

    <figure><img src="../../../.gitbook/assets/user claim 2.png" alt=""><figcaption></figcaption></figure>

### Example

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/oy0gC8ZxgaTXtfIk04FHOJRL.png" alt=""><figcaption></figcaption></figure>

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/Zzj2gT-PmLPMGhF7-eL3PAXA.png" alt=""><figcaption></figcaption></figure>
