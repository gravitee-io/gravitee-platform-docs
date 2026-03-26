---
description: Configuration guide for Mock.
---

# Mock

## Configuration

The **Mock** endpoint allows you to mock a backend service to emulate the behavior of a typical HTTP server and test processes. If you chose this endpoint, you will need to configure:

1. **Interval between messages publication:** Define, in milliseconds (default 1000), the interval between published messages.
2. **Content of published messages:** Define the content of the message body that will be streamed. The default is "mock message."
3. **Count of published messages:** Define, as an integer, the maximum number of published messages that are streamed as a part of the mocking. If left unspecified, there will be no limit.
