---
description: >-
  Create an API proxy in the Gamma console with the from-scratch wizard or a
  quick-start template, then review the proxy Overview page.
hidden: false
noIndex: false
---

# Create an API proxy

An API proxy is the core artifact in API Management. It defines a context path or virtual host that consumers use to reach your API, forwards requests to an upstream backend, and applies security plans and policies at runtime through the API Gateway.

This page covers the from-scratch and template-based wizard flows, and every option each one exposes. To build the API proxy from an existing definition file instead, see [Import an API proxy](import-an-api-proxy.md).

{% hint style="info" %}
For a minimal quickstart, see [Create your first API](../get-started/create-your-first-api.md).
{% endhint %}

## Creation modes

<!-- TODO: one screenshot per task — see style-guide/05-formatting-and-document-structure/images-and-figures.md -->

<figure><img src="../../.gitbook/assets/gamma-wizard-start.png" alt="Create API Proxy page showing the Start from scratch, Quick-start templates, and Import API options"><figcaption><p>The <strong>Create API Proxy</strong> page offers three paths: <strong>Start from scratch</strong> for full control, <strong>Quick-start templates</strong> for common patterns, and <strong>Import API</strong> for an existing definition.</p></figcaption></figure>

To open this page, go to **API Proxies** and click **Create New Proxy**. The Gamma console offers the following three paths:

* **Start from scratch**. This path opens the full four-step wizard, with no preset plans.
* **Quick-start templates**. This path opens a shorter wizard with security and plans preset from a template.
* **Import API**. This path creates the API from a Gravitee definition, an OpenAPI specification, or a WSDL document. See [Import an API proxy](import-an-api-proxy.md).

The rest of this page covers the two wizard flows:

{% tabs %}
{% tab title="From scratch" %}
A four-step wizard that guides you through every configuration option:

1. **API Details**. This step collects the name, version, and description.
2. **Configure Proxy**. This step collects the context path (or virtual hosts) and target URL.
3. **Secure**. This step collects the security plan selection and configuration.
4. **Review & Deploy**. This step shows the summary and the deployment option.

Use this mode when you need full control over every field, or when no template matches your use case.
{% endtab %}

{% tab title="From template" %}
A two-step wizard that preconfigures security and upstream settings based on a common pattern:

1. **Essentials**. This step combines identity, proxy configuration, and the plan name into one form.
2. **Review & Deploy**. This step shows the summary and the deployment option.

Templates preconfigure the security plan type, plan names, and authentication settings. You can override any preconfigured value before deploying.

Use this mode when your API matches a common pattern and you want to skip manual security configuration.
{% endtab %}
{% endtabs %}

## Step 1: API details (scratch mode)

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-87cbe3e3e85275022206c4fbc7fca5f140379342%2Fgamma-wizard-step1.png?alt=media" alt="Wizard Step 1: API Details form"><figcaption><p>The API Details step collects the name, version, and optional description for your API proxy.</p></figcaption></figure>

The following table describes the fields on the **API Details** step:

| Field           | Required | Description                                                                                                   |
| --------------- | -------- | ------------------------------------------------------------------------------------------------------------- |
| **API Name**    | Yes      | A human-readable name that identifies this API in the Gamma console and the Catalog.                          |
| **Version**     | Yes      | A free-text version label, for example `1.0` or `2.3.1`. Not enforced as semantic versioning.                 |
| **Description** | No       | Optional text describing the API's purpose, up to 250 characters. Displayed in the console and, if published, the Developer Portal. |

## Step 1: Essentials (template mode)

When you use a template, the first step combines identity, proxy configuration, and the plan name into a single form.

The following table describes the fields on the **Essentials** step:

| Field                          | Required | Description                                                                                                                                                                                                                                                     |
| ------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API Name**                   | Yes      | Same as scratch mode.                                                                                                                                                                                                                                           |
| **Version**                    | Yes      | Same as scratch mode.                                                                                                                                                                                                                                           |
| **Description**                | No       | Same as scratch mode.                                                                                                                                                                                                                                           |
| **Context path**               | Yes      | The path segment appended to the Gateway URL that consumers use to reach this API. Must start with `/`, be more than 3 characters, and contain only letters, digits, hyphens, underscores, periods, and forward slashes. Double slashes (`//`) are not allowed. |
| **Target URL**                 | Yes      | The upstream backend URL the API Gateway forwards requests to.                                                                                                                                                                                                  |
| Plan name                      | Yes      | The name of the plan the template preconfigures. The field label follows the template's plan type, so the API Key template shows **API Key Plan Name**. Consumers see this name when they subscribe.                                                             |

The security plan type is fixed by the template. To change the plan type or its configuration, click **Customize** in the **SECURITY** section of the review step before deploying.

