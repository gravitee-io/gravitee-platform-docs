---
description: Release-over-release performance results for the API Management Gateway on sync proxy APIs, with the scenarios and controlled environment used to produce them.
---

# Gateway benchmarks

These results track the performance of the API Management Gateway across releases under a fixed configuration. Each scenario differs only in the plan securing the API, or in the policy applied to it, so that the figures isolate the cost of that one difference.

The scenarios and the environment stay fixed between releases so that results remain directly comparable. Any change to either is recorded here, because a change to the environment invalidates comparison with earlier results.

{% hint style="info" %}
These results are measured in a controlled internal environment and are intended to surface changes between releases. They don't establish the maximum capacity of the Gateway, they aren't a capacity guarantee for your own deployment, and the environment isn't published for independent reproduction.
{% endhint %}

## Test scenarios

<table>
    <thead>
        <tr>
            <th width="320">Scenario</th>
            <th>Configuration</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Keyless</td>
            <td>Sync proxy API on a keyless plan, no policies applied</td>
        </tr>
        <tr>
            <td>API Key</td>
            <td>Sync proxy API on an API key plan</td>
        </tr>
        <tr>
            <td>OAuth 2.0</td>
            <td>Sync proxy API on an OAuth 2.0 plan</td>
        </tr>
        <tr>
            <td>Keyless with Rate Limit policy</td>
            <td>Sync proxy API on a keyless plan with a rate limiting policy applied. The policy was configured with Redis as its backing store, so this scenario includes the cost of the Redis round trip.</td>
        </tr>
    </tbody>
</table>

## Test environment

The test uses three separate Kubernetes clusters on Microsoft Azure, so that load generation and backend processing never compete with the Gateway for resources.

<table>
    <thead>
        <tr>
            <th width="260">Setting</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Load generator cluster</td>
            <td><code>Standard_D8s_v6</code> nodes</td>
        </tr>
        <tr>
            <td>Backend cluster</td>
            <td><code>Standard_D8s_v6</code> nodes</td>
        </tr>
        <tr>
            <td>Gateway cluster (system under test)</td>
            <td>CPU-optimized <code>Standard_F8as_v6</code> nodes</td>
        </tr>
        <tr>
            <td>Gateway CPU</td>
            <td>4 vCPU, set as both request and limit</td>
        </tr>
        <tr>
            <td>Gateway memory</td>
            <td>3 GiB</td>
        </tr>
        <tr>
            <td>JVM heap</td>
            <td>75% of allocated memory</td>
        </tr>
    </tbody>
</table>

No tuning was applied beyond the Gateway configuration above.

## Test method

Load is generated from the load generator cluster and sent to the Gateway, which forwards each request to the backend cluster.

<table>
    <thead>
        <tr>
            <th width="260">Setting</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Load generation tool</td>
            <td>k6</td>
        </tr>
        <tr>
            <td>Monitoring</td>
            <td>Grafana</td>
        </tr>
        <tr>
            <td>Protocol</td>
            <td>HTTPS</td>
        </tr>
        <tr>
            <td>Duration</td>
            <td>15 minutes per scenario</td>
        </tr>
        <tr>
            <td>Runs</td>
            <td>One run per scenario, per release</td>
        </tr>
        <tr>
            <td>Measurement window</td>
            <td>The steady-state portion of the run, excluding ramp-up</td>
        </tr>
        <tr>
            <td>Request payload size</td>
            <td>1 KB</td>
        </tr>
        <tr>
            <td>Backend latency</td>
            <td>No artificial latency added</td>
        </tr>
    </tbody>
</table>

## Results

Select a release to see its results. CPU is reported in cores consumed against the 4 cores allocated.

{% hint style="warning" %}
Each figure comes from a single run, so small differences between releases fall within the range that run-to-run variation can produce. Treat them as a record of each release rather than as a measured trend. Repeat runs are planned for future results.
{% endhint %}

{% tabs %}
{% tab title="4.12.20" %}
<table>
    <thead>
        <tr>
            <th width="260">Scenario</th>
            <th align="right">Transactions per second</th>
            <th align="right">Average (ms)</th>
            <th align="right">P95 (ms)</th>
            <th align="right">P99 (ms)</th>
            <th align="right">CPU (cores)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Keyless</td>
            <td align="right">16,900</td>
            <td align="right">4.62</td>
            <td align="right">5.75</td>
            <td align="right">9.14</td>
            <td align="right">3.3</td>
        </tr>
        <tr>
            <td>API Key</td>
            <td align="right">16,500</td>
            <td align="right">4.73</td>
            <td align="right">5.92</td>
            <td align="right">9.48</td>
            <td align="right">3.4</td>
        </tr>
        <tr>
            <td>OAuth 2.0</td>
            <td align="right">15,100</td>
            <td align="right">4.75</td>
            <td align="right">5.76</td>
            <td align="right">9.12</td>
            <td align="right">3.3</td>
        </tr>
        <tr>
            <td>Keyless with Rate Limit policy</td>
            <td align="right">13,500</td>
            <td align="right">5.06</td>
            <td align="right">6.29</td>
            <td align="right">9.18</td>
            <td align="right">3.2</td>
        </tr>
    </tbody>
</table>
{% endtab %}

{% tab title="4.12.19" %}
<table>
    <thead>
        <tr>
            <th width="260">Scenario</th>
            <th align="right">Transactions per second</th>
            <th align="right">Average (ms)</th>
            <th align="right">P95 (ms)</th>
            <th align="right">P99 (ms)</th>
            <th align="right">CPU (cores)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Keyless</td>
            <td align="right">16,900</td>
            <td align="right">4.63</td>
            <td align="right">5.62</td>
            <td align="right">8.01</td>
            <td align="right">3.0</td>
        </tr>
        <tr>
            <td>API Key</td>
            <td align="right">16,800</td>
            <td align="right">4.65</td>
            <td align="right">5.66</td>
            <td align="right">7.96</td>
            <td align="right">3.1</td>
        </tr>
        <tr>
            <td>OAuth 2.0</td>
            <td align="right">15,000</td>
            <td align="right">4.77</td>
            <td align="right">5.70</td>
            <td align="right">7.89</td>
            <td align="right">3.1</td>
        </tr>
        <tr>
            <td>Keyless with Rate Limit policy</td>
            <td align="right">13,500</td>
            <td align="right">5.04</td>
            <td align="right">6.15</td>
            <td align="right">8.15</td>
            <td align="right">3.06</td>
        </tr>
    </tbody>
</table>
{% endtab %}

{% endtabs %}
