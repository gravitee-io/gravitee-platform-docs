---
hidden: false
noIndex: false
description: Read what the gateway recorded about your Kafka Services and Message APIs, from the dashboards down to a single failed connection. Pick the task you need.
---

# Observability

The **Observability** group of the Event Stream Management sidebar holds **Dashboards**, **Logs**, and **Tracing**. All three read what the gateway already reported, and none of them changes an API.

* [**Dashboards**](view-observability-dashboards.md). Open a prebuilt dashboard for the health or the traffic of your Kafka Services and Message APIs.
* [**Logs**](view-connection-logs.md). List the connections and requests the gateway recorded across APIs, and filter them down to the ones you care about.
* [**Tracing**](trace-requests.md). Follow one API's requests through the gateway, span by span.

A failed Kafka connection opens on a plain-language message that says what went wrong, and a badge that says where. See [Diagnose a failed Kafka connection](diagnose-a-failed-kafka-connection.md).

An environment that enables API scoring also renders an **API Score** item in this group. It isn't covered here.

## What the group covers

**Dashboards** and **Logs** show Kafka Services and Message APIs only, never your HTTP proxies, LLM proxies, or other APIs. **Tracing** works on one API at a time, picked from the started Kafka Services and Message APIs of the environment.

## What you need

* A role with read access to the environment's APIs or dashboards. Without either, the **Observability** group isn't shown.
* For **Tracing**, read access to the environment's APIs. A role that reads only dashboards gets **Dashboards** and **Logs**, and no **Tracing** item.
* Reporting switched on for each API you want to see. An API that reports nothing produces no logs and no dashboard data, and its **Overview** page says so. See [View connection logs](view-connection-logs.md#why-an-api-shows-nothing).
