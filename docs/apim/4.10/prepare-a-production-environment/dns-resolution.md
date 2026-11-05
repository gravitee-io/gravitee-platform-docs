---
description: Configure DNS for the Gateway on Kubernetes, and understand the trade-off of the vertx.disableDnsResolver option.
---

# DNS Resolution

## Overview

The Gateway resolves the hostname of a backend each time it opens a new connection to it. This applies to proxied requests and to endpoint health checks. When DNS is slow, requests that need a new connection wait for the answer. A DNS query that gets no answer usually times out after 5 seconds, so slow DNS often appears as requests that take several seconds longer than usual.

On Kubernetes, most DNS delays come from the cluster DNS configuration rather than from the Gateway. The following recommendations reduce the number of DNS queries and make each one faster.

## Recommended configuration on Kubernetes

### Use fully qualified hostnames and lower `ndots`

By default, Kubernetes sets `ndots:5` in the pod DNS configuration. With this setting, any hostname that contains fewer than five dots is first tried with each of the cluster's search domains appended. Even a fully qualified hostname such as `orders.payments.svc.cluster.local` contains only four dots, so a single lookup can produce several queries, and each of them can time out.

To resolve backend hostnames in a single query:

1. Configure endpoint targets with fully qualified hostnames, for example `orders.payments.svc.cluster.local` instead of `orders` or `orders.payments.svc`.
2. Set `ndots` to `2` on the Gateway pods, so that hostnames with two or more dots are tried as absolute names first:

    ```yaml
    dnsConfig:
      options:
        - name: ndots
          value: "2"
    ```

    The Gravitee Helm chart doesn't expose `dnsConfig`. Set it in the Gateway pod specification, at `spec.template.spec.dnsConfig`.

{% hint style="warning" %}
With `ndots:2`, a hostname such as `orders.payments.svc` that relies on a search domain to resolve is tried as an absolute name first. It can take extra queries, or fail to resolve on Alpine-based images when `-Dvertx.disableDnsResolver=true` is set. Replace these hostnames with fully qualified hostnames before you lower `ndots`.
{% endhint %}

### Use a node-local DNS cache

Consider enabling [NodeLocal DNSCache](https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/) on your cluster. It answers DNS queries from a cache on each node, which makes lookups faster and reduces DNS query timeouts.

## The `vertx.disableDnsResolver` option

By default, the Gateway resolves hostnames asynchronously: a request that waits for DNS doesn't delay other requests. In some Kubernetes environments, DNS queries from the default resolver can time out. The JVM option `-Dvertx.disableDnsResolver=true` switches the Gateway to the JVM's built-in resolver, which can avoid some of these timeouts.

You set this option in `JAVA_OPTS`, the Gateway JVM options. With Helm, use the `gateway.env` section of your `values.yaml` file.

{% hint style="danger" %}
With `-Dvertx.disableDnsResolver=true`, a DNS lookup blocks the Gateway thread that performs it until the answer arrives. Each Gateway thread serves many requests, so a slow DNS answer delays **all** requests handled by that thread, not only the request that triggered the lookup. Retries and search-domain queries can accumulate, so a single lookup can delay unrelated requests by several seconds.

The JVM resolver also caches answers for a fixed duration instead of following the time-to-live of each DNS record. After a DNS record changes, the Gateway can keep using the previous address until its cache expires.
{% endhint %}

Before you enable this option, apply the [recommended configuration](dns-resolution.md#recommended-configuration-on-kubernetes), which addresses most DNS timeouts. If you enable it, ensure that DNS is fast and reliable, and monitor the Gateway logs for blocked-thread warnings.

## Diagnose slow DNS

### With `-Dvertx.disableDnsResolver=true`

When a Gateway thread is blocked for more than 2 seconds, the Gateway logs a warning from `BlockedThreadChecker`. Search the Gateway logs for `has been blocked for`. The exact format of the message depends on your APIM version. Consider the following points when you read these warnings:

* Other blocking operations produce the same warning. By default, the warning includes a stack trace when the block lasts longer than 5 seconds. A stack trace that contains `lookupAllHostAddr` confirms that the thread was waiting for DNS.
* Blocks shorter than 2 seconds aren't logged, so the absence of warnings doesn't exclude slow DNS.
* The delay often appears in analytics as endpoint response time rather than as Gateway latency.

### With the default resolver

DNS timeouts make the affected requests fail, usually with a `502 Bad Gateway` response, or with a `504 Gateway Timeout` response if the request timeout expires first. The Gateway doesn't log these failures. Look for them in the API analytics.

### Measure DNS response time

To check how long DNS takes for a backend hostname, run the following command several times from a Gateway pod:

```bash
time nslookup <backend-hostname>
```

Run it several times because a single lookup can be answered from a cache and miss intermittent timeouts. Run it from a Gateway pod because other pods can have a different DNS configuration.
