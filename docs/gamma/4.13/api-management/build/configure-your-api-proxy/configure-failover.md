---
description: >-
  Turn on automatic retries with a circuit breaker so slow or failing backend
  endpoints don't take your API down.
hidden: false
noIndex: false
---

# Configure failover

The **Failover** page configures automatic retries and circuit breaker behavior for endpoint failover. When a threshold of slow calls or connection failures is reached, the circuit breaker opens and stops all requests to the backend. While the circuit is open, the API answers with a `502 - Bad Gateway` status.

To open the page, follow these steps:

1. Click **API Proxies** in the module sidebar.
2. Select your API proxy.
3. Click **Endpoints** in the API proxy sidebar.
4. Click **Failover**.

Editing the settings requires both the `api-definition-u` and `api-gateway_definition-u` permissions. When the API proxy is managed by the Kubernetes operator, the settings are read-only.

<!-- TODO: Screenshot of the Failover page -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-failover-page.png" alt=""><figcaption><p>The Failover page</p></figcaption></figure>

## Enable failover

Turn on the **Enable failover** switch to activate automatic retries with a circuit breaker. The retry and circuit breaker fields stay disabled until failover is enabled. The **More information** button opens a dialog describing the circuit breaker mechanism.

## Set the retry policy

The **Retry policy** card controls how aggressively the gateway retries before giving up:

| Setting                             | Default | Description                                                                                           |
| ----------------------------------- | ------- | ----------------------------------------------------------------------------------------------------- |
| **Max retries**                     | `2`     | The number of retries before giving up.                                                               |
| **Failure condition**               | Empty   | An Expression Language expression evaluated against each response. Return `true` to mark the response as a failure. Leave empty to use connection errors only. |
| **Force next endpoint on failure**  | Off     | Skip the load balancer and pin retries to a different endpoint.                                       |

For example, the failure condition `{#response.status >= 500}` marks every `5xx` response as a failure.

## Tune the circuit breaker

The **Circuit breaker** card sets the conditions for opening the circuit and how long it stays open before transitioning to half-open:

| Setting                              | Default | Description                                                                  |
| ------------------------------------ | ------- | ---------------------------------------------------------------------------- |
| **Slow call duration (ms)**          | `2000`  | The duration above which a call counts as slow. Minimum `50`.                |
| **Open state duration (ms)**         | `10000` | How long the circuit stays open. Minimum `500`.                              |
| **Maximum failures**                 | `5`     | The number of failures that opens the circuit. Minimum `1`.                  |
| **Per subscription circuit breaker** | On      | Track the circuit per subscription, so a noisy subscriber won't affect other consumers. |

{% hint style="info" %}
Configure your endpoints with timeouts greater than the slow call duration. In the half-open state there's no retry mechanism: the circuit breaker reopens if the next call is slow, and closes otherwise.
{% endhint %}

## Verification

To verify failover is working as expected, follow these steps:

1. Enable failover, click **Save changes**, and deploy the API.
2. Make the backend endpoint slow or unreachable, and send more requests than the **Maximum failures** threshold.
3. The API answers with a `502 - Bad Gateway` status while the circuit is open, and recovers after the open state duration once the backend responds normally again.

<!-- TODO: Screenshot of a 502 response while the circuit breaker is open -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-api-failover-502.png" alt=""><figcaption><p>A response while the circuit is open</p></figcaption></figure>
