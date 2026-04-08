# Gravitee Onboarding Documentation: One Pagers

This document provides a comprehensive collection of one-pagers to guide you through the Gravitee onboarding process. It covers everything from initial goal setting and architecture planning to security, observability, and developer experience.

## Understanding Your Goals and Objectives

This phase focuses on defining the foundational goals and objectives for your Gravitee deployment. By establishing **SMART** (Specific, Measurable, Achievable, Relevant, and Time-bound) objectives, you ensure that the API layer is not just a technical component but a "connective tissue" that drives business value. Move away from a project mindset toward a product-centric approach where APIs are treated as reusable assets that reduce integration debt and enhance organizational agility.

### Deliverables

* **SMART Objectives Document:** A formalized list of goals, such as a 30% reduction in response times or a 60% internal reuse rate.
* **Success Criteria Matrix:** Defined milestones for architecture, deployment, and subscriber onboarding.
* **Use Case Catalog:** Identification of primary internal and external developer engagement goals.
* **Compliance and Governance Framework:** Automated reporting standards and data sovereignty requirements.

### Stakeholders

Involve the following stakeholders in goal setting:

* **API Developers:** To define technical requirements and developer experience (DX).
* **Platform and DevOps Engineers:** To align on infrastructure, cloud economics, and FinOps.
* **Architects:** To design the API strategy and integration patterns.
* **Business Owners and Partners:** To ensure APIs align with revenue goals and partner onboarding.

### Prerequisites

* **People:** A cross-functional discovery team available for initial sessions.
* **Knowledge:** Understanding of existing business pain points and current integration debt levels.

### Anticipated Duration

* **Minimum two weeks:** This allows for comprehensive stakeholder discovery sessions, alignment with broader business strategy, and the finalization of success criteria across different departments.

### Potential Risks and Challenges

* **Integration Debt:** Overlooking the time required to connect legacy internal systems.
* **Zombie APIs:** Redundant or abandoned APIs that increase cloud egress costs and security risks.
* **Regulatory Non-Compliance:** Failure to account for regional data sovereignty or industry-specific mandates like PSD3 or FHIR.
* **Misaligned Objectives:** Setting purely technical goals, such as uptime, while ignoring critical user metrics like Time to First Successful Call.

### Actions and Activities

1. **Conduct Discovery Sessions:** Meet with stakeholders to identify the strengths and weaknesses of existing processes and clarify team availability.
2. **Define SMART Objectives:** Establish measurable targets, such as reducing the Time to First Successful Call for internal developers from weeks to hours.
3. **Identify Primary Use Cases:** Determine if the focus is on streamlining internal processes, increasing external engagement, or both.
4. **Finalize Success Criteria:** Agree on phase-specific milestones, including architecture finalization, the first API deployment, and the Developer Portal launch.
5. **Establish Portfolio Rationalization:** Audit the current environment to identify and decommission "zombie APIs" to optimize cloud economics.
6. **Review and Adjust:** Schedule regular intervals to review performance metrics and adjust objectives based on evolving feedback.

### Best Practices

{% hint style="info" %}
Baseline early to prove the success of your project. Gather information on your status quo so you can compare it to the impact your new solution has had once it is live.
{% endhint %}

* **Document Key Challenges:** Identify the key challenges you face today and consider their outcomes, such as business speed, revenue impact, and cost management.
* **Assign KPIs to Challenges:** For each key challenge, assign a quantifiable KPI or success criterion, such as days to build a new API or anticipated sales growth.
* **Balance Indicators:** Balance leading and lagging indicators. Leading indicators predict future success, while lagging indicators show actual outcomes.
* **Keep It Simple:** Start with five to seven key metrics rather than tracking dozens. You can always add more later.

---

## Planning for API Governance

API governance involves the consistent application of processes, policies, and design rules across the entire API lifecycle. In Gravitee, this ensures that all APIs—internal, external, or legacy—are discoverable, secure, and compliant with organizational standards. This planning phase focuses on moving governance "left" into the design phase to reduce costs and complexity at the gateway level.

### Deliverables

* **API Style Guide:** Organization-wide design standards for naming, versioning, and error formats.
* **Centralized API Catalog:** A single source of truth within the Developer Portal.
* **Automated Governance Rulesets:** Integration of tools like **API Score** into the development workflow.
* **Governance Workflow Definition:** Clear processes for design reviews, approval gates, and governance waivers.

