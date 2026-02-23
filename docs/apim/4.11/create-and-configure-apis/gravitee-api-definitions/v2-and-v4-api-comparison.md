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

### **Example of the path parameters allowed for v4 APIs**

Here are examples of path parameters that are allowed for v4 APIs and that are not allowed for v4 APIs:

#### **Allowed**

```bash
GET /products/:productId/items/:itemId
GET /products/:productId/items/details
```

#### **Not allowed**

```bash
GET /products/:id/items/:itemId
GET /products/:productId/items/:id 
```

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
| Multiple Endpoint Groups                                          | ✅                          | ✅                                                        | ⚠️ Supported for NATIVE (Kafka) APIs                    |
| Endpoint Reordering                                               | ✅                          | ✅                                                        | ⚠️ Supported for NATIVE (Kafka) APIs                    |
| Logs                                                              | ✅                          | ✅                                                        | ✅                                                        |
| API Quality                                                       | ✅                          | ⚠️ Replaced by [API score](../../govern-apis/api-score/) | ⚠️ Replaced by[ API score](../../govern-apis/api-score/) |
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
| Maintain analytics continuity during v2 to v4 migration           | 🚫                         | 🚫                                                       | NA                                                       |
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

v2 APIs and v4 APIs support subsets of Gravitee policies. Supported policies are applied to one or more phases of the API transaction. For more information, see [Policies](./).
