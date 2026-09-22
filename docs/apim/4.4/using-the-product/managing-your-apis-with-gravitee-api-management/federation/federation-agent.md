---
description: An overview about Federation Agent.
---

# Federation Agent

## Overview

A federation agent is an executable (e.g., `docker-compose` and configuration files) that integrates with a 3rd-party provider and communicates with an integration defined in Gravitee. For an integration to function, its associated agent to be properly configured and deployed. Agents are necessary because the Gravitee control plane (APIM Console and Management API) may not have direct network access to the 3rd-party provider’s management API.

<figure><img src="../../../.gitbook/assets/federation agent diagram.png" alt="A diagram of federated APIs and events, with the control plane above the dotted line connecting consumers, the portal and console, an agent, and API providers, and the data plane below connecting an application to third-party gateways and event brokers."><figcaption></figcaption></figure>
