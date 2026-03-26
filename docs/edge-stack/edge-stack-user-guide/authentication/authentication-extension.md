---
description: Overview of Authentication Extension.
noIndex: true
---

# Authentication Extension

Edge Stack ships with an authentication service that is enabled to perform OAuth, JWT validation, and custom authentication schemes. It can perform different authentication schemes on different requests allowing you to enforce authentication as your application needs.

The Filter and FilterPolicy resources are used to [configure how to do authentication](../../technical-reference/filters/using-filters-and-filterpolicies.md). This doc focuses on how to deploy and manage the authentication extension.

### Edge Stack configuration

Edge Stack uses the [AuthService plugin](../../technical-reference/plug-in-services/authentication-service.md) to connect to the authentication extension.

The default AuthService is named `ambassador-edge-stack-auth` and is defined as:

```yaml
apiVersion: getambassador.io/v3alpha1
kind: AuthService
metadata:
  name: ambassador-edge-stack-auth
  namespace: ambassador
spec:
  auth_service: 127.0.0.1:8500
  proto: grpc
  status_on_error:
    code: 503
  allow_request_body: false
```

This configures Envoy to talk to the extension process running on port 8500 using gRPC and trim the body from the request when doing so. The default error code of 503 is usually overwritten by the Filter that is authenticating the request.

This default AuthService works for most use cases. If you need to tune how Edge Stack connects to the authentication extension (like changing the default timeout), you can find the full configuration options in the [AuthService plugin docs](../../technical-reference/plug-in-services/authentication-service.md).

### Authentication extension configuration

Certain use cases may require some tuning of the authentication extension. Configuration of this extension is managed via environment variables. [The Ambassador container](../deployment/ambassador-edge-stack-environment-variables-and-ports.md) has a full list of environment variables available for configuration, including the variables used by the authentication extension.

**Redis**

The authentication extension uses Redis for caching the response from the `token endpoint` when performing OAuth.

Edge Stack shares the same Redis pool for all features that use Redis. More information is available for [tuning Redis](../deployment/ambassador-edge-stack-and-redis.md) if needed.

**Timeout variables**

The `AES_AUTH_TIMEOUT` environment variable configures the default timeout in the authentication extension.

This timeout is necessary so that any error responses configured by Filters that the extension runs make their way to the client. Otherwise they would be overruled by the timeout from Envoy if a request takes longer than five seconds.

If you have a long chain of Filters or a Filter that takes five or more seconds to respond, you can increase the timeout value to give your Filters enough time to run.

{% hint style="warning" %}
The `timeout_ms` of the `ambassador-edge-stack-auth` AuthService defaults to a value of 5000 (five seconds). You will need to adjust this as well.`AES_AUTH_TIMEOUT` should always be around one second shorter than the `timeout_ms` of the AuthService to ensure Filter error responses make it to the client.The External Filter also have a `timeout_ms` field that must be set if a single Filter will take longer than five seconds.
{% endhint %}
