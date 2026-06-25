---
description: An overview about v2 and v4 api comparison.
metaLinks:
  alternates:
    - v2-and-v4-api-comparison.md
---

# v2 and v4 API Comparison

## Overview

When you create Gravitee APIs, v2 APIs and v4 APIs differ in functionality and supported features.

## Differences in importing v2 and v4 APIs

v2 APIs and v4 APIs handle path parameters differently. The following table summarizes these differences:

| Feature              | v2                                               | v4                                     |
| -------------------- | ------------------------------------------------ | -------------------------------------- |
| Parameter extraction | Only in the flow where you define the parameter. | When you begin to process the request. |
| Parameter sharing    | Restricted to a single flow.                     | Available across all flows.            |
| Performance          | Requires multiple extractions.                   | Extracted once.                        |
| Validation           | No strict rules.                                 | Prevents conflicts before deployment.  |
| Use in APIs          | Hard to manage across multiple flows.            | Standardized and optimized.            |

## **Example of the path parameters allowed for v4 APIs**

When you save a v4 API, the Management API rejects the configuration if any two flow paths in the API or its plans are ambiguous. Two paths are ambiguous when they have the same number of segments and every segment position is either a parameter in both paths or the same static literal in both paths. The parameter name doesn't matter. Only the path shape does. This validation blocks misconfigured paths before they reach the gateway. The Management API responds with an `Invalid path parameters` validation error and lists the conflicting paths.

### **Allowed**

Two flows whose paths have different shapes:

```bash
GET /products/:productId/items/:itemId
GET /products/:productId/items/details
```

The fourth segment is a parameter (`:itemId`) in one path and a static literal (`details`) in the other, so the shapes differ.

### **Not allowed**

Two flows whose paths have the same shape:

```bash
GET /products/:productId/items/:itemId
GET /products/:id/items/:itemId
```

Both paths have four segments and share the shape `/products/:/items/:`. The parameter names differ, but the gateway can't pick the right flow at runtime, so the API is rejected.

```bash
GET /products/:productId/items/:itemId
GET /products/:productId/items/:id
```

Both paths share the same shape, with parameters in positions 2 and 4 and matching literals at positions 1 and 3. Same shape, same conflict.

#### **Cases that look ambiguous but aren't**

* **Different segment counts.** `/products/:productId/items/:itemId` and `/:productId` don't conflict because they have different numbers of segments.
* **Static literal at the same position as a parameter.** `/products/:productId/items/:itemId` and `/products/:productId/items/static` don't conflict because position 4 is a parameter in one path and a static literal in the other.

## Support for functionalities

| Functionality                                                     | Supported in v2 proxy APIs | Supported for v4 proxy APIs                              | Supported for v4 message APIs                            |
| ----------------------------------------------------------------- | -------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| User Permissions                                                  | ✅                          | ✅                                                        | ✅                                                        |
| Properties                                                        | ✅                          | ✅                                                        | ✅                                                        |
| Resources                                                         | ✅                          | ✅                                                        | ✅                                                        |
| Notifications                                                     | ✅                          | ✅                                                        | ✅                                                        |
| Categories                                                        | ✅                          | ✅                                                        | ✅                                                        |
| Audit Logs                                                        | ✅                          | ✅                                                        | ✅                                                        |
| Response Templates                                                | ✅                          | ✅                                                        | ✅                                                        |
| CORS                                                              | ✅                          | ✅                                                        | ✅                                                        |
| Virtual Hosts                                                     | ✅                          | ✅                                                        | ✅                                                        |
| Failover                                                          | ✅                          | ✅                                                        | ⚠️ Depends on use case                                   |
| Health Check                                                      | ✅                          | ✅                                                        | 🚫                                                       |
| Health Check Dashboard                                            | ✅                          | ✅                                                        | 🚫                                                       |
| Service Discovery                                                 | ✅                          | 🚫                                                       | 🚫                                                       |
| Improved Policy Studio                                            | 🚫                         | ✅                                                        | ✅                                                        |
| Debug Mode                                                        | ✅                          | ✅                                                        | 🚫                                                       |
| Plans                                                             | ✅                          | ✅                                                        | ✅                                                        |
| Subscriptions                                                     | ✅                          | ✅                                                        | ✅                                                        |
| Messages / Broadcasts                                             | ✅                          | ✅                                                        | ✅                                                        |
| Documentation - Markdown                                          | ✅                          | ✅                                                        | ✅                                                        |
| Documentation - OAS                                               | ✅                          | ✅                                                        | ✅                                                        |
| Documentation - AsyncAPI                                          | ✅                          | ✅                                                        | ✅                                                        |
| Documentation - AsciiDoc                                          | ✅                          | ✅                                                        | ✅                                                        |
| Documentation - Home Page                                         | ✅                          | ✅                                                        | ✅                                                        |
| Documentation - Metadata                                          | ✅                          | ✅                                                        | ✅                                                        |
| Documentation - Translations                                      | ✅                          | 🚫                                                       | 🚫                                                       |
| Documentation - Group Access Control                              | ✅                          | ✅                                                        | ✅                                                        |
| Documentation - Role Access Control                               | ✅                          | 🚫                                                       | 🚫                                                       |
| Documentation - Swagger vs. Redoc Control                         | ✅                          | ✅                                                        | ✅                                                        |
| Documentation - Try It Configuration                              | ✅                          | ✅                                                        | ✅                                                        |
| Documentation - Nested Folder Creation                            | ✅                          | ✅                                                        | ✅                                                        |
| Terms & Conditions on a Plan                                      | ✅                          | ✅                                                        | ✅                                                        |
| Tenants                                                           | ✅                          | ✅                                                        | ✅                                                        |
| Sharding Tags                                                     | ✅                          | ✅                                                        | ✅                                                        |
| Deployment History                                                | ✅                          | ✅                                                        | ✅                                                        |
| Rollback                                                          | ✅                          | ✅                                                        | ✅                                                        |
| Compare API to Previous Versions                                  | ✅                          | ✅                                                        | ✅                                                        |
| Custom Dashboards                                                 | ✅                          | 🚫                                                       | 🚫                                                       |
| Path Mappings                                                     | ✅                          | 🚫                                                       | 🚫                                                       |
| Logs                                                              | ✅                          | ✅                                                        | ✅                                                        |
| API Quality                                                       | ✅                          | ⚠️ Replaced by [API score](../../govern-apis/api-score/README.md) | ⚠️ Replaced by[ API score](../../govern-apis/api-score/README.md) |
| API Review                                                        | ✅                          | ✅                                                        | ✅                                                        |
| Export API as Gravitee def (+options)                             | ✅                          | ✅                                                        | ✅                                                        |
| Export API as GKO spec                                            | ✅                          | ✅                                                        | ✅                                                        |
| Import API from Gravitee def (+options)                           | ✅                          | ✅                                                        | ✅                                                        |
| Import API from OAS                                               | ✅                          | ✅                                                        | NA                                                       |
| Import API from OAS and automatically add policies for validation | ✅                          | ✅                                                        | <p>NA</p><p><br></p>                                     |
| Import API from WSDL                                              | ✅                          | 🚫                                                       | NA                                                       |
| Add docs page on import of API from OAS                           | ✅                          | ✅                                                        | NA                                                       |
| APIs show in platform-level dashboards                            | ✅                          | ✅                                                        | ✅                                                        |
| APIs show in platform-level analytics                             | ✅                          | ✅                                                        | ✅                                                        |
| API Alerts                                                        | ✅                          | ✅                                                        | ✅                                                        |
| Custom widgets                                                    | ✅                          | 🚫                                                       | 🚫                                                       |
| V2 to V4 migration without analytics continuity                   | ✅                          | ✅                                                        | NA                                                       |
| Maintain analytics continuity during v2 to v4 migration           | 🚫                         | ✅                                                        | NA                                                       |
| API Score                                                         | ✅                          | ✅                                                        | ✅                                                        |

