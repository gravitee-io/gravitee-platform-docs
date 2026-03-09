# Consuming APIs via API Products

## Client Configuration

Clients consume APIs within an API Product using the same authentication mechanisms as individual API subscriptions.

### Authentication Methods

**API Key plans:**
* Include the key in the `X-Gravitee-Api-Key` header, or
* Pass the key as a query parameter

**JWT plans:**
* Provide the token in the `Authorization: Bearer` header

**mTLS plans:**
* Present the client certificate during the TLS handshake

### Gateway Validation

The gateway validates subscriptions in the following order:

1. Check subscription against the API Product first
2. If no product subscription matches, check API-level plans

### Gateway Context Attributes

For API Product subscriptions, the gateway sets the following context attributes:

* `ATTR_API_PRODUCT`: Set to the API Product ID
* `apiProductId`: Exposed in the Expression Language context

Flow conditions can reference the API Product ID to execute product-specific policies.

### API Key Lookup

The API key lookup mechanism supports both API and API_PRODUCT reference types via `findByKeyAndReferenceIdAndReferenceType()`.
