---
hidden: false
noIndex: false
description: Cut off traffic to an LLM Proxy, MCP Proxy, or A2A Proxy at the gateway, and restore it later. Follow the steps to stop and restart a proxy from its Settings page.
---

# Stop and restart proxy traffic

Stopping a proxy cuts off the traffic it carries. The gateway stops accepting requests for that proxy, and the subscriptions consumers already hold are preserved, so a stop is reversible.

The control works the same way for an LLM Proxy, an MCP Proxy, and an A2A Proxy.

## Open the Settings page

Each proxy carries its runtime controls on its own Settings page. To open the page, follow these steps:

1. Click the list of proxies in the module sidebar: **LLM Proxies**, **MCP Proxies**, or **A2A Proxies**.
2. Select the proxy you want to control.
3. Click the settings entry in the proxy sidebar. The entry is named **General** for an LLM Proxy and an A2A Proxy, and **Settings** for an MCP Proxy.

The page itself is titled **Settings** for all three proxy types.

<!-- TODO: Screenshot of the Settings page of an LLM Proxy showing the Details panel and the API Events card -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-proxy-settings-page.png" alt=""><figcaption><p>The Settings page of a proxy</p></figcaption></figure>

## Check the current state

The **Details** panel on the right of the page is read-only. It lists **Owner**, **Created**, **Updated**, **Visibility**, **Lifecycle**, and **Status**.

The **Status** row carries the runtime state of the proxy, and reads either **Started** or **Stopped**.

## Stop a proxy

The **API Events** card holds the runtime actions. To stop the proxy, follow these steps:

1. Scroll to the **API Events** card.
2. Click the stop action. The button names the type of proxy you opened, so it reads **Stop LLM proxy**, **Stop MCP proxy**, or **Stop A2A proxy**.

The button reads **Stopping…** while the request is in flight. When the request completes, the **Status** row of the **Details** panel reads **Stopped**.

The card states the effect of the action: **Gateway stops accepting requests. Subscriptions are preserved.**

{% hint style="warning" %}
The stop action has no confirmation dialog. The proxy stops as soon as you click, and the change reaches the gateway without a separate deployment.
{% endhint %}

<!-- TODO: Screenshot of the API Events card of a started proxy, showing the Stop action -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-api-events-stop.png" alt=""><figcaption><p>The API Events card of a started proxy</p></figcaption></figure>

## Restart a proxy

A stopped proxy is restarted from the same card. To restart it, follow these steps:

1. Scroll to the **API Events** card.
2. Click the start action. The button reads **Start LLM proxy**, **Start MCP proxy**, or **Start A2A proxy**.

The button reads **Starting…** while the request is in flight. When the request completes, the **Status** row reads **Started**. The card describes the effect as **Gateway starts accepting requests for this proxy.**

## What a stop leaves in place

Stopping changes the runtime state of the proxy. The following are left in place:

* **Subscriptions**. Consumers keep the subscriptions they hold.
* **Plans and policies**. The configuration of the proxy is untouched.
* **The proxy itself**. A stop isn't a delete.

While a proxy is started, the delete action in the **API Events** card is unavailable and the card reads **A running or published proxy cannot be deleted.** Stop the proxy first if you intend to delete it.

## Review a stop or a start

Every stop and start is recorded in the audit log of the proxy, under the event `API_UPDATED`. To review it, follow these steps:

1. Click **Audit Logs** in the proxy sidebar. The entry sits in the **Monitoring** group.
2. Open the **Event** filter and select `API_UPDATED`.

The table lists **Date**, **Actor**, **Event**, and **Target** for each entry.

## Manage a single consumer instead

Stopping a proxy affects every consumer of that proxy at once. To act on a single consumer instead, manage that consumer's subscription. See [Manage subscriptions](../publish/manage-subscriptions.md).
