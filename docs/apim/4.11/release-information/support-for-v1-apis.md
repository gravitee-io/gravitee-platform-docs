---
description: This page details the go-forward strategy for supporting v1 APIs in APIM
---

# Support for v1 APIs

## Overview
This page details Gravitee’s strategy for supporting v1 APIs in API Management (APIM).

{% hint style="info" %}
Gravitee deprecated v1 APIs in version 4.0.0 of APIM. From version 4.12.0, there is no support for v1 APIs.
{% endhint %}

## Create and import v1 APIs

If you run version 3.20 or later of APIM, you cannot create v1 APIs.

If you run version 3.20 of APIM, you can import your v1 API, and then upgrade the API to v2. If you run version 4.0.0 or later, you cannot import v1 APIs.

## Upgrade to APIM 4.x with v1 APIs

Depending on which version of Gravitee that you upgrade to, you have to complete different actions for your v1 APIs. Follow the steps for your upgrade:
* [Upgrade to versions 4.0.0 to 4.11.x](#upgrade-to-versions-400-to-411x)
* [Upgrade to version 4.12.x](#upgrade-to-version-412x)

### Upgrade to versions 4.0.0 to 4.11.x

When you upgrade an existing APIM environment to version 4.0.0 up to 4.11.x, here is how your environment interacts with v1 APIs:

* v1 APIs continue to run on the Gateway.
* Client applications can still call the v1 APIs that you deployed.
* v1 APIs appear as read-only. Gravitee prompts you to upgrade the API to a v2 definition.
* If you run version 4.0.0 of APIM, you can create, publish, deprecate, and close plans for v1 APIs.

### Upgrade to version 4.12.x

From 4.12.0 of APIM, Gravitee no longer supports v1 APIs. Before you upgrade to version 4.12.0, ensure that you migrate all v1 APIs to at least a v2 API definition. If you upgrade to 4.12.0 with a v1 API, here is how Gravitee interacts with v1 APIs:

* Gravitee removes the v1 API code from the APIM codebase.
* The APIM Gateway ignores v1 APIs.
* The Management API automatically stops running v1 APIs.
* In the UI, v1 APIs display an error indicating an invalid version.

## Migrate v1 APIs to v2

APIM versions 3.20 through 4.11.x include tooling that migrates a v1 API to a v2 definition in place. APIM 4.12.0 and later versions don't include this tooling, so migrate your v1 APIs while your installation runs version 4.11.x or earlier.

{% hint style="warning" %}
If you already upgraded to APIM 4.12.0 or later with v1 APIs still present, restore the database backup that you took before the upgrade, start your previous APIM version against the restored database, and migrate the v1 APIs before you upgrade again.
{% endhint %}

### Migrate a v1 API with the Console

In the Console of APIM 4.0.0 through 4.11.x, a v1 API shows a warning banner titled **API version out-of-date** that states that path-based APIs are no longer supported. The following steps reflect the APIM 4.11.x Console. Earlier 4.x versions show the same banner and button with small layout differences.

To migrate the API, follow these steps:

1. Log in to the Console.
2. Open **APIs**.
3. Select the v1 API. The **API version out-of-date** banner appears at the top of the API's pages.
4. Click **Update API version**. APIM converts the API definition to v2.
5. Click **Policy Studio**, and then check that your v1 paths and policies appear as flows.
6. When the **This API is out of sync.** banner appears, click **Deploy API**.
7. In the **Deploy your API** dialog, click **Deploy**.

### Migrate a v1 API with the Management API

To migrate from a script, or to migrate many v1 APIs in bulk, call the migration endpoint of the Management API for each API:

```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  "https://<management-api-host>/management/organizations/<orgId>/environments/<envId>/apis/<apiId>/_migrate"
```

The endpoint exists in APIM 3.20 through 4.11.x, and the **Update API version** button in the Console calls the same endpoint. The call returns the migrated API definition. The caller needs permission to read the API definition and to create APIs in the environment.

After you call the endpoint, deploy the API to apply the migrated definition to the Gateway.

### What the migration changes

The migration updates the API definition in the following ways:

* The API's definition version becomes v2.
* Each v1 path, together with its HTTP methods and policies, becomes a flow on the API.
* On each plan that isn't closed, the plan's paths become flows on that plan.
* The API's flow mode is set to **Best match**.
* The migration saves the new definition but doesn't deploy it. The API keeps serving traffic with its previously deployed definition until you deploy it again.

After the migration, the API behaves like any other v2 API. To continue to a v4 definition, see [Migrate APIs](../create-and-configure-apis/create-apis/migrate-apis.md).

### Verification

To verify that the migration worked as expected, follow these steps:

1. Open **APIs**. The migrated API shows the **V2 HTTP Proxy** label, and the alert icon with the **V1** label no longer appears.
2. Select the API. The **API version out-of-date** banner no longer appears.
3. Click **Policy Studio**. The flows created from your v1 paths appear.
