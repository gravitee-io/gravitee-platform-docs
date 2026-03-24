# JavaScript Policy (New) Reference

## Overview

The JavaScript Policy (New) enables API administrators to execute custom JavaScript logic during request and response processing using a sandboxed GraalJS engine. It supports both V4 Proxy and V4 Message APIs, allowing dynamic header manipulation, content transformation, and conditional routing without deploying custom plugins. The policy enforces strict security boundaries to prevent unauthorized system access.

## Key Concepts

### Sandboxed Execution

JavaScript code runs in an isolated GraalJS context that blocks Java interop, file system access, network operations, thread manipulation, process execution, reflection, ClassLoader access, and environment variable access. Standard JavaScript `eval()`, `console.log()`, `console.error()`, `btoa()`, and `atob()` remain available. Console output routes to SLF4J logging.

### Content Processing Modes

The policy supports three content handling modes controlled by `readContent` and `overrideContent` flags:

| Mode | `readContent` | `overrideContent` | Behavior |
|:-----|:--------------|:------------------|:---------|
| Pass-through | `false` | `false` | Script executes without body access; body unchanged |
| Read-only | `true` | `false` | Script reads body via `content()` method; body unchanged |
| Transform | `true` | `true` | Script reads and modifies body; modified content replaces original |

### Execution Timeout

JavaScript execution is limited by a configurable timeout (default 100ms, range 10–10,000ms). Scripts exceeding the timeout terminate with a 500 error and `"Timeout"` message. Timeout values outside the valid range are clamped to the nearest boundary.

## Prerequisites

- Gravitee API Management 4.x (V4 API architecture)
- Gateway API version 5.0.0-alpha.2 or later
- V4 Proxy API or V4 Message API (V2 APIs not supported)

## Gateway Configuration

### Execution Timeout

Configure the global JavaScript execution timeout in the gateway configuration file:

| Property | Type | Default | Valid Range | Description |
|:---------|:-----|:--------|:------------|:------------|
| `policy.js.timeout` | Long | `100` | 10–10,000 | JavaScript execution timeout in milliseconds |

Values below 10ms are raised to 10ms. Values above 10,000ms are reduced to 10,000ms. If the configuration component is unavailable, the default 100ms applies.

## Creating a JavaScript Policy


Add the JavaScript Policy to a flow in the [API Management Console](../../../guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md) or via the Management API.
 Configure the `script` property with your JavaScript code (e.g., `request.headers().set('X-Custom', 'value');`). Enable `readContent` if your script needs to access the request or response body via the `content()` method. Enable `overrideContent` if your script returns modified content that should replace the original body. The policy executes during REQUEST, RESPONSE, MESSAGE_REQUEST, or MESSAGE_RESPONSE phases depending on the flow configuration. Empty or blank scripts pass through without execution.

## Policy Configuration

### Script Properties

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `script` | String | `"request.headers().set('X-Custom', 'value');"` | JavaScript code to execute |
| `readContent` | boolean | `false` | Enable body access via `content()` method |
| `overrideContent` | boolean | `false` | Enable content replacement with script return value |

### API Bindings

Scripts access the following objects:

- `request` — read and modify request headers, query parameters, path parameters, and attributes
- `response` — read and modify response headers and attributes
- `content()` — read request or response body (requires `readContent: true`)
- `result` — control execution flow with `result.fail(statusCode, message, key)` to short-circuit processing
- `Base64` — encode/decode with `Base64.encode(string)` and `Base64.decode(string)`
- `btoa(string)` / `atob(string)` — Base64 encoding/decoding (aliases for `Base64` methods)
- `console.log()` / `console.error()` — log to SLF4J

## Restrictions

- V2 APIs not supported (V4 Proxy and V4 Message APIs only)
- Timeout range enforced: 10ms minimum, 10,000ms maximum
- `overrideContent: true` requires `readContent: true` (override without read is invalid)
- Java interop blocked: `Java.type()`, `Polyglot.eval()` unavailable
- File system, network, thread, process, reflection, and ClassLoader operations blocked
- `Base64.encode(null)` and `Base64.decode(null)` throw `IllegalArgumentException`
- `atob(null)` and `btoa(null)` throw `IllegalArgumentException` with message `"atob/btoa requires a string argument"`
- Script timeouts return HTTP 500 with error key `JS_EXECUTION_FAILURE` and message `"Timeout"`
- Script exceptions return HTTP 500 with error key `JS_EXECUTION_FAILURE` and message `"JavaScript execution failed"`

## Related Changes

The policy integrates with the V4 Gateway API reactive execution model and supports both proxy and message entrypoints. GraalVM JS engine version was downgraded from 24.1.1 to 23.1.10 for compatibility. Integration tests use Gravitee entrypoint-http-get and entrypoint-http-post version 2.1.0 with reactor-message 10.0.0-alpha.2. Console logging routes to SLF4J via gravitee-node-logging 8.0.0-alpha.10.
