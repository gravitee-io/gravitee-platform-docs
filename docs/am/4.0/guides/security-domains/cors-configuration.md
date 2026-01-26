# CORS Configuration for Security Domains

## Overview

Cross-Origin Resource Sharing (CORS) is a crucial security mechanism that allows web applications running at one domain (origin) to access resources from another domain. In Gravitee Access Management, CORS can be configured at the Security Domain level to manage cross-origin requests for your authentication and authorization endpoints.

This document explains how to configure CORS settings for Security Domains, including the available options, their impact, and the relationship between Security Domain CORS and API-level CORS settings.

## What is CORS?

CORS is a browser security feature that restricts web pages from making requests to a different domain than the one serving the web page, unless that domain explicitly allows it. When a web application tries to access resources from a different origin, the browser performs a "preflight" request to check if the cross-origin request is allowed.

## Why Configure CORS for Security Domains?

In AM, CORS configuration at the Security Domain level is essential when:

- Your frontend applications are hosted on different domains than your AM Gateway
- You enable the "try-it" feature of Swagger pages for API testing
- You have single-page applications (SPAs) that need to authenticate users
- You integrate with third-party applications that consume your authentication endpoints

## Accessing CORS Configuration

CORS settings for Security Domains can be configured through:

1. **AM Console**: Navigate to `Settings > Entrypoints` in your Security Domain
2. **Direct URL**: `https://{console}/environments/default/domains/{domainId}/settings/entrypoints`
3. **AM Management API**: Using the domain configuration endpoints

## CORS Configuration Options

### Enable CORS

The CORS configuration includes a toggle to enable or disable CORS for the Security Domain. When CORS is disabled, AM will use the default values from the `gravitee.yml` configuration file.

```yaml
# Default CORS settings in gravitee.yml
http:
  cors:
    allow-origin: ".*"
    allow-methods: "GET, POST, PUT, PATCH, DELETE"
    allow-headers: "Cache-Control, Pragma, Origin, Authorization, Content-Type, X-Requested-With, If-Match, x-xsrf-token"
    max-age: 86400
    allow-credentials: false
```

### Allow-Origin

Specifies which origins are permitted to access the resources.

- **Description**: The origin parameter specifies a URI that may access the resource. Scheme, domain, and port are part of the same-origin definition.
- **Examples**:
  - `*` - Allows all origins (use with caution)
  - `https://mydomain.com` - Allows specific domain
  - `(http|https).*.mydomain.com` - Allows subdomains using regex patterns
- **Security Note**: Using `*` with credentials enabled is not allowed by browsers and may pose security risks.

### Allow-Methods

Specifies which HTTP methods are allowed when accessing the resource.

- **Description**: Used in response to preflight requests to indicate which methods are permitted.
- **Available Methods**: GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD
- **Default**: GET, POST, PUT, PATCH, DELETE
- **Best Practice**: Only enable the methods your applications actually need.

### Allow-Headers

Defines which headers can be used in cross-origin requests.

- **Description**: The headers allowed in your requests. Your request headers typically include 'Access-Control-Request-Headers', which relies on CORS configuration to allow its values.
- **Common Headers**:
  - `Content-Type` - For sending JSON/form data
  - `Authorization` - For authentication tokens
  - `X-Requested-With` - For AJAX identification
  - `Accept` - For content negotiation
- **Example**: `Content-Type, Authorization, X-Requested-With`

### Max Age (seconds)

Controls how long preflight request results can be cached.

- **Description**: Indicates how long (in seconds) the results of a preflight request can be cached by the browser.
- **Default**: 86400 seconds (24 hours)
- **Range**: 0 to maximum integer value
- **Performance Impact**: Longer cache times reduce preflight requests but may delay policy changes.

### Allow Credentials

Controls whether credentials can be included in cross-origin requests.

- **Description**: Allows the use of credentials (cookies, authorization headers, or TLS client certificates) when performing requests.
- **Default**: false
- **Security Warning**: When enabled, you cannot use `*` for Allow-Origin; you must specify exact origins.

## Configuration Examples

### Basic Development Setup

For development environments where security is less critical:

```json
{
  "corsSettings": {
    "enabled": true,
    "allowedOrigins": ["http://localhost:3000", "http://localhost:4200"],
    "allowedMethods": ["GET", "POST", "PUT", "DELETE"],
    "allowedHeaders": ["Content-Type", "Authorization"],
    "maxAge": 86400,
    "allowCredentials": false
  }
}
```

### Production Setup with Multiple Domains

For production environments with specific allowed origins:

```json
{
  "corsSettings": {
    "enabled": true,
    "allowedOrigins": [
      "https://app.mycompany.com",
      "https://admin.mycompany.com",
      "(https)://.*\\.mycompany\\.com"
    ],
    "allowedMethods": ["GET", "POST", "PUT"],
    "allowedHeaders": [
      "Content-Type", 
      "Authorization", 
      "X-Requested-With",
      "X-CSRF-Token"
    ],
    "maxAge": 7200,
    "allowCredentials": true
  }
}
```

