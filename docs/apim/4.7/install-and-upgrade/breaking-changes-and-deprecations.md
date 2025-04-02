---
description: >-
  This page describes the breaking changes and the deprecated functionality that
  may occur when upgrading Gravitee API Management
---

# Breaking Changes and Deprecations

## Breaking changes

Here are the breaking changes for versions 4.X of Gravitee and versions 3.X of Gravitee

### Breaking changes from 4.X

Here are the breaking changes from versions 4.X of Gravitee.

#### 4.7.0

**Azure API Management update**

There is a new parameter for ingesting Azure APIs. To ingest Azure APIs, you must set `gravitee_integration_providers_0_configuration_subscriptionApprovalType` in your `docker-compose.yaml` and set the `SUBSCRIPTION_APPROVAL_TYPE`  in your `.env` file to `AUTOMATIC` , `MANUAL` or `ALL` .

To keep the previous behavior of Azure API Management, set the `SUBSCRIPTION_APPROVAL_TYPE` to `AUTOMATIC` .

#### 4.6.0

**OpenTracing replaced by OpenTelemetry**

OpenTracing has been replaced by OpenTelemetry. If you use OpenTracing with the Jaeger plugin, you must update your configuration to target your OpenTelemetry endpoint.

#### 4.4.0

**gateway.management.http.trustall update**

The gateway.management.http.trustall has been renamed to trustALL. By default, trustAll is set to `false`. A public CA or a well configured continue to work.

**gateway|api.services.bridge.ssl.clientAuth no longer use a boolean value**

gateway|api.services.bridge.ssl.clientAuth no longer use a boolean value. Possible values are now the following values:

* `none`. This value was previously false
* `required`. Backward compatibility is maintained, true means required
* `request`.

#### 4.0.27

**ssl-redirect option changed to default**

In gateway ingress controller, the ssl-redirect option was changed from "false" to default. For more information about this change, go to [Server-side HTTPS enforcement through redirect](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#server-side-https-enforcement-through-redirect).

### Breaking changes from 3.X

Here are the breaking changes from versions 3.X of Gravitee.

#### 3.2.0

**Moved Probes configuration**

Probes configuration was moved under deployment.

**Probe default configuration**

Changed probe default configuration. For more information about the change to the default configuration, go to the following [GitHub pull request](https://github.com/gravitee-io/gravitee-api-management/pull/8885).

**Removed the apiSync parameter**

Under gateway.readinessProbe, the apiSync parameter was removed.

#### 3.1.55

**Use of smtp.properties.starttlsEnable**

Use smtp.properties.starttls.enable instead of smtp.properties.starttlsEnable.

## Deprecated functionality

Here is the deprecated functionality for 4.X versions of Gravitee and 3.X version of Gravitee.

### Deprecated functionality 4.X

Here is the deprecated functionality from 4.X of Gravitee

#### 4.4.0

**gateway.management.http.username deprecation**

To allow JWT auth to be configured, gateway.management.http.username and password have been deprecated to allow JWT auth to be configured. For more information about the deprecation, go to [Changelog](https://github.com/gravitee-io/gravitee-api-management/blob/master/helm/CHANGELOG.md).

### Deprecated functionality 3.X

Here is the deprecated functionality from 3.X of Gravitee

#### 3.20.28

**Deprecated api | gateway | ui | portal.security context is removed**

The deprecated api | gateway | ui | portal.security context has been removed.
