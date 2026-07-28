---
description: An overview about v2 and v4 api comparison.
---

# v2 and v4 API Comparison

## Overview

When creating Gravitee APIs, keep in mind that v2 APIs and v4 APIs have some differences in functionality. The following table shows the differences for the following API types:

* v2 proxy APIs
* v4 proxy APIs
* v4 message APIs

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

v2 APIs and v4 APIs support subsets of Gravitee policies. Supported policies are applied to one or more phases of the API transaction. For more information, see [https://github.com/gravitee-io/gravitee-platform-docs/blob/main/docs/apim/4.6/create-apis/broken-reference/README.md](https://github.com/gravitee-io/gravitee-platform-docs/blob/main/docs/apim/4.6/create-apis/broken-reference/README.md "mention").
