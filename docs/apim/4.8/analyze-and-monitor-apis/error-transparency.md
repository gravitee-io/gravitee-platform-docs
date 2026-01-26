# Error Transparency

## Overview

Error Transparency is a feature in Gravitee APIM that provides clear, actionable diagnostics when errors occur during API execution. This feature helps API publishers troubleshoot issues independently by exposing detailed information about the root cause of failures and warnings.

### Key benefits

* **Improved visibility**: Clearly identify which component (policy, endpoint, or internal system) caused a failure
* **Actionable diagnostics**: Receive human-readable error messages with specific details about what went wrong
* **Self-service troubleshooting**: Resolve common issues without contacting support
* **Warning tracking**: Monitor non-fatal issues before they become critical problems

### What's included

When an error or warning occurs, you receive structured diagnostic information containing:

* **Key**: A unique identifier for the error type
* **Message**: A human-readable description of what went wrong
* **Component type**: The source of the error (POLICY, ENDPOINT, INTERNAL, etc.)
* **Component name**: The specific component identifier (policy ID, endpoint ID, etc.)

This diagnostic information is available in:

* **Runtime Logs**: Detailed trace views with error context
* **Analytics Dashboard**: Error overview and trends
* **Metrics**: Integrated with Elasticsearch and other reporters

{% hint style="info" %}
Error Transparency is available for V4 APIs and V2 APIs running on the V4 execution engine. It is displayed in Console V2 only.
{% endhint %}

---

## Prerequisites

Before using Error Transparency, ensure you have:

* **Gravitee APIM 4.5+** installed
* **V4 APIs** or **V2 APIs with V4 emulation** enabled
* **Analytics backend** configured (Elasticsearch recommended)
* **Access to Console V2** UI

### Recommended configuration

Enable warning reporting in your gateway configuration to track non-fatal issues:

```yaml
# gravitee.yml
reporters:
  warnings:
    enabled: true  # Default: true
```

Or via environment variable:

```bash
export REPORTERS_WARNINGS_ENABLED=true
```

---

## How it works

### Error detection and reporting flow

1. **Error occurs**: A policy, endpoint, or internal component encounters an issue during API execution
2. **Component tracking**: The gateway automatically captures the component type and identifier
3. **Diagnostic creation**: Structured diagnostic information is generated with error details
4. **Metrics attachment**: The diagnostic is attached to request metrics
5. **Reporter processing**: Metrics are sent to configured reporters (Elasticsearch, JSON, CSV, etc.)
6. **UI display**: Diagnostics appear in Console V2 Runtime Logs and Analytics

### Types of diagnostics

#### ExecutionFailure

Represents a fatal error that interrupts request processing. Common examples:

* Invalid API key (401)
* Backend connection failure (502)
* Request timeout (504)
* Expression language evaluation error (500)

#### ExecutionWarn

Represents a non-fatal issue that doesn't interrupt execution but indicates a potential problem. Examples:

* Rate limit repository unavailable (call passes through)
* Degraded backend performance
* Policy configuration warnings

---

## View error diagnostics

### In Runtime Logs

To view detailed error information for API requests:

1. Open your API Management Console
2. Go to **APIs** in the left sidebar
3. Select your API
4. Click on **API Traffic** in the inner left sidebar
5. Select the **Runtime Logs** tab

The logs list displays:

* Request ID and timestamp
* HTTP status code
* **Error component type and name**
* **Error message**

Click **View details** on any log entry to see the complete diagnostic information in the **Request Metric Overview** section.

<figure><img src="../.gitbook/assets/runtime logs_list message CROP.png" alt=""><figcaption><p>Runtime logs with error diagnostics</p></figcaption></figure>

### In Analytics Dashboard

To view aggregated error statistics:

1. Open your API Management Console
2. Go to **APIs** in the left sidebar
3. Select your API
4. Click on **Analytics** in the inner left sidebar

The Analytics Dashboard shows:

* Errors grouped by component type
* Top failing components
* Error trends over time
* Warning statistics (if enabled)