### Single Page Application (SPA) Setup

For SPAs that need to authenticate users:

```json
{
  "corsSettings": {
    "enabled": true,
    "allowedOrigins": ["https://myapp.example.com"],
    "allowedMethods": ["GET", "POST", "OPTIONS"],
    "allowedHeaders": [
      "Content-Type",
      "Authorization",
      "X-Requested-With",
      "Accept"
    ],
    "maxAge": 3600,
    "allowCredentials": true
  }
}
```

### API Testing and Documentation

For enabling Swagger "try-it" functionality:

```json
{
  "corsSettings": {
    "enabled": true,
    "allowedOrigins": [
      "https://petstore.swagger.io",
      "https://editor.swagger.io"
    ],
    "allowedMethods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allowedHeaders": [
      "Content-Type",
      "Authorization",
      "X-Requested-With",
      "Accept",
      "Origin"
    ],
    "maxAge": 86400,
    "allowCredentials": false
  }
}
```

## Relationship with API-level CORS

It's important to understand that Security Domain CORS settings and API-level CORS settings serve different purposes:

### Security Domain CORS
- Applies to AM Gateway authentication and authorization endpoints
- Controls access to OAuth2, OpenID Connect, SAML, and other auth protocol endpoints
- Managed through AM Console > Domain Settings > Entrypoints

### API-level CORS (in APIM)
- Applies to your business APIs managed through API Management
- Controls access to your application's REST APIs
- Managed through APIM Console > API > Proxy > CORS

### Interaction Between Both
When both are configured:
1. Security Domain CORS handles authentication flows
2. API-level CORS handles business API access
3. Both must be properly configured for end-to-end functionality
4. Frontend applications typically need both to work seamlessly

## Configuration via AM Management API

You can configure CORS settings programmatically using the AM Management API:

```bash
# Get current domain configuration
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type: application/json" \
     -X GET \
     http://GRAVITEE-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains/:domainId

# Update CORS settings
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type: application/json" \
     -X PATCH \
     -d '{
       "corsSettings": {
         "enabled": true,
         "allowedOrigins": ["https://myapp.example.com"],
         "allowedMethods": ["GET", "POST", "PUT"],
         "allowedHeaders": ["Content-Type", "Authorization"],
         "maxAge": 3600,
         "allowCredentials": true
       }
     }' \
     http://GRAVITEE-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains/:domainId
```

## Best Practices

### Security
- **Avoid wildcards in production**: Never use `*` for Allow-Origin in production environments
- **Minimize allowed methods**: Only enable HTTP methods your applications actually use
- **Specific origins**: Always specify exact origins rather than broad patterns when possible
- **Credential handling**: Be cautious when enabling credentials; ensure origins are explicitly listed

### Performance
- **Appropriate cache times**: Set Max Age based on how frequently your CORS policies change
- **Minimal headers**: Only allow headers that your applications actually send
- **Monitor preflight requests**: Track preflight request frequency to optimize cache settings

### Development vs Production
- **Development**: More permissive settings for easier testing
- **Production**: Restrictive settings following the principle of least privilege
- **Staging**: Mirror production settings to catch configuration issues early

## Troubleshooting Common Issues

### CORS Error: "Access blocked by CORS policy"
1. Verify the requesting origin is in the allowedOrigins list
2. Check that the HTTP method is in the allowedMethods list
3. Ensure required headers are in the allowedHeaders list
4. Verify CORS is enabled for the Security Domain

### Preflight Requests Failing
1. Confirm OPTIONS method is allowed (usually automatic)
2. Check that Access-Control-Request-Method header matches allowed methods
3. Verify Access-Control-Request-Headers match allowed headers

### Credentials Not Sent
1. Ensure allowCredentials is set to true
2. Verify allowedOrigins does not contain `*`
3. Check that frontend code includes credentials in requests

### Changes Not Taking Effect
1. Clear browser cache and hard refresh
2. Check Max Age settings - cached preflight responses may be active
3. Verify configuration was saved correctly in AM Console

## Migration from Default Settings

If you're migrating from default CORS settings to Security Domain-specific settings:

1. **Document current behavior**: Test and document what currently works
2. **Start permissive**: Begin with slightly more permissive settings than defaults
3. **Gradually restrict**: Tighten settings incrementally while testing
4. **Monitor logs**: Watch for CORS-related errors during the transition
5. **Have a rollback plan**: Keep default settings ready in case of issues

## Monitoring and Logging

Enable appropriate logging to monitor CORS behavior:

```yaml
# In gravitee.yml
logging:
  gravitee: INFO
  level:
    io.gravitee.am.gateway.handler.vertx.cors: DEBUG
```

This will help you:
- Track CORS-related requests and responses
- Identify configuration issues
- Monitor security-related access attempts
- Debug integration problems

By following this guide, you should be able to successfully configure CORS at the Security Domain level in Gravitee Access Management, ensuring secure and functional cross-origin access to your authentication and authorization endpoints.