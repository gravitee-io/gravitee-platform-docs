---
description: An overview about v2 and v4 api comparison.
---

# v2 and v4 API Comparison

## Overview

When creating Gravitee APIs, keep in mind that there are differences in how v2 APIs and v4 APIs function and what they support.

## Differences in importing v2 and v4 APIs

When you import Gravitee APIs, there are differences between how v2 APIs and v4 APIs handle path parameters. The following table summarizes the differences in the path parameter handling between v2 and v4 APIs:

| Feature              | v2                                               | v4                                     |
| -------------------- | ------------------------------------------------ | -------------------------------------- |
| Parameter extraction | Only in the flow where you define the parameter. | When you begin to process the request. |
| Parameter sharing    | Restricted to a single flow.                     | Available across all flows.            |
| Performance          | Requires multiple extractions.                   | Extracted once.                        |
| Validation           | No strict rules.                                 | Prevents conflicts before deployment.  |
| Use in APIs          | Hard to manage across multiple flows.            | Standardized and optimized.            |

### Example of the path parameters allowed for v4 APIs

Here are examples of path parameters that are allowed for v4 APIs and that are not allowed for v4 APIs:

#### Allowed

```yaml
GET /products/:productId/items/:itemId
GET /products/:productId/items/details
```

#### Not allowed

```yaml
GET /products/:id/items/:itemId
GET /products/:productId/items/:id 
```

## Support for functionalities

| Functionality                                                     | Supported in v2 proxy APIs | Supported for v4 proxy APIs | Supported for v4 message APIs |
| ----------------------------------------------------------------- | -------------------------- | --------------------------- | ----------------------------- |
| User Permissions                                                  | ✅                          | ✅                           | ✅                             |
| Properties                                                        | ✅                          | ✅                           | ✅                             |
| Resources                                                         | ✅                          | ✅                           | ✅                             |
| Notifications                                                     | ✅                          | ✅                           | ✅                             |
| Categories                                                        | ✅                          | ✅                           | ✅                             |
| Audit Logs                                                        | ✅                          | ✅                           | ✅                             |
| Response Templates                                                | ✅                          | ✅                           | ✅                             |
| CORS                                                              | ✅                          | ✅                           | ✅                             |
| Virtual Hosts                                                     | ✅                          | ✅                           | ✅                             |
| Failover                                                          | ✅                          | ✅                           | ⚠️ Depends on use case        |
| Health Check                                                      | ✅                          | ✅                           | 🚫                            |
| Health Check Dashboard                                            | ✅                          | 🚫                          | 🚫                            |
| Service Discovery                                                 | ✅                          | 🚫                          | 🚫                            |
| Improved Policy Studio                                            | 🚫                         | ✅                           | ✅                             |
| Debug Mode                                                        | ✅                          | 🚫                          | 🚫                            |
| Plans                                                             | ✅                          | ✅                           | ✅                             |
| Subscriptions                                                     | ✅                          | ✅                           | ✅                             |
| Messages / Broadcasts                                             | ✅                          | ✅                           | ✅                             |
| Documentation - Markdown                                          | ✅                          | ✅                           | ✅                             |
| Documentation - OAS                                               | ✅                          | ✅                           | ✅                             |
| Documentation - AsyncAPI                                          | ✅                          | ✅                           | ✅                             |
| Documentation - AsciiDoc                                          | ✅                          | 🚫                          | 🚫                            |
| Documentation - Home Page                                         | ✅                          | ✅                           | ✅                             |
| Documentation - Metadata                                          | ✅                          | ✅                           | ✅                             |
| Documentation - Translations                                      | ✅                          | 🚫                          | 🚫                            |
| Documentation - Group Access Control                              | ✅                          | ✅                           | ✅                             |
| Documentation - Role Access Control                               | ✅                          | 🚫                          | 🚫                            |
| Documentation - Swagger vs. Redoc Control                         | ✅                          | ✅                           | ✅                             |
| Documentation - Try It Configuration                              | ✅                          | ✅                           | ✅                             |
| Documentation - Nested Folder Creation                            | ✅                          | ✅                           | ✅                             |
| Terms & Conditions on a Plan                                      | ✅                          | ✅                           | ✅                             |
| Tenants                                                           | ✅                          | 🚫                          | 🚫                            |
| Sharding Tags                                                     | ✅                          | ✅                           | ✅                             |
| Deployment History                                                | ✅                          | ✅                           | ✅                             |
| Rollback                                                          | ✅                          | ✅                           | ✅                             |
| Compare API to Previous Versions                                  | ✅                          | ✅                           | ✅                             |
| Analytics                                                         | ✅                          | ⚠️ WIP                      | ⚠️ WIP                        |
| Custom Dashboards                                                 | ✅                          | 🚫                          | 🚫                            |
| Path Mappings                                                     | ✅                          | 🚫                          | 🚫                            |
| Logs                                                              | ✅                          | ✅                           | ✅                             |
| API Quality                                                       | ✅                          | ⚠️ Replaced by API score    | ⚠️ Replaced by API score      |
| API Review                                                        | ✅                          | ✅                           | ✅                             |
| Export API as Gravitee def (+options)                             | ✅                          | ✅                           | ✅                             |
| Export API as GKO spec                                            | ✅                          | ✅                           | ✅                             |
| Import API from Gravitee def (+options)                           | ✅                          | ✅                           | ✅                             |
| Import API from OAS                                               | ✅                          | ✅                           | NA                            |
| Import API from OAS and automatically add policies for validation | ✅                          | ✅                           | <p>NA</p><p><br></p>          |
| Import API from WSDL                                              | ✅                          | 🚫                          | NA                            |
| Add docs page on import of API from OAS                           | ✅                          | ✅                           | NA                            |
| APIs show in platform-level dashboards                            | ✅                          | ✅                           | ✅                             |
| APIs show in platform-level analytics                             | ✅                          | ✅                           | ✅                             |
| API Alerts                                                        | ✅                          | 🚫                          | 🚫                            |

## Policy support

v2 APIs and v4 APIs support subsets of Gravitee policies. Supported policies are applied to one or more phases of the API transaction. For more information, see [Policies](README.md).
