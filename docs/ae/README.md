---
description: Overview of Gravitee Alert Engine.
---

# Introduction to Gravitee Alert Engine

An API Monitoring solution is a tool or system designed to monitor and analyze the performance and availability of APIs in real-time. This solution helps to ensure that APIs, the critical intermediaries that allow different software applications to communicate and interact, are functioning correctly and efficiently. It checks factors like response time, uptime, error rates, and other essential metrics. If an API fails, is running slow, or returns errors, the monitoring solution can send alerts to the development team so that they can resolve the issue promptly.

Ultimately, API monitoring helps maintain an optimal user experience, especially in today's digital landscape where APIs play a significant role in application functionality and performance.

## Gravitee Alert Engine (AE)

Gravitee Alert Engine (AE) is Gravitee's enterprise grade API Monitoring solution. Alert Engine (AE) provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configuration and notifications sent through their preferred channels, such as email, Slack and Webhooks. Some examples of notifications include:

* Notifications to API publishers that the health check service was able or unable to check an endpoint.
* Notifications to API consumers or publishers when they reach a given percentage threshold of the quota.
* Notifications to administrators that one of the APIM Gateway instances is consuming more than a percentage threshold of heap or CPU, a new one is available, or a node is down.

## Components

AE exists as the sole component and does not require any external components or a database as it does not store anything. It receives events and sends notifications under the conditions which have been pre-configured upstream with triggers.

## Next steps

Ready to start using AE for your API Monitoring? Select from the options below to learn more about AE and get it up and running.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>AE Architecture</td><td></td><td><a href="overview/architecture.md">architecture.md</a></td></tr><tr><td></td><td>AE installation</td><td></td><td><a href="getting-started/install-and-upgrade-guides/">install-and-upgrade-guides</a></td></tr><tr><td></td><td>AE configuration</td><td></td><td><a href="getting-started/configuration/configure-alert-engine.md">configure-alert-engine.md</a></td></tr></tbody></table>
