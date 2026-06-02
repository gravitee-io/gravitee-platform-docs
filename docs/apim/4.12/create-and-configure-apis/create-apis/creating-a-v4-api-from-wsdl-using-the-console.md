# Creating a v4 API from WSDL Using the Console

## Creating a v4 API from WSDL

### Console Import Wizard

1. Navigate to **APIs** > **Import API** and select the **WSDL** format. Supported file types: `.wsdl`, `.xml`.

    <figure><img src="../../.gitbook/assets/wsdl-import-format-selection.png" alt="API import wizard showing WSDL format option enabled"><figcaption></figcaption></figure>

2. Upload a WSDL file or enter a remote URL in the **payload** field.
3. Toggle **Apply REST to SOAP Transformer policy** to enable REST-to-SOAP transformation. This toggle is visible only when the `rest-to-soap` policy is installed and is enabled by default.
4. When the **Apply REST to SOAP Transformer policy** toggle is ON, the **Documentation page** and **OpenAPI Specification Validation** toggles are enabled and checked by default. When the toggle is OFF, both options are disabled and unchecked.
5. Review the import settings and confirm to create the API.

#### Field Reference

| Field | Description | Default |
|:------|:------------|:--------|
| **Apply REST to SOAP Transformer policy** | Adds per-operation flows that translate REST/JSON calls to SOAP/XML. Automatically includes the `xml-json` policy as a dependency. | ON (when `rest-to-soap` is installed) |
| **Documentation page** | Publishes a Swagger page from the converted OpenAPI specification (not the raw WSDL). | Checked when **Apply REST to SOAP Transformer policy** is ON |
| **OpenAPI Specification Validation** | Validates requests and responses against the converted OpenAPI specification. Response validation is ordered after SOAP transformation when policies are enabled. | Checked when **Apply REST to SOAP Transformer policy** is ON |
