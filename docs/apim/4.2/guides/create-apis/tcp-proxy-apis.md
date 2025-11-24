---
description: An overview about TCP Proxy APIs.
---

# TCP Proxy APIs

## Overview

Gravitee supports TCP proxy APIs to provide the lowest latency access to raw backend data. By creating a new TCP server on the Gateway that listens for incoming connections on a predefined port, messages can be proxied from any REST endpoint or event system with an available IP address that accepts TCP socket clients.

Direct TCP socket access to streaming data bypasses the HTTP layer around web traffic and allows API management principles to be applied to formats not commonly available to the standard API consumer. Video streams, WCF data from Excel, HL7 feeds, IoT protocols, mainframe data, etc., can be transmitted as TCP packets through the Gateway to the client in near real-time.

TCP proxy only supports the exposure and consumption of packets, with no other protocols are layered on top (e.g., Kafka or MQTT). Event streams and data feeds are proxied in their native protocol format, and the Gateway does not perform any message or packet-level transformation. In the absence of protocol mediation, the client is responsible for decoding and serializing data into the desired format.

## Limitations

The following limitations currently apply to TCP proxy API support:

* Gravitee 4.2 does not include UI support for TCP proxy APIs. To create and manage TCP proxy APIs, refer to the [Management API documentation](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.0.0/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/management-openapi-v2.yaml).
* Existing Gravitee Helm Charts do not support the creation of a TCP server on the Gateway. User customization of the Helm Charts is required for TCP proxy APIs.

Future releases will add TCP proxy support to the Management Console to offer mTLS plans, rate limiting, IP filtering, and API consumption analytics. Plans will enable TCP proxy monetization via different throughputs associated with subscription tiers that can be managed in the Developer Portal.
