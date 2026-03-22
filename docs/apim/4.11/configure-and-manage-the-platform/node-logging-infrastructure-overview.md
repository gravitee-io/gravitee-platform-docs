# Node Logging Infrastructure Overview

## Overview

The Node Logging Infrastructure enriches log output with contextual metadata using SLF4J's Mapped Diagnostic Context (MDC). It provides centralized logger factories, runtime pattern overrides, and ArchUnit rules to enforce consistent logging practices across Gateway and REST API components. This feature is for platform administrators configuring log formats and developers implementing context-aware logging in plugins and handlers.

## Prerequisites

- Gravitee APIM 4.x or later (gravitee-node 8.0.0+, gravitee-gateway-api 5.0.0+)
- SLF4J-compatible logging backend (Logback recommended)
- For Helm deployments: Helm chart version supporting `logback.override` and `node.logging.*` values
- Write access to `gravitee.yml` or Helm chart values

{% hint style="info" %}
Not all plugins have been migrated to use the Node Logging Infrastructure. Some logs may lack contextual information. Migration is in progress for .
{% endhint %}
