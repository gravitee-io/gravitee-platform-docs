# Configuring Firewall and Whitelisting

This page outlines network security configurations and firewall strategies for Gravitee across different deployment models, including Gravitee Cloud, hybrid, and self-hosted. Learn how to implement IP whitelisting at the infrastructure and gateway levels, manage outbound connection requirements, and integrate with security layers like Web Application Firewalls (WAF) and Zero Trust architectures.

## Deliverables

* **Network Security Perimeter:** A defined perimeter based on your chosen deployment model.
* **IP Filtering Policies:** Configured policies at the API level.
* **Firewall Rules:** Established rules for Control Plane and Data Plane communication.
* **External Security Integration Plan:** A plan for WAF and DDoS protection.

## Stakeholders

Involve the following stakeholders in network security planning:

* **Network Security Engineers:** To manage firewall rules, WAF configurations, and load balancer settings.
* **Platform Engineers:** To handle infrastructure-level whitelisting and Kubernetes ingress annotations.
* **API Developers:** To implement **IP Filtering** policies within Gravitee.
* **Identity and Access Management (IAM) Team:** To coordinate mTLS and token-based security.

## Prerequisites

* **License:** A valid Gravitee Enterprise Edition license for specific features.
* **People:** Access to network administrators with permissions to modify cloud or on-premises firewalls.
* **Knowledge:** Understanding of CIDR notation, `X-Forwarded-For` headers, and TLS/mTLS concepts.

## Anticipated Duration

* **Minimum 1 week:** This accounts for security reviews, firewall change request windows, and cross-departmental testing.

## Potential Risks and Challenges

* **Client IP Obfuscation:** If load balancers do not forward the real client IP, IP Filtering policies might incorrectly block legitimate traffic.
* **Gravitee Cloud Limitations:** Lack of direct private network integration without internet exposure in full cloud models.
* **Static Defense Weakness:** Relying solely on IP whitelisting can be bypassed by IP spoofing or rotation from cloud consumers.

## Actions and Activities

### Identify Your Deployment Model
Determine the security constraints for your architecture:

* **Gravitee Cloud:** Use ingress-level whitelisting for Kubernetes-based infrastructure.
* **Hybrid:** Ensure Gateways can make outbound TLS connections to port 443. No inbound rules are required for the Control Plane.
* **Self-Hosted:** Configure internal firewall policies for all communication. Protect the Bridge Gateway and Management Console at the ingress level.

### Configure Load Balancer Headers
To ensure the API Gateway identifies the original requester's IP:

1. Configure your load balancer to inject the `X-Forwarded-For` or `X-Real-IP` header.
2. In Gravitee, verify that the gateway trusts these headers from your specific load balancer IP.

### Implement API-Level Filtering
1. Log in to the Management Console.
2. Select your API and apply the **IP Filtering** policy.
3. Add allowed or denied IPs or CIDR ranges. The policy supports both IPv4 and IPv6.
4. For partners with multiple IPs, group them into CIDR blocks to maintain a clean configuration.

### Layer External Protections
* **WAF:** Deploy a WAF for Layer 7 protections, such as SQL injection and cross-site scripting (XSS), which IP filtering cannot stop.
* **DDoS Protection:** Use edge services to scrub volumetric traffic before it reaches your Gravitee subnet.

## Best Practices

{% hint style="info" %}
Do not forget egress filtering. While teams often focus on inbound traffic, ensure your firewall also controls where your API Gateway can communicate. Limit outbound access to authorized identity providers and backend services.
{% endhint %}

### Use the Sinkpool Strategy
Instead of only blocking traffic, use your WAF to route requests that do not match your API patterns to a "sinkpool." A sinkpool is a dead-end backend with no resources. This consumes the attacker's bandwidth without impacting your services.

### Use mTLS
In modern cloud environments, IPs rotate frequently. Mutual TLS (mTLS) provides cryptographic proof of identity. Requiring a valid certificate is more secure because it identifies the client regardless of their network or IP.
