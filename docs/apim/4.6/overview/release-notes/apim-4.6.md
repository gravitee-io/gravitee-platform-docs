---
description: An overview about apim 4.6.
---

# APIM 4.6

In Gravitee API Management 4.6, we’re pleased to introduce the brand new Gravitee Kafka Gateway. This page provides a brief overview of the Kafka Gateway, but you can read about it in depth [here](../../kafka-gateway/overview.md).

In addition to the Kafka Gateway, we’re excited to release the following features:

* The ability to use secrets managers in API-level configurations to extract sensitive information from APIs and retrieve the values at runtime.
* An OpenTelemetry plugin to retrieve detailed runtime tracing data for both proxy and message APIs.
* Error notifications and retries with exponential backoff for the Webhook entrypoint.
* A [Status Code Transformation policy](../../policies/status-code-transformation.md) to transform status codes for proxy APIs, and the status codes for message APIs via the HTTP POST or GET entrypoint.
* The addition of the category column in the API list.
* A Management API endpoint to delete portal media.
* Improvements to API Score (tech preview).

Read on for more details about the key features in this release.

### Kafka Gateway

The Gravitee Kafka Gateway proxies Kafka to provide control over security, cost, and scalability. You can apply all the benefits of API Management directly to your Kafka cluster, including policies, subscriptions, and plans. The proxy is at the native protocol level, so clients talk to the Gateway using the regular Kafka consumer, producer, and admin client as if it were a Kafka broker.

Gravitee has added the concept of a Kafka API to represent the proxy between the client and the Kafka cluster. The Gateway can run multiple APIs simultaneously. Each API can:

* Expose one Kafka authentication mechanism (e.g., OAUTHBEARER) to the client, while connecting to the physical cluster with another (e.g., SASL PLAIN).
* Provide quotas on ingress and egress rates, so that all consumers can fetch data at a rate that won’t render the service inaccessible to other users.
* Map topics from one name on the client side to a different name on the physical cluster.
* Control access to resources on the cluster and ensure that only approved users can, for example, rename topics, alter partitions, or consume and produce to a topic.

