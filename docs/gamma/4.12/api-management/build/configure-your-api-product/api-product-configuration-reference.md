---
hidden: false
noIndex: false
description: Every API product property, the flag that decides which APIs can be bundled, and the plan types a product supports. Browse the full reference.
---

# API product configuration reference

This page lists reference values for API products in the Gamma API Management module: the product's own properties, the flag that decides which APIs can be bundled, and the plan types a product supports.

## API product properties

An API product has the following properties:

| Property      | Type       | Required | Description                                                                                                                                                            |
| ------------- | ---------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | string     | Yes      | Product name. Must be unique within the environment. The comparison is case-sensitive, and leading and trailing whitespace is trimmed before the name is checked.       |
| `version`     | string     | Yes      | Product version. The create form pre-fills `1.0.0`.                                                                                                                    |
| `description` | string     | No       | Freeform description of what the product offers to consumers.                                                                                                          |
| `apiIds`      | string\[]  | No       | IDs of the APIs bundled in the product. Every referenced API must exist, use the v4 API definition, and have `allowedInApiProducts` set to `true`.                      |

`name`, `version`, and `description` map to the **Name**, **Version**, and **Description** fields on both the **Create API Product** form and the product's **General** page. `apiIds` is managed from the product's **APIs** page rather than as a text field.

While you type in the **Name** field, the console checks the name against existing products and reports either `Name is available.` or `API Product name '<name>' already exists`. The check is debounced by 400 ms and runs against the trimmed name, so `  Docs Verification Product  ` collides with `Docs Verification Product`, while `docs verification product` does not.

## API eligibility

An API is only offered to an API product when its `allowedInApiProducts` flag is set. The flag applies to v4 HTTP proxy APIs and takes the following values:

| Property                | Type    | Value in Gamma                                                                                                        | Description                                                                              |
| ----------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `allowedInApiProducts`  | Boolean | `false` for an API proxy created in the Gamma console. Absent, that is `null`, for API types other than HTTP proxy.    | Makes the API eligible for inclusion in API products.                                    |

An API proxy created through **Create New Proxy** is created with `allowedInApiProducts` set to `false`. A newly created proxy is not eligible for API products until you enable the flag yourself. When the field is absent from a v4 HTTP proxy API's definition, the Management API also reports it as `false`.

### Enable an API for API products

1. From the API Management sidebar, select **API Proxies**, and then select the API.
2. In the API sidebar, select **General** under **GENERAL**.
3. Turn on the **Allow in API Products** switch. Its helper text reads *When enabled, this API can be bundled into API Products for grouped consumer access.*
4. In the bar that appears in the page header once the form has unsaved edits, select **Save changes**. A `Changes saved` notification confirms the update.

The switch does nothing until the form is saved. When you change it, the form is only marked dirty, which is what makes the **Discard** and **Save changes** buttons appear next to the **General** heading.

The switch is read-only when you lack update permission on the API definition, or when the API is managed by the Gravitee Kubernetes Operator.

### How eligibility affects the Add API picker

The product's **Add API** panel only lists APIs whose `allowedInApiProducts` flag is `true`, and it hides APIs already attached to the product. The panel states this itself: *API visibility — Cannot see all your APIs? APIs must have API products enabled before they appear in this list.* It lists nothing until you type a name or context path.

APIs of a type other than HTTP proxy, such as MCP proxies and LLM proxies, do not carry the flag at all. They never appear in the picker, regardless of what you search for.

### Turn eligibility off again

Gamma does not lock the switch once the API belongs to a product. You can turn **Allow in API Products** off and save while the API is attached, and the API stays attached and listed on the product's **APIs** page.

The constraint is applied when the product's API list is next submitted. When you create or update a product whose `apiIds` include an API with the flag off, the request is rejected. The validation error takes the form `These APIs [<ids>] are not allowed in API Products`. The same validation rejects APIs that do not exist, and APIs that do not use the v4 API definition.

## Plan reference model

The same plan model serves both an API and an API product because plans and subscriptions record the entity they belong to through the following pair of reference fields:

| Property        | Type   | Description                                       |
| --------------- | ------ | ------------------------------------------------- |
| `referenceId`   | string | ID of the parent API or API product.              |
| `referenceType` | enum   | `API` or `API_PRODUCT`.                           |

Plans created for an API product are always stored with `referenceType` set to `API_PRODUCT` and `referenceId` set to the product ID. The legacy `apiId` field on plans is deprecated as of 4.11.0 and marked for removal. These are data-model fields; the Gamma console does not surface them.

## Supported plan security types

An API product supports the following subset of the plan security types available to an API proxy:

| Security type          | API product | API proxy | Notes                                                                                                    |
| ---------------------- | ----------- | --------- | ---------------------------------------------------------------------------------------------------------- |
| **API Key** (`API_KEY`)| Yes         | Yes       | —                                                                                                        |
| **JWT** (`JWT`)        | Yes         | Yes       | —                                                                                                        |
| **mTLS** (`MTLS`)      | Yes         | Yes       | —                                                                                                        |
| **OAuth2** (`OAUTH2`)  | No          | Yes       | Not offered in the product's **Create plan** menu.                                                       |
| **Keyless** (`KEY_LESS`)| No         | Yes       | Not offered in the product's **Create plan** menu, and rejected by the Management API with `400 Bad Request` and the message `Plan Security Type KeyLess is not allowed.` |

On a product's **Plans** page, **Create plan** opens a menu offering **API Key**, **JWT**, and **mTLS**. The same menu on an API proxy's **Plans** page also offers **OAuth2** and **Keyless**.

## Next steps

* [Manage product APIs](manage-product-apis.md). Attach and detach API proxies.
* [Configure API products](README.md). Review where each configuration area lives in the product sidebar.
* [Create API Products](../api-products.md). Create a product and work through the onboarding checklist.
