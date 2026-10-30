---
description: Deploy APIM 4.13 with Prometheus and Grafana using Docker Compose, generate traffic, and explore it with the Gravitee Grafana dashboards.
---

# Monitor APIM with Prometheus and Grafana using Docker Compose

This guide deploys Gravitee API Management (APIM) with Prometheus and Grafana on a single machine using Docker Compose. When you're done, Grafana shows your API traffic, consumers, latency, Gateway health, SLOs, and the headers and payloads of each call.

To add monitoring to an existing installation instead, see [Monitor APIM with Grafana](../../analyze-and-monitor-apis/monitor-apim-with-grafana.md).

{% hint style="info" %}
This guide uses third-party tools. For their full configuration options, see the [Docker Compose](https://docs.docker.com/compose/), [Prometheus](https://prometheus.io/docs/), and [Grafana](https://grafana.com/docs/) documentation.
{% endhint %}

## Architecture

```
API consumers ──► Gateway ──► backend
                    │
                    ├─ internal API :18082 /_node/metrics/prometheus ──► Prometheus ──┐
                    ├─ analytics reporter ──► Elasticsearch  gravitee-v4-metrics-*  ──┼──► Grafana
                    ├─ node monitoring   ──► Elasticsearch  gravitee-monitor-*      ──┤
                    └─ API logs          ──► Elasticsearch  gravitee-v4-log-*       ──┘
```

Grafana reads two kinds of data:

* **Gateway metrics from Prometheus**: real-time request rates, connections, JVM, and CPU for each Gateway node.
* **API analytics from Elasticsearch**: one record per API call, with the API, application, plan, status, latency split between the Gateway and the backend, rejection reason, client country, and user agent.
* **API logs from Elasticsearch**: the headers and payloads of each call, for APIs with logging enabled.

## Prerequisites

* Docker with Docker Compose v2
* 4 GB of RAM available to Docker
* Free local ports `3000`, `8082`, `8083`, `8084`, and `9090`

## Create the project files

1.  Create a project directory:

    ```bash
    mkdir gravitee-prometheus-grafana && cd gravitee-prometheus-grafana
    mkdir -p prometheus grafana/provisioning/datasources grafana/provisioning/dashboards grafana/dashboards
    ```
2.  Create `docker-compose.yml`:

    {% code title="docker-compose.yml" %}
    ```yaml
    services:
      mongodb:
        image: mongo:6
        volumes: [mongo_data:/data/db]
        healthcheck:
          test: ["CMD", "mongosh", "--quiet", "--eval", "db.adminCommand('ping')"]
          interval: 10s
          retries: 12

      elasticsearch:
        image: docker.elastic.co/elasticsearch/elasticsearch:8.11.3
        environment:
          - discovery.type=single-node
          - xpack.security.enabled=false
          - ES_JAVA_OPTS=-Xms512m -Xmx512m
        volumes: [es_data:/usr/share/elasticsearch/data]
        healthcheck:
          test: ["CMD-SHELL", "curl -fs http://localhost:9200/_cluster/health || exit 1"]
          interval: 10s
          retries: 24

      management-api:
        image: graviteeio/apim-management-api:4.13
        depends_on:
          mongodb: { condition: service_healthy }
          elasticsearch: { condition: service_healthy }
        environment:
          - gravitee_ds_mongodb_host=mongodb
          - gravitee_analytics_elasticsearch_endpoints_0=http://elasticsearch:9200
        ports: ["8083:8083"]

      gateway:
        image: graviteeio/apim-gateway:4.13
        depends_on:
          mongodb: { condition: service_healthy }
          elasticsearch: { condition: service_healthy }
        environment:
          # Management and rate-limit repositories are both built from ds.mongodb.*
          - gravitee_ds_mongodb_host=mongodb
          - gravitee_reporters_elasticsearch_endpoints_0=http://elasticsearch:9200
          # Prometheus metrics
          - gravitee_services_metrics_enabled=true
          - gravitee_services_metrics_prometheus_enabled=true
          # Internal API: listen on all interfaces so the Prometheus container can scrape it
          - gravitee_services_core_http_host=0.0.0.0
          - gravitee_services_core_http_port=18082
          - gravitee_services_core_http_authentication_type=basic
          - gravitee_services_core_http_authentication_users_admin=adminadmin
        ports: ["8082:8082"]

      management-ui:
        image: graviteeio/apim-management-ui:4.13
        depends_on: [management-api]
        environment:
          - MGMT_API_URL=http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/
        ports: ["8084:8080"]

      backend:
        image: mccutchen/go-httpbin:v2.15.0

      prometheus:
        image: prom/prometheus:v3.5.0
        volumes:
          - ./prometheus:/etc/prometheus:ro
        command: ["--config.file=/etc/prometheus/prometheus.yml"]
        ports: ["9090:9090"]

      grafana:
        image: grafana/grafana:12.2.0
        environment:
          - GF_SECURITY_ADMIN_PASSWORD=admin
        volumes:
          - ./grafana/provisioning:/etc/grafana/provisioning:ro
          - ./grafana/dashboards:/etc/grafana/dashboards:ro
        ports: ["3000:3000"]

    volumes:
      mongo_data:
      es_data:
    ```
    {% endcode %}

    {% hint style="warning" %}
    The internal API exposes node information and metrics. Outside a local test, change the `adminadmin` password and keep port `18082` on a private network.
    {% endhint %}
3.  Create `prometheus/prometheus.yml`:

    {% code title="prometheus/prometheus.yml" %}
    ```yaml
    global:
      scrape_interval: 5s
      evaluation_interval: 30s

    rule_files:
      - /etc/prometheus/rules/*.yml

    scrape_configs:
      - job_name: gravitee
        metrics_path: /_node/metrics/prometheus
        basic_auth: { username: admin, password: adminadmin }
        static_configs:
          - targets: ['gateway:18082']
    ```
    {% endcode %}
4.  Create the Grafana data sources in `grafana/provisioning/datasources/datasources.yml`:

    {% code title="grafana/provisioning/datasources/datasources.yml" %}
    ```yaml
    apiVersion: 1
    datasources:
      - name: Prometheus
        uid: prometheus
        type: prometheus
        url: http://prometheus:9090
        isDefault: true
      - name: Gravitee Analytics
        uid: gravitee-analytics
        type: elasticsearch
        url: http://elasticsearch:9200
        jsonData: { index: "gravitee-v4-metrics-*", timeField: "@timestamp" }
      - name: Gravitee Node Monitoring
        uid: gravitee-monitor
        type: elasticsearch
        url: http://elasticsearch:9200
        jsonData: { index: "gravitee-monitor-*", timeField: "@timestamp" }
      - name: Gravitee Call Logs
        uid: gravitee-logs
        type: elasticsearch
        url: http://elasticsearch:9200
        jsonData: { index: "gravitee-v4-log-*", timeField: "@timestamp" }
    ```
    {% endcode %}
5.  Create the dashboard provider in `grafana/provisioning/dashboards/gravitee.yml`:

    {% code title="grafana/provisioning/dashboards/gravitee.yml" %}
    ```yaml
    apiVersion: 1
    providers:
      - name: gravitee
        folder: Gravitee
        type: file
        options: { path: /etc/grafana/dashboards }
    ```
    {% endcode %}
6.  Download the [Gravitee Grafana dashboard pack](https://github.com/gravitee-io-labs/gravitee-grafana-prometheus), then copy its files into the project:

    ```bash
    curl -sLO https://github.com/gravitee-io-labs/gravitee-grafana-prometheus/releases/latest/download/gravitee-grafana-dashboards.zip
    unzip gravitee-grafana-dashboards.zip
    cp gravitee-grafana-dashboards/dashboards/*.json grafana/dashboards/
    mkdir -p prometheus/rules && cp gravitee-grafana-dashboards/prometheus-rules/*.rules.yml prometheus/rules/
    ```

## Start the stack

```bash
docker compose up -d
```

The first start takes one to two minutes. Wait until the Management API answers before you create an API:

```bash
until curl -sf -o /dev/null -u admin:admin http://localhost:8083/management/v2/environments/DEFAULT/apis; do sleep 5; done
```

## Create an API and generate traffic

The Gateway only records analytics for calls to a deployed API. Create a keyless API that proxies the demo backend and logs the headers and payloads of every call. The commands keep the top-level `id` of each response:

```bash
MGMT=http://localhost:8083/management/v2/environments/DEFAULT
API=$(curl -s -u admin:admin -H 'Content-Type: application/json' -X POST $MGMT/apis -d '{
  "name": "Demo API", "apiVersion": "1.0", "definitionVersion": "V4", "type": "PROXY",
  "listeners": [{"type": "HTTP", "paths": [{"path": "/demo"}], "entrypoints": [{"type": "http-proxy"}]}],
  "endpointGroups": [{"name": "default", "type": "http-proxy",
    "endpoints": [{"name": "httpbin", "type": "http-proxy", "configuration": {"target": "http://backend:8080"}}]}],
  "analytics": {"enabled": true, "logging": {"mode": {"entrypoint": true, "endpoint": true},
    "phase": {"request": true, "response": true}, "content": {"headers": true, "payload": true}}}
}' | grep -m1 '^  "id"' | cut -d'"' -f4)
PLAN=$(curl -s -u admin:admin -H 'Content-Type: application/json' -X POST $MGMT/apis/$API/plans \
  -d '{"name": "Keyless", "definitionVersion": "V4", "mode": "STANDARD", "security": {"type": "KEY_LESS"}}' \
  | grep -m1 '^  "id"' | cut -d'"' -f4)
curl -s -u admin:admin -X POST $MGMT/apis/$API/plans/$PLAN/_publish > /dev/null
curl -s -u admin:admin -X POST $MGMT/apis/$API/_start > /dev/null
curl -s -u admin:admin -H 'Content-Type: application/json' -X POST $MGMT/apis/$API/deployments -d '{}' > /dev/null
echo "API: $API  Plan: $PLAN"
```

If either ID is empty, the Management API wasn't ready: rerun the commands. The Gateway picks up the API within a few seconds. Until then, calls return `404`.

Then send a mix of successful, failing, and slow calls for two minutes:

```bash
end=$((SECONDS + 120))
while [ $SECONDS -lt $end ]; do
  for path in get get get get status/404 status/500 delay/0.5; do
    curl -s -o /dev/null "http://localhost:8082/demo/$path" &
  done
  sleep 0.3
done
```

## Explore the dashboards

Open Grafana at `http://localhost:3000` (`admin` / `admin`), then open **Dashboards → Gravitee**:

| Dashboard | What it answers |
| --- | --- |
| **API Program Overview** | How are all my APIs doing, who calls them, and what does the Gateway reject and why? |
| **API Drill-down** | What's wrong with one API: which path, which consumer, which call? |
| **Consumers, Plans & Tenants** | Which applications and plans drive traffic, with what quality of service? |
| **Gateway Fleet & Runtime** | Are the Gateway nodes healthy: JVM, GC, CPU, connections, backend pool? |
| **SLOs & Error Budgets** | Are we meeting the availability objective, and which API is breaching it? |
| **Call Logs** | What exactly did one call send and receive, on the client side and on the backend side? |

{% hint style="info" %}
This demo logs every call, which is fine for a test. In production, enable logging per API with a condition, as described in [Monitor APIM with Grafana](../../analyze-and-monitor-apis/monitor-apim-with-grafana.md#enable-api-logging-optional).
{% endhint %}

{% hint style="info" %}
The demo API is keyless and every call comes from `localhost`, so some panels stay empty: applications, subscriptions, rate limiting, credential failures, client countries, and custom dimensions. They fill in when you add API key or OAuth plans and receive real client traffic.
{% endhint %}

For a description of every panel and how to use the dashboards, see [Monitor APIM with Grafana](../../analyze-and-monitor-apis/monitor-apim-with-grafana.md).

## Verify

1.  In Prometheus at `http://localhost:9090`, open **Status → Target health**. The `gravitee` target is `UP`.
2.  In **Status → Rule health**, the `gravitee-slo-*` and `gravitee-gateway` groups are loaded.
3.  In Grafana, **API Program Overview** shows the calls you generated. **Gateway nodes up** shows `1`.

## Run PromQL queries

The Gateway exposes Vert.x and Micrometer metrics. Filter HTTP server metrics on `local=~".*:8082"`: without it, the results also include Prometheus scraping the internal API on port `18082`.

| Question | PromQL |
| --- | --- |
| Request rate by status code | `sum by (code) (rate(http_server_requests_total{local=~".*:8082"}[1m]))` |
| Average response time | `sum(rate(http_server_response_time_seconds_sum{local=~".*:8082"}[1m])) / sum(rate(http_server_response_time_seconds_count{local=~".*:8082"}[1m]))` |
| Share of 5xx | `(sum(rate(http_server_requests_total{local=~".*:8082",code=~"5.."}[1m])) or vector(0)) / sum(rate(http_server_requests_total{local=~".*:8082"}[1m]))` |
| Heap usage | `sum(jvm_memory_used_bytes{area="heap"}) / sum(jvm_memory_max_bytes{area="heap"} > 0)` |
| Time spent in GC | `sum(rate(jvm_gc_pause_seconds_sum[1m]))` |

{% hint style="info" %}
G1 reports a maximum of `-1` for its young-generation pools. Sum the heap pools and keep only positive maxima, as above, or the heap ratio is negative.
{% endhint %}

Percentiles and per-API or per-consumer values aren't available from Prometheus. Query them from the analytics data source, as the dashboards do.

## Clean up

```bash
docker compose down -v
```
