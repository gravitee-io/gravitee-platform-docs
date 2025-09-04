---
noIndex: true
---

# Envoy Statistics with StatsD

> For an overview of other options for gathering statistics on Ambassador Edge Stack, see the [Statistics and Monitoring](statistics-and-monitoring.md) overview.

At the core of Ambassador Edge Stack is [Envoy Proxy](https://www.envoyproxy.io), which has built-in support for exporting a multitude of statistics about its own operations to StatsD (or to the modified DogStatsD used by Datadog).

If enabled, then Ambassador Edge Stack has Envoy expose this information via the [StatsD](https://github.com/etsy/statsd) protocol. To enable this, you will simply need to set the environment variable `STATSD_ENABLED=true` in Ambassador Edge Stack's deployment YAML:

```diff
     spec:
       containers:
       - env:
+        - name: STATSD_ENABLED
+          value: "true"
         - name: AMBASSADOR_NAMESPACE
           valueFrom:
             fieldRef:
```

When this variable is set, Ambassador Edge Stack by default sends statistics to a Kubernetes service named `statsd-sink` on UDP port 8125 (the usual port of the StatsD protocol). You may instead tell Ambassador Edge Stack to send the statistics to a different StatsD server by setting the `STATSD_HOST` environment variable. This can be useful if you have an existing StatsD sink available in your cluster.

We have included a few example configurations in [the `statsd-sink/` directory](https://github.com/emissary-ingress/emissary/tree/master/deployments/statsd-sink) to help you get started. Clone or download the repository to get local, editable copies and open a terminal window in the `emissary/deployments/` folder.

### Using Graphite as the StatsD sink

[Graphite](http://graphite.readthedocs.org/) is a web-based real-time graphing system. Spin up an example Graphite setup:

```
kubectl apply -f statsd-sink/graphite/graphite-statsd-sink.yaml
```

This sets up the `statsd-sink` service and a deployment that contains Graphite and its related infrastructure. Graphite's web interface is available at `http://statsd-sink/` from within the cluster. Use port forwarding to access the interface from your local machine:

```
SINKPOD=$(kubectl get pod -l service=statsd-sink -o jsonpath="{.items[0].metadata.name}")
kubectl port-forward $SINKPOD 8080:80
```

This sets up Graphite access at `http://localhost:8080/`.

### Using Datadog DogStatsD as the StatsD sink

If you are a user of the [Datadog](https://www.datadoghq.com/) monitoring system, pulling in the Envoy statistics from Ambassador Edge Stack is very easy.

Because the DogStatsD protocol is slightly different than the normal StatsD protocol, in addition to setting Ambassador Edge Stack's `STATSD_ENABLED=true` environment variable, you also need to set the `DOGSTATSD=true` environment variable:

```diff
     spec:
       containers:
       - env:
+        - name: STATSD_ENABLED
+          value: "true"
+        - name: DOGSTATSD
+          value: "true"
         - name: AMBASSADOR_NAMESPACE
           valueFrom:
             fieldRef:
```

Then, you will need to deploy the DogStatsD agent in to your cluster to act as the StatsD sink. To do this, replace the sample API key in our [sample YAML file](https://github.com/emissary-ingress/emissary/blob/master/deployments/statsd-sink/datadog/dd-statsd-sink.yaml) with your own, then apply that YAML:

```
kubectl apply -f statsd-sink/datadog/dd-statsd-sink.yaml
```

This sets up the `statsd-sink` service and a deployment of the DogStatsD agent that forwards the Ambassador Edge Stack statistics to your Datadog account.

Additionally, Ambassador Edge Stack supports setting the `dd.internal.entity_id` statistics tag using the `DD_ENTITY_ID` environment variable. If this value is set, statistics will be tagged with the value of the environment variable. Otherwise, this statistics tag will be omitted (the default).
