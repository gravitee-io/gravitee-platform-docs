# Context-aware logging

## Overview

Gravitee Gateway and Management API enrich log entries with request metadata — such as API ID, organization, environment, application, and plan — via MDC (Mapped Diagnostic Context). This lets operators filter and correlate logs across multi-tenant environments without manual instrumentation.

{% hint style="info" %}
Context-aware logging is available from APIM 4.11 onward. Not all plugins have been migrated yet — some logs may lack contextual information until the migration is complete in 4.12.
{% endhint %}

## How it works

Gravitee components use `NodeLoggerFactory` instead of SLF4J's `LoggerFactory` to create loggers. `NodeLoggerFactory` wraps each logger with node-level metadata (node ID, hostname, application name). It then delegates to extensible MDC registration hooks that inject request context.

The `%mdcList` custom Logback converter formats selected MDC keys into log output. Administrators control which keys appear, how they're formatted, and how they're separated through `gravitee.yml` properties.

### Available MDC keys

The following MDC keys are available depending on the component:

<table>
    <thead>
        <tr>
            <th width="180">Key</th>
            <th width="120">Gateway</th>
            <th width="120">Management API</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>nodeId</code></td>
            <td>Yes</td>
            <td>Yes</td>
            <td>Gravitee node identifier</td>
        </tr>
        <tr>
            <td><code>nodeHostname</code></td>
            <td>Yes</td>
            <td>Yes</td>
            <td>Node hostname</td>
        </tr>
        <tr>
            <td><code>nodeApplication</code></td>
            <td>Yes</td>
            <td>Yes</td>
            <td>Node application name</td>
        </tr>
        <tr>
            <td><code>apiId</code></td>
            <td>Yes</td>
            <td>Yes</td>
            <td>API identifier</td>
        </tr>
        <tr>
            <td><code>apiName</code></td>
            <td>Yes</td>
            <td>-</td>
            <td>API name</td>
        </tr>
        <tr>
            <td><code>apiType</code></td>
            <td>Yes</td>
            <td>-</td>
            <td>API type</td>
        </tr>
        <tr>
            <td><code>envId</code></td>
            <td>Yes</td>
            <td>Yes</td>
            <td>Environment identifier</td>
        </tr>
        <tr>
            <td><code>orgId</code></td>
            <td>Yes</td>
            <td>Yes</td>
            <td>Organization identifier</td>
        </tr>
        <tr>
            <td><code>appId</code></td>
            <td>Yes</td>
            <td>Yes</td>
            <td>Application identifier</td>
        </tr>
        <tr>
            <td><code>planId</code></td>
            <td>Yes</td>
            <td>-</td>
            <td>Plan identifier</td>
        </tr>
        <tr>
            <td><code>user</code></td>
            <td>Yes</td>
            <td>-</td>
            <td>Authenticated user</td>
        </tr>
        <tr>
            <td><code>correlationId</code></td>
            <td>-</td>
            <td>Yes</td>
            <td>Request correlation identifier</td>
        </tr>
    </tbody>
</table>

**Gateway-specific keys by API type:**

- **HTTP, Message, A2A, LLM, MCP APIs:** `serverId`, `contextPath`, `requestMethod`
- **TCP APIs:** `serverId`, `sni`
- **Native Kafka APIs:** `connectionId`, `Principal`

For configuration details, see [Node logging configuration](node-logging-configuration.md).
