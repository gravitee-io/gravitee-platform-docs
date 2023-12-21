---
description: Learn more about Gravitee Cockpit
---

# Introduction to Gravitee Cockpit

## Introduction

Previously Cockpit, Gravitee Cockpit is the environment management solution and “homepage” for your entire Gravitee platform.

Here, you can:

* Add and manage various Gravitee API Management and Access Management installations and environments
* Promote APIs across higher and lower environments
* Get started with an enterprise API Management free trial. The trial now includes pre-seeded APIs and a demo application so that you can test out all these new Gravitee 4.0 features without connecting your own application or building all new APIs.

## Gravitee Cockpit hierarchy

Gravitee Cockpit is based on a hierarchy of the following entity types:

<figure><img src=".gitbook/assets/image (1) (1).png" alt=""><figcaption><p>Gravitee Cockpit hierarchy</p></figcaption></figure>

<table><thead><tr><th width="264.008547008547">Entity</th><th>Description</th></tr></thead><tbody><tr><td>Account</td><td>The top level entity, your company. One user can have multiple accounts.</td></tr><tr><td>Organization</td><td>A logical part of your company in the way that makes most sense in your setup, for example a region or business unit. There can be multiple organizations linked to one account.</td></tr><tr><td>Environment</td><td>An environment in an IT infrastructure, such as development or production. There can be multiple environments linked to one organization.</td></tr><tr><td>APIM and AM installations, linked to environments in Gravitee Cockpit. Each linked APIM and AM installation automatically reports its REST API and Gateway nodes to Gravitee Cockpit.</td><td><p>Nodes can belong to multiple environments. You can configure the organizations and environments associated with Gateway nodes in APIM and AM, by updating the Gateway configuration files.</p><p>Only Gateway nodes are configurable in this way, not REST API nodes.</p></td></tr></tbody></table>

Each entity managed in Gravitee Cockpit has some common properties:

* ID: an internal ID that is never shown in the Gravitee Cockpit UI, but that you can find if you look at the API responses.
* HRID: a human readable ID of the entity. This ID is unique (no two environments in the same organization can have the same HRID), and they are used to provide readable URLs.
* Name: the name of the entity.
* Description: a description of the entity.

## Example hierarchy

The Gravitee Cockpit hierarchy pictured below has the following setup:

* One APIM installation, with two Gateway nodes and one REST API node.
* One AM installation, with one Gateway node and one REST API node.

<figure><img src=".gitbook/assets/image (7).png" alt=""><figcaption><p>Example hierarchy</p></figcaption></figure>
