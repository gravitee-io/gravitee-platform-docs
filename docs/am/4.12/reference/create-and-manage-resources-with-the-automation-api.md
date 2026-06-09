# Create and Manage Resources with the Automation API

## Creating Resources

The Automation API uses PUT requests for both creating and updating resources. All resource endpoints follow the pattern `PUT /management/automation/organizations/{orgId}/environments/{envId}/...`. Authentication is performed using either a JWT bearer token or an opaque user service-account access token in the `Authorization` header (format: `Bearer <token>`). Refer to the OpenAPI specification served at the configured entrypoint for complete endpoint definitions and request/response schemas.

### Domains

Create or update a domain by sending a PUT request to `/management/automation/organizations/{orgId}/environments/{envId}/domains` with the domain definition in the request body. The domain key is specified in the request body and becomes the stable identifier for the domain within the environment.

### Identity Providers

Create or update an identity provider by sending a PUT request to `/management/automation/organizations/{orgId}/environments/{envId}/domains/{domainKey}/identities` with the identity provider definition in the request body. For non-system identity providers, the request body must include `name`, `type`, and `configuration` fields. For system identity providers, only the `key` field is required — all other configuration is inherited from `gravitee.yml`.

### Certificates

Create or update a certificate by sending a PUT request to `/management/automation/organizations/{orgId}/environments/{envId}/domains/{domainKey}/certificates` with the certificate definition in the request body. Embedded file content (e.g., keystore base64 blobs) is normalized to filename-only form before persistence; the raw base64 content is not stored in the configuration field.

### Reporters

Create or update a reporter by sending a PUT request to `/management/automation/organizations/{orgId}/environments/{envId}/domains/{domainKey}/reporters` with the reporter definition in the request body. Database reporter types (`mongodb`, `reporter-am-jdbc`) can only be created as system reporters (`system: true`); manual creation via the Automation API is rejected with the error "Reporter type '{type}' cannot be created manually".

## Managing Resources

### Retrieving Resources

Retrieve a single resource by sending a GET request to the resource's endpoint with its key in the path (e.g., `GET .../domains/{domainKey}`). Retrieve all resources of a type by sending a GET request to the collection endpoint (e.g., `GET .../domains`). Refer to the OpenAPI specification for complete endpoint definitions.

### Updating Resources

Update a resource by sending a PUT request to the same endpoint used for creation. The request body must include all required fields. The following fields are immutable and cannot be changed after creation:

- **Identity Providers**: `system` flag, `type` field
- **Certificates**: `type` field
- **Reporters**: `type` field

Attempting to change an immutable field results in a 400 Bad Request error with a message indicating which field cannot be changed.

### Deleting Resources

Delete a resource by sending a DELETE request to the resource's endpoint with its key in the path (e.g., `DELETE .../domains/{domainKey}`).

### Plugin Validation

Before creating or updating an identity provider or reporter, the Automation API validates that the plugin type is deployed on the gateway and that the configuration matches the plugin's schema. If the plugin is not deployed, the request is rejected with a 400 Bad Request error: "Plugin type '{type}' is not deployed". If the configuration is invalid, the request is rejected with a 400 Bad Request error containing validation error details.
