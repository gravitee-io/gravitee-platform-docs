# Add RBAC to your JWT Plan

{% hint style="warning" %}
This tutorial builds off of [Configure JWT Security](configure-jwt-security.md), which must be completed as a prerequisite.
{% endhint %}

## Overview

Gravitee API Management (APIM) has a Role-based Access Control policy that can act as an additional security and access control measure. This allows fine-grained control over which applications can access which resources based on their assigned roles.

Due to some community requests, this tutorial will serve as a short extension of the Configure JWT Security tutorial. This tutorial will show how to configure the Role-based Access Control (RBAC) policy on a JWT plan when using an IdP. Additionally, we will configure the policy to only be active on a sub-resource of our backend API server.

{% hint style="warning" %}
Currently, the RBAC policy can be applied to v2 APIs and v4 proxy APIs. It cannot be applied to v4 message APIs.
{% endhint %}

## Prerequisites <a href="#prerequisites-3" id="prerequisites-3"></a>

To participate in this tutorial, you must have an instance of APIM 4.0 or later up and running. You can check out our installation guides to learn the different ways you can get started with Gravitee.

Additionally, the following guide assumes you have already completed the [Configure JWT Security](configure-jwt-security.md) tutorial, which is referred to here as the previous tutorial.

## Configure your IdP <a href="#configure-your-idp-4" id="configure-your-idp-4"></a>

Gravitee Access Management and third-party IdPs provide a number of ways to add roles to your access token’s claims, such as permissions and custom rules. However, regardless of the method, it is essential for Gravitee’s RBAC policy to receive the roles in a `List` like `['admin', 'user']` as opposed to a space-separated `String` like `'admin user'`.

## Add Policies to the Gateway API <a href="#add-policies-to-the-gateway-api-6" id="add-policies-to-the-gateway-api-6"></a>

The next step is to add the necessary policies to the Gateway API you configured in the previous tutorial. In the Console UI, open the API you created previously, and select **Policy Studio** in the inner sidebar.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-20 at 11.39.43 PM (1).png" alt=""><figcaption></figcaption></figure>

The Policy Studio provides a graphical interface to design and configure flows. Flows define the processing logic and order of policies applied to an API transaction and can be applied at the platform, API, and plan levels. We will use the Policy Studio to apply flows at the plan level.

Add a flow by selecting the + icon next to the JWT plan. Here you have a number of options to set the conditions under which your flow runs, including the path of the API request, the HTTP method used, and even custom expressions set with EL. For the demo, we will set this flow to only run for GET requests to the `/sub-resource` path.

Provide a name and select **Save**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-20 at 11.49.45 PM (1).jpg" alt=""><figcaption></figcaption></figure>

The RBAC policy expects the roles to be in the `gravitee.attribute.user.roles` attribute, where attributes are a kind of variable scoped to the current API transaction. In an OAuth2 plan, OAuth token scopes are automatically added to the `gravitee.attribute.user.roles` attribute. However, in a JWT plan, this must be done manually by using Gravitee’s Expression Language (EL) and the Assign Attributes policy.

### Assign attributes policy <a href="#assign-attributes-policy-7" id="assign-attributes-policy-7"></a>

Next, we will add our first policy to this flow. Select the **+ icon** in the **Request phase**. Search for the **Assign attributes** policy and click **Select**.

This will bring up the configuration options for the Assign Attributes policy. Select **+ Add** under **Assign context attributes** at the bottom of policy settings. The name of the attribute is `gravitee.attribute.user.roles`, and the value is an EL expression. If you remember setting up the JWT plan, we enabled a setting to extract the JWT claims into the `jwt.claims` context attribute, and now we can take advantage of that setting.

The EL expression is `{#context.attributes['jwt.claims']['permissions']}` , which accesses the `permissions` claim from all the JWT’s claims stored in the `jwt.claims` context attribute. Add the expression as the value of the attribute, and then select **Add policy**.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-20 at 11.55.36 PM (1).jpg" alt=""><figcaption></figcaption></figure>

With this set, we can move on to the final step.

### RBAC policy <a href="#rbac-policy-8" id="rbac-policy-8"></a>

Similar to before, Select the **+ icon** after the Assign Attributes policy in the **Request phase**. Search for the **Role Based Access Control** policy and click **Select**.

From here, you simply need to add the roles required to access the API endpoint that you specified in the flow configuration. In our example, that endpoint is `GET https://your-gateway-host/your-api-context-path/sub-resource` and the required roles are `admin` and `user`.

<figure><img src="../../.gitbook/assets/Screenshot 2023-11-20 at 11.58.26 PM (1).png" alt=""><figcaption></figcaption></figure>

After you’ve added the roles, select **Save** in the top right, and redeploy your API. All `GET` requests to the `/sub-resource` route will now have this flow applied that checks the JWT for configured roles.
