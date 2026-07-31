---
hidden: false
noIndex: false
---

# Manage API products with the Management API

Everything you can do to an API product in the Gamma console is also available over the Management API. This page walks through the full lifecycle—check a name, create the product, attach APIs, add and publish plans, and deploy—using the v2 Management API.

## Before you begin

All API product endpoints live under the environment-scoped v2 base path:

```
/management/v2/environments/{envId}/api-products
```

The examples on this page use a local installation, the `DEFAULT` environment, and Basic authentication. Substitute your own host, environment ID, and credentials:

```bash
export MGMT=http://localhost:8083/management/v2/environments/DEFAULT
export AUTH="admin:admin"
```

An API can only be attached to a product when both of the following are true:

* It is a V4 HTTP proxy API (`definitionVersion: V4`, `type: PROXY`).
* Its definition sets `allowedInApiProducts` to `true`.

List the APIs that qualify by filtering the API search on that flag:

```bash
curl -s -u "$AUTH" -X POST "$MGMT/apis/_search?page=1&perPage=10" \
  -H 'Content-Type: application/json' \
  -d '{"allowedInApiProducts": true}'
```

The response is `200 OK` with a standard paginated API list containing only eligible APIs. APIs of other types—for example MCP proxies and LLM proxies—have no `allowedInApiProducts` value at all and never appear in this result.

{% hint style="info" %}
`POST /apis` ignores `allowedInApiProducts` in the creation payload: a newly created API comes back with `"allowedInApiProducts": false`. Set the flag afterward by sending the full definition back with `PUT /apis/{apiId}` and `"allowedInApiProducts": true`.
{% endhint %}

## Check whether a product name is available

Product names must be unique within the environment. Test a name before you use it:

```bash
curl -s -u "$AUTH" -X POST "$MGMT/api-products/_verify" \
  -H 'Content-Type: application/json' \
  -d '{"name": "Partner Platform"}'
```

The endpoint always returns `200 OK`. An available name returns only `ok`:

```json
{
  "ok" : true
}
```

An unavailable name returns `ok: false` and a `reason`:

```json
{
  "ok" : false,
  "reason" : "API Product name 'Partner Platform' already exists"
}
```

A name that is empty, or contains only whitespace, is rejected the same way:

```json
{
  "ok" : false,
  "reason" : "API Product name cannot be empty"
}
```

When you build the check into a workflow, note the following two details:

* The comparison is case-sensitive. If `Partner Platform` exists, `partner platform` still verifies as available.
* Leading and trailing whitespace is trimmed before the comparison, so `"  Partner Platform  "` collides with the existing `Partner Platform`.

To let an existing product keep its own name while you edit it, pass the product ID alongside the name. The product is then excluded from the uniqueness check and its current name verifies as available:

```bash
curl -s -u "$AUTH" -X POST "$MGMT/api-products/_verify" \
  -H 'Content-Type: application/json' \
  -d '{"name": "Partner Platform", "apiProductId": "0bd5d044-885b-4666-95d0-44885b2666cc"}'
```

## Create an API product

Send the product definition to `POST /api-products`. `name` and `version` are required; `description` and `apiIds` are optional:

```bash
curl -s -u "$AUTH" -X POST "$MGMT/api-products" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Partner Platform",
    "version": "1.0.0",
    "description": "APIs bundled for partner consumers."
  }'
```

A successful call returns `201 Created` and the new product:

```json
{
  "id" : "0bd5d044-885b-4666-95d0-44885b2666cc",
  "environmentId" : "DEFAULT",
  "name" : "Partner Platform",
  "description" : "APIs bundled for partner consumers.",
  "version" : "1.0.0",
  "apiIds" : [ ],
  "createdAt" : "2026-07-30T16:29:06.467Z",
  "updatedAt" : "2026-07-30T16:29:06.467Z",
  "disableMembershipNotifications" : false
}
```

The creation response does not carry `primaryOwner` or `deploymentState`. Both appear when you read the product back with `GET /api-products/{apiProductId}`.

### Creation errors

Every validation failure returns `400 Bad Request` with a message and, where relevant, the offending values in `parameters`:

| Condition | Response body |
| --------- | ------------- |
| `version` missing | `{"httpStatus": 400, "message": "API Product version is required.", "technicalCode": "data.invalid", "details": []}` |
| Name already used in the environment | `{"httpStatus": 400, "message": "An API Product already exists in environment.", "parameters": {"name": "Partner Platform", "environmentId": "DEFAULT"}, "details": []}` |
| `apiIds` contains an unknown API | `{"httpStatus": 400, "message": "These APIs [does-not-exist] do not exist", "parameters": {"nonExistentApiIds": "does-not-exist"}, "details": []}` |
| `apiIds` contains an ineligible API | `{"httpStatus": 400, "message": "These APIs [fe90aaac-...] are not allowed in API Products", "parameters": {"notAllowedApiIds": "fe90aaac-..."}, "details": []}` |

