---
description: An overview about v2 API Configuration.
---

# v2 API Configuration

{% hint style="info" %}
v2 vs v4 API configuration

This section covers v2 API configuration. If you are looking for documentation that covers configuration for Gravitee v4 APIs, please refer to the [v4 API configuration section.](../v4-api-configuration/)
{% endhint %}

## Introduction

Gravitee offers two main kinds of API configuration options for v2 APIs, each with several subsets of config options:

* General proxy configurations
  * Entrypoints configuration
  * CORS configuration
  * Deployments configuration (via sharding tags)
  * Response templates configuration
* Backend services proxy configurations
  * Load balancing
  * Failover
  * Health checks

Keep reading to learn more about general concepts related to each. If you want to learn how to configure each, please refer to the relevant how-to guides:

* [API documentation](documentation.md)
* [API General Settings](../v4-api-configuration/general-info-settings.md)
* [Load-balancing, failover, and health checks](load-balancing-failover-and-health-checks.md)
* [Configure service discovery](configure-service-discovery.md)
* [Configure general proxy settings](configure-general-proxy-settings.md)
* [Configure user and group access](configure-user-and-group-access.md)

## API Proxy configuration overview

In Gravitee, you can configure several API proxy settings. You can use the interactive UI explorer or the text descriptions to learn more:

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowid="tn8DhyHNq83ZWp8pyqOC" url="https://app.arcade.software/share/tn8DhyHNq83ZWp8pyqOC" %}
{% endtab %}

{% tab title="Text descriptions" %}
In the Proxy section, you can configure the following settings:

* General settings
  * **Entrypoints**: define the Context Path, or the URL location of your API. So if your URL is `[https://apim-master-gateway.team-apim.gravitee.dev/myAPI]`, then `[/myAPI]` is the context path.
  * **CORS**: CORS is a mechanism that allows restricted resources (e.g. fonts) on a web page to be requested from another domain outside the domain from which the first resource was served. For more information on CORS, refer to the [CORS specification](https://fetch.spec.whatwg.org/) and/or read the [CORS section of this article](./#cors).
  * **Deployments**: choose to use sharding tags to control where your APIs are deployed.
  * **Response templates**: define your own response templates if you're looking to override default responses from the gateway.
* Backend services (more information on each of these in the next section of this article)
  * Load-balancing
  * Failover
  * Health checks
{% endtab %}
{% endtabs %}

## Load balancing

Load balancing is a technique used to distribute incoming traffic across multiple backend servers. The goal of load balancing is to optimize resource utilization, maximize throughput, minimize response time, and avoid overloading any single server. The Gravitee Gateway comes with a built-in load balancer, which you can enable and configure for your API endpoints according to your requirements. Check out the interactive UI exploration or the text descriptions to learn more.

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowid="q2cetEPiktDGaSv7t4gM" url="https://app.arcade.software/share/q2cetEPiktDGaSv7t4gM" %}
{% endtab %}

{% tab title="Text descriptions" %}
In order to successfully use Gravitee load balancing, you'll need to understand two key concepts:

* **Endpoint groups:** a logical grouping of endpoints that share a load balancing algorithm
* **Load balancing types:** Gravitee offers four different types of load balancing:
  * **Round robin:** The algorithm works by maintaining a list of backend servers and assigning each incoming request to the next server in the list. Once the last server in the list has been reached, the algorithm starts again from the beginning of the list, cycling through the servers in a circular fashion.
  * **Random:** The algorithm selects a backend server at random for each incoming request. Each server has an equal chance of being selected, regardless of its current load or processing capacity.
  * **Weighted round robin:** The algorithm works similarly to the Round Robin mode, but doesn't assign incoming requests in a circular fashion, but, instead, assisgns requests based of a specified weight that you have given each backend server.
    * For example, if you have endpoint 1 with a weight of 9 and endpoint 2 with a weight of 1, endpoint 1 is selected 9 times out of 10, whereas endpoint 2 is selected only 1 time out of 10.
  * **Weighted random:** Weighted random load balancing leverages an algorithm that distributes incoming traffic across multiple backend servers based on a predefined weight assigned to each server. The weight represents the relative capacity or processing power of each server, with higher weights indicating a higher capacity to handle incoming requests. The algorithm works by generating a random number within a defined range, based on the total sum of all server weights. The random number is then used to select one of the backend servers for processing the incoming request.
    * For example, if you have a group of three backend servers A, B, and C, with weights of 1, 2, and 3, respectively. The total weight of all servers is 6. When an incoming request arrives, the load balancer generates a random number between 1 and 6. If the number is between 1 and 1 (inclusive), server A is selected. If the number is between 2 and 3, server B is selected. If the number is between 4 and 6, server C is selected.
{% endtab %}
{% endtabs %}

## Failover

Failover is a mechanism to ensure high availability and reliability of APIs by redirecting incoming traffic to a secondary server or backup system in the event of a primary server failure. Gravitee includes built-in failover mechanisms and capabilities. Check out the interactive UI exploration or the text descriptions to learn more.

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowid="VaRhvOcOU39TQb3PtfRd" url="https://app.arcade.software/share/VaRhvOcOU39TQb3PtfRd" %}
{% endtab %}

