---
description: An overview about execution transparency analytics.
metaLinks:
  alternates:
    - execution-transparency-analytics.md
---

# Execution Transparency Analytics

## Overview

Execution transparency analytics provides clear, actionable diagnostics when errors occur during API execution. This feature helps API publishers troubleshoot issues independently by exposing detailed information about the root cause of failures and warnings.

### Why Configure Execution Transparency in Analytics

Execution transparency analytics provides the following benefits:

* Improved visibility: You can identify which component policy, endpoint, or internal system caused a failure.
* Actionable diagnostics: Execution transparency provides human-readable error messages with specific details about what went wrong.
* Warning tracking: Monitor non-fatal issues before they become critical problems.

## Execution Transparency Analytics Components

Execution transparency analytics provides structured diagnostic information when an error or warning occurs. The diagnostic information contains the following:

* Key: A unique identifier for the error type.
* Message: A human-readable description of what went wrong.
* Component type: The source of the error. For example: POLICY, ENDPOINT, INTERNAL.
* Component name: The specific component identifier. For example: policy ID, endpoint ID, etc.

The diagnostic information appears in the trace console:

* Runtime Logs: Detailed trace views with error context in V2 and V4 API.
* Analytics Dashboard: Error overview and trends.
* Metrics: Integrated with Elasticsearch and other reporters.

{% hint style="success" %}
Execution transparency analytics is available for V4 APIs and V2 APIs running on the V4 execution engine.
{% endhint %}

### Prerequisites

Execution transparency analytics requires the following components before you can use it:

* Gravitee APIM 4.9.
* V4 APIs or V2 APIs with V4 emulation enabled.
* Analytics backend configured. For example: Elasticsearch.

## Configure Execution Transparency

* Warning reporting is enabled by default in your environment. Here is what the default configuration looks like in the Gateway section of your `gravitee.yml` file:

```yaml
# gravitee.yml

gateway:
  reporters:
    warnings:
      enabled: true
```

## How Execution Transparency Analytics Works

Execution transparency analytics are enabled by default, and it follows a detection and reporting flow that captures diagnostic information throughout the API execution process.

### Error Detection and Reporting Flow

The Gateway processes errors through the following steps:

1. **Error occurs**: A policy, endpoint, or internal component encounters an issue during API execution.
2. **Component tracking**: The Gateway automatically captures the component type and identifier.
3. **Diagnostic creation**: Structured diagnostic information is generated with error details
4. **Metrics attachment**: The diagnostic is attached to request metrics
5. **Reporter processing**: Metrics are sent to configured reporters. For example: Elasticsearch, JSON, CSV.
6. **UI display**: Diagnostics appear in Console V2 and V4 Runtime Logs and Analytics

### Types of Diagnostics

Execution Transparency Analytics categorizes diagnostics into two types based on their severity.

#### **Errors**

`ExecutionFailure` represents a fatal error that interrupts request processing. For example: Invalid API key `401` , Backend connection failure `502` , Request timeout `504` , Expression language evaluation error `500` .

### **Warnings**

`ExecutionWarn` represents a non-fatal issue that doesn't interrupt execution but indicates a potential problem. For example: Rate limit repository where the call passes through as fallback, degraded backend performance, and policy configuration warnings.

## View Execution Transparency Analytics

Execution transparency displays diagnostic information in Runtime Logs. You can view Execution transparency analytics in V4 and V2 API, by completing the following steps:

