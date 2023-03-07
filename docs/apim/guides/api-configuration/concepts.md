---
description: >-
  This page contains conceptual explanations of how APIs are configured in
  Gravitee. For how-to information on API configuration, please refer to the API
  configuration how-to guides.
---

# Concepts

### Load balancing

Load balancing is a technique used to distribute incoming traffic across multiple backend servers. The goal of load balancing is to optimize resource utilization, maximize throughput, minimize response time, and avoid overloading any single server. The Gravitee Gateway comes with a built-in load balancer, which you can enable and configure for your API endpoints according to your requirements. Check out the interactive UI exploration or the text descriptions to learn more.&#x20;

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="q2cetEPiktDGaSv7t4gM" url="https://app.arcade.software/share/q2cetEPiktDGaSv7t4gM" %}
{% endtab %}

{% tab title="Text descriptions" %}
In order to successfully use Gravitee load balancing, you'll need to understand two key concepts:

* **Endpoint groups:** a logical grouping of endpoints that share a load balancing algorithm
* **Load balancing types:** Gravitee offers four different types of load balancing:
  * **Round robin:** The algorithm works by maintaining a list of backend servers and assigning each incoming request to the next server in the list. Once the last server in the list has been reached, the algorithm starts again from the beginning of the list, cycling through the servers in a circular fashion.
  * **Random:** The algorithm selects a backend server at random for each incoming request. Each server has an equal chance of being selected, regardless of its current load or processing capacity.
  * **Weighted round robin:** The algorithm works similarly to the Round Robin mode, but doesn't assign incoming requests in a ciricular fashion, but, instead, assisgns requests based of a specified weight that you have given each backend server.
    * For example, if you have endpoint 1 with a weight of 9 and endpoint 2 with a weight of 1, endpoint 1 is selected 9 times out of 10, whereas endpoint 2 is selected only 1 time out of 10.
  * **Weighted random:** Weighted random load balancing leverages an algorithm that distributes incoming traffic across multiple backend servers based on a predefined weight assigned to each server. The weight represents the relative capacity or processing power of each server, with higher weights indicating a higher capacity to handle incoming requests. The algorithm works by generating a random number within a defined range, based on the total sum of all server weights. The random number is then used to select one of the backend servers for processing the incoming request.
    * For example, if you have a group of three backend servers A, B, and C, with weights of 1, 2, and 3, respectively. The total weight of all servers is 6. When an incoming request arrives, the load balancer generates a random number between 1 and 6. If the number is between 1 and 1 (inclusive), server A is selected. If the number is between 2 and 3, server B is selected. If the number is between 4 and 6, server C is selected.
{% endtab %}
{% endtabs %}

### Failover

Failover is a mechanism to ensure high availability and reliability of APIs by redirecting incoming traffic to a secondary server or backup system in the event of a primary server failure. Gravitee includes built-in failover mechanisms and capabilities. Check out the interactive UI exploration or the text descriptions to learn more.&#x20;

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="VaRhvOcOU39TQb3PtfRd" url="https://app.arcade.software/share/VaRhvOcOU39TQb3PtfRd" %}
{% endtab %}

{% tab title="Text descriptions" %}
Once you have configured your endpoints as a part of your load-balancing configuration, you can configure failover for those endpoints and whichever load balancing algorithm that you chose. You'll need to understand the following concepts to make the most of Gravitee failover mechanisms:

* **Max attempts**: limits the number of possible tries before returning an error. Each try gets an endpoint according to the load balancing algorithm.
* **Timeout**: limits the time allowed to try another attempt
{% endtab %}
{% endtabs %}

### Health checks&#x20;

A health check is a mechanism used to monitor the availability and health of your endpoints and/or your API gateways. Gravitee includes a built-in health check mechanism that allows you to create global health check configurations. Check out the interactive UI exploration or the text descriptions to learn more.&#x20;

{% tabs %}
{% tab title="Interactive UI exploration" %}
{% @arcade/embed flowId="awIKYCvN2m1DusBD9W7a" url="https://app.arcade.software/share/awIKYCvN2m1DusBD9W7a" %}
{% endtab %}

{% tab title="Text descriptions" %}
Gravitee enables you to configure health checks for both endpoints and Gravitee API gateways. Like load-balancing and failover, health checks are Gravitee backend services. To ensure that you are prepared to use Gravitee health checks, you will want to make sure that you are familiar with the following concepts:

* **Trigger**: define what triggers the health checks. Triggers are:
  * HTTP methods
  * Paths
  * Headers
* **Schedule**: the schedule at which health checks can be triggered. These can be configured at the levels of seconds, minutes, hours, days, weeks, months, and years.&#x20;
* **From root path:** this is an option that you can enable to apply the specified path at the root URL leel. For example, if your endpoint is URL is `www.test.com/api`, this option removes /api before appending the path.
* **Assertions:** where you specify any specify conditions to test for in the API response that will trigger a health check. Assertions are written in the Gravitee Expression Language. An assertion can be a simple 200 response (`#response.status == 200`) but you can also test for specific content.

After you've configured health checks, you can view health check information and results in the **Health-check dashboard** for that specific API. Here, you have multiple charts to track:

* **Global availability**: average availability and average response times for _all_ health-checked endpoints
* **Per-endpoint availability:** average availability and average response times for _specific_ endpoints
* **Per-gateway availability:** average availability and response times per API gateway where health-check is enabled
* **Latest check:** a running list of most recent health checks. [You can choose to show only status transitions](https://app.arcade.software/share/awIKYCvN2m1DusBD9W7a)[https://app.arcade.software/share/awIKYCvN2m1DusBD9W7a](https://app.arcade.software/share/awIKYCvN2m1DusBD9W7a)
{% endtab %}
{% endtabs %}

### Service Discovery

