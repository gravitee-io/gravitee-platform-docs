---
hidden: false
noIndex: false
description: Create or replace an API proxy by importing a Gravitee definition, an OpenAPI specification, or a WSDL document. Follow the steps to import a file.
---

# Import an API proxy

The Gamma console builds an API proxy from a definition file you supply. The same three formats and the same two file sources are available whether you're creating a new API proxy or replacing the configuration of an existing one.

## Import formats

The console supports the following three formats:

* **Gravitee definition**. A Gravitee v4 API definition, in JSON.
* **OpenAPI specification**. An OpenAPI or Swagger descriptor, in JSON or YAML. The console generates the API proxy from the descriptor.
* **WSDL**. A SOAP WSDL document, in XML. The console converts the document to an OpenAPI specification, then generates the API proxy from it.

An OpenAPI or WSDL import produces a v4 HTTP proxy API definition. A Gravitee definition import needs a v4 definition, and the import is rejected when the file declares a different definition version.

{% hint style="info" %}
An OpenAPI or WSDL import creates the API proxy without a plan, because neither format carries plan information. Add a security plan after the import. See [Secure your API proxy](secure-your-api-proxy.md).
{% endhint %}

## Import sources

Every format accepts the following two sources:

* **Local file**. Upload a file from your machine.
* **Remote URL**. Fetch the file from an `http` or `https` URL.

The following table lists what each format accepts:

| Format                    | Local file extensions    | Remote URL field label |
| ------------------------- | ------------------------ | ---------------------- |
| **Gravitee definition**   | `.json`                  | **Definition URL**     |
| **OpenAPI specification** | `.json`, `.yml`, `.yaml` | **Specification URL**  |
| **WSDL**                  | `.wsdl`, `.xml`          | **WSDL URL**           |

A local Gravitee definition file has to parse as JSON. When it doesn't, the console reports a parse error and blocks the import.

### Remote URL restrictions

The Management API fetches a remote file server-side, so the URL has to resolve from the Management API rather than from your browser. The following two settings in `gravitee.yml` restrict which URLs the Management API accepts:

| Setting                        | Description                                                                                                                          | Default |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | ------- |
| `imports.whitelist`            | A list of allowed URL prefixes. An import URL that matches no entry is rejected. An empty list applies no prefix restriction.         | Empty   |
| `imports.allow-from-private`   | Allows imports from private network addresses. This setting is ignored while `imports.whitelist` holds at least one entry.            | `true`  |

## Create an API proxy by import

To create an API proxy from a definition file, follow these steps:

1. Open **API Proxies**.
2. Click **Create New Proxy**.
3. Click **Import API**.
4. Click the card for the format you're importing: **Gravitee definition**, **OpenAPI specification**, or **WSDL**.

    <!-- TODO: Screenshot of the Create API Proxy page with the Import API card expanded to show the three format cards -->

    <figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-import-format-cards.png" alt=""><figcaption><p>The <strong>Import API</strong> card expands to show one card per import format.</p></figcaption></figure>
