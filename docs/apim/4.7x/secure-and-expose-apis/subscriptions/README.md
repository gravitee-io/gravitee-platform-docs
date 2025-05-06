---
description: Validating and managing subscriptions
---

# Subscriptions

In Gravitee API Management, a subscription is the mechanism by which an API publisher controls who can use their API, under what conditions, and with what level of access. API publishers can define policies for approving or rejecting subscription requests to ensure that only authorized consumers can interact with their APIs. API publishers can then refer to subscriptions to track usage metrics, including consumption volume and performance.

Subscriptions can be created, approved, suspended, or revoked, depending on the API consumer’s needs or policy violations. Initially, an API consumer (such as a developer, application, or team) creates a subscription to request access to an API that's managed within Gravitee. During the subscription process, the consumer must select the API [plan](../plans/) they wish to subscribe to. The plans for an API were predefined by the API publisher to set up access criteria and implement usage restrictions, such as rate limits and quotas.

After choosing a plan, a consumer selects an [application](../applications/) to use with the subscription. The application contains information about the user, some of which may be required by the plan. When a subscription is approved, a consumer can use their application credentials to consume the API. In addition to basic types of authentication, Gravitee supports built-in API key management and integration with identity providers (including Gravitee’s own[ Access Management](https://www.gravitee.io/platform/access-management)) for OAuth and JWT support.