---

## Common error scenarios

### 401 - Unauthorized

**Typical causes:**

* Invalid or expired API key
* No subscription found
* Plan selection rule not matching
* Subscription paused or closed

**Example diagnostic:**

```json
{
  "key": "API_KEY_INVALID",
  "message": "API key is invalid or expired",
  "componentType": "POLICY",
  "componentName": "api-key"
}
```

**Resolution:**

* Verify the API key is correct and active
* Check subscription status in **Applications → Subscriptions**
* Review plan selection rules

### 502 - Bad Gateway

**Typical causes:**

* Backend service unavailable
* Connection refused
* Unknown host
* SSL certificate issues between gateway and backend

**Example diagnostic:**

```json
{
  "key": "CONNECTION_ERROR",
  "message": "Connection refused (Connection refused)",
  "componentType": "ENDPOINT",
  "componentName": "http-proxy-endpoint-123"
}
```

**Resolution:**

* Verify backend service is running
* Check endpoint configuration in **Endpoints**
* Validate network connectivity from gateway to backend
* Review SSL/TLS certificate configuration

### 504 - Gateway Timeout

**Typical causes:**

* Backend response exceeds timeout (default 30s)
* Custom timeout configuration exceeded
* Slow downstream service

**Example diagnostic:**

```json
{
  "key": "TIMEOUT",
  "message": "Request timeout after 30000ms",
  "componentType": "ENDPOINT",
  "componentName": "http-proxy-endpoint-123"
}
```

**Resolution:**

* Investigate backend service performance
* Adjust timeout settings in endpoint configuration if appropriate
* Consider implementing caching or async patterns

### 404 - No Context Path Matching

**Typical causes:**

* API not deployed to gateway
* Wrong virtual host configuration
* API not started
* No published plan available

**Example diagnostic:**

```json
{
  "key": "NO_CONTEXT_PATH_MATCHING",
  "message": "No API matching the context path",
  "componentType": "INTERNAL",
  "componentName": "router"
}
```

**Resolution:**

* Verify API is deployed in **Deployment → Status**
* Check virtual host configuration matches request
* Ensure API is started
* Confirm at least one plan is published

### 500 - Expression Language (EL) Error

**Typical causes:**

* Invalid EL syntax in policy configuration
* Reference to undefined variable
* Type mismatch in expression

**Example diagnostic:**

```json
{
  "key": "EL_EVALUATION_ERROR",
  "message": "Expression evaluation failed (Property 'user' not found)",
  "componentType": "POLICY",
  "componentName": "transform-headers-abc"
}
```

**Resolution:**

* Review EL expressions in the failing policy
* Verify variable names and paths are correct
* Use [Gravitee Expression Language](../gravitee-expression-language.md) documentation for reference
* Test expressions in a development environment

### Warning: Rate Limit Repository Unavailable

**Typical causes:**

* Redis or other rate limit repository connection lost
* Repository temporarily down (call passes through as fallback)

**Example warning:**

```json
{
  "key": "RATE_LIMIT_REPOSITORY_UNAVAILABLE",
  "message": "Rate limit check skipped due to repository unavailability",
  "componentType": "POLICY",
  "componentName": "rate-limit-123"
}
```

**Resolution:**

* Check rate limit repository (Redis) health
* Verify network connectivity to repository
* Review repository configuration in gateway settings
* Monitor for patterns indicating infrastructure issues

---

## Configuration

### Enable or disable warning reporting

Warnings are enabled by default. To disable warning reporting:

**Via configuration file** (`gravitee.yml`):

```yaml
reporters:
  warnings:
    enabled: false
```

**Via environment variable**:

```bash
export REPORTERS_WARNINGS_ENABLED=false
```

**Via Helm values** (`values.yaml`):

```yaml
gateway:
  reporters:
    warnings:
      enabled: false
```

{% hint style="warning" %}
Disabling warnings may hide important non-fatal issues that could help prevent future failures.
{% endhint %}

### Reporter configuration

Error diagnostics are sent to all configured reporters. Ensure your analytics backend is properly configured:

