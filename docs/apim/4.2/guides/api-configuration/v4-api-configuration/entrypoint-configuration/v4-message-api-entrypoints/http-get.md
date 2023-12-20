---
description: This page describes the configuration options of the HTTP GET entrypoint
---

# HTTP GET

## Configuration

If you chose **HTTP GET** as an entrypoint, you will be brought to a page where you can configure:

* **Limit messages count:** Defines the maximum number of messages to retrieve via HTTP GET. The default is 500. To set a custom limit, enter a numeric value in the **Limit messages count** text field.
* **Limit messages duration:** Defines the maximum duration, in milliseconds, to wait to retrieve the expected number of messages (see **Limit messages count**). To set a custom limit, enter a numeric value in the **Limit messages duration** text field. The actual number of retrieved messages could be less than expected if maximum duration is reached before all messages are retrieved.
* **HTTP GET permissions:** Allow or disallow **Allow sending messages headers to client in payload** and **Allow sending messages metadata to client in payload** by toggling these actions ON or OFF.
* **Quality of service:** Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](../../quality-of-service.md).
