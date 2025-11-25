---
description: Configuration guide for v4 Proxy API Entrypoints.
---

# v4 Proxy API Entrypoints

## Configuration

To configure v4 proxy API entrypoints:

1. Select **APIs** from the left nav
2. Select your API
3. Select **Entrypoints** from the inner left nav

Refer to the following sections for step-by-step configuration details per proxy type.

## HTTP proxy APIs

Edit the entrypoint's settings under the **Entrypoints** tab.

<figure><img src="../../../../../../../.gitbook/assets/edit HTTP entrypoint (1).png" alt=""><figcaption><p>v4 HTTP proxy API entrypoint configuration</p></figcaption></figure>

You have the option to:

* Alter existing entrypoints by changing the context path
* Add a new entrypoint by clicking **Add context path** and adding a new context path
* Enable or disable virtual hosts. Enabling virtual hosts requires you to define your virtual host and optionally enable override access.

Redeploy the API for your changes to take effect.

## TCP proxy APIs

Edit the entrypoint's settings under the **Entrypoints** tab.

<figure><img src="../../../../../../../.gitbook/assets/tcp_entrypoints (1).png" alt=""><figcaption><p>v4 TCP proxy API entrypoint configuration</p></figcaption></figure>

You have the option to:

* Alter existing entrypoints by changing the host
* Add a new entrypoint by clicking **Add host** and adding a new host

Redeploy the API for your changes to take effect.