### Stakeholders

Involve the following stakeholders in governance planning:

* **API Center of Excellence (CCoE):** A cross-functional group leading the strategy.
* **Platform and API Architects:** Responsible for technical standards and policy inheritance.
* **Security and Compliance Teams:** To define authentication, such as OAuth 2.0, and data sovereignty rules.
* **Product Managers:** To align API development with business value and unit economics.
* **Legal Team:** To ensure ethical data usage and intellectual property protection.

### Prerequisites

* **License:** Gravitee Enterprise Edition is required for advanced features like **API Score** and **Shared Policy Groups**.
* **People:** A dedicated API owner for every managed endpoint.
* **Knowledge:** Familiarity with OpenAPI and AsyncAPI specifications and Gravitee Expression Language (EL).

### Anticipated Duration

* **Two to four weeks:** Initial planning requires cross-departmental alignment on standards and legal compliance.

### Potential Risks and Challenges

* **Developer Friction:** Overly strict governance can lead to shadow APIs, where teams bypass standards to meet deadlines.
* **API Sprawl:** Managing visibility across multi-gateway environments without a unified control plane.
* **Financial Impact:** Large "cost-to-serve" ratios where cloud compute costs exceed the business value of the API.

### Actions and Activities

1. **Establish Visibility:** Catalog every API into the Developer Portal and tag them by team, lifecycle status, and usage metrics.
2. **Define and Enforce Design Standards:** Create a style guide and use the **API Score** feature to automatically validate API definitions against your style guide.
3. **Expand Automation:** Use toolsets like **API Score** to automate the enforcement of governance standards.
4. **Implement Policy-Based Governance:** Create **Shared Policy Groups** for reusable configurations and apply global policies at the organization or environment level.
5. **Automate the Shift-Left Stack:** Provide developers with local linting rulesets and integrate governance checks into CI/CD pipelines using the Management API or GKO.
6. **Manage the Lifecycle:** Set clear deprecation schedules and use the Developer Portal to guide consumers toward the latest versions.

### Best Practices

{% hint style="info" %}
Govern the intent. Use a contract-first mandate where stakeholders sign off on the API contract before backend code is written.
{% endhint %}

* **Balance Freedom and Control:** Use governance to guide rather than block. Provide templates and "golden paths" to speed up production readiness.
* **Ensure Data Sovereignty:** Use gateway sharding tags to ensure PII for specific regions never leaves an authorized gateway.
* **Implement Federated Governance:** If you use multiple gateway brands, use a federated API control plane for a single point of documentation and access control.
* **Use Governance Waivers:** Establish a waiver workflow for legacy systems that cannot meet modern standards to maintain a path toward compliance.

---

## APIM Implementation Planning

This phase focuses on transitioning from a technical implementation project to a comprehensive API program. Move beyond mere installation to create a sustainable, self-service API ecosystem that delivers long-term business value by aligning stakeholders, establishing rollout phases, and defining governance and compliance.

### Deliverables

* **Jointly Owned Project Plan:** A mutual document with clear task assignments and weekly review cycles.
* **API Style Guide:** Standardized naming conventions, versioning strategies, and error formats.
* **Governance Framework:** Defined processes for API design-first principles and centralized cataloging to prevent shadow APIs.
* **Operational SLA and Support Model:** Clear definitions of support tiers and responsibilities.
* **Success Criteria Report:** Documentation of architecture finalization, core component setup, and initial subscriber onboarding.

### Stakeholders

Involve the following stakeholders:

* **Executive Leadership:** API Product Manager or C-Suite for program ownership.
* **Technical Teams:** API developers, platform engineers, and DevOps engineers.
* **Business Owners:** To identify required versus optional features.
* **Legal and Compliance:** To ensure data residency and Terms of Service alignment.
* **API Champions:** Internal advocates to foster community.

### Prerequisites

* **People:** A dedicated project manager and a cross-functional team available for discovery sessions.

### Anticipated Duration

* **Minimum one week:** For initial alignment and intensive discovery before technical work begins.

### Potential Risks and Challenges

* **Inconsistent APIs:** Without early governance, the Developer Portal may become unorganized.
* **Shadow APIs:** APIs built outside the platform creating security blind spots.
* **Friction-Heavy DX:** If the response from the platform is too slow, developers will seek workarounds.

### Actions and Activities

