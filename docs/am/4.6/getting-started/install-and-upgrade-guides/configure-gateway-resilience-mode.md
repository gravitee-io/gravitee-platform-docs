# Configure Gateway Resilience Mode

## Overview

Authenticating user is vital to ensuring that the correct user has access to the correct information at the correct time. Gravitee Access Management (AM) is a critical component in this setup, and it is key to many customers that Access Management performs well in resilience.

The AM Gateway is a key node for handling authentication traffic. However Access Management Applications relies on the Control Plane and the database connection to fulfill its capabilities.

{% hint style="info" %}
**Definitions**

The **Control Plane** is the management part of Access Management where configurations are defined before been deployed on the Gateway. In term of data storage, Control plan relies on the `management` repository scope.

The **Data Plane** is the runtime part of Access Management where configuration are loaded and allows end user or application authentication. For data storage, the data plan relies on the `gateway` and `oauth2` repository scopes.
{% endhint %}

To ensure that the AM can still perform its key responsibilities when the the gateway cannot communicate with the control plane, there is a **resilience mode**. This mode comes with some drawbacks of non functioning features that require connection to the control plane.

{% hint style="info" %}
Resilience mode is the first step in the evolution of Access Management architecture  to providing a clean separation between the Control plane and the Data plane. The resilience mode has been introduce to reduce the gateway interactions with the control plan without major architecture changes.
{% endhint %}

## Limitations

As the gateway relies on the control plane for many capabilities, in relisience mode, a few reduced functionality areas have been identified when the Control Plane becomes unreachable. Here are identified areas:

* If identity providers are not backed by the Control Plan (social providers, LDAP, ...) login works.
* WebAuhtn will not be usable as the credentials are currently under the `management` repository scope.
* Audits sent to the default reporter will be lost. To fix this issue, alternative reporters can be configured. For example, Kafka reporter.&#x20;
* If tokens are generated for an end user, introspection will work without Control Plan access only if the user profile remains in the User cache. If the user is missing from the cache, instrospect will reject the token.&#x20;
* Tokens delivered when Control Plan is down may not be possible to revoke.
* Refresh token works as far as the user is present into the cache. If the cache does not contain the user profile, refreshing the token fails.
* Groups and roles statically assigned to a user may not be retrieved for the user. Tokens are generated without those information. To fix this issue, dynamic group mapping has been introduced.
* If the user profile is store in the cache, MFA works with OTP, Email, or SMS factors. If the user profile is evicted from the cache before the connectivity with the Control plan is back to normal, the user experience may be degraded. For example, if the user profile with an enrolled factor is present in the Control Plane but the user profile is missing from the cache on the Data Plan side, then during the sign in phase when the Control Plan is unreachable, factor enrollment is proposed to the user once again. When the Control Plan returns, the user may have to ask for a factor reset because information owned by the Factor App may differ from the information owned by the Control Plan.
* The gateway can only propagate claims or attributes coming from the Identity Provider.
* **Reset password** does not work
* **User registration** does not work
* SCIM does not work
* Usage of Extension Grant flow does not work
* Without connection to Control Plane/Database, the Gateway does not start&#x20;

{% hint style="warning" %}
Resilience mode is available only for domains created starting from the version 4.5.0. Domains created in previous version ignore this mode.
{% endhint %}

## Configuring the resilience mode

The resilience mode requires configuration on the Gateway gravitee.yaml.&#x20;

* Configure the gateway and oauth2 scopes to target a database different from the one used for the management scope

```
repositories:
  management:
    type: mongodb
    mongodb:
      dbname: myCPDatabase
      host: control-plan.hostname
      ...
  gateway:
    type: mongodb
    # do not use the same connection pool
    # as the management scope
    use-management-settings: false
    mongodb:
      dbname: myDPDatabase
      host: data-plan.hostname
      ...
  oauth2:
    type: mongodb
    # do not use the same connection pool
    # as the management scope
    use-management-settings: false
    mongodb:
      dbname: myDPDatabase
      host: data-plan.hostname
      ...
```

* Configure the cache storage. For more information about configuring the cache storage, see [Configuration](configure-gateway-resilience-mode.md#configuration) section. Here is an example of a cache storage configuration:

```
cache:
  type: redis
  redis:
    host: localhost
    port: 6379
```

* Configure the User cache time to live. For more information about configuring the cache storage, see [Configuration](configure-gateway-resilience-mode.md#configuration) section. Here is an example of a User management configuration:

```
# User management configuration
user:
  # keep user profile during authentication flow
  # into a cache to limit read access to the Database
  # when the Gateway is looking for the profile linked to the session
  cache:
    # retention duration in seconds
    ttl: 3600
```

* Enable the resilience mode by using the following code

```
resilience:
    enabled: true
```