## Attach APIs to the product

There is no dedicated attach endpoint. The set of bundled APIs is the `apiIds` array on the product itself, so you attach and detach APIs by updating the product with `PUT /api-products/{apiProductId}`.

Send the full list of API IDs you want the product to contain—the array is replaced, not merged:

```bash
curl -s -u "$AUTH" -X PUT "$MGMT/api-products/0bd5d044-885b-4666-95d0-44885b2666cc" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Partner Platform",
    "version": "1.0.0",
    "description": "APIs bundled for partner consumers.",
    "apiIds": ["337417f2-4a4f-40f7-b417-f24a4f10f7ed"]
  }'
```

The call returns `200 OK` with the updated product, including the new `apiIds`. The same validation rules as creation apply: unknown or ineligible API IDs are rejected with `400 Bad Request`.

The update is partial rather than a wholesale replacement—a field you omit keeps its current value. If you omit `apiIds`, the bundle stays untouched, and if you omit `description`, the existing description stays in place. To detach every API from the product, send `"apiIds": []` explicitly.

To read back what is currently bundled, use the product's APIs collection:

```bash
curl -s -u "$AUTH" "$MGMT/api-products/0bd5d044-885b-4666-95d0-44885b2666cc/apis?page=1&perPage=10"
```

The response is `200 OK` and paginated. Each entry in `data` is a full API object—the same shape returned by `GET /apis/{apiId}`, including `listeners`, `endpointGroups`, and `allowedInApiProducts`—alongside the usual pagination block:

```json
{
  "pagination" : {
    "page" : 1,
    "perPage" : 10,
    "pageCount" : 1,
    "pageItemsCount" : 1,
    "totalCount" : 1
  }
}
```

## Create a plan

Consumers subscribe to a product through its plans. Create one with `POST /api-products/{apiProductId}/plans`:

```bash
curl -s -u "$AUTH" -X POST "$MGMT/api-products/0bd5d044-885b-4666-95d0-44885b2666cc/plans" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Partner API Key",
    "description": "API Key plan for partner consumers.",
    "validation": "MANUAL",
    "security": {
      "type": "API_KEY",
      "configuration": {}
    }
  }'
```

A successful call returns `201 Created`. The new plan starts in `STAGING`—it exists but no one can subscribe to it yet:

```json
{
  "id" : "7eed1799-dbbb-4d0b-ad17-99dbbb1d0b0b",
  "name" : "Partner API Key",
  "description" : "API Key plan for partner consumers.",
  "security" : {
    "type" : "API_KEY",
    "configuration" : { }
  },
  "mode" : "STANDARD",
  "characteristics" : [ ],
  "commentRequired" : false,
  "createdAt" : "2026-07-30T16:30:48.362Z",
  "excludedGroups" : [ ],
  "order" : 0,
  "status" : "STAGING",
  "tags" : [ ],
  "updatedAt" : "2026-07-30T16:30:48.362Z",
  "validation" : "MANUAL"
}
```

`validation` accepts `AUTO` or `MANUAL` and controls whether subscription requests are approved automatically or by hand.

### Plan security types

Product plans use the following security types:

| Type | Notes |
| ---- | ----- |
| `API_KEY` | Pass an empty `configuration` object. |
| `JWT` | Requires a `configuration` with the signature and key resolution settings, for example `{"signature": "RSA_RS256", "publicKeyResolver": "GIVEN_KEY", "resolverParameter": "..."}`. |
| `MTLS` | `configuration` can be omitted. |

Keyless plans are rejected outright:

```json
{
  "httpStatus" : 400,
  "message" : "Plan Security Type KeyLess is not allowed.",
  "technicalCode" : "planSecurity.invalid",
  "parameters" : { },
  "details" : [ ]
}
```

{% hint style="warning" %}
`KEY_LESS` is the only security type the Management API blocks. An `OAUTH2` product plan is accepted with `201 Created` and can even be published. However, OAuth2 is not one of the plan types the Gamma console offers for API products. Use `API_KEY`, `JWT`, or `MTLS`.
{% endhint %}

## Publish a plan

A plan only becomes subscribable once it is published:

```bash
curl -s -u "$AUTH" -X POST \
  "$MGMT/api-products/0bd5d044-885b-4666-95d0-44885b2666cc/plans/7eed1799-dbbb-4d0b-ad17-99dbbb1d0b0b/_publish"
```

The call returns `200 OK` with the plan, its `status` now `PUBLISHED` and a `publishedAt` timestamp added:

```json
{
  "id" : "7eed1799-dbbb-4d0b-ad17-99dbbb1d0b0b",
  "name" : "Partner API Key",
  "description" : "API Key plan for partner consumers.",
  "security" : {
    "type" : "API_KEY",
    "configuration" : { }
  },
  "mode" : "STANDARD",
  "characteristics" : [ ],
  "commentRequired" : false,
  "createdAt" : "2026-07-30T16:30:48.362Z",
  "excludedGroups" : [ ],
  "order" : 2,
  "publishedAt" : "2026-07-30T16:31:53.064Z",
  "status" : "PUBLISHED",
  "tags" : [ ],
  "updatedAt" : "2026-07-30T16:31:53.064Z",
  "validation" : "MANUAL"
}
```