1. **Identify Project Owners:** Outline the Executive Sponsor, Owner, and Technical SME for the project.
2. **Complete Current State Analysis:** Perform stakeholder interviews to understand requirements and set baselines.
3. **Define Success Criteria:** Determine what success looks like from each stakeholder's perspective.
4. **Prioritize Teams and APIs:** Identify priority teams and APIs, considering "low-hanging fruit" that proves immediate value.
5. **Understand Timelines and Dependencies:** Identify key milestones and dependencies for the project.
6. **Align with the Supplier:** Discuss a mutual action plan with your supplier to complete the implementation.

### Best Practices

{% hint style="info" %}
Treat your APIM platform as a product, not a one-time project.
{% endhint %}

* **Use SMART Criteria:** Avoid vague goals. Use SMART criteria to define completion for each phase.
* **Use a RACI Matrix:** Define who is Responsible, Accountable, Consulted, and Informed for critical decisions.
* **Establish Feedback Loops:** Schedule office hours or create a dedicated Slack channel from day one to capture developer pain points.

---

## Gravitee Topology and Architecture

This section outlines the fundamental decisions required to establish a Gravitee infrastructure, including selecting a deployment model and placing API Gateways strategically to ensure system stability.

### Deliverables

* **Primary Deployment Model:** Selection of Gravitee Cloud, hybrid, or self-hosted.
* **Network Topology Document:** Plan for gateway placement and inbound and outbound flow rules.
* **Isolation Model:** Strategy for shared versus dedicated gateways to manage the blast radius.
* **IAM Integration Strategy:** A plan for token validation and identity management.

### Stakeholders

Involve platform engineers, architects, security officers, and API developers.

### Prerequisites

* **License:** A valid Gravitee license key.
* **Knowledge:** Familiarity with containerization, networking (TLS, port 443, DNS), and OIDC or SAML.
* **Infrastructure:** Access to cloud providers or on-premises servers.

### Anticipated Duration

* **Minimum two weeks:** For cross-departmental alignment on security and infrastructure.

### Actions and Activities

1. **Define the Deployment Model:** Assess organizational needs and select the appropriate model.
2. **Plan Gateway Placement:** Place gateways as close to backend service locations as possible to reduce latency.
3. **Configure Network and Security:** Establish secure outbound connections for hybrid models or internal routing for self-hosted models.
4. **Set Up IAM:** Configure the gateway to trust your existing identity provider (IdP).
5. **Implement Isolation and Scaling:** Apply gateway tags (sharding tags) to control traffic and plan for scaling.

### Best Practices

{% hint style="info" %}
The hybrid model is recommended for most organizations as it balances operational simplicity with data control.
{% endhint %}

* **Manage Secrets:** Use an external vault instead of storing keys and certificates locally on gateway nodes.
* **Use the Blast Radius Strategy:** Deploy separate gateway clusters for specific business units.
* **Ensure Data Residency:** Verify that your topology ensures PII remains on regional gateways within required legal boundaries.

---

## Outlining and Provisioning Hardware Requirements

This section provides resource allocation guidelines for Gravitee APIM components to ensure optimal performance under load.

### Deliverables

* **Infrastructure Specification:** Defined specs for Gravitee Gateway instances.
* **Resource Baseline:** Resource requirements for the Management Console, Developer Portal, and databases.
* **Scalable Deployment Strategy:** Strategy for horizontal and vertical scaling.

### Prerequisites

* **License:** A valid Gravitee license key for Enterprise Edition features.
* **Knowledge:** Understanding of expected RPS and policy complexity.

### Anticipated Duration

* **One week:** For traffic analysis and resource provisioning.

### Actions and Activities

1. **Identify Your Traffic Profile:** Determine if your environment is small, medium, or large.
2. **Provision Gateway Resources:** Allocate CPU and RAM based on your deployment method (Kubernetes or VM-based).
3. **Configure Heap Memory:** Set the gateway heap size ensuring the JVM has sufficient memory.
4. **Deploy Control Plane Components:** Provision instances for the Developer Portal and Management Console.
5. **Set Up Databases:** Configure MongoDB or JDBC for configuration and Elasticsearch for analytics.
6. **Enable High Availability:** Deploy at least two nodes for the API Gateway and Alert Engine.

### Best Practices

{% hint style="info" %}
Prefer horizontal scaling (adding more replicas) over increasing the size of a single instance.
{% endhint %}