5. In the **Configure file source** section, click **Local file** or **Remote URL**.
6. Provide the source. For a local file, click the upload area and select the file. For a remote URL, enter the URL in the field.
7. Optional: for an OpenAPI specification or a WSDL, set the toggles in the **Options** section. See [Import options](#import-options).

    <!-- TODO: Screenshot of the import page showing the Configure file source and Options sections -->

    <figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-import-create-form.png" alt=""><figcaption><p>The import page collects the file source and, for OpenAPI and WSDL, the import options.</p></figcaption></figure>
8. Click **Create API**.

The console creates the API proxy and opens its **Overview** page. The new API proxy is in the **Stopped** state. Deploy it to push the imported configuration to the Gateway.

## Update an existing API proxy by import

Importing into an existing API proxy replaces its configuration with the contents of the imported file. To update an API proxy from a definition file, follow these steps:

1. Open **API Proxies**.
2. Click the API proxy you want to update.
3. In the **GENERAL** section, click **General**.
4. Click **Import**.
5. In the **Import API Definition** panel, click the tab for the format you're importing: **Gravitee definition**, **OpenAPI specification**, or **WSDL**.

    <!-- TODO: Screenshot of the Import API Definition panel on the General page, with the API format tabs visible -->

    <figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-import-update-panel.png" alt=""><figcaption><p>The <strong>Import API Definition</strong> panel opens from the action strip on the <strong>General</strong> page.</p></figcaption></figure>
6. In the **Configure file source** section, click **Local file** or **Remote URL**.
7. Provide the source. For a local file, click the upload area and select the file. For a remote URL, enter the URL in the field.
8. Optional: for an OpenAPI specification or a WSDL, set the toggles in the **Options** section. See [Import options](#import-options).
9. Click **Import**.

The console confirms the update and reloads the **General** page with the imported values. Deploy the API proxy to push the imported configuration to the Gateway. While the API proxy holds changes that aren't live, the console shows a **This API is out of sync** banner with a **Deploy API** button.

### What an update keeps

An import replaces the API proxy configuration with the imported file, with the following two exceptions:

* **API properties**. When the imported file declares no API properties and the API proxy already has some, the existing properties are kept.
* **Plans**. What happens to the plans on the API proxy depends on the imported file, as described in the following table.

| Imported file                                    | Effect on the plans of the API proxy                                                            |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| An OpenAPI specification or a WSDL               | Every existing plan is kept, because neither format carries plan information.                     |
| A Gravitee definition that declares no plan      | Every existing plan is kept.                                                                      |
| A Gravitee definition that declares at least one plan | Plans in the file are created or updated on the API proxy, and every plan on the API proxy that the file doesn't declare is deleted. |

{% hint style="warning" %}
A plan that has active subscriptions can't be deleted. An import that would delete such a plan reports an error, so resolve the active subscriptions on that plan before you import.
{% endhint %}

### Kubernetes-managed API proxies

The **Import** button is disabled while the API proxy is managed by the Gravitee Kubernetes Operator.

## Import options

The **Options** section appears for the OpenAPI specification and WSDL formats only. The Gravitee definition format has no options.

The following table describes each option:

| Option                                          | Formats             | Default                                                                                 | Description                                                                                             |
| ----------------------------------------------- | ------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Apply REST to SOAP Transformer policy**       | WSDL                | Enabled                                                                                 | Generates the flows from the WSDL operations and applies the REST to SOAP Transformer policy to them.    |
| **Create documentation page from spec**         | OpenAPI, WSDL       | Enabled for OpenAPI. For WSDL, this option follows **Apply REST to SOAP Transformer policy**. | Adds a published, public documentation page named **Swagger** that holds the specification used for the import. |
| **Add OpenAPI Specification Validation**        | OpenAPI, WSDL       | Enabled for OpenAPI. For WSDL, this option follows **Apply REST to SOAP Transformer policy**. | Adds a flow named **OpenAPI Specification Validation** that validates every request and response against the imported specification. |

Two of these options depend on a policy being installed on the Gateway:

* **Apply REST to SOAP Transformer policy** appears only while the REST to SOAP Transformer policy is installed.
* **Add OpenAPI Specification Validation** appears only while the OpenAPI Specification Validation policy is installed.

For the WSDL format, **Create documentation page from spec** and **Add OpenAPI Specification Validation** are unavailable while **Apply REST to SOAP Transformer policy** is turned off. Turning **Apply REST to SOAP Transformer policy** back on re-enables both.

{% hint style="info" %}
Importing a WSDL with **Apply REST to SOAP Transformer policy** turned off imports the API proxy without generating any flow from the WSDL operations.
{% endhint %}

## Required permissions

The console gates the import entry points on the following permissions:

| Operation                              | Required permission |
| -------------------------------------- | ------------------- |
| Create an API proxy by import          | `environment-api-c` |
| Update an existing API proxy by import | `api-definition-u`  |

{% hint style="info" %}
The **Import** button on the **General** page appears for users who hold `api-definition-c`, while the update itself needs `api-definition-u`.
{% endhint %}

## Verification

To verify the import worked as expected, follow these steps:

1. Open **API Proxies**.
2. Click the imported API proxy.
3. In the **GENERAL** section, click **Overview**.
4. Confirm the **Gateway Endpoint** and **Upstream Service** match the imported file.

    <!-- TODO: Screenshot of the Overview page of an imported API proxy showing Gateway Endpoint and Upstream Service -->

    <figure><img src="../../.gitbook/assets/PLACEHOLDER-gamma-import-verification-overview.png" alt=""><figcaption><p>The <strong>Overview</strong> page of an API proxy created from an OpenAPI specification.</p></figcaption></figure>
5. In the **GENERAL** section, click **General**, and confirm the name and version match the imported file.

## Next steps

* [Secure your API proxy](secure-your-api-proxy.md). Attach a security plan to the imported API proxy.
* [Configure your API proxy](configure-your-api-proxy/README.md). Review endpoints, consumer access, and policies.
* [Create an API proxy](create-an-api-proxy.md). Build an API proxy from scratch or from a template instead.
