
# Creating and updating APIs from remote URLs (Console)


## Creating APIs from Remote Gravitee Definitions

Navigate to the API import form and select the Gravitee definition format. Choose the **Remote source** card and enter the URL of the hosted Gravitee API definition (e.g., `https://cdn.example.com/api-definition.json`). The Management API server fetches the definition file, validates its JSON structure, and creates the API. If the URL is not in the configured whitelist or resolves to a private address (when disallowed), the request is rejected with a `400 Bad Request` error. The Console displays backend error messages in a snackbar notification. If the Management API is unreachable (network error), the message "Unable to reach the Management API. Please check your network connection and try again." is shown.

<figure><img src="../../.gitbook/assets/apim-api-import-from-remote-url-step-01.png" alt="Import API wizard showing API format selection with Gravitee definition, OpenAPI specification, and WSDL options"><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/apim-api-import-from-remote-url-step-02.png" alt="Import API file source configuration with remote source selected and URL field populated"><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/apim-api-import-from-remote-url-step-03.png" alt="Import API review screen showing Gravitee definition format, remote source, and GitHub URL configuration"><figcaption></figcaption></figure>

## Updating APIs from Remote Definitions

### Updating from Remote Gravitee Definition URL

Navigate to the API import form in update mode and select the Gravitee definition format. The **Remote source** card is now enabled (previously disabled with a tooltip). Enter the URL of the updated Gravitee API definition. The Management API fetches the definition and updates the API, preserving the API ID from the path parameter. The same whitelist and private-address validation rules apply as in create mode.

### Updating from Remote OpenAPI/Swagger URL

When updating an API from a remote OpenAPI or Swagger specification, the Console sends an `ImportSwaggerDescriptor` with `type: 'URL'` and `payload` set to the specification URL. The backend validates the URL, fetches the specification server-side, and updates the API. Optional fields `withDocumentation` and `withOASValidationPolicy` control whether to import documentation and apply OAS validation policies.

<figure><img src="../../.gitbook/assets/apim-api-import-from-remote-url-step-04.png" alt="Import API wizard with OpenAPI specification format selected"><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/apim-api-import-from-remote-url-step-05.png" alt="Import API review screen showing OpenAPI specification format with documentation page and validation options enabled"><figcaption></figcaption></figure>