* **Monitor CPU Usage:** Consider adding gateway replicas when sustained load exceeds 75%.
* **Plan for Logging Storage:** Allocate approximately 0.5 GB of storage in Elasticsearch per million requests for advanced logging.

---

## Configuring Firewall and Whitelisting

This section outlines network security configurations and firewall strategies for Gravitee across different deployment models.

### Deliverables

* **Network Security Perimeter:** A defined perimeter based on your deployment model.
* **IP Filtering Policies:** Configured policies at the API level.
* **Firewall Rules:** Established rules for Control Plane and Data Plane communication.

### Actions and Activities

1. **Identify Your Deployment Model:** Determine the security constraints for your architecture.
2. **Configure Load Balancer Headers:** Ensure the API Gateway identifies the original requester's IP by configuring headers like `X-Forwarded-For`.
3. **Implement API-Level Filtering:** Apply the **IP Filtering** policy in the Management Console to allowed or denied IPs/CIDR ranges.
4. **Layer External Protections:** Deploy a WAF for Layer 7 protection and use DDoS protection services.

### Best Practices

{% hint style="info" %}
Limit outbound access to authorized identity providers and backend services to prevent the gateway from being used as a "jump box."
{% endhint %}

* **Use the Sinkpool Strategy:** Route non-matching requests to a dead-end backend to consume attacker bandwidth.
* **Use mTLS:** Mutual TLS provides cryptographic proof of identity, which is more secure than simple IP whitelisting.

---

## Planning for Gravitee Access and SSO

This section outlines the strategy for securing the Gravitee ecosystem, recommending delegation to an external IdP for production.

### Deliverables

* **Authentication Strategy:** Selection of federated SSO or local authentication.
* **Access Control Model:** Defined RBAC mapping for all users.
* **Security Hardening:** Removal of default credentials and configuration of recovery paths.

### Actions and Activities

1. **Select Your Identity Source:** Choose between an external IdP or managing users within Gravitee.
2. **Configure Authentication:** Update your `gravitee.yml` with the appropriate credentials and endpoints.
3. **Establish Role Mapping:** Ensure users have the correct permissions immediately upon login.
4. **Remove Default Accounts:** Address default accounts like `admin` before production.
5. **Define Emergency Access:** Maintain one emergency local account for "break-glass" scenarios.

### Best Practices

{% hint style="info" %}
Gravitee can federate multiple identity sources into a single login layer to support different user types simultaneously.
{% endhint %}

* **Use Local Authentication Appropriately:** Local authentication is for PoCs or air-gapped environments, but SSO is preferred for production.
* **Define Password Reset Workflows:** Local users require an administrative workflow for password resets as there is no self-service feature.

---

## Planning for API Authentication

This page outlines the selection of authentication mechanisms within Gravitee to secure API resources, from simple keys to complex OIDC.

### Deliverables

* **Authentication Strategy:** A mapping of API use cases to specific consumer plans.
* **Security Configuration Schema:** Validated settings for JWKS URLs and issuer constraints.
* **Threat Protection Suite:** Rules for JSON, XML, and regex threat protection.

### Actions and Activities

1. **Define the Authentication Model:** Select between API Key, JWT, or OAuth 2.0 based on client type.
2. **Configure the IdP Connection:** Gather OIDC metadata and ensure network line-of-sight.
3. **Create a Gravitee Plan:** Create a new plan in the Management Console and input security constraints.
4. **Map Scopes to Policies:** Link identity claims to gateway-level permissions.
5. **Layer Threat Protection:** Add threat protection policies to the API flow.
6. **Secure the Backend Connection:** Configure mTLS between the gateway and backend microservices.

### Best Practices

{% hint style="info" %}
Use the **JWT policy** for performance or across networks. Use the **OAuth 2.0 policy** for opaque tokens requiring introspection.
{% endhint %}

* **Use Token Redaction:** Configure tools to automatically redact `Authorization` headers.
* **Set Token Lifetimes:** Use short-lived access tokens (5 to 15 minutes) combined with refresh token rotation.
* **Secure Web Applications:** Use secure, `HttpOnly` cookies or a BFF pattern to mitigate risks.

---

## Planning for Gateway Deployment

This section focuses on the strategic assessment of infrastructure models and resilience strategies for gateway deployment.

### Deliverables