{% tab title="Text descriptions" %}
Once you have configured your endpoints as a part of your load-balancing configuration, you can configure failover for those endpoints and whichever load balancing algorithm that you chose. You'll need to understand the following concepts to make the most of Gravitee failover mechanisms:

* **Max attempts**: limits the number of possible tries before returning an error. Each try gets an endpoint according to the load balancing algorithm.
* **Timeout**: limits the time allowed to try another attempt
{% endtab %}
{% endtabs %}

## Health checks

A health check is a mechanism used to monitor the availability and health of your endpoints and/or your API Gateways. Gravitee includes a built-in health check mechanism that allows you to create global health check configurations. Check out the interactive UI exploration or the text descriptions to learn more.

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowid="awIKYCvN2m1DusBD9W7a" url="https://app.arcade.software/share/awIKYCvN2m1DusBD9W7a" %}
{% endtab %}

{% tab title="Text descriptions" %}
Gravitee enables you to configure health checks for both endpoints and Gravitee API Gateways. Like load-balancing and failover, health checks are Gravitee backend services. To ensure that you are prepared to use Gravitee health checks, you will want to make sure that you are familiar with the following concepts:

* **Trigger**: define what triggers the health checks. Triggers are:
  * HTTP methods
  * Paths
  * Headers
* **Schedule**: the schedule at which health checks can be triggered. These can be configured at the levels of seconds, minutes, hours, days, weeks, months, and years.
* **From root path:** this is an option that you can enable to apply the specified path at the root URL leel. For example, if your endpoint is URL is `www.test.com/api`, this option removes /api before appending the path.
* **Assertions:** where you specify any specify conditions to test for in the API response that will trigger a health check. Assertions are written in the Gravitee Expression Language. An assertion can be a simple 200 response (`#response.status == 200`) but you can also test for specific content.

After you've configured health checks, you can view health check information and results in the **Health-check dashboard** for that specific API. Here, you have multiple charts to track:

* **Global availability**: average availability and average response times for _all_ health-checked endpoints
* **Per-endpoint availability:** average availability and average response times for _specific_ endpoints
* **Per-gateway availability:** average availability and response times per API Gateway where health-check is enabled
* **Latest check:** a running list of most recent health checks. You can choose to show only status transitions.
{% endtab %}
{% endtabs %}

## Service Discovery

Gravitee comes with built-in support for:

*   **Hashicorp Service Discovery:** HashiCorp Consul is a service mesh solution providing a full featured control plane with service discovery, configuration, and segmentation functionality. Hashicopr consul offers the following features:

    * **Service Discovery:** One of the main goals of service discovery is to provide a catalog of available services and to potentially associate it with a health check. Clients of HashiCorp Consul can register a service, such as a backend api, and other clients can use HashiCorp Consul to discover providers of a given service. Using either DNS or HTTP, applications can easily find the services they depend upon.
    * **Health Checking:** HashiCorp Consul clients can provide any number of health checks, either associated with a given service ("is the webserver returning 200 OK"), or with the local node ("is memory utilization below 90%"). This information is used by the service discovery components to route traffic away from unhealthy hosts.

    Gravitee Service discovery for HashiCorp Consul allows you to bind the backend endpoints of your API to a service managed by HashiCorp Consul so that API requests are always routed to the proper, healthy backend service dynamically managed by HashiCorp Consul.

## CORS

CORS, or Cross-Origin Resource Sharing, is a mechanism that allows web pages to make requests to a different domain than the one that served the original content. It is a security feature implemented by web browsers to prevent malicious websites from making unauthorized requests to another website, and is enforced by default by most modern browsers.

CORS works by adding an extra HTTP header to the response sent by the server, which tells the browser whether or not the request is allowed. This header is known as the Access-Control-Allow-Origin header, and it specifies which domains are allowed to access the resource. For example, if the header is set to "Access-Control-Allow-Origin: https://example.com", then only requests from the https://example.com domain will be allowed.

CORS is valuable because it enables web developers to build web applications that interact with multiple domains and APIs, without compromising security. Without CORS, web applications would only be able to make requests to the same domain that served the original content, which would severely limit the functionality of many modern web applications.

{% hint style="danger" %}
While beneficial for certain use cases, there are also risks to CORS. One risk is that by allowing cross-origin requests, a server may inadvertently expose sensitive information to unauthorized parties. For example, if a server includes sensitive data in a response that is accessible via CORS, an attacker could use a malicious website to extract that data. To mitigate this risk, servers can use more restrictive CORS policies, or avoid exposing sensitive data altogether.
{% endhint %}

## Sharding tags

The sharding tags mechanism allows you to specify which “shard” of of your Gravitee API Gateway an API should be deployed too. This feature is useful when you have many API Gateways dedicated to different networks, audiences, programs, and so forth. To explain this further, let’s dive into an example scenario.\
\
In the diagram below we have an example of a typical deployment an organization may use for their API Management. This scenario looks to deploy two APIs in a distributed manner, providing high availability across different regions and in different network environments.

<figure><img src="../../../.gitbook/assets/Example architecture.png" alt=""><figcaption><p>Example architecture diagram to illustrate value of sharding tags.</p></figcaption></figure>

If using sharding tags, you could tag these Gateways with specific keywords. Once the Gateways are tagged, you can [select that tag in an APIs Deployments proxy settings](configure-general-proxy-settings.md#configure-deployments). Whatever tag you select for that API will end up being the Gateway where that API is deployed.
