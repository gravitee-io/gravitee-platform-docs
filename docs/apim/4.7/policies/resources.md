---
description: An overview about resources.
---

# Resources

## Overview

The following sections summarize resource descriptions, configuration parameters, and configuration examples.

## Create a resource

To create a resource:

1. Log in to APIM Management Console.
2. Click **APIs** in the left sidebar.
3. Select the API you want to add the resource to.
4. Click **Configuration** in the inner left sidebar.
5.  Click the **Resources** header.

    <figure><img src="../.gitbook/assets/A 1 config resources (1).png" alt=""><figcaption></figcaption></figure>
6. Click **+ Add resource**.
7.  Use the search field or scroll to select the resource you'd like to configure.

    <figure><img src="../.gitbook/assets/A 1 resources 2 (1).png" alt=""><figcaption></figcaption></figure>
8. Set the parameters in the resultant form. Configuration varies by resource type.

## Resource types

APIM includes several default resources, each of which is described in more detail below.

### Cache

The Cache resource maintains a cache linked to the API lifecycle, i.e., the cache is initialized when the API starts and released when the API stops. It is responsible for storing HTTP responses to avoid subsequent calls to the backend.

<table><thead><tr><th width="167">Config param</th><th width="304">Description</th><th>Default</th></tr></thead><tbody><tr><td>Cache name</td><td>Name of the cache</td><td>my-cache</td></tr><tr><td>Time to idle</td><td>The maximum number of seconds an element can exist in the cache without being accessed. When this threshold is reached, the element expires and will no longer be returned from the cache. The default value is 0, i.e., no timeToIdle (TTI) eviction takes place (infinite lifetime).</td><td>0</td></tr><tr><td>Time to live</td><td>Maximum number of seconds an element can exist in the cache, regardless of usage. When this threshold is reached, the element expires and will no longer be returned from the cache. The default value is 0, i.e., no timeToLive (TTL) eviction takes place (infinite lifetime).</td><td>0</td></tr><tr><td>Max entries on heap</td><td>The maximum objects to be held in local heap memory (0 = no limit).</td><td>1000</td></tr></tbody></table>

{% code title="Example" %}
```json
{
    "name": "cache",
    "type": "cache",
    "enabled": true,
    "configuration": {
        "name": "my-cache",
        "timeToIdleSeconds":0,
        "timeToLiveSeconds":0,
        "maxEntriesLocalHeap":1000
    }
}
```
{% endcode %}

### Cache Redis

