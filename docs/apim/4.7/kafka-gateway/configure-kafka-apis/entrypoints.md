---
description: An overview about entrypoints.
---

# Entrypoints

## Overview

Entrypoints define the protocol and configuration settings by which the API consumer accesses the Gateway API. The **Entrypoints** section allows you to modify the host name of your Kafka API entrypoint.

<figure><img src="../../.gitbook/assets/A%2011%20entrypoint%20(1).png" alt=""><figcaption></figcaption></figure>

Change the host name by modifying and saving the value of **Host prefix**. The host name must meet the following requirements:

* Allowed character types are lowercase letters, numbers, dots, dashes, and underscores.
* The first host label segment must be fewer than 50 characters.
* Each subsequent host label segment must be fewer than 64 characters.

This host is used to uniquely route clients to this API. Your client must trust the certificate provided by the gateway, and as there is a variable host in the proxy bootstrap server URL, you likely need to request a wildcard SAN for the certificate presented by the gateway.

Save your changes, then redeploy the API for your changes to take effect.
