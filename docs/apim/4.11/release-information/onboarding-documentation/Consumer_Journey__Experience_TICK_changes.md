# Consumer Journey and Experience

This page defines the strategic foundation for rolling out a Gravitee **Developer Portal**. Learn how to define the consumer journey, from initial discovery and SEO optimization to registration, subscription management, and long-term retention. Create a self-service ecosystem that minimizes manual intervention while maximizing developer success and reducing Time to First Hello World (TTFHW).

## Deliverables

* **Segmented Audience Map:** Defined user groups, such as internal, partner, and public, with specific access levels.
* **Branded Self-Service Portal:** A customized interface matching your corporate identity for API discovery and management.
* **Subscription Workflows:** Documented approval paths, such as automatic versus manual, and plan structures.
* **Analytics Dashboard:** Tools for consumers to monitor their usage and performance.

## Stakeholders

Involve the following stakeholders in consumer experience planning:

* **API Owners:** To define documentation, plans, and approval workflows.
* **Platform Engineers:** To handle infrastructure, SSO integration, and portal implementation.
* **Marketing and Brand Team:** To customize themes, logos, and landing page content.
* **Legal and Compliance:** To manage Terms of Service (ToS) versioning and privacy consent.
* **Product Management:** To oversee monetization strategies and usage quotas.

## Prerequisites

* **License:** An active Gravitee license.
* **People:** A technical lead for portal configuration and a content owner for documentation.
* **Knowledge:** Familiarity with OpenAPI and AsyncAPI specifications and identity provider (IdP) protocols like OIDC or SAML.

## Anticipated Duration

* **Two to three weeks:** One week for strategy and branding, one week for technical setup and SSO, and one week for content and testing.

## Potential Risks and Challenges

* **Manual Approval Bottlenecks:** High friction during the subscription phase can hinder developer momentum.
* **Outdated Documentation:** If API specifications, such as OpenAPI, are not synchronized, the portal loses trust.
* **SEO and AI Visibility:** Failure to optimize for search engines and AI agents can result in low portal traffic.
* **Bill Shock:** A lack of transparency in usage metrics for monetized plans can lead to disputes.

## Actions and Activities

### Define Audience and Access
Segment users into groups, such as internal, external, and public. Determine visibility rules for your API catalog.

### Configure Authentication
Integrate your IdP, such as GitHub, Google, or corporate SSO, for seamless registration and sign-in.

### Organize the Catalog
Categorize APIs and tag them by popularity or functionality to enable efficient search and filtering.

### Publish Documentation
Upload OpenAPI, AsyncAPI, or Markdown files. Enable **Try It Now** features for interactive testing.

### Set Up Plans and Subscriptions
1. Create plans, such as Keyless, API Key, or JWT plans.
2. Define subscription workflows. Select automatic approval for low-risk tiers and manual review for sensitive data.

### Brand the Experience
Use the theme editor to adjust colors, fonts, and logos. Create custom landing pages that highlight specific use cases.

### Implement Management Tools
Configure the analytics dashboard so consumers can track their usage milestones and logs.

### Establish Support Channels
Add FAQs, guides, and an integrated support ticketing system within the portal.

## Best Practices

{% hint style="info" %}
Offer copy-paste code samples in multiple languages, such as Python, Go, and JavaScript, to reduce developer friction.
{% endhint %}

### Optimize for Time to First Hello World
Use mock servers or limited public tiers to provide instant access without waiting for manual approval.

### Focus on Use Cases
Write landing page copy that highlights the value proposition, such as "Process payments in five minutes," rather than only listing endpoints.

### Manage the Lifecycle Proactively
Use targeted notifications for version deprecations or scheduled maintenance to keep developers informed.

### Ensure Legal Transparency
Maintain versioned Terms of Service and an independent status page to build long-term trust.

### Leverage AI Optimization
Use structured metadata, such as Schema.org, to ensure your documentation is crawlable by AI agents and search engines.
