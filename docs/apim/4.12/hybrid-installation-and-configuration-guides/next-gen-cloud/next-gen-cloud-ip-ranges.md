---
description: Add the new Next-Gen Cloud IP ranges to your firewall rules before Gravitee migrates your environment.
---

# Add Next-Gen Cloud IP ranges to your firewall rules

## Overview

Gravitee is moving Next-Gen Cloud hosted environments behind Cloudflare to strengthen security and protect public access to Gravitee services.

After the change, client traffic to your Gravitee environment will reach Cloudflare first, which securely proxies requests to Gravitee. As a result, the public IP addresses resolved and contacted by your client applications may change.

If your organization restricts network traffic with firewall rules, add the following IP ranges to your firewall rules before Gravitee migrates your environment, and keep them in place after the migration. If your firewall rules don't allow the new IP ranges, this might block access to Gravitee endpoints from your side.

{% hint style="warning" %}
**Add the new ranges alongside your existing rules. Do not replace your current entries.**

Keep the IP addresses that your firewall rules already allow for your Gravitee environment. Both your current addresses and the new ranges are needed until your environment has migrated. After Gravitee confirms that your migration is complete, you can remove the entries you no longer need.
{% endhint %}

{% hint style="info" %}
Gravitee contacts hosted customers before their environments are migrated.
{% endhint %}

## Incoming IP ranges

Your environment receives incoming traffic on the following IP ranges. If your network restricts the destinations that your client applications reach, allow these ranges as destinations.

```text
103.21.244.0/22
103.22.200.0/22
103.31.4.0/22
104.16.0.0/13
104.24.0.0/14
108.162.192.0/18
131.0.72.0/22
141.101.64.0/18
162.158.0.0/15
172.64.0.0/13
173.245.48.0/20
188.114.96.0/20
190.93.240.0/20
197.234.240.0/22
198.41.128.0/17
2400:cb00::/32
2405:8100::/32
2405:b500::/32
2606:4700::/32
2803:f800::/32
2a06:98c0::/29
2c0f:f248::/32
```

These are Cloudflare's published IP ranges. Cloudflare maintains the authoritative list at [cloudflare.com/ips](https://www.cloudflare.com/ips/). If you generate your firewall rules automatically, source the ranges from there so that you pick up any future changes to the list.

## Ports

Allow the following ports alongside the IP ranges above.

| Traffic | Protocol and port |
| ------- | ----------------- |
| Client applications to your Gravitee environment endpoints | TCP 443 (HTTPS) |
| Self-hosted hybrid Gateway to Gravitee | TCP 443 (HTTPS), outbound |

{% hint style="info" %}
If you use the Kafka Gateway, its endpoint is not covered by the incoming IP ranges above and uses a different port. Contact Gravitee for the address and port that apply to your environment.
{% endhint %}

## Hybrid Gateway connectivity

If you run self-hosted hybrid Gateways, they connect outbound to the Cloud Gate for your Control Plane region over HTTPS on port 443. For the Cloud Gate URL for each region, see the Next-Gen Cloud hybrid installation guide.

Your Gateway always initiates this connection. Gravitee does not open connections into your network, so you do not need to open any inbound ports for your hybrid Gateway.
