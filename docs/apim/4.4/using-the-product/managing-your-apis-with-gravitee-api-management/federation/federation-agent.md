---
description: An overview about Federation Agent.
---

# Federation Agent

## Overview

A federation agent is an executable (e.g., `docker-compose` and configuration files) that integrates with a 3rd-party provider and communicates with an integration defined in Gravitee. For an integration to function, its associated agent to be properly configured and deployed. Agents are necessary because the Gravitee control plane (APIM Console and Management API) may not have direct network access to the 3rd-party provider’s management API.

<figure><img src="../../../../../../.gitbook/assets/federation agent diagram (1).png" alt=""><figcaption></figcaption></figure>
