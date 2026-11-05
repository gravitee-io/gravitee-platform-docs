---
description: Overview of Compatibility.
---

# Compatibility and limitations

In its early iterations, the Gravitee Kubernetes Operator (GKO) focused on managing the most important aspect of any API Management platform: the APIs themselves. Over time, GKO has evolved to manage API documentation pages, API access controls, API resources (such as authentication servers and caches), and more. In the future, GKO will continue to expand its reach to cover new parts of the API lifecycle.&#x20;

## Compatibility

As of GKO 4.4, GKO follows a strict compatibility policy whereby a given minor version of GKO requires the same minor version of APIM. As such, GKO 4.4 is compatible with APIM 4.4.

GKO 4.3 is compatible for the most part with APIM 4.3, 4.2, and 4.1. GKO 4.3 is based on the same codebase as GKO 0.13.1 and was tagged as 4.3 in order to make the new support policy easier to follow.&#x20;

## Known limitations and future direction

Below are some examples of resources that are not managed by GKO. Not all of these will come under management by GKO, but some will. Please reach out to us if you'd like to talk about expanding GKO's scope in one of these areas.

**API-level** elements that are not managed by GKO:

* Notification settings
* Picture & background
* Alerts
* Documentation page translations
* Documentation page attached resources (aka API Media)
* V4 API primary owner management

GKO does not manage any **environment-level** objects such as:

* Subscriptions and/or keys
* Platform-level common policies
* APIM dictionaries
* Developer Portal themes

GKO does not manage other **Gravitee components** such as:

* Gravitee gateway
* Gravitee Access Management
* Gravitee Alert Engine

