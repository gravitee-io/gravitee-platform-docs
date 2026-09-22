---
description: Secure an MCP proxy API in API Management 4.12 with an OAuth2 plan and Access Management. Learn the use cases and how the flow works.
---

# Secure MCP Proxy with OAuth2

## Overview

This guide explains how to secure an MCP proxy API using Gravitee API Management (APIM) with an OAuth2 plan and Gravitee Access Management (AM).

### Why secure your MCP proxy?

Model Context Protocol (MCP) servers provide AI applications with access to tools, data sources, and system capabilities. In production environments, unsecured MCP endpoints create significant risks:

* **Unauthorized access:** Without authentication, any client can connect to your MCP server and invoke tools or access sensitive data.
* **Resource abuse:** Uncontrolled access can lead to excessive API calls, increased costs, and degraded performance.
* **Compliance violations:** Many industries require authenticated and auditable access to systems that handle sensitive data.
* **Multi-tenant exposure:** In shared environments, unsecured endpoints can expose one tenant's resources to another.

Securing your MCP proxy with OAuth2 ensures that only authenticated and authorized clients can access your MCP server through the Gravitee Gateway.

### Use cases

This solution is designed for the following scenarios:

* **Enterprise AI deployments:** Organizations deploying AI assistants that need controlled access to internal tools and data sources.
* **Multi-tenant platforms:** SaaS providers offering MCP-based integrations where each customer's access must be isolated and authenticated.
* **Regulated environments:** Industries such as finance, healthcare, or government, where audit trails and access controls are mandatory.
* **Development teams:** Teams using MCP-enabled IDEs (such as VSCode or Cursor) that require secure connections to shared development resources.

### How it works

Gravitee provides end-to-end security for MCP traffic by combining API Management and Access Management:

1. **Gravitee APIM** acts as a gateway, proxying requests to your MCP server and enforcing security policies.
2. **Gravitee AM** serves as the OAuth2 authorization server, handling client authentication and token issuance.
3. **Dynamic Client Registration (DCR)** allows MCP clients to register automatically with AM, simplifying client onboarding.
4. **OAuth2 plans** in APIM verify tokens and control access to the MCP proxy API.

When an MCP client connects, it authenticates through AM, receives an access token, and uses that token to communicate with the MCP server through the Gravitee Gateway.

### Components

This guide uses three separate Gravitee components:

* **MCP Server**: Your upstream Model Context Protocol server, the service being secured.
* **Gravitee APIM**: The API gateway that proxies requests to your MCP server.
* **Gravitee AM**: The OAuth2 authorization server that handles authentication.
* **MCP Client:** The application that connects to your MCP server through the Gravitee Gateway. For example: VSCode, Cursor, or Native SDK.

## Prerequisites

