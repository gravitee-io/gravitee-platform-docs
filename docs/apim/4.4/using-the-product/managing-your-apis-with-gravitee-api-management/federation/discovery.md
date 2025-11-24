---
description: An overview about Discovery.
---

# Discovery

## Overview

The process of an integration connecting to the management API of a 3rd-party provider to discover its assets is known as discovery. Discovery generates an in-memory collection of the assets offered by the 3rd-party provider, which can be used to create different types of Gravitee APIs. Assets that can be discovered by an integration are:

* **APIs:** REST API proxies running on 3rd-party API gateways. The integration can potentially discover their OAS definitions.
* **Event streams:** e.g., Kafka or Solace topics. The integration can potentially discover their AsyncAPI definitions.
* **Documentation:** OAS/AsyncAPI definitions and other suitable assets form a solid foundation for the documentation of federated APIs.
* **Plans:** Assets that satisfy or contribute to Gravitee's concept of a plan, which provides a service and access layer on top of an API that specifies access limits, subscription validation modes, and authentication protocols.

### Scope of discovery

The scope of assets discovered by an integration depends on several factors. For example, instead of an integration automatically discovering every API that belongs to the entire underlying account, discovery is scoped to a subset of the APIs owned by that organization.

Limiting factors include:

* The permissions given to the agent by the 3rd-party account administrator that dictate which resources can be accessed
* Integration-specific parameters that provide a boundary as to which assets should be discovered (e.g., the integration region or stage)
* User-specified filters to narrow discovery based on tags or other metadata
* Asset relevance, e.g., ignoring APIs that are undeployed, in draft mode, or archived

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

* Discovery adds APIs to a collection, but does not modify or delete existing APIs. Repeated discovery only displays APIs that don’t already have a Gravitee counterpart.
* Once an API has been imported, any changes to that same API on the 3rd-party provider will not be imported into Gravitee unless the Gravitee API is deleted and the API is rediscovered.
{% endhint %}
