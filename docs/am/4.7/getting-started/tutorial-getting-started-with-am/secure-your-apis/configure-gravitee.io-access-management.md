---
description: Configuration guide for Configure Gravitee.
---

# Configure Gravitee.io Access Management

## Overview

Once you've added the OAuth2 policy to your API, you will need to configure it with an authorization server resource. To configure the Gravitee.io Access Management Authorization Server resource, follow the steps below.

{% hint style="info" %}
The `clientId` used for the resource configuration must match the `clientId` of the application in APIM.
{% endhint %}

## Configuration

1. Log in to APIM Management Console.
2. Click **APIs** in the left sidebar.
3. Select the API you want to add the resource to.
4. Click **Resources** in the inner left sidebar.
5.  Select the **Gravitee.io AM Authorization Server** resource:

    <figure><img src="../../../../4.0/.gitbook/assets/oauth2 resources gravitee.png" alt=""><figcaption></figcaption></figure>
6.  In the CREATE RESOURCE form, enter the **Resource name** that will be used to link this resource to an OAuth 2 plan:

    <figure><img src="../../../../4.0/.gitbook/assets/resource name.png" alt=""><figcaption></figcaption></figure>
7.  Specify the base URL to reach the AM Gateway:

    <figure><img src="../../../../4.0/.gitbook/assets/base url.png" alt=""><figcaption></figcaption></figure>
8.  If you toggle **System proxy** ON, the resource will use the proxy settings defined in the APIM Gateway's `gravitee.yaml` file:

    <figure><img src="../../../../4.0/.gitbook/assets/system proxy.png" alt=""><figcaption></figcaption></figure>
9.  Specify the AM version you want to target. For AM v3 and v4, use "v3\_x":

    <figure><img src="../../../../4.0/.gitbook/assets/version.png" alt=""><figcaption></figcaption></figure>
10. In the **Security domain** field, enter the HRID of the domain declared on AM:

    <figure><img src="../../../../4.0/.gitbook/assets/security domain.png" alt=""><figcaption></figcaption></figure>
11. Specify the client credentials to authorize access to the introspect endpoint in AM. The application needs to be configured in AM using the "client\_secret\_basic" method.

    <figure><img src="../../../../4.0/.gitbook/assets/client credentials.png" alt=""><figcaption></figcaption></figure>
12. Specify the claim that contains the user identifier (AM provides this information through the `sub` claim by default):

    <figure><img src="../../../../4.0/.gitbook/assets/user claim 2.png" alt=""><figcaption></figcaption></figure>

### Example

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/PTtH6lt9KhkmlOEMixpm2dPr.png" alt=""><figcaption></figcaption></figure>
