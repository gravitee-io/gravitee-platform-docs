---
description: This page describes the configuration options of the HTTP GET entrypoint
---

# HTTP GET

## Configuration

If you chose **HTTP GET** as an entrypoint, you will be brought to a page where you can configure:

1. **Limit messages count:** Defines the maximum number of messages to retrieve via HTTP GET. The default is 500. To set a custom limit, enter a numeric value in the **Limit messages count** text field.
2. **Limit messages duration:** Defines the maximum duration, in milliseconds, to wait to retrieve the expected number of messages (see **Limit messages count**). To set a custom limit, enter a numeric value in the **Limit messages duration** text field. The actual number of retrieved messages could be less than expected if maximum duration is reached before all messages are retrieved.
3. **HTTP GET permissions:** Allow or disallow **Allow sending messages headers to client in payload** and **Allow sending messages metadata to client in payload** by toggling these actions ON or OFF.
4. **Quality of service:** Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](docs/apim/4.2/guides/api-configuration/v4-api-configuration/quality-of-service.md).
