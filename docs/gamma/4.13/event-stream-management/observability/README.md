---
hidden: false
noIndex: false
description: Read what the gateway recorded about your Kafka Services and Message APIs, from the dashboards down to a single failed connection. Pick the task you need.
---

# Observability

The **Observability** group of the Event Stream Management sidebar holds **Dashboards**, **Logs**, and **Tracing**. All three read what the gateway already reported, and none of them changes an API.

* [**Dashboards**](view-observability-dashboards.md). Open a prebuilt board for the health or the traffic of your Kafka Services and Message APIs.
* [**Logs**](view-connection-logs.md). List the connections and requests the gateway recorded across APIs, and filter them down to the ones you care about.
* [**Tracing**](trace-requests.md). Follow one API's requests through the gateway, span by span.

A failed Kafka connection opens on a plain-language verdict that names where it broke. See [Diagnose a failed Kafka connection](diagnose-a-failed-kafka-connection.md).

An environment that enables API scoring also renders an **API Score** item in this group. It isn't covered here.

## What the group covers

**Dashboards** and **Logs** are scoped to the two families Event Stream Management manages, Kafka Services and Message APIs. They never show your HTTP proxies, LLM proxies, or other APIs, whichever environment you open them in.

**Tracing** is scoped differently. It asks you to pick one API first, and its picker offers the started Kafka Services and Message APIs of the environment.

## What you need

* An environment role that can read either the APIs or the dashboards of the environment. Without one, the **Observability** group isn't rendered at all.
* Reading the APIs of the environment, specifically, for **Tracing**. A role that can read dashboards but not APIs gets **Dashboards** and **Logs**, and no **Tracing** item.
* Reporting switched on for each API you want to see. An API that reports nothing produces no logs and no dashboard rows, and its detail page says so. See [View connection logs](view-connection-logs.md#why-an-api-shows-nothing).