* **Architecture Design:** Finalized gateway model and regional placement.
* **Capacity Plan:** Plan based on throughput (RPS) and payload analysis.
* **Gateway Environment:** High-availability environment integrated with observability and security.

### Actions and Activities

1. **Select Deployment Model:** Choose between Gravitee Cloud, hybrid, or self-hosted.
2. **Size and Scale:** Analyze peak RPS and payload sizes for resource requirements.
3. **Define Topologies:** Group gateways logically by function or security zone.
4. **Configure Resilience:** Set up active-active clusters with anti-affinity rules.
5. **Automate Deployment:** Use IaC like Terraform or Helm for managing configurations.

### Best Practices

{% hint style="info" %}
Gateways cache configuration and will continue to process traffic even if the control plane is unavailable.
{% endhint %}

* **Use Rolling Updates:** Ensure zero downtime during upgrades by using rolling update strategies.
* **Use Redis for Rate Limiting:** Prevent memory bottlenecks in high-throughput environments by using Redis for rate limiting.

---

## Deciding on an Enablement Strategy

This section outlines the enablement strategy for new customers, focusing on technical training and organizational operating models.

### Deliverables

* **API Operating Model:** Documented governance structure (centralized, federated, or hybrid).
* **Enablement Plan:** Curriculum for role-based training and workshops.
* **Certified Power Users:** Cohort of members through level 1 to level 3 certification.

### Actions and Activities

1. **Establish Enablement Baseline:** Schedule trainer-led sessions and register for certifications.
2. **Define Your Operating Model:** Select between centralized, federated, or hybrid models.
3. **Conduct Role-Based Training:** Deliver instructor-led general and specialized workshops.
4. **Launch Internal Marketing:** Host hackathons and establish recognition programs for API quality.

### Best Practices

{% hint style="info" %}
Treat APIs as products and focus on the consumer experience to drive adoption.
{% endhint %}

* **Use Clear Writing:** Keep internal guide sentences under 30 words and use active voice.
* **Standardize Product Naming:** Maintain professionalism by using correct capitalization for Gravitee products.
* **Use the Certification Program:** Continuously assess knowledge as teams progress through certification levels.

---

## Preparing to Build Your First API

This section covers the foundational phase of the API lifecycle, from selecting API types to publishing on the portal.

### Deliverables

* **API Contract and Design Strategy:** Defined strategy for design and development.
* **Protocol Mediation Configuration:** Entrypoints and endpoints configured for mediation.
* **Published API:** Discoverable API with documentation on the Developer Portal.

### Actions and Activities

1. **Choose Your API Type:** Select between proxy or event-native APIs.
2. **Choose Your Design Approach:** Use a design-first approach with the **Gravitee API Designer**.
3. **Plan Entrypoints and Endpoints:** Define interaction methods and backend destinations.
4. **Apply Policies:** Use **Policy Studio** to add security and transformation policies.
5. **Publish to the Developer Portal:** Provide usage guidelines and code samples to ensure a low TTFHW.

---

## Setting Up Observability

This section outlines the strategy for implementing monitoring, analytics, and alerting across your Gravitee ecosystem.

### Deliverables

* **Monitoring Framework:** Defined set of KPIs and metrics.
* **Alerting System:** Real-time notifications for critical system events.
* **Operational Dashboards:** Visibility into API usage and infrastructure health.

### Actions and Activities

1. **Define Key Metrics:** Identify core data points like error codes, latency, and request volumes.
2. **Use Built-in Dashboards:** Access immediate insights through the Management Console dashboards.
3. **Configure Alert Engine:** Set up real-time alerts for critical events and SLO breaches.
4. **Enable External Integrations:** Use reporters to export data to your enterprise observability stack.
5. **Implement Advanced Logging:** Configure per-API logging and use data masking for PII protection.

### Best Practices

{% hint style="info" %}
Focus on the four golden signals: latency, traffic, errors, and saturation.
{% endhint %}

* **Use Outside-In Monitoring:** Supplement gateway metrics with regional synthetic probes.
* **Integrate with Security Tools:** Pipe logs into a SIEM for anomaly detection and audit trails.

---

## Setting Up Analytics

This page outlines a comprehensive strategy for API measurement and analytics beyond native capabilities.

### Deliverables

* **Integrated Observability Stack:** Correlation between gateway metrics and infrastructure health.
* **BI Sync:** Automated pipelines into corporate BI and CRM tools.
* **Compliance Framework:** Documented process for data masking and Right to Erasure.

