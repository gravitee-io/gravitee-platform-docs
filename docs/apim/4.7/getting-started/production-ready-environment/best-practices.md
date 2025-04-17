# Best Practices

## Overview

High-level best practices and sizing recommendations for a production deployment of Gravitee API Management (APIM) are discussed in the sections below.

{% hint style="info" %}
For more detailed guidance specific to your deployment, [book a demo](https://www.gravitee.io/demo) with our solutions engineering team.
{% endhint %}

## Production best practices <a href="#production-best-practices" id="production-best-practices"></a>

High availability focuses on increasing resilience and uptime. Reduction of both scheduled and unscheduled downtime relies on the implementation of 3 principles:

* Eliminate single points of failure (SPOF)
* Reliable crossover
* Detect failures as they occur

{% tabs %}
{% tab title="Eliminate SPOF" %}
One critical aspect of ensuring system reliability is the elimination of single points of failure (SPOFs). A single point of failure refers to any component within a system that, if it fails, will cause the entire system to fail. To mitigate this risk, redundancy is introduced, allowing for continued operation even if one component fails.

In the context of APIM, redundancy is achieved by deploying multiple instances of the APIM Gateway and optionally, Alert Engine.  These instances are configured to operate in either Active/Active or Active/Passive mode, depending on the specific requirements and configurations of the system.

#### **Active/Active Mode**

In Active/Active mode, both instances of the component are actively processing requests or performing their respective functions simultaneously. This setup distributes the workload across multiple instances, thereby reducing the risk of overload on any single component. In the event of a failure in one instance, the remaining instance(s) continue to operate without interruption, ensuring continuous service availability.

#### **Active/Passive Mode**

Alternatively, Active/Passive mode involves designating one instance as active while the other remains in standby mode, ready to take over operations if the active instance fails. In this setup, the passive instance remains idle until it is needed, thereby conserving resources. Automatic failover mechanisms are employed to detect failures in the active instance and seamlessly transition operations to the passive instance without causing service disruptions.

<figure><img src="../../.gitbook/assets/deployments and capacity.png" alt=""><figcaption><p>Load balancer</p></figcaption></figure>

{% hint style="info" %}
**VM installation**

When installing on bare metal, e.g., VMs, use dedicated VMs for the Gateways and Alert Engine instances.
{% endhint %}
{% endtab %}

{% tab title="Reliable crossover" %}
To ensure seamless and reliable traffic distribution to the Gravitee API Gateways, it is essential to implement a robust load-balancing solution (e.g., Nginx, HAproxy, F5, Traefik, Squid, Kemp, LinuxHA, etc.). By placing a reliable load balancer in front of the gateways, incoming requests can be efficiently distributed across multiple gateway instances, thereby optimizing performance and enhancing system reliability.

#### **Health Checks**

Incorporating active or passive health checks into the load balancer configuration is essential for maintaining the reliability of the crossover setup. Health checks monitor the status and availability of backend gateway instances, enabling the load balancer to make informed routing decisions and dynamically adjust traffic distribution based on the health and performance of each instance.

* **Active Health Checks**: Active health checks involve sending periodic probes or requests to the backend instances to assess their health and responsiveness. If an instance fails to respond within a specified timeout period or returns an error status, it is marked as unhealthy, and traffic is diverted away from it until it recovers.
* **Passive Health Checks**: Passive health checks rely on monitoring the actual traffic and responses from the backend instances. The load balancer analyzes the responses received from each instance and detects anomalies or errors indicative of a failure. Passive health checks are typically less intrusive than active checks but may have slightly longer detection times.

There are some key differences to note between active and passive health checks as noted in the table below:

|                         | Active health checks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Passive health checks (circuit breakers)                                               |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Re-enable a backend** | Automatically re-enables a backend in the backend group as soon as it is healthy                                                                                                                                                                                                                                                                                                                                                                                                                           | Cannot automatically re-enable a backend in the backend group as soon as it is healthy |
| **Additional traffic**  | Produces additional traffic to the target                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Does not produce additional traffic to the target                                      |
| **Probe endpoint**      | Requires a known URL with a reliable status response in the backend to be configured as a request endpoint (e.g.,"/"). By providing a custom probe endpoint for an active health checker, a backend can determine its health metrics and produce a status code to be consumed by Gravitee. Even though a target continues to serve traffic which looks healthy to the passive health checker, it can respond to the active probe with a failure status, essentially requesting to stop taking new traffic. | Does not require configuration                                                         |
{% endtab %}

{% tab title="Detect failures" %}
Monitoring the health and performance of Gravitee APIM Gateways and Management API is crucial for ensuring optimal operation and identifying potential issues before they impact users. By actively monitoring various metrics and endpoints, administrators can proactively address any anomalies and maintain the reliability of the API infrastructure.

**Gateway Internal API Endpoints**

The[ Gateway internal API](../../gravitee-gateway/gateway-internal-api.md) and [Management API Internal API](../../management-api/mapi-internal-api.md) provide a set of RESTful endpoints that enable administrators to retrieve vital information about the node status, configuration, health, and monitoring data.

**Mock Policy for Active Health Checks**

Utilizing an API with a [Mock policy](broken-reference) enables administrators to perform active health checks on the Gravitee APIM Gateways. By configuring mock endpoints that simulate various scenarios, such as successful requests, timeouts, or errors, administrators can verify the gateway's responsiveness and behavior under different conditions.

**Prometheus Metrics**

[Integration with Prometheus](../../gravitee-gateway/logging.md#expose-metrics-to-prometheus) allows administrators to expose and collect metrics related to Gravitee APIM Gateways, including Vert.x 4 metrics. By accessing the `/_node/metrics/prometheus` endpoint on the internal API, administrators can retrieve detailed metrics with customizable labels, enabling them to monitor system performance and identify trends over time.

**OpenTracing with Jaeger**

Enabling OpenTracing with Jaeger facilitates comprehensive tracing of every request that passes through the API Gateway. This tracing capability offers deep insights into the execution path of API policies, enabling administrators to debug issues, analyze performance bottlenecks, and optimize API workflows effectively.
{% endtab %}
{% endtabs %}

## Capacity planning overview <a href="#capacity-planning" id="capacity-planning"></a>

Effective capacity planning relies on the specifics and optimization of the following 3 components:

* Storage
* Memory
* CPU

{% tabs %}
{% tab title="Storage" %}
Storage concerns reside at the analytics database level and depend on:

* Architecture requirements (redundancy, backups)
* API configurations (i.e., are advanced logs activated on requests and responses payloads)
* API rate (RPS: Requests Per Second)
* API payload sizes

To avoid generating excessive data and reducing Gateway capacity, refrain from [activating the advanced logs](../../gravitee-gateway/logging.md#modify-logging-information) on all API requests and responses.

For example, if you have activated the advanced logs on requests and responses with an average (requests + responses) payload size of 10kB and at 10 RPS, then retaining the logs for 6 months will require 1.5 TB of storage.
{% endtab %}

{% tab title="Memory" %}
Memory consumption tends to increase with the complexity and volume of API requests.&#x20;

APIs employing operations that require loading payloads into memory, such as encryption policies, payload transformation policies, and advanced logging functionalities, may require additional memory to accommodate the processing overhead. Similarly, high-throughput environments with a large volume of concurrent requests may necessitate increased memory allocation to ensure optimal performance and prevent resource exhaustion.

Administrators should carefully assess the memory requirements of their Gravitee APIM deployments based on factors such as anticipated API traffic patterns, payload sizes, and the specific policies implemented within each API. Regular monitoring and capacity planning efforts are essential to accurately gauge memory usage trends over time, allowing for proactive adjustments to infrastructure resources to meet evolving workload demands.
{% endtab %}

{% tab title="CPU" %}
The CPU load of Gravitee APIM Gateways is directly proportional to the volume of API traffic they handle.&#x20;

Monitoring CPU load serves as a crucial metric for evaluating the overall load level of the Gateways and determining the need for horizontal scalability. For instance, if the CPU utilization consistently exceeds a predefined threshold, such as 75%, it indicates that the Gateways are operating near or at capacity, potentially leading to performance degradation or service disruptions under high loads.

By regularly monitoring CPU load levels, administrators can assess the current capacity of the Gateways and make informed decisions regarding horizontal scalability. Horizontal scalability involves adding additional Gateway instances to distribute the workload and alleviate resource contention, thereby ensuring optimal performance and responsiveness for API consumers. Scaling horizontally based on CPU load enables organizations to effectively accommodate fluctuating API traffic patterns and maintain service reliability during peak usage periods.
{% endtab %}
{% endtabs %}

## Node sizing recommendations

The following table shows baseline hardware recommendations for a self-hosted deployment.

<table><thead><tr><th width="239">Component</th><th width="156" align="center">vCPU</th><th width="165" align="center">RAM (GB)</th><th align="center">Disk (GB)</th></tr></thead><tbody><tr><td><strong>Dev Portal + REST API</strong> (Dev Portal only)</td><td align="center">1</td><td align="center">2</td><td align="center">20</td></tr><tr><td><strong>Console + REST API</strong> (Console only)</td><td align="center">1</td><td align="center">2</td><td align="center">20</td></tr><tr><td><strong>Dev Portal + Console + REST API</strong></td><td align="center">2</td><td align="center">4</td><td align="center">20</td></tr><tr><td><strong>API Gateway instance</strong><br>Production best practice (HA) is 2 nodes.</td><td align="center">0.25 - 4</td><td align="center">512 MB - 8</td><td align="center">20</td></tr><tr><td><strong>Alert Engine instance</strong><br>Production best practice (HA) is 2 nodes</td><td align="center">0.25 - 4</td><td align="center">512 MB - 8</td><td align="center">20</td></tr><tr><td><strong>Analytics DB instance (ElasticSearch)</strong><br><a href="https://www.elastic.co/guide/en/elasticsearch/reference/7.17/setup.html">Production best practice is 3 nodes</a>.<br><a href="https://www.elastic.co/guide/en/elasticsearch/guide/master/hardware.html">Official hardware recommendations</a>.</td><td align="center">1 - 8</td><td align="center"> 2 - 8 or more</td><td align="center">20 + 0.5 per million requests for default metrics</td></tr><tr><td><strong>Config DB instance</strong> (MongoDB or JDBC DB)<br><a href="https://www.mongodb.com/docs/manual/administration/production-notes">Production best practice is 3 nodes</a></td><td align="center">1</td><td align="center">2</td><td align="center">30</td></tr><tr><td><strong>Rate Limit DB instance</strong> (Redis)<br><a href="https://docs.redis.com/latest/rs/installing-upgrading/hardware-requirements/#productionenvironment">Production best practice is 3 nodes</a></td><td align="center">2</td><td align="center">4</td><td align="center">20</td></tr></tbody></table>

## Gravitee JVM Memory Sizing <a href="#gravitee-jvm-memory-sizing" id="gravitee-jvm-memory-sizing"></a>

You can specify the JVM memory sizing for each of the Gravitee nodes.

{% hint style="warning" %}
* `GIO_MIN_MEM` is the same as `Xms` and `GIO_MAX_MEM` is the same as `Xmx` .
* To avoid resizing during normal JVM operations, set the same value for both the `GIO_MIN_MEM` and the `GIO_MAX_MEM` .&#x20;
{% endhint %}

{% tabs %}
{% tab title="Docker Compose" %}
To configure JVM memory sizing with `docker compose`, complete the following steps:

1. In your `docker-compose.yml` file, navigate to the Gravitee component that you want to configure. For example, `gateway`.
2. In the `environment` section, add the `GIO_MIN_MEM` and the `GIO_MAX_MEM` lines with the value of the JVM heap size. Ensure that both these values are the same to avoid resizing during normal operations.&#x20;

Here is an example configuration of the JVM for the Gravitee API Gateway.

{% code title="docker-compose.yml" %}
```yaml
services:
  gateway:
    ...
    environment:
      - GIO_MIN_MEM=512m
      - GIO_MAX_MEM=512m
      ...
```
{% endcode %}

**Note:** During bootstrap, which occurs when the Gravitee component starts up, the `GIO_MIN_MEM`and `GIO_MAX_MEM` variables are injected into the `JAVA_OPTS`.

2. Run `docker compose up -d` to restart your containers with this new configuration.
{% endtab %}

{% tab title="Kubernetes (Helm)" %}
When deploying containers within Kubernetes, it is typical to configure the JVM and resources at the same time. The best practice is to configure the JVM to be 70% of the defined resources.  If you define `resources.limits.memory: 1024Mi` and define `resources.requests.memory:1024Mi`, then `GIO_MIN_MEM` and `GIO_MAX_MEM` should be `716m`.

{% hint style="info" %}
We recommend that you set the same value for `resources.limits.memory` and `resources.requests.memory`
{% endhint %}

To configure resources and JVM memory sizing with Kubernetes, complete the following steps:

1. In your `values.yaml` file, navigate to the Gravitee component that you want to configure. For example, `gateway`.
2. In the `env` section, add the following lines:

```yaml
    ...
    env:
      - name: GIO_MIN_MEM
        value: <value>m
      - name: GIO_MAX_MEM
        value: <value>m
      ...
```

* Replace `<value>` with the value of your heap size. To avoid resizing during normal operations, ensure that this value is the same for the `GIO_MIN_MEM` and the `GIO_MAX_MEM` .

Here is an example of configuring resources and JVM of the API Gateway:

<pre class="language-yaml" data-title="values.yaml"><code class="lang-yaml">api-management:
  gateway:
    ...
    resources:
      limits:
        cpu: 1
        memory: 1024Mi      
      requests:
        cpu: 500m
        memory: 1024Mi
<strong>    ...
</strong>    env:
      - name: GIO_MIN_MEM
        value: 1152m
      - name: GIO_MAX_MEM
        value: 1152m
      ...
</code></pre>

**Note:** During bootstrap, which occurs when the Gravitee component starts up, the `GIO_MIN_MEM` and `GIO_MAX_MEM` variables are injected into the `JAVA_OPTS` .

2. To apply the updated configuration, redeploy the values.yaml file with your specific command `helm upgrade [release] [chart] -f values.yml` . For example, `helm upgrade gravitee-apim graviteeio/apim -f values.yml`
{% endtab %}
{% endtabs %}

## Roles, permissions, and groups

Gravitee offers the ability to fine-tune a permissions list and the concept of roles, which can be used to **restrict user access to only what is required**.

Some good practices to establish:

* Use groups and permissions to restrict a given user's access to only a necessary subset of APIs.
* Ensure each user only has the necessary permissions (e.g., assign the API\_PUBLISHER role instead of ADMIN).
* Assign permissions to a group instead of each user individually.
* Automatically associate a group with each new API or application to facilitate permission management.

You can find detail on roles, groups, and permissions in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/administration/user-management-and-permissions).

## API review & quality

You can **enable API review and quality** to avoid public exposure to the Developer Portal that is unexpected and lacks strong security requirements, or if you want a member of a Quality team to review API designs prior to deploying the API and making it accessible to API consumers. This can seamlessly establish a robust API strategy.

You can find more information about API review and quality in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/api-measurement-tracking-and-analytics/using-the-api-quality-feature).

## API design

There is no "rule of thumb" when it comes to designing and exposing your APIs, as this always depends on the business requirements. However, consider the following to avoid mistakes and open unexpected security breaches:

* Enable and configure CORS at the API level. This ensures the best level of security when APIs are consumed by browser-based applications. See [details here](https://documentation.gravitee.io/apim/guides/api-configuration/v2-api-configuration/configure-cors#configure-cors).
* Avoid exposing an API without security (i.e., using a keyless plan) when possible. Always prefer stronger security solutions such as JWT or OAuth2.
* Disable auto-validation of API subscriptions. Instead, manually validate each subscription to ensure that you are familiar with your API consumers.
* Require the API consumer to enter a comment when subscribing to an API. This is a simple way to understand the motivation for a subscription and helps detect malicious attempts to access an API.
* Regularly review subscriptions and revoke those that are no longer used.

More information on how to manage API subscriptions is detailed in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/api-exposure-plans-applications-and-subscriptions/subscriptions).
