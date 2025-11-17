# Gateway Resource Sizing Guidelines

## Overview

Resource recommendations for a Gateway instance are based on traffic, the deployment context, and expected usage.

The following matrix defines the most common use cases for an APIM Gateway and considers both the expected global throughput and the number of APIs that will be deployed.

<table><thead><tr><th width="120.87890625">Gateway size</th><th width="123.30078125">Number of APIs</th><th width="122.06640625">Throughput</th><th>Usage</th></tr></thead><tbody><tr><td><strong>Small</strong></td><td>1 - 20</td><td>~200 req/s</td><td>Development, test, or small production environment that is not used intensively but may sometimes encounter peaks in traffic.</td></tr><tr><td><strong>Medium</strong></td><td>20 - 200</td><td>~1000 req/s</td><td>Real production environment that can handle considerable throughput.</td></tr><tr><td><strong>Large</strong></td><td>200+</td><td>5000+ req/s</td><td>Mission-critical environment such as a centralized enterprise gateway that must handle a very high throughput.</td></tr></tbody></table>

## Sizing your Gateway instances

The Gravitee Gateway supports both container-based (cloud) and VM-based deployments.

Based on the [above matrix](gateway-resource-sizing-guidelines.md#overview) summarizing the different use cases, we recommend the minimum resource allocations shown in the tables below.

{% hint style="warning" %}
These are informative estimates only and you should adjust allocations as needed.
{% endhint %}

### Cloud-based deployments

| Gateway size | CPU            | System memory | Gateway memory |
| ------------ | -------------- | ------------- | -------------- |
| **Small**    | 500 millicore  | 512m          | 128m           |
| **Medium**   | 750 millicore  | 768m          | 256m           |
| **Large**    | 1000 millicore | 1024m         | 512m           |

For a cloud-based architecture such as Kubernetes, adapt the CPU and memory of your pods depending on your requirements. For low latency, consider increasing CPU limits. For optimized payload transformation, consider increasing memory.

Container-based deployments are characterized by resource constraints, so instead of increasing your resources, we recommend adjusting your minimum and maximum number of replicas.

### VM-based deployments

| Gateway size | CPU     | System memory | Gateway memoy | Disk space |
| ------------ | ------- | ------------- | ------------- | ---------- |
| **Small**    | 1 core  | 1024m         | 256m          | 20 GB      |
| **Medium**   | 2 cores | 1536m         | 512m          | 20 GB      |
| **Large**    | 4 cores | 2048m         | 1024m         | 20 GB      |

VM-based deployments are resource intensive and require more memory and CPU than container-based deployments.

## High availability

At least 2 Gateway instances are required to ensure your platform will experience 0 downtime in the event of critical issues or during rolling updates. In practice, you should set up the number of Gateway instances your platform requires to satisfy your performance criteria, plus one more. Then, if one instance is compromised, the remaining instances are able to handle all traffic until the failing instance recovers.

For more information on high availability best practices, see [High availability recommendations](production-sizing-guidelines.md#production-best-practices).

## Performance considerations

To optimize the performance and cost-effectiveness of your APIM Gateway, consider the following factors when sizing your infrastructure:&#x20;

<details>

<summary>The number of deployed APIs</summary>

Deployed APIs are maintained in memory. Increasing the number of deployed APIs consumes more memory.

</details>

<details>

<summary>The number of plugins on an API</summary>

The more plugins you add to your APIs, the more demand you place on your Gateway, which could negatively impact latency. Some plugins, such as `generate-http-signature`, are particularly CPU intensive. Others, when badly configured or handling large payloads, can require excessive memory or CPU.&#x20;

</details>

<details>

<summary>Payload size</summary>

The Gateway is optimized to minimize memory consumption when serving requests and responses, so payload data is only loaded to memory when necessary. Some plugins, such as `json-xml`, `xslt`, `cache`, require that the entire payload is loaded into memory. When using these plugins, you must adjust the available memory allocated to the Gateway. We recommend using an initial value of `Maximum payload size x Maximum throughput`, which you can refine as needed.

</details>

<details>

<summary>Analytics and logging</summary>

Gravitee offers multiple methods to export analytics using [reporters](../gravitee-gateway/reporters/README.md). Depending on throughput and the level of precision used for logging, you may need to increase the memory or disk space of your Gateway and choose the reporter best suited to handle your traffic analytics.

</details>

<details>

<summary>Rate limit and quota</summary>

Rate limit, quota, and spike arrest are patterns that are commonly applied to control API consumption. By default, Gravitee applies rate limiting in strict mode, where defined quotas are strictly respected across all load-balanced Gateways. For high throughput, we recommend using Redis, but keep in mind that some amount of CPU is required to call Redis for each API request where rate limiting is enabled.

</details>

<details>

<summary>Cryptographic operations</summary>

TLS, JWT encryption/decryption, and signature verifications can be CPU intensive. If you plan to handle high throughput that involves many costly operations, such as JWT signature, HTTP signature, or SSL, you may need to increase your CPU to keep the Gateway's latency as low as possible.

</details>
