---
description: Validating and managing subscriptions
metaLinks:
  alternates:
    - ./
---

# Subscriptions

In Gravitee API Management, a subscription is the mechanism by which an API publisher controls who can use their API, under what conditions, and with what level of access. API publishers can define policies for approving or rejecting subscription requests to ensure that only authorized consumers can interact with their APIs. API publishers can then refer to subscriptions to track usage metrics, including consumption volume and performance.

Subscriptions can be created, approved, suspended, or revoked, depending on the API consumer’s needs or policy violations. Initially, an API consumer (such as a developer, application, or team) creates a subscription to request access to an API that's managed within Gravitee. During the subscription process, the consumer must select the API [plan](../plans/) they wish to subscribe to. The plans for an API were predefined by the API publisher to set up access criteria and implement usage restrictions, such as rate limits and quotas.

After choosing a plan, a consumer selects an [application](../applications/) to use with the subscription. The application contains information about the user, some of which may be required by the plan. When a subscription is approved, a consumer can use their application credentials to consume the API. In addition to basic types of authentication, Gravitee supports built-in API key management and integration with identity providers (including Gravitee’s own[ Access Management](https://www.gravitee.io/platform/access-management)) for OAuth and JWT support.

### API Product subscriptions

Subscriptions can be associated with either an individual API or an API Product. The subscription list in the Application view displays an **API** or **API Product** label for each subscription to indicate the associated resource type.

When creating a subscription from an Application, the search returns results for both APIs and API Products. Select the desired resource, then choose an available published plan to subscribe to.

### Subscription forms

API administrators can define custom subscription forms that API consumers complete when subscribing to an API plan. Forms are built using Gravitee Markdown (GMD) syntax and collect structured metadata (key-value pairs) stored with each subscription. Subscription forms are scoped to a single environment and are displayed only for plans with security types other than `KEY_LESS`.

#### Management API v2 endpoints

**GET** `/environments/{envId}/subscription-form`

Returns the subscription form for the specified environment. Throws `SubscriptionFormNotFoundException` if the form does not exist.

**PUT** `/environments/{envId}/subscription-form`

Updates the subscription form. The request body must include:

| Property | Type | Description |
|:---------|:-----|:------------|
| `id` | string | Unique identifier for the subscription form |
| `gmdContent` | string | Gravitee Markdown content defining the form structure (required, cannot be null, empty, or whitespace-only) |
| `enabled` | boolean | Visibility flag; when `false`, form is hidden from Portal API |

#### Portal API endpoint

**GET** `/environments/{envId}/subscription-form`

Returns the subscription form for the current environment. Throws `SubscriptionFormNotFoundException` if the form does not exist or if `enabled = false`.

For more information about managing subscriptions:

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Subscription Requests</td><td><a href="subscription-requests.md">subscription-requests.md</a></td></tr><tr><td>Manage Subscriptions</td><td><a href="manage-subscriptions.md">manage-subscriptions.md</a></td></tr><tr><td>Transfer Subscriptions</td><td><a href="transfer-subscriptions.md">transfer-subscriptions.md</a></td></tr></tbody></table>
