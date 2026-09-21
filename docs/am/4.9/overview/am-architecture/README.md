---
description: How Access Management 4.9 is put together, covering the global architecture and the role of the AM Gateway. See how it fits before you install.
---

# AM Architecture

This page provides details on Gravitee Access Management's (AM) architecture. Before you install and use the product, take a few moments to get to know the AM architecture.

## Global Architecture

<figure><img src="../../.gitbook/assets/graviteeio-am-overview-global-architecture.png" alt="An architecture diagram in which admins and developers reach the Console and tools reach the API, while end users and their apps reach the Gateway, which authenticates against external identity providers over OIDC, OAuth, SAML, and CAS."><figcaption><p>AM global architecture</p></figcaption></figure>

## AM Gateway

AM Gateway is the core component of the AM platform. It acts as a trust broker with your identity providers and provides an authentication and authorization flow for your users.

<figure><img src="../../.gitbook/assets/graviteeio-am-overview-components-gateway.png" alt="A diagram of the AM Gateway with flows processing and audit processing at its centre, serving end users and apps through sign-in, MFA, consent, and token capabilities, each backed by external providers and standards."><figcaption><p>AM - Internal Gateway</p></figcaption></figure>
