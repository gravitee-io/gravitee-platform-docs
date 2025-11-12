---
description: >-
  This section focuses on configuring load-balancing, failover, and
  health-checks as Gravitee backend services
---

# Load-balancing, Failover, and Health-checks

## Overview

APIM offers three main backend services for managing your APIs that are built into the Gravitee platform:

* [**Load-balancing**](load-balancing-failover-and-health-checks.md#load-balancing)**:** A technique that distributes incoming traffic across multiple backend servers to optimize resource utilization, maximize throughput, minimize response time, and avoid overloading any single server.
* [**Failover**](load-balancing-failover-and-health-checks.md#failover)**:** Ensures high availability and reliability by redirecting incoming traffic to a secondary server or backup system in the event of a primary server failure.&#x20;
* [**Health-checks**](load-balancing-failover-and-health-checks.md#health-checks)**:** A health check is a mechanism used to monitor the availability and health of your endpoints and/or API Gateways.&#x20;

## Load-balancing

Gravitee load-balancing relies on:

* **Endpoint groups:** A logical grouping of endpoints that share a load-balancing algorithm.
* **Load-balancing types:** Gravitee offers four different types of load-balancing: [round robin](load-balancing-failover-and-health-checks.md#round-robin), [random](load-balancing-failover-and-health-checks.md#random), [weighted round robin](load-balancing-failover-and-health-checks.md#weighted-round-robin), and [weighted random](load-balancing-failover-and-health-checks.md#weighted-random).

{% tabs %}
{% tab title="Round robin" %}
Maintains a list of backend servers and assigns each incoming request to the next server on the list. Once the last server has been reached, the algorithm starts again from the beginning of the list, cycling through the servers in a circular manner.
{% endtab %}

{% tab title="Random" %}
Selects a backend server at random for each incoming request. Each server has an equal chance of being selected, regardless of its current load or processing capacity.
{% endtab %}

{% tab title="Weighted round robin" %}
Works similarly to round robin, but instead of assigning incoming requests in a circular manner, requests are assigned based on the specified weight given to each backend server.

**Example:** If endpoint 1 has a weight of 9 and endpoint 2 has a weight of 1, endpoint 1 is selected 9 times out of 10, whereas endpoint 2 is selected only 1 time out of 10.
{% endtab %}

{% tab title="Weighted random" %}
Distributes incoming traffic across multiple backend servers based on the predefined weight assigned to each server. The weight represents relative capacity or processing power, where higher weights indicate greater ability to handle incoming requests. The algorithm generates a random number within a defined range based on the total sum of all server weights. This number is used to select one of the backend servers for processing the request.

**Example:** If three backend servers, A, B, and C, have weights of 1, 2, and 3, respectively, the total weight of all servers is 6. When a request arrives, the load-balancer generates a random number between 1 and 6. If the number is between 1 and 1 (inclusive), server A is selected. If the number is between 2 and 3, server B is selected. If the number is between 4 and 6, server C is selected.
{% endtab %}
{% endtabs %}

To configure load-balancing:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select your API
4.  From the inner left nav, select **Endpoints** under **Backend services**&#x20;

    <figure><img src="../../../.gitbook/assets/v2 endpoint group.png" alt=""><figcaption><p>Endpoint configuration</p></figcaption></figure>
5.  To confirm the load-balancing algorithm (chosen when your endpoint's group was created), click **Edit group** and select the **General** tab. Click the arrow to **Go back** to the endpoint configuration

    <figure><img src="../../../.gitbook/assets/v2 endpoint group edit.png" alt=""><figcaption><p>Edit endpoint group</p></figcaption></figure>
6.  Click the pencil icon for your endpoint and select the **General** tab to edit the load-balancing weight&#x20;

    <figure><img src="../../../.gitbook/assets/v2 endpoint weight.png" alt=""><figcaption><p>Configure load-balancing weight</p></figcaption></figure>
7. Click **Save**

### Failover

To configure failover:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select your API
4.  From the inner left nav, select **Failover** under **Backend services**&#x20;

    <figure><img src="../../../.gitbook/assets/v2 failover.png" alt=""><figcaption><p>Configure failover</p></figcaption></figure>
5. Configure the following:
   * Toggle **Enable Failover** ON
   * **Max Attempts:** Define the upper limit for the number of possible Gravitee API Gateway attempts to find a suitable endpoint, according to the load-balancing algorithm, before returning an error
   * **Timeout:** Defines the upper limit for time (in ms) between successive attempts before timing out
6. Click **Save**

## Health-checks

To configure health-checks:

1. Log in to your APIM Console
2. Select **APIs** from the left nav
3. Select your API
4.  From the inner left nav, select **Health-check** under **Backend services**&#x20;

    <figure><img src="../../../.gitbook/assets/v2 health-check.png" alt=""><figcaption><p>Configure health-checks</p></figcaption></figure>
5. Configure the following:
   * Toggle **Enable health-check** ON
   * Define the **Trigger Schedule** to establish the time interval between successive health-checks
   * Select the **HTTP Method** that will trigger the health-check
   * Define the **Path** that will trigger the health check
   * Toggle **From root path ('/')** ON to apply the path specified at the root URL level, e.g., for the endpoint URL `www.test.com/api`, this option removes `/api` before appending the path
   * Specify the **HTTP Headers** that will trigger a health check (supports [Gravitee Expression Language](../../gravitee-expression-language.md))
   * Use Gravitee Expression Language to define an **Assertion** that specifies conditions to test for in the API response that will trigger a health-check, then click **+ Add assertion**
   * Click **Save**, which also generates a visual summary of the health-check configuration
