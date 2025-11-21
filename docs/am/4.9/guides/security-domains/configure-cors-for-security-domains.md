# Configure CORS for Security Domains

## Overview

Cross-Origin Resource Sharing (CORS) is a browser security feature that restricts web pages from making requests to a different domain than the one serving the web page, unless that domain explicitly allows it. When a web application tries to access resources from a different origin, the browser performs a "preflight" request to check if the cross-origin request is allowed. In Gravitee Access Management, CORS can be configured at the Security Domain level to manage cross-origin requests for your authentication and authorization endpoints.

This guide explains how to configure CORS settings for Security Domains, including the available options, their impact, and the relationship between Security Domain CORS and API-level CORS settings.

### Why Configure CORS for Security Domains?

In AM, CORS configuration at the Security Domain level is important for scenarios like:

* When frontend applications are hosted on different domains than the AM Gateway and need to make cross-origin requests.
* Single-page applications (SPAs) need to authenticate users.
* Third-party applications integrate with and consume authentication endpoints.

## Access CORS in the AM Console

1.  Sign in to your AM Console. The Access Management dashboard appears after login.

    <figure><img src="../../../4.8/.gitbook/assets/access-management-dashboard (1).png" alt=""><figcaption></figcaption></figure>
2.  From the Dashboard, Click **Settings.**

    <figure><img src="../../../4.8/.gitbook/assets/am-settings-left-nav (1).png" alt=""><figcaption></figcaption></figure>
3.  In the settings menu, click **Entrypoints.**

    <figure><img src="../../../4.8/.gitbook/assets/entrypoint-security-domain (1).png" alt=""><figcaption></figcaption></figure>
4.  Turn on the **Enable CORS** toggle.

    <figure><img src="../../../4.8/.gitbook/assets/enable-cors-toggle-button (1).png" alt=""><figcaption></figcaption></figure>

The CORS configuration includes a toggle to enable or disable CORS for the Security Domain. When CORS is disabled, AM uses the default values from the `gravitee.yml` configuration file.

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

## Configure CORS Parameters

You can configure the following CORS parameters:

* [#allow-origin](configure-cors-for-security-domains.md#allow-origin "mention")
* [#allow-methods](configure-cors-for-security-domains.md#allow-methods "mention")
* [#allow-headers](configure-cors-for-security-domains.md#allow-headers "mention")
* [#max-age-seconds](configure-cors-for-security-domains.md#max-age-seconds "mention")
* [#allow-credentials](configure-cors-for-security-domains.md#allow-credentials "mention")

### Allow-Origin

The `Allow-Origin` setting specifies which origins are permitted to access the resources. An origin consists of three components: the scheme, domain, and the port. All three components must match for requests to be considered same-origin.

{% hint style="danger" %}
When Allow Credentials is enabled, the wildcard (`*`) cannot be used for Allow-Origin. You must specify exact origins instead.
{% endhint %}

<figure><img src="../../../4.8/.gitbook/assets/allow-origin-parameter (1).png" alt=""><figcaption></figcaption></figure>

The following examples demonstrate common `Allow-Origin` configurations:

* `*` - Allows all origins
* `https://mydomain.com` - Allows specific domain
* `(http|https).*.mydomain.com` - Allows subdomains using regex patterns

### Allow-Methods

The `Allow-Methods` setting specifies which HTTP methods are allowed when accessing the resource.

<figure><img src="../../../4.8/.gitbook/assets/allow-methods-parameter (1).png" alt=""><figcaption></figcaption></figure>

Configuration details for `Allow Methods` include the following:

* Available methods: GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD.
* Default: GET, POST, PUT, PATCH, DELETE.

### Allow-Headers

The `Allow-Headers` setting defines which headers can be used in cross-origin requests. The request headers include 'Access-Control-Request-Headers', which relies on CORS configuration to allow its values.

<figure><img src="../../../4.8/.gitbook/assets/allow-headers-access-management (1).png" alt=""><figcaption></figcaption></figure>

Configuration details for `Allow Headers` include:

* `Content-Type` - For sending JSON/form data.
* `Authorization` - For authentication tokens.
* `X-Requested-With` - For AJAX identification.
* `Accept` - For content negotiation. Example: `Content-Type, Authorization, X-Requested-Wita`

### Max Age (Seconds)

The `Max age` setting controls how long pre-flight request results are cached.

<figure><img src="../../../4.8/.gitbook/assets/max-age-seconds (1).png" alt=""><figcaption></figcaption></figure>

The following configuration details apply to `Max age`:

* **Default**: 86400 seconds (24 hours)
* **Range**: 0 to 2147483647 seconds

### Allow Credentials

The `Allow Credentials` setting controls whether credentials can be included in cross-origin requests. For example: cookies, authorization headers, and TLS client certificates.

{% hint style="danger" %}
When enabled, you cannot use `*` for Allow-Origin; you must specify exact origins.
{% endhint %}

<figure><img src="../../../4.8/.gitbook/assets/allow-use-credentials (1).png" alt=""><figcaption></figcaption></figure>

For example:

* **Default**: false

## Configuration Examples

The following examples demonstrate common CORS configurations for different use cases and environments:

### Basic Development Setup

For development environments use the following configuration:

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

For production environments with specific allowed origins use the following configuration:

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

For SPAs that need to authenticate users use the following configuration:

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

For enabling Swagger interactive testing functionality:

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
