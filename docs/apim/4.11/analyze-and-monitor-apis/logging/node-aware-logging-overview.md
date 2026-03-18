# Node-Aware Logging Overview

## Overview

Node-aware logging enriches log entries with contextual metadata using SLF4J's Mapped Diagnostic Context (MDC). This feature enables distributed tracing and request correlation across Gateway and REST API components by automatically injecting identifiers such as node ID, API ID, environment ID, organization ID, application ID, and plan ID into every log entry.

Node-aware logging is designed for platform administrators managing multi-node deployments and developers building custom policies or plugins.
