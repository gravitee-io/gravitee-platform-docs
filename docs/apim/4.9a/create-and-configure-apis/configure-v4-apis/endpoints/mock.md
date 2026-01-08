---
description: Configuration guide for mock.
metaLinks:
  alternates:
    - mock.md
---

# Mock

## Configuration

The **Mock** endpoint allows you to mock a backend service to emulate the behavior of a typical HTTP server and test processes. Modifying the following configuration parameters is optional.

1. **Interval between messages publication:** Define, in milliseconds (default 1000), the interval between published messages.
2. **Content of published messages:** Define the content of the message body that will be streamed. The default is "mock message."
3. **Count of published messages:** Define, as an integer, the maximum number of published messages that are streamed as a part of the mocking. If left unspecified, there will be no limit.
4. **Message headers:** Add static headers to the message for downstream consumption.
5. **Message metadata:** Add static metadata to the message for downstream consumption.

## Tenants

You can configure tenants to specify which users can proxy requests to this endpoint. Tenants ensure that certain groups of users receive information from only specific APIs. For more information about configuring tenants, see [tenants.md](../../../configure-and-manage-the-platform/gravitee-gateway/tenants.md "mention").
