---
description: >-
  Release notes for Gravitee API Management 4.14, covering new features,
  improvements, breaking changes, and deprecations. Browse the full list of
  changes.
---

# APIM 4.14

## Highlights

* The New Developer Portal lists the AI Workspaces that a user is a member of, with the budget, consumption, endpoint path, API key, and models of each one.
* The Management API reference lists the Portal API once per Developer Portal: **Next Gen Portal** for the New Developer Portal, the entry to build a custom developer portal on, and **Classic Portal** for the Classic Developer Portal.

## New Features

APIM 4.14 adds the following features.

#### **AI Workspaces in the New Developer Portal**

* With **Enable AI Workspaces** turned on in the **Portal capabilities** of the Portal Settings, the New Developer Portal shows **My Workspace**, which lists the AI Workspaces that the logged-in user is a member of. The setting is off by default and requires an Enterprise license.
* The details of an AI Workspace show the allocated budget, the tokens, requests, and spend of the last 30 days, the endpoint path, a request snippet for the selected model and client, the user's API key, and the models with their input and output prices.
* A user becomes a member when an administrator adds them to an AI Workspace in Agent Management.
* For more information, see [Show AI Workspaces in the Developer Portal](../../developer-portal/new-developer-portal/show-ai-workspaces-in-the-developer-portal.md).

#### **Kafka Gateway**

* A native Kafka API endpoint group can set **Backend metadata max age (seconds)** on its **Configuration** tab. With a value above `0`, each gateway instance sends its own all-topics metadata request to the brokers at most about once per that many seconds, instead of on every new client connection. The field is empty by default, which applies the gateway-wide default of `0`: one request per connection, as before.
* The gateway configuration gains a default max age for the endpoint groups, Kafka clusters, and Virtual Clusters that set none of their own, and a setting that lets Virtual Cluster metadata refreshes reuse one connection per backend. Both are also Helm values.
* With a max age above `0`, a topic that a gateway instance hasn't seen yet is looked up on the brokers the first time a client fetches from it, and gateway instances that share a distributed cache share the topics they learn.
* In Event Stream Management, a Cluster or a Virtual Cluster sets the same max age for every Kafka Service bound to it.
* The feature also ships in APIM 4.13.2.
* For more information, see [Configure native Kafka API endpoints](../../kafka-gateway/create-and-configure-kafka-apis/configure-kafka-apis/endpoints.md#bound-the-gateways-own-metadata-requests) and [Configure the Kafka Client & Gateway](../../kafka-gateway/configure-the-kafka-client-and-gateway.md#set-the-default-backend-metadata-max-age).

#### **Portal API reference for each Developer Portal**

* The **API** selector of the Management API reference lists the Portal API twice. **Next Gen Portal** lists the operations of the New Developer Portal, and **Classic Portal** lists the operations of the Classic Developer Portal. An operation common to both Developer Portals appears in both entries.
* Build a custom developer portal on the **Next Gen Portal** entry. Operations that only the Classic Developer Portal uses, for example API ratings, tickets, and application alerts, appear only under **Classic Portal**.
* A link saved with the single **Portal** entry of earlier versions opens **Next Gen Portal**, unless it points to an operation that only **Classic Portal** lists.
* In the Portal API specification, each operation declares the entry it's listed under in its `x-gravitee-portal` field: `classic`, `next`, or `both`.
* For more information, see [Management API Reference](../../management-api-reference.md).
