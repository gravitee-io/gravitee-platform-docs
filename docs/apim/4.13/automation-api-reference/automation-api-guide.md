---
description: Authenticate to the API Management 4.13 Automation API, address resources by HRID, preview changes with a dry run, and read the state each call returns.
---

# Automation API guide

## Overview

The Automation API manages APIM resources declaratively. A `PUT` carries the full desired state of one resource, and APIM creates the resource or converges it to that state.

This guide covers the conventions that every resource follows. For the fields of each resource, see the [Automation API reference](https://apim-api-docs.gravitee.io/?v=4.13&api=automation).

## Prerequisites

* The Management API serves the Automation API, which is enabled by default. To turn it off, set `http.api.automation.enabled` to `false` in `gravitee.yml`. To change its base path, which defaults to `/automation`, set `http.api.automation.entrypoint`.
* If you install APIM with the Helm chart, enable the `api.ingress.automation` ingress and configure its `hosts` and `tls`.
* This API doesn't manage organizations and environments. Every path starts with `/organizations/{orgId}/environments/{envId}`. Create the organization and the environment before you call it. A default installation ships both with the ID `DEFAULT`.

## Base URL and authentication

| Property                 | Value                                                                                                                                   |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Base URL, self-hosted    | `https://<your-gravitee-mapi-host>/automation`                                                                                          |
| Base URL, Gravitee Cloud | `https://<your-gravitee-cloud-host>/apim/automation`                                                                                    |
| Authentication           | A bearer token in the `Authorization` header: a personal access token, such as a service account's, or a Gravitee Cloud token. Basic authentication is also accepted. |
| Content type             | `application/json`                                                                                                                      |

The caller needs the environment permission of the resource type it manages, such as API or Application, for the action the call performs. A call without that permission returns `403`.

The following request creates or updates the API that `api.json` declares:

```bash
curl -X PUT "https://<your-gravitee-mapi-host>/automation/organizations/DEFAULT/environments/DEFAULT/apis" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @api.json
```

## Resource pattern

Every resource type follows the same pattern:

| Operation        | Method   | Path                                 | Identifier                  |
| ---------------- | -------- | ------------------------------------ | --------------------------- |
| Create or update | `PUT`    | The collection, for example `/apis`  | `hrid` in the request body  |
| Read one         | `GET`    | The item, for example `/apis/{hrid}` | `hrid` in the path          |
| Delete           | `DELETE` | The item, for example `/apis/{hrid}` | `hrid` in the path          |

A `PUT` always targets the collection, and the `hrid` in the body says which resource it creates or updates. The API has no list operation.

A resource that belongs to another one sits under its parent's HRID:
* The subscriptions, documentation pages and links of an API are under `/apis/{apiHrid}/`.
* The listings, documentation pages and links of a portal are under `/portals/{portalHrid}/`.

## Human-readable IDs

You name each resource with an HRID of your choice, in the `hrid` field. The HRID is the resource's identity in this API: a `PUT` with an existing HRID updates that resource, and a `PUT` with a new HRID creates another one. APIM derives the resource's internal ID from the environment and the HRID, so the same declaration applied to the same environment always reaches the same resource.

An HRID has at least three characters. It starts and ends with a letter or a digit, and its other characters are letters, digits, `_`, `-`, or `.`. Gamma module resources reject `.` and accept up to 256 characters.

Groups created before you used the Automation API have a UUID and no HRID. To manage one, pass its UUID as the HRID and add `?hridContainsUUID=true`. Don't use this option for new resources.

## Preview a change with a dry run

Add `?dryRun=true` to a `PUT` to validate a declaration without applying it. APIM validates the declaration and returns the state it would produce, with its findings in `errors`. Nothing is persisted. A dry run returns `200`, even when it reports severe errors.

## Response state and errors

A `PUT` and a `GET` return the state of the resource. The state holds the declared spec, the identifiers APIM assigned, such as `id`, `organizationId`, and `environmentId`, and an `errors` object:

* `errors.severe` lists findings that block the apply. A `PUT` with a severe finding returns `400` and persists nothing.
* `errors.warning` lists findings that don't block the apply, typically a value APIM ignored or replaced with a default.

| Status | Meaning                                                                                                                       |
| ------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `200`  | The `PUT` applied the declaration or completed the dry run, or the `GET` found the resource.                                     |
| `204`  | The `DELETE` removed the resource.                                                                                            |
| `400`  | The declaration is invalid, or the apply reported severe errors.                                                                |
| `401`  | The credentials are missing or invalid.                                                                                       |
| `403`  | The caller lacks the permission, or the license lacks the feature of a Gamma module.                                          |
| `404`  | No resource has this HRID in the environment, or the Gamma module or its resource type is unavailable.                           |

## Settings managed outside the declaration

Two query parameters leave a setting to the platform instead of the declaration:

* On a `PUT` of an API or an application, `ignoreGroups=true` leaves the resource's groups out of the declaration. The groups assigned in the Console stay. A new resource receives the environment's default groups, as it does when created in the Console.
* On a `PUT` of a group, `ignoreMembers=true` leaves its members out of the declaration. Use it for groups whose members an identity provider manages through group mapping. The name, `notifyMembers`, and `defaultMemberRoles` still converge.

## Gamma module resources

Gamma modules add resources under a path segment named after the module:

* `PUT /organizations/{orgId}/environments/{envId}/{module}/{type}`
* `GET` and `DELETE /organizations/{orgId}/environments/{envId}/{module}/{type}/{hrid}`

They follow the conventions of this guide: HRID in the body of a `PUT`, `dryRun`, and the `errors` object. Before a call reaches the module, APIM checks the following, in this order:

| Check                                  | Status and error key                   |
| -------------------------------------- | -------------------------------------- |
| The module is installed                | `404` `gamma.module.unavailable`       |
| The module serves this resource type   | `404` `gamma.resource.kind.notFound`   |
| The license includes the module feature | `403` `feature.missing`                |
| The caller has the permission          | `403`                                  |

For the modules APIM 4.13 ships and their license features, see [Gamma module resources](README.md#gamma-module-resources).

## Resource index

| Resource                     | Collection path                         | Reference                                                                                                         |
| ---------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| APIs                         | `/apis`                                 | [APIs](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdateApis)                     |
| Applications                 | `/applications`                         | [Applications](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdateApplications)     |
| Groups                       | `/groups`                               | [Groups](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdateGroup)                  |
| Dictionaries                 | `/dictionaries`                         | [Dictionaries](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdateDictionaries)     |
| Shared policy groups         | `/shared-policy-groups`                 | [Shared policy groups](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdatePolicyGroup) |
| Subscriptions                | `/apis/{apiHrid}/subscriptions`         | [Subscriptions](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdateApiSubscriptions) |
| API documentation            | `/apis/{apiHrid}/documentations`        | [API documentation](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdateApiDocumentation) |
| API links                    | `/apis/{apiHrid}/links`                 | [API links](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdateApiLink)             |
| Portals                      | `/portals`                              | [Portals](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdatePortal)                |
| Portal listings              | `/portals/{portalHrid}/listings`        | [Portal listings](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdatePortalListing) |
| Portal documentation         | `/portals/{portalHrid}/documentations`  | [Portal documentation](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdatePortalDocumentation) |
| Portal links                 | `/portals/{portalHrid}/links`           | [Portal links](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdatePortalLink)       |
| Portal themes                | `/portal-themes`                        | [Portal themes](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdatePortalTheme)     |
| AI Catalog MCP servers       | `/aim/catalog/mcp-servers`              | [AI Catalog](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdateAimCatalogMcpServer) |
| MCP proxies                  | `/aim/mcp-proxies`                      | [MCP Proxies](https://apim-api-docs.gravitee.io/?v=4.13&api=automation#/operations/createOrUpdateAimMcpProxy)       |

For the portal resources, see also [Portal automation](../developer-portal/new-developer-portal/customize-the-navigation/portal-automation/README.md).
