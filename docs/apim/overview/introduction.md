---
title: Introduction to Gravitee API Management (APIM)
tags:
  - APIM
  - Introduction
---

# Introduction to Gravitee API Management (APIM)

Organizations need API management solutions to publish their APIs to
external developers, internal developers, and other partners. API
management can unlock the potential of the organization’s data and
services, as well as facilitate the transformation to OpenAPI and
OpenData, extending the company’s digital platform offerings, opening
new communication channels, and finding new customers.

Naturally, a growing customer base brings new challenges, such as:

-   How to reduce the time taken to enroll new partners.

-   How to identify partners and manage their API consumption.

-   How to measure consumption from a consumer and/or producer point of
    view.

-   How to share existing APIs and how to discover them.

-   How to manage the API lifecycle, versioning, documentation, and so
    on.

How can businesses address all these challenges seamlessly, for all
APIs, using a centralized tool? Simple – by choosing Gravitee.io API
Management.

## What Is Gravitee.io API Management?

Gravitee.io API Management (APIM) is a flexible, lightweight, and
blazing-fast open source API management solution that gives your
organization full control over who accesses your API — when and how.
APIM is both simple to use and powerful, acting as a global solution for
API management. Gravitee.io APIM is composed of four main components:

1. [APIM Gateway](#apim-gateway)
2. [APIM API](#apim-api)
3. [APIM Console](#apim-console)
4. [APIM Portal](#apim-portal)

We’ll dive into these components in detail in their respective sections.

## Why Gravitee.io API Management?

Our goal in launching Gravitee.io APIM is to provide users with a highly
flexible and scalable solution that integrates with their infrastructure
seamlessly and fits their business needs perfectly. We’ve designed and
developed APIM to be fully extensible using its own internal plugin
system, so you can define your own policy, develop your own reporting
system, and more.

Additionally, all APIM components (including [APIM Gateway](#apim-gateway) and
[APIM API](#apim-api)) are incredibly lightweight. We took a consciously aggressive approach to
CPU and memory management with our products to supply high availability
through our lightning-fast component start-up times.

Typically, ***it takes less than 5 seconds*** for the API Gateway to be
accessible to consumers (subject to the number of APIs being deployed).

## Concepts

### API

**API** is the root concept defined and used by APIM. Think of this as
the starting point through which services are exposed to the gateway.

### Publisher

In our platform, we define a **publisher** (also called **API
publisher**) as the role that declares and manages APIs.

### Consumer

In our platform, we define a **consumer** (also called **API consumer**)
as the role that consumes APIs.

!!! tip "PRO-TIP:"

    A consumer can only consume an API after subscribing to it.

### Application

An **application** is an intermediate level between a **consumer** and
an API. The consumer uses an application to subscribe to the API before
they are able to consume it.

Ready to use Gravitee.io API Management? Let’s get started!
