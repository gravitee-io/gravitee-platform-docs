---
hidden: false
noIndex: true
---

# Create your first API
<!-- GAP-STRUCTURAL: Missing procedural content source -->

This quickstart walks you through creating an API proxy in the Gamma console, deploying it to the API Gateway, and verifying it with a test request. You'll use the simplest configuration — a keyless plan with a single upstream — to get a working proxy in under five minutes.

{% hint style="info" %}
For a complete reference on all creation options, see [Create an API proxy](../build/create-an-api-proxy.md).
{% endhint %}

## Prerequisites

* Access to a running Gamma console instance
* A backend service accessible via HTTP (this guide uses `https://api.gravitee.io/echo` as a sample upstream)

## Step 1: Open the API creation wizard

<figure><img src="https://3745118555-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fa6QVD3iIxTvnV5eQ8OH1%2Fuploads%2Fgit-blob-5b79910b6cf51553e14438b4b1a4eb8c172637a2%2Fgamma-apis-list.png?alt=media" alt="API Proxies list in the Gamma APIM module"><figcaption><p>The API Proxies list. Select <strong>Create New Proxy</strong> (top-right) to open the creation wizard.</p></figcaption></figure>

1. From the Gamma console sidebar, select **API Management**.
2. Navigate to the **APIs** list.
3. Select **Create API**.
4. Choose **Create from scratch** to open the full step-by-step wizard.

{% hint style="info" %}
You can also choose a **template** for common patterns. Templates preconfigure security and upstream settings, reducing the wizard to two steps: **Essentials** and **Review & Deploy**. This guide uses the scratch flow to show every configuration step.
{% endhint %}

## Step 2: Enter API details

The first wizard step (**API Details**) collects the basic identity of your API.

| Field           | Value                             | Notes                                                    |
| --------------- | --------------------------------- | -------------------------------------------------------- |
| **API name**    | `My First API`                    | Required. Identifies the API in the console and Catalog. |
| **Version**     | `1.0`                             | Required. Free-text version label.                       |
| **Description** | `A sample API proxy for testing.` | Optional.                                                |

Select **Next** to proceed.

## Step 3: Configure the proxy entrypoint

The second wizard step (**Configure Proxy**) defines how consumers reach your API and where it forwards requests.

| Field            | Value                          | Notes                                                                                                                                                                    |
| ---------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Context path** | `/my-first-api`                | Required. Must start with `/`, be more than 3 characters, and contain only alphanumeric characters, hyphens, underscores, and forward slashes. No double slashes (`//`). |
| **Target URL**   | `https://api.gravitee.io/echo` | Required. The upstream backend that the API Gateway proxies to.                                                                                                          |

{% hint style="info" %}
For advanced use cases, you can enable **virtual hosts** instead of a context path. Virtual hosts let you route by hostname and path simultaneously. This guide uses the simpler context-path approach.
{% endhint %}

Select **Next** to proceed.

## Step 4: Select a security plan

The third wizard step (**Secure**) attaches a security plan that controls how consumers authenticate.

For this quickstart, select **Keyless**. A keyless plan requires no authentication — any consumer can call the API without credentials. This is the fastest way to verify your proxy works.

{% hint style="warning" %}
Keyless plans are intended for testing and internal use. For production APIs, use an API Key, JWT, OAuth2, or mTLS plan to authenticate consumers. See [Secure your API proxy](../build/secure-your-api-proxy.md).
{% endhint %}

Select **Next** to proceed.

## Step 5: Review and deploy

The final wizard step (**Review & Deploy**) summarizes your configuration.

1. Review the API name, context path, target URL, and plan type.
2. Enable **Deploy immediately** to publish the API proxy to the API Gateway in one step.
3. Select **Create & Deploy**.

The console creates the API proxy, attaches the keyless plan, and deploys the configuration to the API Gateway.

## Step 6: Verify your API proxy

Once the API proxy is deployed, send a test request to confirm it works:

```bash
curl -v https://<your-gateway-host>/my-first-api

```

A successful response returns the echo payload from the upstream, confirming that the API Gateway is proxying requests through your new API.

## Next steps

* **Secure your API** — Replace the keyless plan with an [API Key or JWT plan](../build/secure-your-api-proxy.md) before exposing the API externally.
* **Configure advanced settings** — Add CORS rules, sharding tags, and entrypoint customization. See [Configure your API proxy](../build/configure-your-api-proxy/README.md).
* **Establish consumer access** — Register applications and create subscriptions. See [Establish consumer access](../build/configure-your-api-proxy/establish-consumer-access.md).
* **Expose as an API Tool** — Bridge your API to the AI agent layer by creating an API Tool in the Catalog. See [Create API tools](../../agent-management/import/create-api-tools.md).
