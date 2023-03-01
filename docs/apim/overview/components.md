---
title: APIM components
tags:
  - APIM
  - Components
---


# APIM components overview

Gravitee.io APIM is separated into four main components:

1. [APIM Gateway](#apim-gateway)
2. [APIM API](#apim-api)
3. [APIM Console](#apim-console)
4. [APIM Portal](#apim-portal)

## APIM Gateway

APIM Gateway is the core component of the APIM platform. You can think
of it like a ***smart*** proxy.

Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply [policies](plugins.md#policies) (i.e., rules) to both HTTP requests and responses according to your needs. With these policies, you can enhance request and response processing by adding transformations, security, and many other exciting features.

**Gravitee.io - Internal Gateway**

![Gravitee.io — Internal Gateway](/images/apim/3.x/overview/components/new-components-apim-gateway-internal-gateway.png "Gravitee.io — Internal Gateway")

## APIM API

This RESTful API exposes services to manage and configure the [APIM Console](introduction.md#apim-console) and [APIM Portal](introduction.md#apim-portal) web UIs. All exposed services are restricted by authentication and authorization rules. For more information, see the [API Reference](../api-reference/apim-rest-api-reference-index.md) section.

## APIM Console

This web UI gives easy access to some key [APIM API](#apim-api) services. [API Publishers](introduction.md#publisher) can use it to publish APIs. Administrators can also configure global platform settings and specific portal settings.

## APIM Portal

This web UI gives easy access to some key [APIM API](#apim-api) services. [API Consumers](introduction.md#consumer) can use it to search for, view, try out and subscribe to a published API. They can also use it to manage their [applications](introduction.md#application).