The Kafka Gateway is a standalone product of Gravitee and has its own documentation [here](../../kafka-gateway/overview.md). Using the Kafka Gateway requires an Enterprise Edition license with a special entry for the Kafka Gateway. To get access, contact Gravitee sales [here](https://www.gravitee.io/contact-us).

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXddGaoAvEonFmveHY0rva10NDbbJgYL1avplbWQysu8rKSG0wQ3gYK1F0BX18VLU_OzPvC8rzS6WOJEc9jxj_eL8U6OCN4_5_MGguYrkzP8VpaGisU49WRerKwzBMPqkbEgcrNj?key=CqXLtJSolCHGsUVprn59ZLlK" alt=""><figcaption></figcaption></figure>

Policies on the Kafka Gateway can apply quotas, access controls, and topic mapping.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXexb1AV0GkKqmnAEWCjZkalYiMfDQ4vn0bpgA-yBS58Src2esIPliHDMtui4oE5JdA996eV8eWiA3EzStxn0mOlMCpKEgrg51yEc0dp3RetHscO-HQ_qoYX30Z8cG6Z7Q8VIfR-?key=CqXLtJSolCHGsUVprn59ZLlK" alt=""><figcaption><p>Subscriptions in the Developer Portal showing a connection to the Kafka Gateway</p></figcaption></figure>

### Secrets Managers

In Gravitee APIM 4.4, we introduced secrets managers to obscure sensitive information in the Gravitee Gateway configuration file, such as the database password and API properties secret. APIM 4.6 extends this capability to API-level configuration. Gateways can connect to HashiCorp Vault or the Kubernetes Secrets API to retrieve secrets at runtime.

Secrets are now supported in:

* HTTP Proxy, Kafka, MQTT, RabbitMQ, and Solace endpoints
* OAuth2, Redis, LDAP, and Inline Authentication resources
* HTTP Callout policy

To obtain secrets at runtime you must use a special syntax. The secrets are stored in off-heap memory and never written to disk.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXcs39A1uBrwV0hUCh-zRnNTF92ZmWVGatOo-pLyD12wOdztBj1vFXVDdIZExGUHlBVwZmFuj95vBn0PJ10p2fBV1X9VuHX6dhqLJKFWAayI5_zplf6LGm0Kzf0iR3pw9MonK8uHQA?key=CqXLtJSolCHGsUVprn59ZLlK" alt=""><figcaption><p>Using a secret in the Redis resource</p></figcaption></figure>

### OpenTelemetry

[OpenTelemetry](https://opentelemetry.io/) is a standard tool for generating, collecting, and visualizing network request metrics and traces. With this release, we’ve included support for generating OpenTelemetry data and exporting it via the standard exporter using OTLP and gRPC or regular HTTP. To use the OpenTelemetry exporter, simply point the Gateway’s exporter to the collector of your choice and send the trace data to your preferred OTel target or vendor.

OpenTelemetry works for proxy or message APIs and can provide a simple or verbose trace. The verbose trace generates very detailed data about what the Gravitee Gateway is doing when processing a request or messages. Trace data extends to the policy level and can show message details as needed.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXfcBRMrgKLG5HI2efZZw-BiMKr8HLSH-mfCaQfhCnhCXolaGgYhNyWTS-Cq2iHa-fmQU4ppJAALB0VTfFcYFdrIIBlqvh-kM7XFkiKFTHrUZbnSMzguYpt-E72qZrRqtcoq2VsTHA?key=CqXLtJSolCHGsUVprn59ZLlK" alt=""><figcaption><p>Using Jaegar to visualize a Webhook with OpenTelemetry sent from Gravitee</p></figcaption></figure>

### Error Notifications and Retries for Webhooks

The Webhook entrypoint is used to push data from a messaging system like Kafka to an HTTP target. It can be used purely as a data ingestion and transformation mechanism, as a push-based notification system for events, or as a mechanism to off-load pressure from a REST backend to a messaging system.

We’ve made three enhancements to the Webhook entrypoint to make it even more robust and scalable:

* When an error occurs during consumption of a message, the entrypoint notifies the API manager via the configured notifier (e.g., Webhook or email).
* Subscriptions to the [push plan ](../../expose-apis/plans/push.md)associated with the Webhook entrypoint can be manually restarted via a button-click in the subscription UI of the Console.
* The entrypoint can retry the Webhook request a configurable number of times, with exponential backoff that can also be configured. The backoff ensures that the Webhook won’t overload the target with requests when it is in a legitimately failed state.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXfZfKh6OW4Fdxou9cAiELSjTxhyxHX-kfeTJBZ7aqwVVEO0Z2aVrWHF-AFwS3llOo9kyN2LJNleJ_9q_i7GeBLjeyifp7QX7gdwuAEvraiT1UJyfTmgWO_2Szz0xc9JQHcO4NpZmQ?key=CqXLtJSolCHGsUVprn59ZLlK" alt=""><figcaption><p>Example configuration for retrying a Webhook subscription</p></figcaption></figure>

### API Score improvements (tech preview)

Gravitee 4.6 includes three major updates to the API Score feature for automated governance:

* A new UI for managing custom rulesets, where you can upload Spectral rulesets that meet your organization's requirements
* Support for custom JavaScript functions, so that you can write more complex rules
* Support for scoring the Gravitee API definition for v4 proxy and message APIs (in addition to the already supported OpenAPI and AsyncAPI scoring)

<figure><img src="../../.gitbook/assets/image (141).png" alt=""><figcaption></figcaption></figure>

### Updates to the APIM v2-v4 Comparison Matrix

With APIM 4.6, we’ve added environment-level logs and additional API-level analytics to works towards functional parity between previous API versions and the latest version. The current comparison matrix is shown below:

| Functionality                                                     | Supported in v2 proxy APIs | Supported for v4 proxy APIs | Supported for v4 message APIs |
| ----------------------------------------------------------------- | -------------------------- | --------------------------- | ----------------------------- |
| User Permissions                                                  | ✅                          | ✅                           | ✅                             |
| Properties                                                        | ✅                          | ✅                           | ✅                             |
| Resources                                                         | ✅                          | ✅                           | ✅                             |
| Notifications                                                     | ✅                          | ✅                           | ✅                             |
| Categories                                                        | ✅                          | ✅                           | ✅                             |
| Audit Logs                                                        | ✅                          | ✅                           | ✅                             |
| Response Templates                                                | ✅                          | ✅                           | ✅                             |
| CORS                                                              | ✅                          | ✅                           | ✅                             |
| Virtual Hosts                                                     | ✅                          | ✅                           | ✅                             |
| Failover                                                          | ✅                          | ✅                           | ⚠️ Depends on use case        |
| Health Check                                                      | ✅                          | ✅                           | 🚫                            |
| Health Check Dashboard                                            | ✅                          | 🚫                          | 🚫                            |
| Service Discovery                                                 | ✅                          | 🚫                          | 🚫                            |
| Improved Policy Studio                                            | 🚫                         | ✅                           | ✅                             |
| Debug Mode                                                        | ✅                          | 🚫                          | 🚫                            |
| Plans                                                             | ✅                          | ✅                           | ✅                             |
| Subscriptions                                                     | ✅                          | ✅                           | ✅                             |
| Messages / Broadcasts                                             | ✅                          | ✅                           | ✅                             |
| Documentation - Markdown                                          | ✅                          | ✅                           | ✅                             |
| Documentation - OAS                                               | ✅                          | ✅                           | ✅                             |
| Documentation - AsyncAPI                                          | ✅                          | ✅                           | ✅                             |
| Documentation - AsciiDoc                                          | ✅                          | 🚫                          | 🚫                            |
| Documentation - Home Page                                         | ✅                          | ✅                           | ✅                             |
| Documentation - Metadata                                          | ✅                          | ✅                           | ✅                             |
| Documentation - Translations                                      | ✅                          | 🚫                          | 🚫                            |
| Documentation - Group Access Control                              | ✅                          | ✅                           | ✅                             |
| Documentation - Role Access Control                               | ✅                          | 🚫                          | 🚫                            |
| Documentation - Swagger vs. Redoc Control                         | ✅                          | ✅                           | ✅                             |
| Documentation - Try It Configuration                              | ✅                          | ✅                           | ✅                             |
| Documentation - Nested Folder Creation                            | ✅                          | ✅                           | ✅                             |
| Terms & Conditions on a Plan                                      | ✅                          | ✅                           | ✅                             |
| Tenants                                                           | ✅                          | 🚫                          | 🚫                            |
| Sharding Tags                                                     | ✅                          | ✅                           | ✅                             |
| Deployment History                                                | ✅                          | ✅                           | ✅                             |
| Rollback                                                          | ✅                          | ✅                           | ✅                             |
| Compare API to Previous Versions                                  | ✅                          | ✅                           | ✅                             |
| Analytics                                                         | ✅                          | ⚠️ WIP                      | ⚠️ WIP                        |
| Custom Dashboards                                                 | ✅                          | 🚫                          | 🚫                            |
| Path Mappings                                                     | ✅                          | 🚫                          | 🚫                            |
| Logs                                                              | ✅                          | ✅                           | ✅                             |
| API Quality                                                       | ✅                          | ⚠️ Replaced by API score    | ⚠️ Replaced by API score      |
| API Review                                                        | ✅                          | ✅                           | ✅                             |
| Export API as Gravitee def (+options)                             | ✅                          | ✅                           | ✅                             |
| Export API as GKO spec                                            | ✅                          | ✅                           | ✅                             |
| Import API from Gravitee def (+options)                           | ✅                          | ✅                           | ✅                             |
| Import API from OAS                                               | ✅                          | ✅                           | NA                            |
| Import API from OAS and automatically add policies for validation | ✅                          | ✅                           | <p>NA</p><p><br></p>          |
| Import API from WSDL                                              | ✅                          | 🚫                          | NA                            |
| Add docs page on import of API from OAS                           | ✅                          | ✅                           | NA                            |
| APIs show in platform-level dashboards                            | ✅                          | ✅                           | ✅                             |
| APIs show in platform-level analytics                             | ✅                          | ✅                           | ✅                             |
| API Alerts                                                        | ✅                          | 🚫                          | 🚫                            |

### Wrapping Up

We’re very excited to launch the Kafka Gateway and continue our evolution towards building the world’s leading API and event stream management platform. Don’t hesitate to contact us with any questions or feedback.
