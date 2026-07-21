---
hidden: false
noIndex: false
---

# Create an API proxy
<!-- GAP-STRUCTURAL: Missing procedural content source -->

An API proxy is the core artifact in API Management. It defines a context path or virtual host that consumers use to reach your API, forwards requests to an upstream backend, and applies security plans and policies at runtime through the API Gateway.

This page covers every option available when creating an API proxy in the Gamma console, including both the from-scratch and template-based wizard flows.

{% hint style="info" %}
For a minimal quickstart, see [Create your first API](../get-started/create-your-first-api.md).
{% endhint %}

## Creation modes

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-1dc3660a72200cd6e49d39c5e84c9cd57f0ea4ac%2Fgamma-wizard-start.png?alt=media" alt="API creation wizard showing scratch and template options"><figcaption><p>The creation wizard offers two paths: <strong>Start from scratch</strong> for full control, or <strong>Quick-start templates</strong> for common patterns.</p></figcaption></figure>

The Gamma console offers two paths for creating an API proxy:

{% tabs %}
{% tab title="From scratch" %}
A four-step wizard that guides you through every configuration option:

1. **API Details** — Name, version, and description
2. **Configure Proxy** — Context path (or virtual hosts) and target URL
3. **Secure** — Security plan selection and configuration
4. **Review & Deploy** — Summary and deployment

Use this mode when you need full control over every field, or when no template matches your use case.
{% endtab %}

{% tab title="From template" %}
A two-step wizard that preconfigures security and upstream settings based on a common pattern:

1. **Essentials** — Name, version, context path, and target URL (combined into one step)
2. **Review & Deploy** — Summary and deployment

Templates preconfigure the security plan type, plan names, and authentication settings. You can override any preconfigured value before deploying.

Use this mode when your API matches a common pattern and you want to skip manual security configuration.
{% endtab %}
{% endtabs %}

## Step 1: API details (scratch mode)

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-87cbe3e3e85275022206c4fbc7fca5f140379342%2Fgamma-wizard-step1.png?alt=media" alt="Wizard Step 1: API Details form"><figcaption><p>The API Details step collects the name, version, and optional description for your API proxy.</p></figcaption></figure>

| Field           | Required | Description                                                                                                   |
| --------------- | -------- | ------------------------------------------------------------------------------------------------------------- |
| **API name**    | Yes      | A human-readable name that identifies this API in the Gamma console and the Catalog.                          |
| **Version**     | Yes      | A free-text version label (e.g., `1.0`, `2.3.1`). Not enforced as semantic versioning.                        |
| **Description** | No       | Optional text describing the API's purpose. Displayed in the console and, if published, the Developer Portal. |

## Step 1: Essentials (template mode)

When using a template, the first step combines identity and proxy configuration into a single form.

| Field            | Required | Description                                                                                                                                                                                                                                                     |
| ---------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API name**     | Yes      | Same as scratch mode.                                                                                                                                                                                                                                           |
| **Version**      | Yes      | Same as scratch mode.                                                                                                                                                                                                                                           |
| **Context path** | Yes      | The path segment appended to the Gateway URL that consumers use to reach this API. Must start with `/`, be more than 3 characters, and contain only letters, digits, hyphens, underscores, periods, and forward slashes. Double slashes (`//`) are not allowed. |
| **Target URL**   | Yes      | The upstream backend URL the API Gateway forwards requests to.                                                                                                                                                                                                  |

The security plan type and its configuration are inherited from the template. You can modify these on the review step before deploying.

## Step 2: Configure the proxy (scratch mode)

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-81712342c6b5848ce4f24b2ffdfbf54617892989%2Fgamma-wizard-step2.png?alt=media" alt="Wizard Step 2: Configure Proxy with context path and target URL"><figcaption><p>The Configure Proxy step defines the gateway path and upstream target URL.</p></figcaption></figure>

### Context path

By default, consumers reach your API through a **context path** — a path segment appended to the Gateway's base URL.