### List plans

```bash
curl -s -u "$AUTH" "$MGMT/api-products/0bd5d044-885b-4666-95d0-44885b2666cc/plans"
```

`GET /plans` returns `200 OK` and, by default, **only published plans**. To see plans in other states, pass `statuses` as a comma-separated list. If you repeat the parameter, as in `?statuses=STAGING&statuses=PUBLISHED`, the values are not combined—only one of them takes effect:

```bash
curl -s -u "$AUTH" \
  "$MGMT/api-products/0bd5d044-885b-4666-95d0-44885b2666cc/plans?statuses=STAGING,PUBLISHED"
```

### Other plan transitions

| Action | Request | Result |
| ------ | ------- | ------ |
| Deprecate | `POST .../plans/{planId}/_deprecate` | `200 OK`, `status` becomes `DEPRECATED`. |
| Close | `POST .../plans/{planId}/_close` | `200 OK`, `status` becomes `CLOSED` and `closedAt` is set. |
| Update | `PUT .../plans/{planId}` with the full plan definition | `200 OK` with the updated plan. |
| Delete | `DELETE .../plans/{planId}` | `204 No Content`, in any status. |

## Deploy the product

Deployment pushes the product and its published plans to the Gateway. Check first that the installation is allowed to deploy products:

```bash
curl -s -u "$AUTH" "$MGMT/api-products/0bd5d044-885b-4666-95d0-44885b2666cc/deployments/_verify"
```

The check returns `200 OK` with an `ok` flag:

```json
{
  "ok" : true
}
```

The check is a license check only—it does not inspect the product's APIs or plans, so a product with no APIs attached still verifies as deployable. When the organization's license lacks the required universe tier, `ok` is `false` and `reason` explains that API product deployment requires a universe license.

Trigger the deployment:

```bash
curl -s -u "$AUTH" -X POST \
  "$MGMT/api-products/0bd5d044-885b-4666-95d0-44885b2666cc/deployments" \
  -H 'Content-Type: application/json' -d '{}'
```

Deployment is asynchronous, so the call returns `202 Accepted` with the product as it stood when the request was taken:

```json
{
  "id" : "0bd5d044-885b-4666-95d0-44885b2666cc",
  "environmentId" : "DEFAULT",
  "name" : "Partner Platform",
  "description" : "APIs bundled for partner consumers.",
  "version" : "1.0.0",
  "apiIds" : [ "337417f2-4a4f-40f7-b417-f24a4f10f7ed" ],
  "createdAt" : "2026-07-30T16:29:06.467Z",
  "updatedAt" : "2026-07-30T16:29:56.052Z",
  "disableMembershipNotifications" : false
}
```

Read the product back to confirm the outcome—`deploymentState` is `DEPLOYED` once the deployment has been applied:

```bash
curl -s -u "$AUTH" "$MGMT/api-products/0bd5d044-885b-4666-95d0-44885b2666cc"
```

```json
{
  "id" : "0bd5d044-885b-4666-95d0-44885b2666cc",
  "environmentId" : "DEFAULT",
  "name" : "Partner Platform",
  "description" : "APIs bundled for partner consumers.",
  "version" : "1.0.0",
  "apiIds" : [ "337417f2-4a4f-40f7-b417-f24a4f10f7ed" ],
  "createdAt" : "2026-07-30T16:29:06.467Z",
  "updatedAt" : "2026-07-30T16:29:56.052Z",
  "primaryOwner" : {
    "id" : "a2dbae73-8ec6-4fe9-9bae-738ec6ffe9c7",
    "displayName" : "admin",
    "type" : "USER"
  },
  "deploymentState" : "DEPLOYED",
  "disableMembershipNotifications" : false
}
```

If you publish another plan afterward, `deploymentState` moves to `NEED_REDEPLOY`. Post to `/deployments` again to bring the Gateway back in sync.

## Find and delete products

Search products by name or ID with `POST /api-products/_search`, which returns the same paginated list as `GET /api-products`:

```bash
curl -s -u "$AUTH" -X POST "$MGMT/api-products/_search?page=1&perPage=5" \
  -H 'Content-Type: application/json' \
  -d '{"query": "Partner"}'
```

Delete a product with `DELETE /api-products/{apiProductId}`, which returns `204 No Content`:

```bash
curl -s -u "$AUTH" -X DELETE "$MGMT/api-products/0bd5d044-885b-4666-95d0-44885b2666cc"
```

## Next steps

* [Manage product APIs](manage-product-apis.md). Attach and detach APIs from the Gamma console.
* [Configure API products](README.md). Plans, consumers, and permissions for a product.
* [Create API Products](../api-products.md). How products differ from API proxies.
