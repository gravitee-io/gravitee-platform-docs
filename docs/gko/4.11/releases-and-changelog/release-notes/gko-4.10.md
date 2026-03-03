---
Gravitee Kubernetes Operator 4.10 Release Notes.
---

# GKO 4.10

## Highlights

This release brings bug fixes and new features focused on HTTP Client configuration, and **official Gateway API v1.3 partial conformance** recognition.

## New Features

**GKO HTTP Client configuration enhancements**

* Management APIs connection through proxy. 
* Support for custom CA certificates outside of `/etc/ssl/certs`.
* Connection timeout

Refer to the Helm Chart section to know how to configure proxy URL & auth, timeouts and CAs.
All of the above were back-ported to 4.8.x and 4.9.x versions of GKO.

**Windowed Count Sample Strategy**

This release adds support for the Windowed Count sampling strategy for message APIs.

## Gateway API Conformance

We're excited to announce that **Gravitee Kubernetes Operator 4.10 is now officially recognized** as a **Partially Conformant** implementation of the Kubernetes Gateway API specification version 1.3! The Gravitee Kubernetes Operator is now officially listed on the [Gateway API implementations page](https://gateway-api.sigs.k8s.io/implementations/#gravitee-kubernetes-operator), joining a select group of gateway providers recognized by the Kubernetes community.

This milestone, first achieved in version 4.8.5, recognizes our commitment to providing a standards-compliant API gateway solution for Kubernetes environments.

### What This Means for You

**Gravitee Kubernetes Operator 4.10** delivers partial conformance for Gateway and HTTPRoute resources, enabling you to leverage the Gateway API standard for managing your API infrastructure. While the current implementation focuses on core Gateway and HTTPRoute functionality with Kubernetes Core v1 services, we're working on expanding support for additional matching rules across routes and alternative service types in upcoming releases.
