---
description: Overview of Push Interface.
---

# Push Interface

## Overview

The push interface allows you to make use of your API design. It includes two panes: **API Settings** and **Push API**.

## API Settings

Here you can view and (optionally) edit the basic parameters of the API (name, version, description). You can also download the API design in JSON format. Lastly, you can review the documentation.

<figure><img src="https://docs.gravitee.io/images/cockpit/apid_documentation.png" alt="" width="375"><figcaption></figcaption></figure>

## Push API

<figure><img src="https://docs.gravitee.io/images/cockpit/apid_push.png" alt="" width="563"><figcaption></figcaption></figure>

Three possible methods for pushing an API to a linked API Management installation result in the following API classifications:

**Documented:** The API documentation (OAS) is created. The API is not deployed on the Gateway, nor published on the Developer Portal.

**Mocked:** Same as Documented, plus the API is deployed with a keyless plan and mock policy on the Gateway. Consumers can retrieve mock responses from the API, where the body of the mock response is based on the examples defined in the design interface.

**Published:** Same as Mocked, plus the API is published on the Developer Portal. Consumers can subscribe to the API.
