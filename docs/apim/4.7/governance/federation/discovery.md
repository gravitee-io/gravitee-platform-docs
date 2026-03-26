---
description: An overview about discovery.
---

# Discovery

## Overview

The process of an integration connecting to the management API of a 3rd-party provider to discover its assets is known as discovery. Assets that can be discovered by an integration are:

* **APIs:** REST API proxies running on 3rd-party API gateways. The integration can potentially discover their OAS definitions.
* **Event streams:** e.g., Kafka or Solace topics and their schemas. The integration can potentially discover their AsyncAPI definitions.
* **Productisation and consumption related objects like API products and Plans:** Assets that satisfy or contribute to Gravitee's concept of a plan, which provides a service and access layer on top of an API that specifies access limits, subscription validation modes, and authentication protocols.

## Scope of discovery

The scope of assets discovered by an integration depends on several factors. For example, instead of an integration automatically discovering every API that belongs to the entire underlying account, discovery is scoped to a subset of the APIs owned by that organization.

Limiting factors include:

* The permissions given to the agent by the 3rd-party account administrator that dictate which resources can be accessed
* Filter parameters that are provided as part of the agent's configuration and provide a boundary as to which assets should be discovered (e.g., the AWS stage, Solace application domain, or Confluent topic prefix)
* Asset relevance, e.g., ignoring APIs that are undeployed, in draft mode, or archived, or not part of an API product

## Discovery execution

Discovery must be executed to initially import APIs, then subsequently if the scope of discovery has changed or new 3rd-party APIs are discoverable.

{% hint style="warning" %}
To execute the discovery process, the user must have at least the READ permission on integrations and the CREATE permission on APIs.
{% endhint %}

1. Log in to your APIM Console
2. Select **Integrations** from the left nav
3. Click on the integration you're interested in
4. Select **Overview** from the inner left nav
5. Ensure the agent status is **Connected**
6. Click the **Discover** button

{% hint style="info" %}
Impact on existing APIs

* Discovery provides the option to add new APIs to a collection, if new APIs are discovered on the 3rd-party provider
* Discovery provides the option to update existing APIs that were previously discovered. In this case, changes to attributes made in Gravitee will be overwritten by conflicting attributes coming from the 3rd-party.
{% endhint %}
