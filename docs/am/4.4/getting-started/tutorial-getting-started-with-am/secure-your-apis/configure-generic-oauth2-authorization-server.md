---
description: Configuration guide for Configure Generic OAuth2 Authorization Server.
---

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
5.  Select the **Generic OAuth2 Authorization Server** resource:

    <figure><img src="../../../.gitbook/assets/oauth2 resources generic.png" alt="The API Resources page with the Generic OAuth2 Authorization Server resource circled among the available resource types."><figcaption></figcaption></figure>
6.  In the CREATE RESOURCE form, enter the **Resource name** that will be used to link this resource to an OAuth 2 plan:

    <figure><img src="../../../.gitbook/assets/resource name 2.png" alt="The Resource name field of the Create Resource form, containing myresource."><figcaption></figcaption></figure>
7.  Specify the base URL to reach the OAuth2 server. It must be the longest common path between the introspection URL and the user info endpoint URL:

    <figure><img src="../../../.gitbook/assets/server url 2.png" alt="The Authorization server URL field containing the address of the authorization server."><figcaption></figcaption></figure>
8.  Enter the introspection endpoint used to validate the AccessToken:

    <figure><img src="../../../.gitbook/assets/token introspection.png" alt="The Token introspection endpoint field containing /oauth/introspect."><figcaption></figcaption></figure>
9.  If you toggle **System proxy** ON, the resource will use the proxy settings defined in the APIM Gateway's `gravitee.yaml` file:

    <figure><img src="../../../.gitbook/assets/use system proxy.png" alt="The System proxy toggle, switched off."><figcaption></figcaption></figure>
10. Enter the HTTP method used to request the introspection endpoint:

    <figure><img src="../../../.gitbook/assets/introspection method.png" alt="The Token introspection method list set to POST."><figcaption></figcaption></figure>
11. Enter the path at which the user information will be requested:

    <figure><img src="../../../.gitbook/assets/user endpoint.png" alt="The Userinfo endpoint field containing /oidc/userinfo."><figcaption></figcaption></figure>
12. Enter the HTTP method used to request the user info endpoint:

    <figure><img src="../../../.gitbook/assets/userinfo method.png" alt="The Userinfo method list set to GET."><figcaption></figcaption></figure>
13. Specify the client credentials to authorize access to the introspect endpoint in AM:

    <figure><img src="../../../.gitbook/assets/client credentials 2.png" alt="The Client Id field holding an identifier, above a masked Client Secret field."><figcaption></figcaption></figure>
14. Toggle **Use HTTP header for client authorization** ON to specify that the client credentials are sent to the authorization server using the **Basic** scheme:

    <figure><img src="../../../.gitbook/assets/use http header for client auth.png" alt="The Use HTTP header for client authorization toggle switched on, with the Authorization header name and the Basic scheme below it."><figcaption></figcaption></figure>
15. The OAuth2 server accepts 3 different options for providing the `access_token` to the introspection endpoint. AM expects the `access_token` to be provided through the token parameter of a POST form:

    <figure><img src="../../../.gitbook/assets/access token.png" alt="The access token delivery options, with the query parameter and HTTP header methods switched off and form-urlencoded delivery switched on."><figcaption></figcaption></figure>
16. Specify the claim that contains the user identifier (AM provides this information through the `sub` claim by default):

    <figure><img src="../../../.gitbook/assets/user claim 2.png" alt="The User claim field set to sub."><figcaption></figcaption></figure>

### Example

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/oy0gC8ZxgaTXtfIk04FHOJRL.png" alt="The Create Resource form for a generic OAuth2 authorization server, with the authorization server URL, token introspection endpoint and method, userinfo endpoint and method, client ID, and masked client secret."><figcaption></figcaption></figure>

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/Zzj2gT-PmLPMGhF7-eL3PAXA.png" alt="The client authorization settings of the OAuth2 resource, with HTTP header authorization enabled using the Basic scheme, form-urlencoded token delivery enabled, and the user claim set to sub."><figcaption></figcaption></figure>