### Actions and Activities

1. **Establish the Baseline:** Export logs and enable distributed tracing for long-term analysis.
2. **Integrate Business Data:** Connect usage data to internal ERP or billing systems.
3. **Configure Guardrails:** Apply masking policies and define data residency.
4. **Deploy Synthetic Monitoring:** Set up external tools to measure availability from the customer's perspective.

### Best Practices

{% hint style="info" %}
Understand the difference between RUM (native) and synthetic monitoring (proactive) for a complete availability picture.
{% endhint %}

* **Use Data Redaction:** Define masking strategies with your legal team first to ensure compliance.
* **Track Long-Term Trends:** Export data to long-term storage as gateway retention periods are shorter.

---

## Setting Up Logging and Support

This section ensures your Gravitee deployment remains performant and secure through robust logging and a multi-tier support model.

### Deliverables

* **Logging Policy:** A policy that balances observability with performance.
* **LogGuard Protection:** Safeguards against memory-related crashes.
* **Support Matrix:** A defined L1–L3 matrix for incident resolution.

### Actions and Activities

1. **Configure Logging Thresholds:** Define global limits in `gravitee.yml` and enable **LogGuard**.
2. **Implement Per-API Logging:** Set specific logging levels and use conditions to conserve resources.
3. **Secure and Route Data:** Add masking policies and configure reporters to forward logs asynchronously.
4. **Establish the Support Matrix:** Assign responsibilities to Service Desk, Platform Team, and Producers.

### Best Practices

{% hint style="info" %}
Ensure backend services accept `X-Gravitee-Request-Id` to allow support teams to stitch requests across multiple systems.
{% endhint %}

* **Define Log Retention:** Match external backend settings to industry compliance requirements.
* **Monitor for Memory Pressure:** Use the `gc-pressure` health probe and adjust thresholds based on traffic patterns.

---

## Consumer Journey and Experience

This section outlines the strategic foundation for rolling out the Developer Portal and defining the consumer journey.

### Deliverables

* **Segmented Audience Map:** User groups with specific access levels.
* **Branded Portal:** Customized interface matching corporate identity.
* **Subscription Workflows:** Documented approval paths and plan structures.

### Actions and Activities

1. **Define Audience and Access:** Segment users and determine visibility rules.
2. **Configure Authentication:** Integrate your IdP for seamless registration and sign-in.
3. **Publish Documentation:** Upload specifications and enable **Try It Now** features.
4. **Set Up Plans:** Create plans and define manual or automatic subscription workflows.
5. **Brand the Experience:** Use the theme editor and create custom landing pages.

### Best Practices

{% hint style="info" %}
Offer copy-paste code samples in multiple languages and optimize for a low Time to First Hello World.
{% endhint %}

* **Focus on Use Cases:** Highlight the value proposition on landing pages rather than just listing endpoints.
* **Manage the Lifecycle:** Use targeted notifications for deprecations or maintenance to keep developers informed.

---

## Developer Portal Best Practices

This page focuses on establishing a high-quality API Catalog and Developer Portal to ensure APIs are discoverable and easy to consume.

### Deliverables

* **Centralized API Catalog:** Searchable catalog with logical categories.
* **Self-Service Portal:** Features for automated onboarding and key provisioning.
* **Analytics Dashboards:** Dashboards for providers and consumers to monitor usage.

### Actions and Activities

1. **Define Information Architecture:** Organize APIs logically and use a design-first approach.
2. **Configure Access Flows:** Set up plans and implement SSO or LDAP for internal consumers.
3. **Establish Golden Paths:** Provide templates for new APIs pre-configured with security standards.
4. **Populate Documentation:** Upload specs and ensure every API includes usage examples.
5. **Enable Self-Service:** Configure automatic provisioning to reduce administrative overhead.

### Best Practices

{% hint style="info" %}
Interactive OpenAPI documentation is not enough. Supplement it with conceptual guides and step-by-step tutorials.
{% endhint %}

* **Treat the Portal as a Product:** Assign a product owner to monitor adoption metrics and user feedback.
* **Use Descriptive Link Text:** Avoid "click here." Use descriptive terms to improve accessibility and SEO.
* **Plan for API Retirement:** Use sunset banners to provide a clear migration path for consumers.