### Environment-level Analytics

| Functionality                               | v2 Proxy APIs | v4 Proxy APIs | v4 Message APIs |
| ------------------------------------------- | ------------- | ------------- | --------------- |
| Env-level total APIs & apps                 | ✅             | ✅             | ✅               |
| Env-level API lifecycle state               | ✅             | ✅             | ✅               |
| Env-level API state                         | ✅             | ✅             | ✅               |
| Env-level API Response Status               | ✅             | ✅             | ✅               |
| Env-level top APIs                          | ✅             | ✅             | ✅               |
| Env-level top failed APIs                   | ✅             | ✅             | ✅               |
| Env-level API Request Stats                 | ✅             | ✅             | ✅               |
| Env-level top applications                  | ✅             | ✅             | ✅               |
| Env-level hits by response status over time | ✅             | ✅             | ✅               |
| Env-level average response time over time   | ✅             | ✅             | ✅               |
| Env-level API events                        | ✅             | ✅             | ✅               |
| Env-level tenant repartition                | ✅             | 🚫            | 🚫              |
| Env-level top slow APIs                     | ✅             | 🚫            | 🚫              |
| Env-level top overhead APIs                 | ✅             | 🚫            | 🚫              |
| Env-level hits by host                      | ✅             | 🚫            | 🚫              |

### **API-level Analytics**

| Functionality                             | v2 Proxy APIs | v4 Proxy APIs | v4 Message APIs |
| ----------------------------------------- | ------------- | ------------- | --------------- |
| API-level request stats                   | ✅             | ✅             | ✅               |
| API-level response status pie chart       | ✅             | ✅             | ✅               |
| API-level hits by HTTP status over time   | ✅             | ✅             | 🚫              |
| API-level average response time over time | ✅             | ✅             | 🚫              |
| API-level hits by application over time   | ✅             | ✅             | 🚫              |
| API-level top applications                | ✅             | ✅             | 🚫              |
| API-level top plans                       | ✅             | ✅             | 🚫              |
| API-level top paths                       | ✅             | ✅             | 🚫              |
| API-level top slow applications           | ✅             | ✅             | 🚫              |
| API-level hits by host                    | ✅             | ✅             | 🚫              |

### **Application-level Analytics**

| Functionality             | v2 Proxy APIs | v4 Proxy APIs | v4 Message APIs |
| ------------------------- | ------------- | ------------- | --------------- |
| App-level top APIs        | ✅             | 🚫            | 🚫              |
| App-level top failed APIs | ✅             | 🚫            | 🚫              |
| App-level top paths       | ✅             | 🚫            | 🚫              |
| App-level status          | ✅             | 🚫            | 🚫              |

## Policy support

v2 APIs and v4 APIs support subsets of Gravitee policies. Supported policies are applied to one or more phases of the API transaction. For more information, see [Policies](README.md).
