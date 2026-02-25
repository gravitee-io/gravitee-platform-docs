# AM Architecture

This page provides details on Gravitee Access Management's (AM) architecture. Before you install and use the product, take a few moments to get to know the AM architecture.

## Global Architecture

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-overview-global-architecture.png" alt=""><figcaption><p>AM global architecture</p></figcaption></figure>

## AM Gateway

AM Gateway is the core component of the AM platform. It acts as a trust broker with your identity providers and provides an authentication and authorization flow for your users.

The gateway uses an event-driven architecture to propagate configuration changes across distributed nodes. When domain settings are updated via the Management API, the system publishes events that all gateway instances subscribe to. For example, when certificate settings are modified, a `DomainCertificateSettingsEvent.UPDATE` event is published, allowing all gateway nodes to reload the settings from the database without requiring a domain restart. This ensures zero-downtime configuration changes across distributed deployments.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-overview-components-gateway.png" alt=""><figcaption><p>AM - Internal Gateway</p></figcaption></figure>