* A Gravitee Access Management (AM) domain with configuration rights and the Gateway URL. For example: `https://am-gateway.example.com` For more information on getting started with AM Console, see [how to access AM Console.](https://documentation.gravitee.io/am/getting-started/tutorial-getting-started-with-am/login-to-am-console)
* An MCP client that supports OAuth2 authentication with Dynamic Client Registration (DCR). For example, VSCode with MCP support.
* An unsecured MCP server to proxy.

## **Configuration Workflow**

To secure your MCP proxy, complete the following steps:

1. [#create-the-mcp-proxy-api-in-apim](secure-mcp-proxy-with-oauth2.md#create-the-mcp-proxy-api-in-apim "mention")
2. [#register-the-mcp-server-in-am](secure-mcp-proxy-with-oauth2.md#register-the-mcp-server-in-am "mention")
3. [#enable-dynamic-client-registration-in-am](secure-mcp-proxy-with-oauth2.md#enable-dynamic-client-registration-in-am "mention")
4. [#optional-enable-user-registration-in-am](secure-mcp-proxy-with-oauth2.md#optional-enable-user-registration-in-am "mention")
5. [#configure-the-0auth2-plan-in-apim](secure-mcp-proxy-with-oauth2.md#configure-the-0auth2-plan-in-apim "mention")
6. [#verification-1](secure-mcp-proxy-with-oauth2.md#verification-1 "mention")
7. [#connect-mcp-client](secure-mcp-proxy-with-oauth2.md#connect-mcp-client "mention")

## Create the MCP Proxy API in APIM

1.  From the **Dashboard**, click **APIs.**

    <figure><img src="../.gitbook/assets/mcp-click-api.png" alt=""><figcaption></figcaption></figure>
2.  Click **+ Add API.**

    <figure><img src="../.gitbook/assets/mcp-click-add-api.png" alt=""><figcaption></figcaption></figure>
3.  Click **Create V4 API.**

    <figure><img src="../.gitbook/assets/select-create-v4-api-mcp.png" alt=""><figcaption></figcaption></figure>
4. Configure the API. To configure the API, complete the following steps:
   1. **Name**: Enter a name. For example, `My MCP Secure API`
   2. **Version**: Enter a version. For example, `1`.
   3. **(Optional) Description**: Enter a description.
5.  Click **Validate my API details.**<br>

    <figure><img src="../.gitbook/assets/1.png" alt=""><figcaption></figcaption></figure>
6.  Select AI **Gateway**, and then click **Select my API architecture.**

    <figure><img src="../.gitbook/assets/ai-gateway-mcp.png" alt=""><figcaption></figcaption></figure>
7.  Select MCP Proxy, and then click **Select my entrypoints.**

    <figure><img src="../.gitbook/assets/select-my-entrypoint-mcp.png" alt=""><figcaption></figcaption></figure>
8.  Enter the `context-path` . For example: `/my-mcp-secure-api` , and then click **Validate my entrypoints.**<br>

    <figure><img src="../.gitbook/assets/2.png" alt=""><figcaption></figcaption></figure>
9.  Enter your MCP server URL in the **MCP Server Backend URL field**. For example: [`http://localhost:3001/mcp`](http://localhost:3001/mcp) , and then click **Validate my endpoints.**<br>

    <figure><img src="../.gitbook/assets/environment-mcp-server-url.png" alt=""><figcaption></figcaption></figure>
10. Click **Validate my plans.**

    <figure><img src="../.gitbook/assets/validate-my-plans-keyless.png" alt=""><figcaption></figcaption></figure>
11. Click **Save & Deploy API**.

    <figure><img src="../.gitbook/assets/save-and-deploy-api-mcp.png" alt=""><figcaption></figcaption></figure>

### Verification

The API appears in your API management console with your configuration.<br>

<figure><img src="../.gitbook/assets/3.png" alt="The Configuration page of an MCP API, showing its name, version, and description above a Danger Zone offering start, publish, make public, deprecate, and delete."><figcaption></figcaption></figure>

## Register the MCP Server in AM

1.  From the AM dashboard, click **MCP Servers.**

    <figure><img src="../.gitbook/assets/am-click-mcp-servers.png" alt=""><figcaption></figcaption></figure>
2.  Click the **+ (plus)** icon to create a new MCP server.

    <figure><img src="../.gitbook/assets/plus-icon-mcp-server.png" alt=""><figcaption></figcaption></figure>
3. Configure your MCP server. To configure your MCP server, complete the following steps:
   1. **Name:** Enter a name. For example, `My MCP Server`.
   2. **MCP Resource Identifier:** Enter the APIM API entrypoint URL from [Step 9 above](secure-mcp-proxy-with-oauth2.md#create-the-mcp-proxy-api-in-apim) in [#create-the-mcp-proxy-api-in-apim](secure-mcp-proxy-with-oauth2.md#create-the-mcp-proxy-api-in-apim "mention") section. For example, `https://apim-gateway.example.com/mcp-proxy`.
   3.  (Optional) **Description:** Enter a description.<br>

       <figure><img src="../.gitbook/assets/am-entrypoint-url.png" alt=""><figcaption></figcaption></figure>
   4. **Client ID:** Enter your Client ID
   5. **Client Secret:** Enter your Client secret.
4.  Click **Create.**

    <figure><img src="../.gitbook/assets/agent-mesh-secure-mcp-proxy-with-oa-160.png" alt=""><figcaption></figcaption></figure>
5. In the **copy your client secret** pop-up box, copy the **Client Secret** and store the credentials securely.

{% hint style="danger" %}
The Client Secret is displayed only once. Copy and store it securely before closing the pop-up box.
{% endhint %}

<figure><img src="../.gitbook/assets/agent-mesh-secure-mcp-proxy-with-oa-161.png" alt=""><figcaption></figcaption></figure>

## Enable Dynamic Client Registration in AM

Dynamic Client Registration (DCR) allows MCP clients to automatically register with AM without manual configuration.

{% hint style="info" %}
If DCR isn't enabled, you must create the client manually on both sides, using the same Client ID:

* **In AM:** Create an Application for the MCP client and configure its redirect URLs. Configure the MCP client with this Application's Client ID and Client Secret. For more information, see [Applications](https://documentation.gravitee.io/am/guides/applications).
* **In APIM:** Create an Application that uses the same Client ID, then subscribe it to the OAuth2 plan on your MCP proxy API. The Gateway matches the Client ID in each access token to an active subscription on the plan. If no matching subscription exists, the Gateway rejects the request with `401 Unauthorized`.
{% endhint %}

To enable DCR, complete the following steps:

1.  In the AM Console, navigate to Settings.

    <figure><img src="../.gitbook/assets/am-dcr-settings.png" alt="The General settings of a security domain in Access Management, with Settings highlighted in the left navigation, showing the domain enabled, its name, and empty post-logout redirect and request URI lists."><figcaption></figcaption></figure>
2.  Click **Client Registration**.

    <figure><img src="../.gitbook/assets/client-registration.png" alt="The Client Registration Settings page, with Client Registration highlighted under OpenID in the settings menu and dynamic client registration, open registration, templates, localhost redirects, and unsecured redirects all enabled."><figcaption></figcaption></figure>
3.  Turn on the **Enable Dynamic Client Registration** toggle.

    <figure><img src="../.gitbook/assets/enable-dynamic-client-registration.png" alt="The Client Registration Settings page in Access Management, with dynamic client registration, open registration, templates, localhost redirects, and unsecured redirects all enabled."><figcaption></figcaption></figure>
4. Configure the settings. To configure settings, complete the following steps:
   * **Allow localhost redirect URIs:** (Optional) Enable for local development and testing.
   *   **Allow custom redirect URIs:** (Optional) Enable for production clients with custom redirect configurations.

       <figure><img src="../.gitbook/assets/enable-dynamic-client-registration.png" alt="The Client Registration Settings page in Access Management, with dynamic client registration, open registration, templates, localhost redirects, and unsecured redirects all enabled."><figcaption></figcaption></figure>
5. Click **Save**.

## (Optional) Enable user registration in AM

User registration allows new users to create accounts during authentication.

{% hint style="info" %}
User registration is not required to secure an MCP API with OAuth2. Enable this feature only if you want to allow new users to self-register during authentication. This is useful for demonstration or development environments.
{% endhint %}

Complete the following steps to enable user registration:

1.  In the AM Console, navigate to **Settings**<br>

    <figure><img src="../.gitbook/assets/agent-mesh-secure-mcp-proxy-with-oa-162.png" alt="The General settings of a security domain, with Settings highlighted in the left navigation, showing the domain enabled and master domain switched off."><figcaption></figcaption></figure>
2.  Click **Login**.

    <figure><img src="../.gitbook/assets/click-login-am-settings.png" alt="The security domain settings with Login highlighted in the settings menu, showing user registration, forgot password, and passwordless options all switched off."><figcaption></figcaption></figure>
3.  Turn on the **Enable user registration** toggle.

    <figure><img src="../.gitbook/assets/user-registration-am.png" alt="The Login settings with the User registration toggle switched on above the remaining login and passwordless options."><figcaption></figcaption></figure>
4.  Click **Save**.

    <figure><img src="../.gitbook/assets/click-save-am-registration.png" alt="The Login settings scrolled to the foot, with the Save button highlighted below the passwordless and certificate-based authentication options."><figcaption></figcaption></figure>

## Configure the OAuth2 Plan in APIM

Now that you have configured AM, you need to add an OAuth2 resource in APIM. This resource establishes the connection between APIM and your OAuth2 provider (AM), enabling the Gateway to do the following:

* Verify and secure connections from MCP clients
* Allow the MCP Client to discover the API's security requirements through the WWW-Authenticate header

For more information on protected resource metadata discovery, see the [MCP specification](https://modelcontextprotocol.io/specification/draft/basic/authorization#protected-resource-metadata-discovery-requirements).

1.  In the API Console, navigate to your MCP proxy API.

    <figure><img src="../.gitbook/assets/3.png" alt="The Configuration page of an MCP API, showing its name, version, and description above a Danger Zone offering start, publish, make public, deprecate, and delete."><figcaption></figcaption></figure>
2.  Click **Resources**.<br>

    <figure><img src="../.gitbook/assets/4.png" alt="The Configuration page of an MCP API, with the Resources tab highlighted above an empty API resources table."><figcaption></figcaption></figure>
3.  Click **+ Add Resource**.

    <figure><img src="../.gitbook/assets/add-resource-am.png" alt="The Resources tab of an API&#x27;s Configuration page, empty, with the Add resource button highlighted."><figcaption></figcaption></figure>
4.  In the Add API Resource screen, click **Oauth2**, select **Gravitee.io AM Authorization Server**, and then click **Select**.

    <figure><img src="../.gitbook/assets/gravitee-am-authorisation-server.png" alt="The Add API Resource dialog filtered to OAuth2, with the Gravitee.io AM Authorization Server selected over a generic OAuth2 server and a Keycloak adapter."><figcaption></figcaption></figure>
5.  Configure the resource to establish the connection to your AM instance by providing the following values:

    * **Name:** Enter a name. For example, `AM OAuth2 Resource`
    * **Server URL:** Enter the AM Gateway URL. For example, `https://am-gateway.example.com`
    * **Security Domain:** Enter the AM security domain name.
    * **Client ID:** Enter the Client ID from [Step 3](secure-mcp-proxy-with-oauth2.md#register-the-mcp-server-in-am) in the [#register-the-mcp-server-in-am](secure-mcp-proxy-with-oauth2.md#register-the-mcp-server-in-am "mention") section.
    * **Client Secret:** Enter the Client Secret from [Step 3](secure-mcp-proxy-with-oauth2.md#register-the-mcp-server-in-am) in the [#register-the-mcp-server-in-am](secure-mcp-proxy-with-oauth2.md#register-the-mcp-server-in-am "mention")section.

    <figure><img src="../.gitbook/assets/gravitee-am-gateway.png" alt="The Configure Gravitee.io AM Authorization Server resource dialog, with a resource name, a partly masked server URL, the V3_X version, a security domain, a placeholder client ID, a masked secret, and the user claim set to sub."><figcaption></figcaption></figure>
6.  Click **Save**.

    <figure><img src="../.gitbook/assets/click-save-am.png" alt="The same resource dialog scrolled to the foot, with the Save button highlighted below the user claim and security configuration."><figcaption></figcaption></figure>
7.  Click **Consumers** in the API menu.

    <figure><img src="../.gitbook/assets/consumers-master-dev.png" alt="The Consumers page of an API under an out-of-sync banner, with Consumers highlighted in the API menu and one published keyless plan listed."><figcaption></figcaption></figure>
8.  Locate the Keyless plan, and then click the **close icon**.<br>

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p>This operation is irreversible. You cannot reopen a closed plan.</p></div>

    <figure><img src="../.gitbook/assets/close-plan-resource.png" alt="The Plans tab with the Close the plan tooltip shown over the cross icon beside the published keyless plan."><figcaption></figcaption></figure>

*   In the confirmation pop-up box, enter the Keyless plan name, then click **Close this plan**.

    <figure><img src="../.gitbook/assets/confirmation-dialog-close-plan.png" alt="The Close plan dialog, warning that the operation is irreversible and that closing removes free access, with the plan name typed to confirm."><figcaption></figcaption></figure>

9.  Click **+ Add plan.**

    <figure><img src="../.gitbook/assets/consumer-add-new-plan.png" alt="The Plans tab with no plans left published and the Add new plan button highlighted."><figcaption></figcaption></figure>
10. Select **OAuth2**.<br>

    <figure><img src="../.gitbook/assets/select-oauth2.png" alt="The Plans tab with the Add new plan menu open and OAuth2 highlighted among mTLS, JWT, API Key, and Keyless plan types."><figcaption></figcaption></figure>
11. Configure the plan by providing the following values:

    1. **Name**: Enter a name. For example, `OAuth2 Plan`
    2. **(Optional) Description**: Enter a description
    3. Click **Next**.

    <figure><img src="../.gitbook/assets/Oauth2-plan-name.png" alt="The General step of plan creation, with an OAuth2 plan named and empty description and characteristics fields."><figcaption></figcaption></figure>
12. Configure the OAuth2 settings:

    1.  **OAuth2 resource**: Select the AM resource you created in [step 5](secure-mcp-proxy-with-oauth2.md#configure-the-0auth2-plan-in-apim)

        <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>(Required for MCP clients only) Turn on the <strong>Add WWW-Authenticate header</strong> toggle.</p></div>
    2. Click **Next**.

    <figure><img src="../.gitbook/assets/oauth2-authentication-config.png" alt="The OAuth2 authentication configuration step, with the AM resource selected, an empty cache resource, payload extraction and scope checking off, and the WWW-Authenticate header and strict mode both on."><figcaption></figcaption></figure>
13. Click **Create**.

    <figure><img src="../.gitbook/assets/create-am-auth.png" alt="The Restriction step of plan creation, with rate limiting, quota, and resource filtering all switched off and the Create button highlighted."><figcaption></figcaption></figure>
14. Click **Publish the plan**.

    <figure><img src="../.gitbook/assets/publish-the-plan.png" alt="The Plans tab with the STAGING filter selected and the Publish the plan tooltip shown over the upload icon beside the OAuth2 plan."><figcaption></figcaption></figure>
15. Click the **Deploy API** pop-up box.

    <figure><img src="../.gitbook/assets/deploy-api.png" alt="The Consumers page with the out-of-sync banner and its Deploy API button highlighted, showing no plans left in staging."><figcaption></figcaption></figure>

The MCP client uses the OAuth2 server configured in APIM upon connection.

## Verification

Verify your configuration in both the APIM Console and AM Console.

{% tabs %}
{% tab title="APIM Console" %}
**APIM Console**

1.  Navigate to your MCP proxy API.<br>

    <figure><img src="../.gitbook/assets/api-configuration.png" alt="The Configuration page of an API, showing its name and version with empty description, labels, and categories, above a Danger Zone."><figcaption></figcaption></figure>
2.  Click **Consumers**, and then verify the OAuth2 plan is published.

    <figure><img src="../.gitbook/assets/auth2-consumers-publichsed.png" alt="The Plans tab with the PUBLISHED filter selected, listing one published OAuth2 plan with edit, deprecate, and close actions."><figcaption></figcaption></figure>
3.  Click **Deployments** and confirm the latest deployment is successful and in use.

    <figure><img src="../.gitbook/assets/agent-mesh-secure-mcp-proxy-with-oa-163.png" alt="The Deployment History tab of an API, listing three versions by date with the most recent marked in use."><figcaption></figcaption></figure>
{% endtab %}

{% tab title="AM Console" %}
1.  Navigate to your AM domain.<br>

    <figure><img src="../.gitbook/assets/am-domain-mcp-server.png" alt="The Access Management dashboard with MCP Servers highlighted in the left navigation, showing login, sign-up, user, and application counts above a login activity chart."><figcaption></figcaption></figure>
2.  Click **MCP Servers**.

    <figure><img src="../.gitbook/assets/am-domain-mcp-server.png" alt="The Access Management dashboard with MCP Servers highlighted in the left navigation, showing login, sign-up, user, and application counts above a login activity chart."><figcaption></figcaption></figure>
3.  Verify your MCP server resource is configured.<br>

    <figure><img src="../.gitbook/assets/mcp-clients-to-use-am-server.png" alt="The Configure MCP Clients page in Access Management, showing the MCP server resource URI and OAuth client ID both masked, above a Tools panel with a View Tools button."><figcaption></figcaption></figure>
{% endtab %}
{% endtabs %}

### Verify the OAuth2 Protection

Replace `<apim-gateway-url>` with your APIM Gateway URL and `<context-path>` with your configured context path, then run the following command:

<pre class="language-bash"><code class="lang-bash"><strong>curl -i -X GET https://&#x3C;apim-gateway-url>&#x3C;context-path>
</strong></code></pre>

The output shows the expected response:

* HTTP 401 Unauthorized
* `WWW-Authenticate` header present in the response

This confirms the API requires OAuth2 authentication.

## Connect MCP Client

Your MCP proxy API is secured with OAuth2. To connect an MCP client to your secured API:

1. Configure your MCP client with the APIM Gateway URL and context path
2. The client handles OAuth2 authentication automatically through (DCR) Dynamic Client Registration.

For client-specific configuration instructions, refer to your MCP client's documentation. For example, For VSCode MCP, see the [MCP servers in VS code documentation](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) , For Native language SDKs see the [MCP SDK documentation](https://modelcontextprotocol.io/docs/develop/connect-remote-servers)

The MCP client uses the OAuth2 server configured in APIM to authenticate upon connection.
