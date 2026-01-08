---
description: Configuration guide for federation.
metaLinks:
  alternates:
    - ./
---

# Federation

## Why federation

{% hint style="warning" %}
If you're hosting Gravitee yourself, then Federation is **deactivated by default**. To enable it, please refer to the dedicated sections in the installation guide of choice:

* [Enable Federation when installing with Kubernetes](https://documentation.gravitee.io/apim/install-and-upgrade/kubernetes#federation)
* [Enable Federation when installing with Docker Compose](../../self-hosted-installation-guides/docker/docker-compose.md#enable-federation)
* [Enable Federation when installing with .zip](../../self-hosted-installation-guides/.zip.md#federation)
{% endhint %}

A growing number of organizations have an IT footprint that extends across multiple clouds and multiple enterprise software solutions. All of these systems contain valuable data and services that your organization can use to get ahead. As architects and platform engineers, your success will be measured against your ability to harness this complexity to the benefit of the business. This means two things:

1. **Governance**: maintaining up-to-date knowledge and control of the solutions used in the organization, ensuring they meet the organization’s standards in terms of security, quality, and consistency.
2. **Developer experience**: ensuring that developers inside and outside the organization can easily discover, consume, build upon, and even configure these systems.

It just so happens that the systems you need to govern and productize for your developers often take the form of APIs deployed on different enterprise products, whether they’re REST APIs running on Gravitee, AWS API Gateway, and IBM API Connect, or event streams running on message-based systems like Kafka or Solace.

Beyond APIs, you might be thinking why not apply the same approach to centralize access to integrations from your iPaaS solution, or OpenAPI or AsyncAPI specifications spread across Github repositories, to name a few examples.

Developers are struggling to find and consume what they need because everything is spread across multiple platforms and technologies. Each platform has its own portal or catalog, and its own way of handling access control. Developers are wasting days or weeks in long email chains before they can start building applications that deliver value to the business.

## Manage APIs and event streams from any vendor

Gravitee is known as the leading full-lifecycle API management solution that natively supports both synchronous and asynchronous APIs across a wide range of protocols.

Today, many of the same API management principles can also be applied to APIs and event streams deployed on AWS API Management, Azure API Management, IBM API Connect, Apigee, Confluent, and Solace, with many more to come. We call this federated API management, and it is accelerating Gravitee’s vision to become the API management platform for any type of API running on any platform.

Thanks to the integrations we support, you can now:

* Discover APIs, OAS & AsyncAPI definitions, API products, Kafka schemas, and other useful metadata from 3rd-party providers
* Ingest these as first-class citizens into Gravitee’s API management platform
* Enrich these assets with documentation and access controls
* Publish these assets for discovery by developers on the Gravitee Developer Portal
* Manage subscription requests from developers, providing them with API keys or OAuth tokens that will allow them to directly consume the 3rd-party systems, without having to go through the Gravitee gateway

Developers no longer need to navigate to different catalogs or portals to discover useful APIs and event streams, they can find them all in one place.

## Centralized API subscription management

Whether your API is running on IBM API Connect, Solace, or anything in between, Gravitee can take care of managing requests from developers to subscribe to and consume your APIs.

The screenshot below shows the vanilla Gravitee Developer Portal that includes an API from AWS. Hitting the “Subscribe” button will allow any developer to easily obtain an API key to directly consume the underlying AWS API.

By integrating concepts like API Products and Plans from 3rd-party platforms, Gravitee can expose these concepts to your developers who will be able to request subscriptions for their applications to consume these APIs. Gravitee acts as a middleman, allowing you, the admin team, to accept or reject subscription requests before they are forwarded to the 3rd-party platform.

JWT, OAuth, and API key subscriptions can be configured according to your needs, including integrations with external authorization servers to perform token generation and validation.
