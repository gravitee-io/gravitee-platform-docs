---
description: Documentation about secure & expose apis in the context of APIs.
---

# Secure & Expose APIs

Gravitee APIM uses plans, applications, and subscriptions to govern API exposure. A published Gateway API is visible in the Developer Portal but cannot be consumed without a published plan. A Keyless plan can be consumed immediately, but all other authentication types require the API consumer to register an application and subscribe to a published plan. This system promotes granular control over API access.

The securing and exposing of your APIs is split into the following categories:

* [#plans](./#plans "mention")
* [#applications](./#applications "mention")
* [#subscriptions](./#subscriptions "mention")

## Plans

To learn more about adding plans to your APIs, see the following articles:

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Keyless</td><td><a href="plans/keyless.md">keyless.md</a></td></tr><tr><td>API Key</td><td><a href="plans/api-key.md">api-key.md</a></td></tr><tr><td>OAuth2</td><td><a href="plans/oauth2.md">oauth2.md</a></td></tr><tr><td>JWT</td><td><a href="plans/jwt.md">jwt.md</a></td></tr><tr><td>Push</td><td><a href="plans/push.md">push.md</a></td></tr><tr><td>mTLS</td><td><a href="plans/mtls.md">mtls.md</a></td></tr></tbody></table>

## Applications

To learn more about creating applications, see the following articles

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Create an Application</td><td><a href="applications/create-an-application.md">create-an-application.md</a></td></tr><tr><td>Global Settings</td><td><a href="applications/global-settings.md">global-settings.md</a></td></tr><tr><td>User and Group Access</td><td><a href="../create-and-configure-apis/configure-v2-apis/user-and-group-access.md">user-and-group-access.md</a></td></tr></tbody></table>

## Subscriptions

To learn more about subscriptions, see the following articles:

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Subscription Requests</td><td><a href="subscriptions/subscription-requests.md">subscription-requests.md</a></td></tr><tr><td>Manage Subscriptions</td><td><a href="subscriptions/manage-subscriptions.md">manage-subscriptions.md</a></td></tr><tr><td>Transfer subscriptions</td><td><a href="subscriptions/transfer-subscriptions.md">transfer-subscriptions.md</a></td></tr></tbody></table>