**Validation rules:**

* Must start with `/`
* Must be more than 3 characters
* Allowed characters: `a-z`, `A-Z`, `0-9`, `-`, `_`, `.`, `/`
* Double slashes (`//`) are not permitted

**Example:** A context path of `/orders/v2` makes your API available at `https://<gateway-host>/orders/v2`.

### Virtual hosts

For advanced routing, enable **virtual hosts** to route by both hostname and path.

Each virtual host entry requires:

| Field               | Required | Description                                                         |
| ------------------- | -------- | ------------------------------------------------------------------- |
| **Host**            | Yes      | The hostname consumers use (e.g., `api.example.com`).               |
| **Path**            | No       | An optional path prefix under that hostname.                        |
| **Override access** | No       | Whether this virtual host overrides the default Gateway access URL. |

You can configure multiple virtual host entries for a single API proxy.

### Target URL

The **target URL** is the upstream backend that the API Gateway forwards requests to (e.g., `https://backend.internal:8443/api`). This field is required for all API proxies.

## Step 3: Security plan (scratch mode)

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-6eac6d02b66ab6c163eb7cafb2a20695fc4ebe7c%2Fgamma-wizard-step3.png?alt=media" alt="Wizard Step 3: Security plan selection"><figcaption><p>Choose a security plan type. Keyless is selected by default for open access.</p></figcaption></figure>

A security plan defines how consumers authenticate when calling your API. The Gamma console supports five plan types:

{% tabs %}
{% tab title="Keyless" %}
No authentication required. Any consumer can call the API without credentials.

**Configuration:** None — select **Keyless** and proceed.

**Use case:** Internal testing, health checks, public APIs with no consumer tracking.

{% hint style="warning" %}
Keyless plans provide no consumer identification. You cannot track usage per consumer, revoke access, or enforce per-consumer rate limits. Do not use Keyless for production APIs exposed externally.
{% endhint %}
{% endtab %}

{% tab title="API Key" %}
Consumers authenticate by including an API key in the request header or query parameter.

| Field         | Required | Description                                       |
| ------------- | -------- | ------------------------------------------------- |
| **Plan name** | Yes      | A label for this plan (e.g., `Standard API Key`). |

**Use case:** Consumer tracking, rate limiting per key, simple onboarding.
{% endtab %}

{% tab title="JWT" %}
Consumers authenticate by presenting a signed JSON Web Token.

| Field                   | Required | Description                                                          |
| ----------------------- | -------- | -------------------------------------------------------------------- |
| **Plan name**           | Yes      | A label for this plan.                                               |
| **Signature algorithm** | Yes      | The algorithm used to verify JWT signatures.                         |
| **JWKS resolver**       | Yes      | How the Gateway resolves the public keys for signature verification. |
| **Resolver parameter**  | Yes      | The JWKS URL or certificate used by the resolver.                    |

**Use case:** Integration with external identity providers, fine-grained claims-based access control.
{% endtab %}

{% tab title="OAuth2" %}
Consumers authenticate by presenting an OAuth 2.0 access token, validated against an OAuth2 resource.

| Field               | Required | Description                                                                                        |
| ------------------- | -------- | -------------------------------------------------------------------------------------------------- |
| **Plan name**       | Yes      | A label for this plan.                                                                             |
| **OAuth2 resource** | Yes      | The OAuth2 resource configured in the Gamma console that the Gateway uses for token introspection. |

**Use case:** Enterprise SSO, delegated authorization, integration with identity platforms.
{% endtab %}

{% tab title="mTLS" %}
Consumers authenticate by presenting a client TLS certificate during the TLS handshake.

| Field         | Required | Description            |
| ------------- | -------- | ---------------------- |
| **Plan name** | Yes      | A label for this plan. |

**Use case:** Machine-to-machine communication, zero-trust network environments, internal service mesh.
{% endtab %}
{% endtabs %}