## Step 2: Configure the proxy (scratch mode)

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-81712342c6b5848ce4f24b2ffdfbf54617892989%2Fgamma-wizard-step2.png?alt=media" alt="Wizard Step 2: Configure Proxy with context path and target URL"><figcaption><p>The Configure Proxy step defines the gateway path and upstream target URL.</p></figcaption></figure>

### Context path

By default, consumers reach your API through a **Context path**, which is a path segment appended to the Gateway's base URL.

A context path must meet the following validation rules:

* It must start with `/`.
* It must be more than 3 characters.
* It can contain only the characters `a-z`, `A-Z`, `0-9`, `-`, `_`, `.`, and `/`.
* It must not contain double slashes (`//`).

For example, a context path of `/orders/v2` makes your API available at `https://<gateway-host>/orders/v2`.

### Virtual hosts

For advanced routing, enable the **Virtual hosts** toggle to route by both hostname and path.

The following table describes the fields on each virtual host row:

| Field    | Required | Description                                                                  |
| -------- | -------- | ---------------------------------------------------------------------------- |
| **Host** | Yes      | The hostname consumers use, for example `api.example.com`.                   |
| **Path** | No       | An optional path prefix under that hostname.                                 |

Click **Add virtual host** to configure multiple virtual host entries for a single API proxy.

{% hint style="info" %}
The wizard configures only the host and path. To set a portal access URL override for a virtual host, open the proxy after creation and go to the **Entrypoints** page in the **GATEWAY** section, where each virtual host row also has an **Override access** field.
{% endhint %}

### Target URL

The **Target URL** is the upstream backend that the API Gateway forwards requests to, for example `https://backend.internal:8443/api`. This field is required for all API proxies.

## Step 3: Security plan (scratch mode)

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-6eac6d02b66ab6c163eb7cafb2a20695fc4ebe7c%2Fgamma-wizard-step3.png?alt=media" alt="Wizard Step 3: Security plan selection"><figcaption><p>Choose a security plan type. Keyless (Open) is selected by default for open access.</p></figcaption></figure>

A security plan defines how consumers authenticate when calling your API. The Gamma console supports five plan types:

{% tabs %}
{% tab title="Keyless (Open)" %}
No authentication required. Any consumer can call the API without credentials. This is the default selection.

**Configuration:** None. Select **Keyless (Open)** and proceed.

**Use case:** Internal testing, health checks, public APIs with no consumer tracking.

{% hint style="warning" %}
Keyless plans provide no consumer identification. You cannot track usage per consumer, revoke access, or enforce per-consumer rate limits. Do not use a Keyless plan for production APIs exposed externally.
{% endhint %}
{% endtab %}

{% tab title="API Key" %}
Consumers authenticate by including an API key in the request header or query parameter.

The following table describes the fields for an API Key plan:

| Field                  | Required | Description                                                       |
| ---------------------- | -------- | ----------------------------------------------------------------- |
| **API Key Plan Name**  | Yes      | The name consumers see when they subscribe to the plan.           |

**Use case:** Consumer tracking, rate limiting per key, simple onboarding.
{% endtab %}

{% tab title="JWT" %}
Consumers authenticate by presenting a signed JSON Web Token.

The following table describes the fields for a JWT plan:

| Field              | Required | Description                                                                                                                                                                                    |
| ------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **JWT Plan Name**  | Yes      | The name consumers see when they subscribe to the plan.                                                                                                                                        |
| **Signature**      | Yes      | The algorithm used to verify JWT signatures. Defaults to **RS256 (RSA + SHA-256)**.                                                                                                            |
| **JWKS Resolver**  | Yes      | How the Gateway resolves the public keys for signature verification. Choose **JWKS URL**, **Given key (PEM, single key)**, or **Gateway keys (configured globally)**.                           |
| Resolver value     | Yes      | The value the resolver needs. The field label follows your resolver choice, so it reads **JWKS URL**, **Public key**, or **Resolver parameter**. This field supports Expression Language.       |

**Use case:** Integration with external identity providers, fine-grained claims-based access control.
{% endtab %}

{% tab title="OAuth 2.0" %}
Consumers authenticate by presenting an OAuth 2.0 access token.

The following table describes the fields for an OAuth 2.0 plan:

| Field                  | Required | Description                                                                                                                                       |
| ---------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **OAuth2 Plan Name**   | Yes      | The name consumers see when they subscribe to the plan.                                                                                           |
| **OAuth2 Provider**    | Yes      | The provider type, for example **Auth0**. The wizard creates a resource of this type on the API and uses it to validate OAuth 2.0 tokens.          |
| Provider settings      | Yes      | The connection details the selected provider requires, for example **Auth0 Domain** and **Audience**. An optional **User claim** field identifies the end user in analytics logs and defaults to `sub`. |

**Use case:** Enterprise SSO, delegated authorization, integration with identity platforms.
{% endtab %}

{% tab title="mTLS" %}
Consumers authenticate by presenting a client TLS certificate during the TLS handshake.