The Cache Redis resource is the same as [Cache](resources.md#cache), but the current implementation is based on Redis. The Cache Redis resource can be configured standalone or as part of the Redis Sentinel monitoring solution. The majority of Cache Redis configuration options are common to both modes of operation, but several are exclusive to either standalone or Sentinel as indicated with a **bold asterisk (\*)**.

{% hint style="warning" %}
The **Cache Redis** plugin is not included in the default APIM distribution, but you can [download](https://download.gravitee.io/#graviteeio-apim/plugins/resources/gravitee-resource-cache-redis/) and [deploy](../getting-started/plugins/deployment.md#deployment) it. For information on configuring cache in APIM, see [Configure cache](../configure-apim/cache.md). For information on configuring the rate limit repository plugin for Redis, see [Redis](../configure-apim/repositories/redis.md#redis).
{% endhint %}

<table><thead><tr><th width="167">Config param</th><th width="304">Description</th><th>Default</th><th>EL support</th><th>Secret support</th></tr></thead><tbody><tr><td>name</td><td>Name of the cache</td><td>my-redis-cache</td><td>Yes</td><td>No</td></tr><tr><td>releaseCache</td><td><p>Enabled: The resource will release the cache when the API is stopped</p><p>Disabled: The cache must be managed manually on the Redis server</p></td><td>false</td><td>No</td><td>No</td></tr><tr><td>maxTotal</td><td>Maximum number of connections supported by the pool</td><td>8</td><td>No</td><td>No</td></tr><tr><td>password</td><td>The password for the instance</td><td>-</td><td>Yes</td><td>yes</td></tr><tr><td>timeToLiveSeconds</td><td>Maximum number of seconds an element can exist in the cache, regardless of usage. When this threshold is reached, the element expires and will no longer be returned from the cache. The default value is 0, i.e., no timeToLive (TTL) eviction takes place (infinite lifetime).</td><td>0</td><td>No</td><td>No</td></tr><tr><td>Timeout</td><td>Specifies the connection timeout and the read/write timeout</td><td>2000</td><td>No</td><td>No</td></tr><tr><td>useSsl</td><td>Toggle to use SSL connections</td><td>true</td><td>No</td><td>No</td></tr><tr><td>Use standalone mode</td><td>Toggle to use standalone mode</td><td>true</td><td></td><td></td></tr><tr><td>Host</td><td>The host of the instance<br><strong>*Standalone config only</strong></td><td>localhost</td><td>Yes</td><td>No</td></tr><tr><td>Port</td><td>The port of the instance<br><strong>*Standalone config only</strong></td><td>6379</td><td>No</td><td>No</td></tr><tr><td>sentielMode</td><td>Sentinel provides high availability for Redis. In practical terms this means that using Sentinel you can create a Redis deployment that resists without human intervention certain kinds of failures.</td><td>false</td><td>No</td><td>No</td></tr><tr><td>Master</td><td>Sentinel master ID<br><strong>*Sentinel config only</strong></td><td>sentinel-master</td><td>No</td><td>No</td></tr><tr><td>Sentinel password</td><td>Sentinel password<br><strong>*Sentinel config only</strong></td><td>-</td><td>Yes</td><td>Yes</td></tr><tr><td>Sentinel nodes</td><td>Array of sentinel nodes<br><strong>*Sentinel config only</strong></td><td>-</td><td>No</td><td>No</td></tr></tbody></table>

{% code title="Standalone example" %}
```json
{
    "name": "my-redis-cache",
    "type": "cache-redis",
    "enabled": true,
    "configuration": {
        "name": "my-redis-cache",
        "releaseCache": false,
        "maxTotal": 8,
        "password": "secret",
        "timeToLiveSeconds": 600,
        "timeout": 2000,
        "useSsl": true,
        "sentinelMode" : false,
        "standalone": {
            "host": "localhost",
            "port": 6379
        }
    }
}
```
{% endcode %}

{% code title="Sentinel example" %}
```json
{
    "name" : "my-redis-cache",
    "type" : "cache-redis",
    "enabled" : true,
    "configuration" : {
        "name" : "my-redis-cache",
        "releaseCache": false,
        "maxTotal" : 8,
        "password" : "secret",
        "timeToLiveSeconds" : 600,
        "timeout" : 2000,
        "useSsl" : true,
        "sentinelMode" : true,
        "sentinel" : {
            "masterId" : "sentinel-master",
            "password" : "secret",
            "nodes": [
              {
                "host" : "localhost",
                "port" : 26379
              },
              {
                "host" : "localhost",
                "port" : 26380
              },
              {
                "host" : "localhost",
                "port" : 26381
              }
            ]
        }
    }
}
```
{% endcode %}

### OAuth2 Gravitee AM Authorization Server

The OAuth2 Gravitee AM Authorization Server resource introspects an access token generated by a Gravitee AM instance.

<table><thead><tr><th width="177">Config param</th><th width="414">Description</th><th>Default</th></tr></thead><tbody><tr><td>Resource name</td><td>Name of the resource</td><td>-</td></tr><tr><td>Server URL</td><td>URL of the Gravitee Access Management server</td><td>-</td></tr><tr><td>System proxy</td><td>Toggle to use system proxy</td><td>false</td></tr><tr><td>Version</td><td>Version of the Access Management server</td><td>V3_X</td></tr><tr><td>Security domain</td><td>Security domain (realm) from which the token has been generated and must be introspected</td><td>-</td></tr><tr><td>Client ID</td><td>Client identifier</td><td>-</td></tr><tr><td>Client secret</td><td>Client secret</td><td>-</td></tr><tr><td>User claim</td><td>User claim field to store end user in log analytics</td><td>sub</td></tr></tbody></table>

{% code title="Example" %}
```json
{
    "configuration": {
        "clientId": "my-client",
        "clientSecret": "f2ddb55e-30b5-4a45-9db5-5e30b52a4574",
        "securityDomain": "my-security",
        "serverURL": "https://graviteeio_access_management",
        "userClaim": "sub"
    }
}
```
{% endcode %}

### OAuth2 Generic Authorization Server

The OAuth2 Generic Authorization Server resource introspects an access token generated by a generic OAuth2 authorization server. This resource provides a configuration for how token introspection is applied to accommodate common authorization servers.

<table><thead><tr><th width="190">Property</th><th width="245">Description</th><th>Default</th><th>Support EL</th><th>Support Secret</th></tr></thead><tbody><tr><td>introspectionEndpoint</td><td>URL the resource uses to introspect an incoming access token</td><td>/oauth/check_token</td><td>Yes</td><td>No</td></tr><tr><td>useSystemProxy</td><td>Toggle to use system proxy</td><td>false</td><td>No</td><td>No</td></tr><tr><td>introspectionEndpointMethod</td><td>HTTP method to introspect the access token</td><td>GET</td><td>No</td><td>No</td></tr><tr><td>clientId</td><td>Client identifier</td><td>-</td><td>Yes</td><td>Yes</td></tr><tr><td>clientSecret</td><td>Client secret</td><td>-</td><td>Yes</td><td>Yes</td></tr><tr><td>useClientAuthorizationHeader</td><td>To prevent token scanning attacks, the endpoint MUST require access authorization. Gravitee uses an HTTP header for client authentication</td><td>true</td><td>No</td><td>No</td></tr><tr><td>clientAuthorizationHeaderName</td><td>Authorization header</td><td>Authorization</td><td>Yes</td><td>No</td></tr><tr><td>AuthclientAuthorizationHeaderScheme</td><td>Authorization scheme</td><td>Basic</td><td>Yes</td><td>No</td></tr><tr><td>tokenIsSuppliedByQueryParam</td><td>Access token is passed to the introspection endpoint using a query parameter</td><td>true</td><td>No</td><td>No</td></tr><tr><td>tokenQueryParamName</td><td>Query parameter that supplies the access token</td><td>token</td><td>No</td><td>No</td></tr><tr><td>tokenIsSuppliedByHttpHeader</td><td>The access token is passed to the introspection endpoint using an HTTP header</td><td>false</td><td>No</td><td>No</td></tr><tr><td>tokenHeaderName</td><td>HTTP header used to supply the access token</td><td>-</td><td>Yes</td><td>No</td></tr></tbody></table>

{% code title="Example" %}
```json
{
    "configuration": {
        "introspectionEndpoint": "https://my_authorization_server/oauth/check_token",
        "introspectionEndpointMethod": "POST",
        "clientAuthorizationHeaderName": "Authorization",
        "clientAuthorizationHeaderScheme": "Basic",
        "clientId": "my-client",
        "clientSecret": "f2ddb55e-30b5-4a45-9db5-5e30b52a4574",
        "tokenIsSuppliedByHttpHeader": false,
        "tokenIsSuppliedByQueryParam": true,
        "tokenQueryParamName": "token",
        "useClientAuthorizationHeader": true
    }
}
```
{% endcode %}

### Confluent Schema Registry

The Confluent Schema Registry resource fetches serialization/deserialization data from a Confluent schema registry.

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, the ability to use Confluent Schema Registry as a resource is an [Enterprise Edition](../overview/enterprise-edition.md) capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

<table><thead><tr><th width="199">Config param</th><th width="316">Description</th><th>Default</th></tr></thead><tbody><tr><td>Resource name</td><td>Name of the resource</td><td>-</td></tr><tr><td>Registry URL</td><td>URL of the schema registry</td><td>-</td></tr><tr><td>Use proxy</td><td>Toggle to use proxy to fetch schema</td><td>false</td></tr><tr><td>Proxy type</td><td>The type of the proxy</td><td>HTTP CONNECT proxy</td></tr><tr><td>Use system proxy</td><td>Toggle to use proxy configured at system level</td><td>false</td></tr><tr><td>Proxy host</td><td>Proxy host to connect to</td><td>-</td></tr><tr><td>Proxy port</td><td>Proxy port to connect to</td><td>-</td></tr><tr><td>Proxy username</td><td>Optional proxy username</td><td>-</td></tr><tr><td>Proxy password</td><td>Optional proxy password</td><td>-</td></tr><tr><td>Authentication mode</td><td>The authentication mode used to connect to Schema Registry</td><td>Basic</td></tr><tr><td>Authentication username</td><td>Authentication username</td><td>-</td></tr><tr><td>Authentication password</td><td>Authentication password</td><td>-</td></tr><tr><td>Verify host</td><td>Toggle to enable host name verification</td><td>true</td></tr><tr><td>Trust all</td><td>Toggle to force the Gateway to trust any origin certificates. Use with caution over the Internet. The connection will be encrypted but this mode is vulnerable to 'man in the middle' attacks.</td><td>false</td></tr><tr><td>Trust store type</td><td>The type of the trust store</td><td>None</td></tr><tr><td>Key store type</td><td>The type of the key store</td><td>None</td></tr></tbody></table>

### Keycloak Adapter

The Keycloak Adapter resource introspects an access token.

| Config param                  | Description                                           | Default |
| ----------------------------- | ----------------------------------------------------- | ------- |
| Resource name                 | The name of the resource                              | -       |
| Keycloak client configuration | The configuration of the Keycloak client              | -       |
| Local token validation        | Toggle to use local token validation                  | true    |
| User claim                    | User claim field to store end user in log analytics   | sub     |
| Verify host                   | Verify certificate on SSL connection to Keycloak host | false   |
| Trust all                     | Trust all certificates, including self-signed         | true    |

### Content Provider Inline Resource

The Content Provider Inline Resource is used to store an inline text and provide it to compatible policies.

<table><thead><tr><th width="167">Config param</th><th width="304">Description</th><th>Default</th></tr></thead><tbody><tr><td>Resource name</td><td>The name of the resource</td><td>-</td></tr><tr><td>Content</td><td>The content to provide</td><td></td></tr><tr><td>Attributes</td><td>List of attributes as key value pairs</td><td></td></tr></tbody></table>

### HTTP Authentication Provider

The HTTP Authentication Provider resource validates user credentials against an HTTP server.

<table><thead><tr><th width="174">Config param</th><th width="227">Description</th><th>Default</th></tr></thead><tbody><tr><td>Resource name</td><td>The name of the resource</td><td>-</td></tr><tr><td>HTTP method</td><td>HTTP method to invoke the endpoint</td><td>POST</td></tr><tr><td>Use system proxy</td><td>Toggle to use the system proxy configured by your administrator</td><td>false</td></tr><tr><td>URL</td><td>Server URL</td><td>-</td></tr><tr><td>Request body</td><td>The body of the HTTP request. Supports the Gravitee Expression Language.</td><td>-</td></tr><tr><td>Authentication condition</td><td>The condition to be verified to validate that the authentication is successful. Supports the Gravitee Expression Language.</td><td>{#authResponse.status == 200}</td></tr></tbody></table>

### Inline Authentication Provider

The Inline Authentication Provider resource authenticates a user in memory.

| Property       | Required | Description                                                                                 | Type   | Default |
| -------------- | -------- | ------------------------------------------------------------------------------------------- | ------ | ------- |
| serverURL      | Yes      | The URL of the Gravitee.io Access Management server.                                        | string | N/A     |
| securityDomain | Yes      | The security domain (realm) from where the token has been generated and must be introspect. | string |         |
| clientId       | Yes      | The client identifier.                                                                      | string |         |
| clientSecret   | Yes      | The client secret                                                                           | string |         |

### LDAP Authentication Provider

The LDAP Authentication Provider resource authenticates a user in LDAP.

#### Configuration

The following table shows the available configurations for the LDAP Authentication provider, including if the resource supports Secrets. For more information about Secrets, see [api-level-secrets.md](../configure-v4-apis/api-level-secrets.md "mention").

| Property              | Required | Description                                                                                                                                                    | Type             | Default                         | Supports EL | Supports Secrets |
| --------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ------------------------------- | ----------- | ---------------- |
| contextSourceUrl      | Yes      | URL to the LDAP server instance                                                                                                                                | string           | ldap://myserver.example.com:389 | Yes         | Yes              |
| contextSourceBase     | Yes      | The source base used to authenticate to the LDAP server and query for users when validating user’s credentials                                                 | string           | N/A                             | Yes         | Yes              |
| contextSourceUsername | Yes      | Username credential used to connect to the LDAP server                                                                                                         | string           | N/A                             | Yes         | Yes              |
| contextSourcePassword | Yes      | Password credential used to connect to the LDAP server                                                                                                         | string           | N/A                             | Yes         | Yes              |
| useStartTLS           | No       | Should the API gateway use SSL to connect to the LDAP server                                                                                                   | boolean          | false                           | No          | No               |
| userSearchFilter      | Yes      | LDAP Filter to select the relevant attribute to check the username                                                                                             | string           | uid={0}                         | Yes         | No               |
| userSearchBase        | No       | Search base within `contextSourceBase` used to search into the correct OU when validating user’s credentials.                                                  | string           | ou=users                        | Yes         | No               |
| cacheMaxElements      | Yes      | Maximum number of elements within the cache used to store successful authentications. 0 means no cache.                                                        | positive integer | 100                             | No          | No               |
| cacheTimeToLive       | Yes      | Maximum time to live (in milliseconds) of the elements from the cache used to store successful authentications.                                                | positive integer | 6000 (min 1000)                 | No          | No               |
| attributes            | Yes      | User LDAP attributes to put in the request context. Attributes can then be read from any other policy supporting EL i.e. `gravitee.attribute.user.{attribute}` | array of string  | \[\*]\(all)                     | No          | No               |
| connectTimeout        | No       | Duration of time in milliseconds that connects will block.                                                                                                     | positive integer | 5000                            | No          | No               |
| responseTimeout       | No       | Duration of time in milliseconds to wait for responses                                                                                                         | positive integer | 5000                            | No          | No               |
| minPoolSize           | No       | Minimum pool of connections to be initialized                                                                                                                  | positive integer | 5                               | No          | No               |
| maxPoolSize           | No       | Maximum pool of connections can grow to                                                                                                                        | positive integer | 15                              | No          | No               |