{% hint style="info" %}
You can attach multiple plans to a single API proxy. The API Gateway evaluates plans in order and uses the first plan that matches the consumer's credentials.
{% endhint %}

## Step 4: Review and deploy

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-fb0c8b9151b434b859885eb06469349a7d0c2587%2Fgamma-wizard-step4.png?alt=media" alt="Wizard Step 4: Review and deploy summary"><figcaption><p>The Review &#x26; Deploy step shows the full configuration before creation. Enable <strong>Deploy immediately</strong> to publish the API in one step.</p></figcaption></figure>

The final step summarizes your API proxy configuration:

* **API identity** — Name, version, description
* **Proxy settings** — Context path or virtual hosts, target URL
* **Security plan** — Plan type and configuration

### Deploy immediately

Enable **Deploy immediately** to publish the API proxy to the API Gateway as part of creation. The console creates the API definition, attaches the security plan, and pushes the configuration to the Gateway in one step.

When enabled, the button label changes to **Create & Deploy**.

If you leave this option disabled, the API proxy is created in a draft state. You can deploy it later from the API detail page.

## After creation

Once your API proxy is created, the console opens the **Overview** page for that proxy (`API Management` → **API Proxies** → select your API → **General** → **Overview**). This page summarizes setup progress, endpoint details, traffic, and active policies.

### Overview page layout

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-8cbb703ea089ea39a4ba2f088f0d3d6f0642798d%2Fgamma-api-overview.png?alt=media" alt="API proxy overview page with checklist and endpoint summary"><figcaption><p>The Overview page shows setup progress, gateway and upstream endpoints, and a traffic snapshot.</p></figcaption></figure>

The Overview page includes:

* **Checklist** — A guided list of recommended next steps. Each item links to the relevant configuration screen. You can mark items complete to track progress; a completion percentage reflects how many checklist items you have finished.
* **Gateway endpoint** — The URL consumers use to call your API through the Gateway (derived from your context path or virtual hosts).
* **Upstream service** — The target URL the Gateway forwards requests to.
* **Traffic snapshot** — Recent metrics for the proxy: **Requests (24h)**, **Avg Latency**, **Success Rate**, and **Active Consumers**. Select **More details** to open the observability dashboard.
* **Active security policies** — A summary of policies currently enforced on incoming requests (for example, authentication and rate limiting).

### Overview checklist

The checklist helps you finish configuring a new API proxy. Work through the items below in any order; each row includes a shortcut action in the console.

| Checklist item                                        | What it covers                                                                                              | Where to configure                                          |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **Configure backend security on your endpoint group** | Set up SSL/TLS or authentication between the gateway and your upstream service.                              | **Gateway** → **Endpoints** → **Open configuration**        |
| **Apply security policies**                           | Use the Policy Studio to add rate limiting, transformations, or custom security policies to your API flows. | **Design** → **Policy Studio** → **Open Policy Studio**     |
| **Set up alerts**                                     | Get notified when your API exceeds error thresholds or latency spikes.                                      | **Observability** → **Alerts** → **Open Alerts**            |
| **Invite teammates and assign roles**                 | Collaborate on the API — control who can view, edit, deploy, or own the proxy.                              | **Security** → **User Permissions** → **Manage Access**     |

{% hint style="info" %}
The checklist is optional tracking — you can dismiss it when you no longer need the guided list. Consumer access (plans, applications, and subscriptions) is configured separately under **Consumer Access**. See [Establish consumer access](configure-your-api-proxy/establish-consumer-access.md).
{% endhint %}

### Related configuration

After reviewing the Overview checklist, continue with:

* [Configure backend security](configure-your-api-proxy/configure-backend-security.md) — Upstream TLS and backend credentials.
* [Establish consumer access](configure-your-api-proxy/establish-consumer-access.md) — Plans, applications, and subscriptions.
* [Apply security policies](configure-your-api-proxy/apply-security-policies.md) — Policy Studio and request/response policies.
* [Observe](../observe/README.md) — Platform-wide logs and dashboards.
