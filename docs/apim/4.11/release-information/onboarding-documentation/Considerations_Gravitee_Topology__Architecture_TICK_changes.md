# Gravitee Topology and Architecture

This page focuses on the fundamental decisions required to establish a Gravitee infrastructure. Learn how to select a deployment model (Gravitee Cloud, hybrid, or self-hosted), place API Gateways, and isolate traffic to ensure system stability. Align Gravitee’s Control Plane and Data Plane architecture with your organization's security, latency, and compliance requirements.

## Deliverables

* **Primary Deployment Model:** Selection of Gravitee Cloud, hybrid, or self-hosted.
* **Network Topology Document:** Plan for Gateway placement and inbound and outbound flow rules.
* **Isolation Model:** Defined strategy for shared versus dedicated gateways to manage the blast radius of API traffic.
* **IAM Integration Strategy:** A plan for token validation and identity management.

## Stakeholders

Involve the following stakeholders in architecture planning:

* **Platform and DevOps Engineers:** To manage infrastructure, Kubernetes, or Docker deployment.
* **Architects:** To design the traffic steering and multi-region strategy.
* **Security and Compliance Officers:** To verify data residency and firewall configurations.
* **API Developers:** To define requirements for specific API backend proximity.

## Prerequisites

* **License:** A valid Gravitee license key.
* **Knowledge:** Familiarity with containerization (Docker or Kubernetes), networking (TLS, port 443, DNS), and OIDC or SAML concepts.
* **Infrastructure:** Access to cloud providers (AWS, Azure, GCP) or on-premises servers.

## Anticipated Duration

* **Minimum two weeks:** This involves cross-departmental alignment on security and infrastructure procurement.

## Potential Risks and Challenges

* **Latency Bottlenecks:** Placing gateways too far from backends or consumers.
* **Noisy Neighbor Effect:** A single high-traffic API consuming resources and impacting mission-critical services on a shared gateway.
* **Egress Costs:** High costs associated with shipping logs from cloud gateways to on-premises monitoring tools.
* **Compliance Violations:** Accidentally routing Personally Identifiable Information (PII) across restricted regional boundaries.

## Actions and Activities

### Review Core Concepts
Review the [Gravitee core concepts](https://documentation.gravitee.io/apim/readme/core-concepts) before proceeding.

### Define the Deployment Model
Assess your organizational needs for speed versus control and select Gravitee Cloud, hybrid, or self-hosted. Determine which components you will host (Data Plane) and what Gravitee will manage (Control Plane).

### Plan Gateway Placement
Identify your backend service locations and place gateways as close to them as possible, ideally within your firewall, to reduce latency. Map out regional needs for global traffic steering if consumers are distributed across multiple cloud providers.

### Configure Network and Security
Establish secure outbound connections for hybrid models or internal network routing for self-hosted models. Verify that no inbound firewall rules are required for the gateway-to-control plane connection in a hybrid setup.

### Establish the Infrastructure Environment
Prepare your environment using your preferred tooling, such as Kubernetes (Helm or GKO), Docker, or Linux. Configure database and storage requirements based on your model. Gravitee Cloud manages all storage, while self-hosted models require you to maintain all databases.

### Set Up Identity and Access Management (IAM)
Configure the gateway to trust your existing identity provider (IdP), such as Okta, Auth0, or Microsoft Entra ID. Ensure the gateway can reach the IdP's JWKS endpoint for signature verification.

### Implement Isolation and Scaling
Apply gateway tags (sharding tags) to control which nodes serve specific environments or traffic types. Plan for horizontal and vertical scaling to handle varying workloads.

## Best Practices

{% hint style="info" %}
The hybrid model is recommended for most organizations. It balances operational simplicity with data control.
{% endhint %}

### Manage Secrets
Use an external vault, such as HashiCorp Vault or Azure Key Vault, instead of storing keys and certificates locally on gateway nodes.

### Use the Blast Radius Strategy
Deploy separate gateway clusters for specific business units. This ensures that a failure in one area does not impact others.

### Handle Noisy Neighbors
Avoid using a single large shared gateway for all traffic. Use your topology to separate internal traffic from high-risk, public-facing traffic.

### Ensure Data Residency
Verify that your APIM topology ensures PII remains on regional gateways within the required legal boundaries to comply with regulations like GDPR.
