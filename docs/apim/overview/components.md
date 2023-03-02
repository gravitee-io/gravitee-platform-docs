# Components

Gravitee.io APIM is separated into four main components:

1. [APIM Gateway](components.md#apim-gateway)
2. [APIM API](components.md#apim-api)
3. [APIM Console](components.md#apim-console)
4. [APIM Portal](components.md#apim-portal)

## APIM Gateway

APIM Gateway is the core component of the APIM platform. You can think of it like a _**smart**_ proxy.

Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply [policies](broken-reference) (i.e., rules) to both HTTP requests and responses according to your needs. With these policies, you can enhance request and response processing by adding transformations, security, and many other exciting features.

**Gravitee.io - Internal Gateway**

![Gravitee.io — Internal Gateway](../../../images/apim/3.x/overview/components/new-components-apim-gateway-internal-gateway.png)

## APIM API

This RESTful API exposes services to manage and configure the [APIM Console](broken-reference) and [APIM Portal](broken-reference) web UIs. All exposed services are restricted by authentication and authorization rules. For more information, see the [API Reference](broken-reference) section.

## APIM Console

This web UI gives easy access to some key [APIM API](components.md#apim-api) services. [API Publishers](broken-reference) can use it to publish APIs. Administrators can also configure global platform settings and specific portal settings.

## APIM Portal

This web UI gives easy access to some key [APIM API](components.md#apim-api) services. [API Consumers](broken-reference) can use it to search for, view, try out and subscribe to a published API. They can also use it to manage their [applications](broken-reference).
