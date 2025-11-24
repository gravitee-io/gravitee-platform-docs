---
description: 'API documentation for API Exposure: Plans, Applications, & Subscriptions.'
---

# API Exposure: Plans, Applications, & Subscriptions

Gravitee APIM uses plans, applications, and subscriptions to govern API exposure. A published Gateway API is visible in the Developer Portal but cannot be consumed without a published plan. A Keyless plan can be consumed immediately, but all other authentication types require the API consumer to register an application and subscribe to a published plan. This system promotes granular control over API access.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Plans</strong></td><td>Instead of requiring external tools and backend modification to support API access, APIM deploys Gateway APIs with plans that can quickly iterate on and extend functionality</td><td></td><td><a href="plans/">plans</a></td></tr><tr><td><strong>Applications</strong></td><td>An application allows an API consumer to register and agree to a plan, resulting in a subscription, and allows an API publisher to monitor and control API access</td><td></td><td></td></tr><tr><td><strong>Subscriptions</strong></td><td>An API consumer uses a registered application to create a subscription request to a published plan</td><td></td><td><a href="subscriptions.md">subscriptions.md</a></td></tr></tbody></table>