The following table describes the fields for an mTLS plan:

| Field                | Required | Description                                              |
| -------------------- | -------- | -------------------------------------------------------- |
| **mTLS Plan Name**   | Yes      | The name consumers see when they subscribe to the plan.  |

**Use case:** Machine-to-machine communication, zero-trust network environments, internal service mesh.
{% endtab %}
{% endtabs %}

{% hint style="info" %}
The wizard creates one plan. After creation, you can add more plans to the same API proxy from the **Plans** page in the **CONSUMER ACCESS** section, and use **Reorder** to set their order. The API Gateway evaluates plans in that order and uses the first plan that matches the consumer's credentials.
{% endhint %}

## Step 4: Review and deploy

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-fb0c8b9151b434b859885eb06469349a7d0c2587%2Fgamma-wizard-step4.png?alt=media" alt="Wizard Step 4: Review and deploy summary"><figcaption><p>The Review &#x26; Deploy step shows the full configuration before creation. The <strong>Deploy and start API immediately</strong> toggle publishes the API as part of creation.</p></figcaption></figure>

The final step summarizes your API proxy configuration in the following three sections, each with its own **Edit** action:

* **API DETAILS**. This section shows the name, version, and protocol.
* **PROXY CONFIGURATION**. This section shows the gateway path and the upstream URL.
* **SECURITY**. This section shows the auth type and plan name.

### Deploy and start API immediately

The **Deploy and start API immediately** toggle publishes the API proxy to the API Gateway as part of creation. The console creates the API definition, attaches the security plan, and pushes the configuration to the Gateway in one step.

This toggle is enabled by default, and the create button reads **Create & Deploy**. If you disable it, the button reads **Create API** and the API proxy is created in a draft state. You can deploy it later from the API detail page.

## After creation

Once your API proxy is created, the console opens the **Overview** page for that proxy. To return to it later, go to **API Proxies**, select your API, and open **Overview** in the **GENERAL** section. This page summarizes setup progress, endpoint details, and traffic.

### Overview page layout

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-8cbb703ea089ea39a4ba2f088f0d3d6f0642798d%2Fgamma-api-overview.png?alt=media" alt="API proxy overview page with checklist and endpoint summary"><figcaption><p>The Overview page shows setup progress, gateway and upstream endpoints, and a traffic snapshot.</p></figcaption></figure>

The Overview page includes the following sections:

* **Checklist**. This is a guided list of recommended next steps. Each item links to the relevant configuration screen. You can mark items complete to track progress, and a completion percentage reflects how many checklist items you have finished.
* **Gateway Endpoint**. This is the URL consumers use to call your API through the Gateway, derived from your context path or virtual hosts.
* **Upstream Service**. This is the target URL the Gateway forwards requests to.
* **Traffic snapshot (last 24 h)**. These are recent metrics for the proxy. The snapshot shows **Total Requests**, **Min Response Time**, **Max Response Time**, **Avg Response Time**, and **Requests / Second**.

### Overview checklist

The checklist helps you finish configuring a new API proxy. Work through the items in any order. Each row includes a shortcut action in the console.

The following table describes the checklist items and where each one is configured:

| Checklist item                                        | What it covers                                                                                              | Where to configure                                                     |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Configure backend security on your endpoint group** | Set up SSL/TLS or authentication between the gateway and your upstream service.                              | The **Endpoints** page in the **GATEWAY** section. Click **Open configuration**. |
| **Apply security policies**                           | Use the Policy Studio to add rate limiting, transformations, or custom security policies to your API flows. | The **Policy Studio** page in the **DESIGN** section. Click **Open Policy Studio**. |
| **Set up alerts**                                     | Get notified when your API exceeds error thresholds or latency spikes.                                      | The **Alerts** page in the **MONITORING** section. Click **Open Alerts**. |
| **Invite teammates and assign roles**                 | Collaborate on the API and control who can view, edit, deploy, or own the proxy.                            | The **User Permissions** page in the **SECURITY** section. Click **Manage Access**. |

{% hint style="info" %}
The checklist is optional tracking. Click **Collapse checklist** when you no longer need the guided list. Consumer access, which covers plans, applications, and subscriptions, is configured separately in the **CONSUMER ACCESS** section. See [Establish consumer access](configure-your-api-proxy/establish-consumer-access.md).
{% endhint %}

### Related configuration

After reviewing the Overview checklist, continue with the following pages:

* [Configure backend security](configure-your-api-proxy/configure-backend-security.md). This page covers upstream TLS and backend credentials.
* [Establish consumer access](configure-your-api-proxy/establish-consumer-access.md). This page covers plans, applications, and subscriptions.
* [Apply security policies](configure-your-api-proxy/apply-security-policies.md). This page covers the Policy Studio and request/response policies.
* [Observe](../observe/README.md). This page covers platform-wide logs and dashboards.
