---
description: >-
  Change the context paths of an API proxy, or switch to virtual hosts, from
  the Entrypoints page.
hidden: false
noIndex: false
---

# Configure entrypoints

The **Entrypoints** page configures how consumers reach this API through the gateway. The API listens either on one or more context paths under the shared gateway host, or on virtual hosts, where each row maps a host to a path.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **Entrypoints** in the API proxy sidebar.

Editing entrypoints requires both the `api-definition-u` and `api-gateway_definition-u` permissions. When the API proxy is managed by the Kubernetes operator, the page is read-only.

<!-- TODO: Screenshot of the Entrypoints page in context-path mode -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-entrypoints-page.png" alt=""><figcaption><p>The Entrypoints page</p></figcaption></figure>

## Manage context paths

The **Entrypoint context-paths** card defines the URL prefixes consumers use to reach this API through the gateway. Each row is served under the shared gateway host.

* Add a row with **Add context path**. Add more than one path when the API is exposed under several routes.
* Each **Context path** starts with `/`. An empty path shows **Path is required.**, and a path without a leading slash shows **Path must start with /.**
* Delete a row with its delete button. The last remaining row can't be deleted.
* Click **Save changes** to apply, or **Discard** to revert. A successful save shows **Configuration successfully saved!**

## Switch to virtual hosts

Turn on the **Enable virtual hosts** switch to map hosts instead of plain context paths. The **Virtual hosts** card carries one row per listener with the following fields:

| Field               | Description                                                        |
| ------------------- | ------------------------------------------------------------------ |
| **Virtual host**    | Host that must be set in the HTTP request to access this entrypoint. |
| **Context path**    | Path segment appended to the virtual host for this listener.       |
| **Override access** | Portal access URL override for this virtual host.                  |

Turning the switch off again opens the **Switch to context-path mode** dialog, which warns that all virtual-host configuration is lost while the paths you entered are preserved.

## Preview the exposed entrypoints

The **Exposed entrypoints** card previews the gateway URLs derived from your context paths or virtual hosts. These are the same values consumers see in the Developer Portal. When nothing is configured, the card reads **No exposed entrypoints available.**

## Verification

To verify an entrypoint is working as expected, follow these steps:

1. Add a context path and click **Save changes**.
2. Deploy the API.
3. Call the URL shown in the **Exposed entrypoints** card. The gateway routes the request to your API.

<!-- TODO: Screenshot of the Exposed entrypoints card with a resolved gateway URL -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-entrypoints-exposed.png" alt=""><figcaption><p>The Exposed entrypoints card</p></figcaption></figure>
