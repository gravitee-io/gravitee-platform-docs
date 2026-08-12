---
title: Gravitee Kubernetes Operator 4.13 Release Notes
---

# GKO 4.13

This page describes the new features and breaking changes introduced in GKO 4.13.

## Highlights

* The Kubernetes Gateway API implementation is upgraded to Gateway API v1.6.1.
* A Gateway serves several domains on the same port, each with its own TLS certificate, using Server Name Indication (SNI).
* HTTPRoute resources support method matching, host rewrite, backend request header modification, and H2C backends.

{% hint style="info" %}
The Gateway API updates listed on this page are also available in GKO 4.12 starting with version 4.12.11.
{% endhint %}

## Breaking changes

This release changes how the Gateway API controller handles one existing field.

### Gateway infrastructure parameters are rejected

In earlier releases, GKO ignored the `spec.infrastructure.parametersRef` field of a `Gateway` resource. A Gateway that sets `spec.infrastructure.parametersRef` is now rejected: its `Accepted` condition is set to `False`, with a message reporting that the parameters reference isn't supported. Use the `GatewayClassParameters` resource to configure Gravitee-specific settings instead.

## New features

The following features extend the Kubernetes Gateway API support in GKO.

#### Gateway API v1.6.1

GKO builds against Kubernetes Gateway API v1.6.1 and installs the v1.6.1 standard channel CRDs. The conformance report for this release is published in the [GKO repository](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/test/conformance/kubernetes.io/gateway-api/report).

#### Multi-domain TLS with SNI

A Gateway accepts several HTTPS listeners on the same port, each with its own hostname and TLS certificate. The deployed Gateway presents the certificate matching the requested server name through SNI, and requests reach the listener with the most specific matching hostname. For details, see [Configure multi-domain TLS on a Gateway](../../guides/gateway-api/multi-domain-tls.md).

#### HTTPRoute feature coverage

HTTPRoute resources support method matching, host rewrite through `URLRewrite`, backend request header modification on rules that declare a single `backendRef`, and backend Services that advertise `appProtocol: kubernetes.io/h2c`. For details, see [HTTPRoute](../../guides/gateway-api/httproute.md).

#### Client certificate validation on HTTPS listeners

The `spec.tls.frontend` field of a `Gateway` resource configures client certificate validation for HTTPS listeners, with a default configuration and per-port overrides. The CA bundle comes from a ConfigMap that contains a `ca.crt` key, and the deployed Gateway then requires client certificates on the configured port.

#### Cross-route matching

The `gatewayAPI.controller.matchAcrossRoutes` Helm option merges HTTPRoute resources with overlapping context paths on the same Gateway into a single API definition, so matching works across routes. The option is disabled by default. For details, see [HTTPRoute](../../guides/gateway-api/httproute.md).

#### Gateway infrastructure metadata

Labels and annotations set under `spec.infrastructure` of a `Gateway` resource propagate to the Kubernetes resources GKO creates for the Gateway deployment.