* [#view-execution-transparency-analytics-in-v4-apis](execution-transparency-analytics.md#view-execution-transparency-analytics-in-v4-apis "mention")
* [#view-execution-transparency-analytics-in-v2-apis](execution-transparency-analytics.md#view-execution-transparency-analytics-in-v2-apis "mention")
* [#view-execution-transparency-analytics-in-dashboard-console](execution-transparency-analytics.md#view-execution-transparency-analytics-in-dashboard-console "mention")

### View Execution Transparency Analytics in V4 APIs

Runtime Logs provide detailed error information for individual API requests. To view error diagnostics in Runtime Logs complete the following steps:

1.  Navigate to your API Management Console.

    <figure><img src="../.gitbook/assets/api-mangement-console (1).png" alt=""><figcaption></figcaption></figure>
2.  Click **APIs** in the left sidebar.

    <figure><img src="../.gitbook/assets/apis-sidebar (1).png" alt=""><figcaption></figcaption></figure>
3.  Select your API.

    <figure><img src="../.gitbook/assets/select-your-api (1).png" alt=""><figcaption></figcaption></figure>
4. Select **Logs** to view detailed request information including: Timestamp, Method, Status, URI, Application, Response time.

<figure><img src="../.gitbook/assets/view-logs-v4 (1).png" alt=""><figcaption></figcaption></figure>

5.  Click on the **Timestamp** or Log details of any log entry.

    <figure><img src="../.gitbook/assets/timestamp-log-details (1).png" alt=""><figcaption></figcaption></figure>
6.  The Log Overview section displays complete diagnostic information including:Complete Request Details, Header Details, Response Information, Gateway status, Error Message, Error Key, Component Name, Component Type.

    <figure><img src="../.gitbook/assets/v4-execution-transparency-analytics-logs (4) (1).png" alt=""><figcaption></figcaption></figure>

### View Execution Transparency Analytics in V2 APIs

V2 APIs display execution transparency directly in the logs without requiring additional configuration. To view execution transparency for your V2 API, complete the following steps:

1.  Navigate to your API Management Console.

    <figure><img src="../.gitbook/assets/api-mangement-console (1).png" alt=""><figcaption></figcaption></figure>
2.  Click **APIs** in the left sidebar.

    <figure><img src="../.gitbook/assets/apis-sidebar (1).png" alt=""><figcaption></figcaption></figure>
3.  Select your V2 API.

    <figure><img src="../.gitbook/assets/select-v2-api (1).png" alt=""><figcaption></figcaption></figure>
4.  Click **Logs** in the left sidebar.

    <figure><img src="../.gitbook/assets/click-logs-v2 (1).png" alt=""><figcaption></figcaption></figure>
5.  The logs list displays the following for each request: Errors, Warnings, Date, Status, Application, Plan, Method, Path.

    <figure><img src="../.gitbook/assets/view-logs-v2-api (1).png" alt=""><figcaption></figcaption></figure>
6.  Click on a specific Date.

    <figure><img src="../.gitbook/assets/click-on-a-specific-date (1).png" alt=""><figcaption></figcaption></figure>
7.  The log details appear, showing all warnings and errors associated with the request.

    <figure><img src="../.gitbook/assets/log-details-request-errors-v2 (1).png" alt=""><figcaption></figcaption></figure>

### **View Execution Transparency Analytics in Dashboard Console**

You can view execution transparency logs from the global analytics page in your dashboard. To view execution transparency from the Dashboard console, complete the following steps:

1.  Navigate to your API Management Console home page.

    <figure><img src="../.gitbook/assets/apim-management-console (1).png" alt=""><figcaption></figcaption></figure>
2.  Click **Analytics** in the left sidebar.

    <figure><img src="../.gitbook/assets/global-analytics (1).png" alt=""><figcaption></figcaption></figure>
3.  Click **Logs** to view the list of log entries.

    <figure><img src="../.gitbook/assets/click-global-logs (1).png" alt=""><figcaption></figcaption></figure>
4.  Click on a specific log entry to view error details, warn information with complete request and response information.

    <figure><img src="../.gitbook/assets/failure-details (1).png" alt=""><figcaption></figcaption></figure>

### Common Error Scenarios

Execution transparency analytics helps you diagnose and resolve common API errors. The following scenarios describe causes and resolutions for frequent error codes.

#### 401 Unauthorized

A 401 Unauthorized error occurs when authentication fails due to an invalid or expired API key, missing subscription, plan selection rule not matching, or a paused or closed subscription.

For Example:

```json
{
  "key": "GATEWAY_PLAN_UNRESOLVABLE",
  "message": "The provided authentication token is invalid for the following plans",
  "componentType": "SYSTEM",
  "componentName": "SECURITY"
}
```

#### 502 Bad Gateway

A 502 Bad Gateway error occurs when the Gateway cannot reach the backend service due to Backend service unavailable, Connection refused, Unknown host, SSL certificate issues between gateway and backend.

For Example:

```json
{
  "key": "GATEWAY_CLIENT_CONNECTION_ERROR",
  "message": "An error occurred when invoking the backend",
  "componentType": "ENDPOINT",
  "componentName": "INVOKER ADAPTER"
}
```

#### 504 Gateway Timeout

A 504 Gateway Timeout error occurs when the backend response exceeds the configured timeout due to: Backend response exceeding timeout of 30 seconds, Custom timeout configuration exceeded, Slow downstream service.

For Example:

```json
{
  "key": "TIMEOUT",
  "message": "Request timeout after 30000ms",
  "componentType": "ENDPOINT",
  "componentName": "http-proxy-endpoint-123"
}
```

#### 500 Expression Language Error

A 500 Expression language error occurs when an expression evaluation fails due to Invalid EL syntax in policy configuration, reference to undefined variable, type mismatch in expression.

For Example:

```json
{
  "key": "TRANSFORM_HEADER_FAILURE",
  "message": "Expression evaluation failed Property 'user' not found",
  "componentType": "POLICY",
  "componentName": "transform-headers-policy"
}
```

#### Warning: Rate Limit Repository Unavailable

A Rate Limit Repository Unavailable warning occurs when the rate limit repository connection is lost, but the call passes through as a fallback due to Redis or other rate limit repository connection lost, and the Repository temporarily down.

Example warning:

```json
{
  "key": "RATE_LIMIT_NOT_APPLIED",
  "message": "Request bypassed rate limit policy due to internal error",
  "componentType": "POLICY",
  "componentName": "rate-limit-policy"
}
```
