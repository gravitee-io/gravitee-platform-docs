---
description: >-
  This article focuses on how to configure environment variables, system
  properties, and the gravitee.yaml file as they pertain to the Gravitee API
  Gateway
---

# The Gravitee API Gateway

### Introduction

This section focuses on the following Gravitee API Gateway configuration settings:&#x20;

* Environment variables
* System properties
* the `gravitee.yaml` file

{% hint style="info" %}
The order in which the above are listed corresponds to their order of precedence. In other words, environment variables override the other two configuration types, and system properties override `gravitee.yml`.
{% endhint %}

* Internal API
* OpenTracing
* Sharding tags
* Tenants
