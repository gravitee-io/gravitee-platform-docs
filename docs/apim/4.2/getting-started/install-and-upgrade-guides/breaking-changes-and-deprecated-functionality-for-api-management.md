---
description: >-
  This page describes the breaking changes and the deprecated functionality that
  may occur when upgrading Gravitee API Management
---

# Breaking changes and deprecated functionality

## Breaking changes

Here are the breaking changes for versions 4.X of Gravitee and versions 3.X of Gravitee

### Breaking changes from 4.X

Here are the breaking changes from versions 4.X of Gravitee.&#x20;

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

### Deprecated functionality 3.X

Here is the deprecated functionality from 3.X of Gravitee

#### 3.20.28

**Deprecated api | gateway | ui | portal.security context is removed**

The deprecated api | gateway | ui | portal.security context has been removed.
