---
description: Add the new Next-Gen Cloud IP ranges to your firewall rules before Gravitee migrates your environment.
---

# Add Next-Gen Cloud IP ranges to your firewall rules

## Overview

Gravitee is moving Next-Gen Cloud hosted environments behind Cloudflare to strengthen security and protect public access to Gravitee services.

After the change, client traffic to your Gravitee environment reaches Cloudflare first, which securely proxies requests to Gravitee. As a result, the public IP addresses resolved and contacted by your client applications can change.

If your organization restricts network traffic with firewall rules, add the following IP ranges to your firewall rules before Gravitee migrates your environment, and keep them in place after the migration. If your firewall rules don't allow the new IP ranges, your client applications might not reach your Gravitee endpoints.

{% hint style="warning" %}
**Add the new ranges alongside your existing rules, and keep your current entries in place.**

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

The preceding IP ranges are published by Cloudflare. Cloudflare maintains the authoritative list at [cloudflare.com/ips](https://www.cloudflare.com/ips/). If you generate your firewall rules automatically, source the ranges from that list so that you capture any future changes.

## Ports

The following table lists the ports to allow alongside the preceding IP ranges:

| Traffic | Protocol and port |
| ------- | ----------------- |
| Client applications to your Gravitee environment endpoints | HTTPS over TCP 443 |
| Self-hosted hybrid Gateway to Gravitee | Outbound HTTPS over TCP 443 |

{% hint style="info" %}
If you use the Kafka Gateway, its endpoint isn't covered by the preceding incoming IP ranges and uses a different port. Contact Gravitee for the address and port that apply to your environment.
{% endhint %}

## Hybrid Gateway connectivity

If you run self-hosted hybrid Gateways, they connect outbound to the Cloud Gate for your Control Plane region over HTTPS on port 443. For the Cloud Gate URL of your region, see the [Next-Gen Cloud architecture](./#architecture).

Your Gateway always initiates this connection. Gravitee doesn't open connections into your network, so you only need to allow outbound traffic for your hybrid Gateway.
