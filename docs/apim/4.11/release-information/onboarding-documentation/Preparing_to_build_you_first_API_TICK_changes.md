# Preparing to Build Your First API

This page covers the foundational phase of the API lifecycle within Gravitee. Learn how to select API types, define design approaches (design-first versus wizard-based), and plan the protocol mediation required to expose synchronous or asynchronous event streams to consumers.

## Deliverables

* **API Contract and Design Strategy:** A defined strategy for API design and development.
* **Protocol Mediation Configuration:** Configured entrypoints and endpoints for mediation.
* **Published API:** An API published on the Developer Portal with associated documentation and plans.

## Stakeholders

Involve the following stakeholders in API development:

* **API Developers:** To build and consume APIs.
* **Architects:** To design API strategies and integration patterns.
* **Platform Engineers:** To manage the underlying infrastructure and deployment.
* **Technical Writers:** To ensure Developer Portal content is clear and usable.

## Prerequisites

* **License:** A valid Gravitee license key. Gravitee Enterprise Edition is required for features like specific security policies or message validation.
* **People:** A cross-functional team, including a developer and a platform administrator.
* **Knowledge:** Familiarity with RESTful naming conventions, versioning strategies like Semantic Versioning (SemVer), and basic networking, such as HTTP and TCP.

## Anticipated Duration

* **Minimum one week:** This allows for initial design, iterative testing of two to three simple APIs, and documentation setup.

## Potential Risks and Challenges

* **Database-as-an-API:** Tight coupling between database schemas and API endpoints can lead to breaking changes.
* **Versioning Complexity:** Failure to define a deprecation policy or versioning strategy early in the process.
* **Protocol Mismatch:** Misconfiguring the entrypoint versus the endpoint during protocol mediation, such as HTTP to Kafka.
* **Onboarding Friction:** High Time to First Hello World (TTFHW) if the Developer Portal or documentation is unclear.

## Actions and Activities

### Choose Your API Type
Decide between a standard proxy or an event-native API, such as exposing Kafka or MQTT streams.

### Choose Your Design Approach
Use **Gravitee API Designer** for a design-first approach, or import existing specifications like OpenAPI or WSDL.

### Plan Entrypoints and Endpoints
Define how consumers will interact with the API, such as via webhooks, Server-Sent Events (SSE), or GET requests, and where the API Gateway sends traffic.

### Define Your Plans
Create the contract for your consumers. Specify the authentication mechanism, such as JWT, OAuth 2.0, or mTLS, and set rate limits.

### Apply Policies in Policy Studio
Add security, transformation, or validation policies to the request, response, or message phases.

### Develop and Test
Implement best practices, such as throttling, and thoroughly test endpoints for reliability and security.

### Set Up Observability
Configure monitoring in the Management Console to track response times and error rates.

### Publish to the Developer Portal
Make the API discoverable by publishing usage guidelines and code samples.

## Best Practices

{% hint style="info" %}
Aim for a low Time to First Hello World. Include language-specific SDKs and idiomatic designs, such as camelCase for iOS or snake_case for Python.
{% endhint %}

### Use Domain-Driven Design (DDD)
Use nouns rather than verbs in URLs. For example, use `/orders` instead of `/getOrders`. Keep resources flat rather than deeply nested.

### Standardize Your Error Taxonomy
Provide standardized JSON error objects with clear codes and links to documentation instead of generic 404 errors.

### Implement Idempotency
For write operations like POST, ensure your backend supports an `Idempotency-Key` header to handle network retries gracefully.

### Apply Strict Input Validation
Be strict about what you accept from consumers but flexible about what you send back to ensure backward compatibility.

### Select a Versioning Strategy
SemVer is the industry standard. Path-based versioning, such as `/v1/products`, is common, while header-based versioning keeps URLs cleaner but can be more difficult to test.

### Identify Enterprise Features
Identify features restricted to the Enterprise Edition using a warning hint box in your internal documentation.
