---
description: Add the new Classic Cloud IP ranges to your firewall rules before Gravitee migrates your environment.
---

# Add Classic Cloud IP ranges to your firewall rules

## Overview

Gravitee is migrating Classic Cloud hosted environments to a new platform. This migration changes the public IP addresses of your environment for both incoming and outgoing traffic.

If your organization restricts network traffic with firewall rules, add the following IP ranges to your firewall rules before Gravitee migrates your environment, and keep them in place after the migration. If your firewall rules don't allow the new IP ranges, traffic to and from your environment's endpoints is blocked after the migration.

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

## Outgoing IP ranges

Traffic that leaves your environment, for example calls from your Gateways to your backend services, originates from the following IP ranges. Allow these ranges as sources in the firewall rules that protect your backend services.

```text
48.222.129.24/29
2603:1020:203:2d::8/125
```