**Elasticsearch example**:

```yaml
reporters:
  elasticsearch:
    enabled: true
    endpoints:
      - http://localhost:9200
```

For detailed reporter configuration, see [Reporters](reporters/).

---

## Verification

### Verify in Elasticsearch

To confirm diagnostics are being recorded, query your Elasticsearch index:

```bash
curl -X GET "http://localhost:9200/gravitee-v4-metrics-*/_search?pretty" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "exists": {
        "field": "errorComponentType"
      }
    },
    "size": 10
  }'
```

**Expected response structure**:

```json
{
  "hits": {
    "hits": [
      {
        "_source": {
          "requestId": "abc123",
          "timestamp": "2025-10-03T10:00:00.000Z",
          "status": 401,
          "errorKey": "API_KEY_INVALID",
          "errorMessage": "API key is invalid",
          "errorComponentType": "POLICY",
          "errorComponentName": "api-key",
          "warnings": [
            {
              "key": "WARNING_KEY",
              "message": "Warning message",
              "componentType": "POLICY",
              "componentName": "rate-limit"
            }
          ]
        }
      }
    ]
  }
}
```

### Verify in Console UI

**In Runtime Logs list:**

* Error key displayed
* Component type and name visible
* Error message shown

**In Runtime Logs detail view:**

* Detailed diagnostic information in "Request Metric Overview"
* Warnings list displayed (if any)
* Component information clearly indicated

**In Analytics Dashboard:**

* Error statistics aggregated by component type
* Trends showing error patterns over time

---

## Best practices

### For API publishers

1. **Review diagnostics regularly**: Check Runtime Logs for recurring errors and identify patterns
2. **Use filters effectively**: Filter by component type or error key to focus on specific issues
3. **Monitor warnings**: Address warnings proactively before they become failures
4. **Understand component hierarchy**:
   * POLICY errors → Review policy configuration
   * ENDPOINT errors → Check backend service availability
   * INTERNAL errors → Contact platform administrator

### For platform administrators

1. **Keep warnings enabled**: Provides early warning signals with minimal performance impact
2. **Monitor analytics backend**: Ensure adequate storage and performance for diagnostic data
3. **Configure alerts**: Set up alerts for high error rates by component type or specific error keys
4. **Review log retention**: Balance storage costs with diagnostic needs (typical: 7-30 days)

---

## Troubleshooting

### Diagnostics not appearing in UI

**Symptoms**: Errors occur but no diagnostic details shown

**Checks**:

1. Verify analytics backend is configured and running:
   ```bash
   curl http://localhost:9200/_cluster/health
   ```

2. Check gateway can connect to analytics backend (review gateway logs)

3. Verify API is V4 or V2 with V4 emulation enabled

4. Confirm reporter is enabled in gateway configuration

### Warnings not recorded

**Symptoms**: Failures visible but warnings missing

**Checks**:

1. Verify warnings are enabled in gateway configuration
2. Ensure gateway version is 4.5 or higher
3. Confirm component actually emits warnings (not all components support warnings yet)

### Incomplete diagnostic information

**Symptoms**: Some diagnostic fields are missing

**Checks**:

1. Verify the component is properly setting error information
2. Check component is within proper execution scope
3. Review gateway logs for any errors during diagnostic creation

---

## Limitations

### Current limitations

* **UI support**: Only available in Console V2 (not available in legacy Console)
* **API version support**: V4 APIs and V2 APIs with V4 emulation only
* **Policy coverage**: Not all policies emit detailed diagnostics (legacy policies may provide basic information only)

### Known issues

* **Stacktrace not included**: Full stacktraces are not exposed to avoid verbosity; only specific error messages are extracted
* **Error centralization**: Error keys are distributed across different plugins with no central registry

---

## Related documentation

* [Logging](logging.md)
* [Dashboards](dashboards.md)
* [Reporters](reporters/)
* [Gravitee Expression Language](../gravitee-expression-language.md)
* [OpenTelemetry](opentelemetry.md)
