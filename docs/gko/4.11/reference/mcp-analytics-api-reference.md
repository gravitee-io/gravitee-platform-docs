# MCP Analytics API Reference

## Overview

MCP Analytics & Dashboard Enhancements extend the Gravitee analytics platform to support Model Context Protocol (MCP) API monitoring. This feature introduces MCP-specific facets and filters for HTTP metrics, a pre-built MCP dashboard template, and refactored chart widget types. It enables API administrators to track MCP method distribution, resource usage, tool invocations, and prompt activity alongside standard HTTP metrics.

## Prerequisites

Before creating MCP analytics queries or dashboards, ensure the following:

* Gravitee API Management platform with analytics enabled
* Elasticsearch backend configured for analytics storage
* MCP APIs deployed and generating traffic with MCP-specific additional metrics fields
* User permissions:
  * `Environment-dashboard-r`: View dashboards
  * `Environment-dashboard-c`: Create dashboards
  * `Environment-dashboard-u`: Update dashboards
  * `Environment-dashboard-d`: Delete dashboards

{% hint style="info" %}
MCP-specific Elasticsearch fields must be populated by the gateway at request time. Ensure your MCP APIs are configured to emit these fields.
{% endhint %}

## Creating MCP Analytics Queries

To query MCP analytics, construct an analytics request using the standard HTTP metrics API with MCP facets or filters.

1. Select an HTTP metric (for example, `HTTP_REQUESTS`).
2. Add one or more MCP facets to group results by MCP dimension (for example, `MCP_PROXY_METHOD`).
3. (Optional) Add MCP filters to restrict results to specific MCP methods, tools, resources, or prompts.

{% hint style="info" %}
Filters are applied at the request level, not the metric level.
{% endhint %}

## Next Steps

* Create custom dashboards with MCP facets and filters
* Add filters to existing dashboards to segment MCP data
* Monitor MCP usage patterns to identify abnormal behavior or underutilized tools
