# Deciding on an Enablement Strategy

This page outlines the enablement strategy for new customers, focusing on the "whole product" approach. Combine technical enablement, such as role-based training and certification, with organizational strategy. This includes defining operating models (centralized, federated, or hybrid) and moving toward an API-as-a-Product management style. Ensure your organization not only installs the software but also drives internal adoption and cultural change.

## Deliverables

* **API Operating Model:** A documented governance structure (centralized, federated, or hybrid).
* **Enablement Plan:** A scheduled curriculum of role-based training and topic-specific workshops.
* **Certified Power Users:** A cohort of team members who have completed level 1 to level 3 certification paths.
* **Strategic Roadmap:** A plan for full-lifecycle management, including sunset policies and business KPI tracking.

## Stakeholders

Involve the following stakeholders in enablement planning:

* **Lead Architect or CTO:** Responsible for defining the operating model and technical standards.
* **API Product Manager:** Responsible for developer experience (DX), documentation, and business value.
* **DevOps and SRE:** Responsible for ecosystem synchronization and observability alignment.
* **Developer Advocate:** Responsible for internal marketing and driving platform adoption.
* **Technical Account Manager (TAM):** Provides personalized guidance and weekly check-ins.

## Prerequisites

* **License:** A valid Gravitee license. Gravitee Enterprise Edition is required for certain advanced workshops.
* **People:** Identification of a dedicated API Product Manager and a Lead Architect.

## Anticipated Duration

* **Two to four weeks:** Initial enablement typically requires six hours of instructor-led sessions plus hands-on implementation, spanning at least one month of onboarding activity.

## Potential Risks and Challenges

* **Shadow IT:** Failure to define a clear operating model can lead to decentralized, unmanaged gateway sprawl.
* **Bottlenecked Delivery:** A strictly centralized model can slow down development teams.
* **Skills Gap:** Teams might lack the Kubernetes or GitOps expertise required for advanced automation.
* **Low Adoption:** Without a "hearts and minds" campaign, developers might resist changing their existing workflows.

## Actions and Activities

### Establish the Enablement Baseline
1. Schedule the initial two-hour remote training session covering Gravitee API Management and Access Management.
2. Register relevant team members for the level 1 (foundations) certification.
3. Set up a recurring weekly check-in with your TAM.

### Define Your Operating Model
Choose between the following operating models:

* **Centralized:** High consistency, where enablement is driven by core Subject Matter Experts (SMEs) and product owners.
* **Federated:** High speed, with localized SMEs in teams to enable and train their own members.
* **Hybrid:** Standardized but decentralized, where enablement is driven by core SMEs but entrusted to localized SMEs.

Document the "golden path" for security and governance that all teams must follow.

### Conduct Role-Based Training
1. Deliver instructor-led general training, typically six hours split into two three-hour sessions.
2. Perform hands-on API building with TAM support to reinforce high-level concepts.
3. Host workshops on specific functionality, such as Kafka, protocol mediation, or the Gravitee Kubernetes Operator (GKO).

### Integrate into the Technical Ecosystem
* **Skills Analysis:** Assess team proficiency with YAML, Kubernetes, and OpenAPI specifications.
* **Observability:** Configure Gravitee analytics to export data to your existing monitoring tools, such as Datadog or Splunk.
* **Legacy Bridge:** Identify any SOAP or COBOL services that require protocol translation.

### Launch Internal Marketing
1. Host an internal hackathon to encourage use of the new Developer Portal.
2. Establish an "API of the month" award to incentivize reuse and high-quality documentation.

## Best Practices

{% hint style="info" %}
Treat APIs as products. Focus on the consumer experience and track Time to First Hello World to measure success.
{% endhint %}

### Use Clear Writing
When documenting internal APIs, keep sentences under 30 words to ensure clarity. Use active voice and direct, imperative language in your internal guides. For example, use "Set the tags property" instead of "The tags property should be set."

### Standardize Product Naming
Ensure Gravitee product names are capitalized correctly, such as API Gateway and Management Console, to maintain professional standards.

### Use the Certification Program
Use the certification program continuously to assess and confirm user knowledge as teams progress from level 1 (foundations) to level 3 (architect).

### Address Technical Debt
Plan for protocol translation early. Your strategy is only as effective as the backends the gateway communicates with.
