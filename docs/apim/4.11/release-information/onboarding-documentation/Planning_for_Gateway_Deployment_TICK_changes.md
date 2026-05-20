# Planning for Gateway Deployment

This page focuses on the strategic assessment of infrastructure models, performance requirements, and resilience strategies for Gravitee gateway deployment. Learn how to align these factors with your organizational needs to ensure high availability, optimal throughput, and seamless operational control.

## Deliverables

* **Architecture Design:** A finalized design for the gateway model and regional placement.
* **Capacity Plan:** A defined plan based on throughput (RPS) and payload analysis.
* **Gateway Environment:** A deployed, high-availability gateway environment integrated with your existing observability and security stacks.

## Stakeholders

Involve the following stakeholders in gateway deployment planning:

* **Infrastructure and Cloud Architects:** To manage Kubernetes setup and networking.
* **API Platform Team:** To configure gateways and manage policies.
* **Security Team:** To manage TLS, authentication (OAuth 2.0 or OIDC), and compliance requirements.
* **DevOps and SRE:** To manage automation (CI/CD) and monitoring or alerting integration.

## Prerequisites

* **Knowledge:** Proficiency in Kubernetes or container orchestration and API lifecycle management.
* **Infrastructure:** Access to cloud providers, such as AWS, Azure, or GCP, or on-premises data centers and load balancers.
* **Tools:** Terraform or Helm for Infrastructure as Code (IaC) and established observability stacks, such as Elasticsearch or New Relic.
* **External Dependencies:** Redis instances for implementing rate limiting.

## Anticipated Duration

* **Varies by complexity:** Duration ranges from a few days for Gravitee Cloud implementations to several weeks for complex hybrid or self-hosted global architectures.

## Potential Risks and Challenges

* **Resource Contention:** Insufficient memory or CPU allocation that can cause latency.
* **Configuration Drift:** Inconsistent settings across environments without GitOps.
* **Observability Gaps:** A lack of visibility into gateway health for cloud-hosted setups.

## Actions and Activities

### Select a Deployment Model
Choose between Gravitee Cloud, hybrid, or self-hosted based on your control needs.

### Size and Scale the Environment
Analyze peak RPS, payload sizes, and plugin intensity to determine resource requirements.

### Define Topologies
Group gateways logically by function, security zone, or department. For example, deploy gateways for internal APIs separately from those for externally facing APIs.

### Map Networks and Regions
Deploy gateways physically close to backend services to minimize latency.

### Configure Resilience and High Availability
Set up active-active clusters with anti-affinity rules.

### Integrate Security
Configure authentication providers and TLS management.

### Automate Deployment
Implement IaC, such as Terraform or Helm, and CI/CD pipelines to manage configuration.

### Monitor the Environment
Connect gateways to your existing observability and alerting stacks.

## Best Practices

{% hint style="info" %}
Gateways cache the last-known configuration. They will continue to process traffic even if the control plane becomes unavailable, ensuring resilience.
{% endhint %}

### Use Rolling Updates
Use rolling updates with `maxUnavailable=0` and `maxSurge=1` to maintain zero downtime during upgrades.

### Use Redis for Rate Limiting
Use Redis for rate limiting in high-throughput environments to prevent memory bottlenecks.

### Synchronize Versions
Keep gateway and bridge versions synchronized, particularly in hybrid deployments.
