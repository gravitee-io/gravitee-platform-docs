# Outlining and Provisioning Hardware Requirements

This page provides resource allocation guidelines for Gravitee API Management (APIM) components. It covers conceptual sizing based on traffic volume and API count, as well as specific hardware requirements for both Kubernetes and VM-based deployments. Proper sizing ensures the **Data Plane** and **Control Plane** remain performant under varying loads.

## Deliverables

* **Infrastructure Specification:** A defined specification for Gravitee Gateway instances.
* **Resource Baseline:** A resource baseline for the Management Console, Developer Portal, and backend databases.
* **Scalable Deployment Strategy:** A strategy for horizontal and vertical scaling.

## Stakeholders

Involve the following stakeholders in hardware provisioning:

* **Platform Engineers:** To provision Kubernetes or VM resources.
* **Architects:** To design the deployment model, such as self-hosted or hybrid.
* **DevOps Engineers:** To configure Helm charts or installation scripts.

## Prerequisites

* **License:** A valid Gravitee license key for Enterprise Edition features.
* **People:** Personnel with expertise in Kubernetes, Linux administration, or Gravitee architecture.
* **Knowledge:** Understanding of expected Requests Per Second (RPS) and the complexity of planned policies, such as transformations or logging.

## Anticipated Duration

* **One week:** This includes traffic analysis, resource provisioning, and initial environment validation.

## Potential Risks and Challenges

* **Payload Complexity:** Large payloads or memory-intensive policies, such as transformations or encryption, can increase memory consumption beyond baseline estimates.
* **Storage Exhaustion:** Analytics and advanced payload logging can consume disk space rapidly if not monitored.
* **Under-provisioning:** High CPU load above 75% can lead to increased latency and gateway instability.

## Actions and Activities

### Review the Resourcing Guide
Review the latest information in the [Gravitee resourcing guide](https://documentation.gravitee.io/apim/prepare-a-production-environment/gateway-resource-sizing-guidelines).

### Identify Your Traffic Profile
Determine if your environment fits a small, medium, or large gateway profile based on API count and RPS.

### Provision Gateway Resources
Allocate CPU and RAM based on your deployment method:

* **Kubernetes:** Use 500 millicore CPU and 512 MB RAM for small profiles, up to 1,000 millicore and 1,024 MB RAM for large profiles.
* **VM-based:** Use 1 vCPU and 1 GB RAM for small profiles, up to 4 vCPU and 2 GB RAM for large profiles.

### Configure Heap Memory
Set the gateway heap size to ensure the JVM has sufficient memory for processing. For example, use 128 MB for small Kubernetes deployments or 1 GB for large VM deployments.

### Deploy Control Plane Components
Provision instances for the Developer Portal, Management Console, and Management API. We recommend 2 vCPU and 4 GB RAM if these components are combined.

### Set Up Backend Databases
* **Configuration Database:** Configure MongoDB or JDBC with 1 vCPU and 2 GB RAM.
* **Analytics Database:** Configure Elasticsearch with at least 1 vCPU and 2 GB RAM.

### Enable High Availability
Deploy at least two nodes for the API Gateway and Alert Engine to ensure system resilience.

## Best Practices

{% hint style="info" %}
Prefer horizontal scaling (adding more replicas) over increasing the size of a single instance.
{% endhint %}

### Monitor CPU Usage
Monitor CPU usage and consider adding gateway replicas when sustained load exceeds 75%.

### Plan for Logging Storage
Advanced logging and payload capture increase storage needs. Allocate approximately 0.5 GB of storage in **Elasticsearch** per million requests.

### Provision for Rate Limiting
If you use a **Redis** database for rate limiting, provision at least 2 vCPU and 4 GB RAM for the Redis instance.
