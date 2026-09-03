---
hidden: false
noIndex: false
description: Read the rolling 24-hour activity snapshot on the Overview page of an LLM Proxy or MCP Proxy. Learn what each stat card and chart reports.
---

# Monitor proxy activity on the Overview page

Every LLM Proxy and MCP Proxy carries an activity snapshot on its own **Overview** page, so you can judge whether a proxy is healthy without leaving it. The snapshot covers a rolling 24 hours, ending at the moment you load the page.

This is a different surface from the dashboards. The **LLM — Overview** dashboard reports across every LLM Proxy in the environment over a time range you choose. See [Monitor your LLM proxy](monitor-your-llm-proxy.md) for that. The **Overview** page of a proxy reports on that one proxy over a fixed 24 hours.

## What each proxy type reports

The three proxy types don't carry the same snapshot:

| Proxy type | Stat cards on the Overview page |
| --- | --- |
| **LLM Proxy** | Requests, cost, error rate, and P95 latency, plus three charts |
| **MCP Proxy** | Requests, error rate, and P95 latency. There's no cost card, because the gateway records token cost for LLM traffic only |
| **A2A Proxy** | None. The Overview page carries the proxy's general details and its connection, and no activity snapshot |

## Open the Overview page

To open the snapshot for an LLM Proxy, follow these steps:

1. Click **LLM Proxies** in the module sidebar.
2. Select your proxy.
3. Click **Overview** in the proxy sidebar.

For an MCP Proxy, click **MCP Proxies** in step 1 instead.

<!-- TODO: Screenshot of the Overview page of an LLM Proxy showing the four stat cards -->

<figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-aim-proxy-overview-stats.png" alt=""><figcaption><p>The Overview page of an LLM Proxy</p></figcaption></figure>

## Read the stat cards

Each card is labeled with the window it covers, so **Requests (24h)** is the request count for the last 24 hours and not a lifetime total.

| Card | Reports |
| --- | --- |
| **Requests (24h)** | Requests the gateway served for this proxy. |
| **Cost (24h)** | Token cost the gateway computed for this proxy. LLM Proxies only. |
| **Error rate (24h)** | Share of those requests that returned an error, as a percentage to two decimal places. |
| **P95 latency (24h)** | 95th percentile gateway response time, in milliseconds. |

**Cost (24h)** is always formatted as US dollars. A model priced in another currency still reports with a dollar sign on this card, so read the figure as the number rather than the currency.

## Read the LLM Proxy charts

Below the stat cards, an LLM Proxy carries three charts and a provider list:

| Card | Reports |
| --- | --- |
| **Requests by type — last 24 hours** | Request volume broken down by request type. |
| **Cost over time — last 24 hours** | Token cost over the window. |
| **Cost by request type** | How the cost divides across request types. |
| **Providers** | The providers this proxy routes to, with the URL each one resolves to. |

## What a zero means

A proxy that served no traffic in the window reports zeros, not blanks. Every card fills in, so `0` requests and `0.00%` error rate are the normal reading for an idle proxy.

A zero doesn't only mean no traffic. When the analytics query behind the cards fails, the snapshot falls back to the same zeros rather than reporting the failure. A broken analytics backend and an idle proxy read identically here. Confirm against the **LLM — Overview** dashboard or the proxy's **Logs** before you conclude that a proxy is idle.

The cards show an em dash only while the figures are still loading, or when the request for them didn't complete.
