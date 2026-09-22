---
description: API subscribers view paginated logs for every API their application subscribes to in the Developer Portal 4.8. Learn how to read them.
---

# Application Logs


As an API subscriber, you can view paginated logs for all of the APIs your application has subscribed to. The list of logs displays the name, timestamp, HTTP method, and response status of each API.

If you have [set the new Developer Portal as your default Developer Portal](configure-the-new-portal.md), you can access it from the Developer Portal button in your APIM Console header. If you have not set the new Developer Portal as your default, follow the instructions to [enable the new Developer Portal](configure-the-new-portal.md).

The Developer Portal opens in a new browser tab. To view the logs for an API:

1.  Click **Applications** from its header menu.

    <figure><img src="../../.gitbook/assets/00 apps.png" alt="The Applications page of the developer portal, showing five application cards with their owners and descriptions."><figcaption></figcaption></figure>
2. Click on an application, then select the **Analytics & Logs** tab.
3.  Use the filters to set constraints on which API logs are shown.

    <figure><img src="../../.gitbook/assets/00 logs.png" alt="The Analytics and Logs tab of an application in the developer portal, with API, method, response time, and period filters above a table of requests and their status."><figcaption></figcaption></figure>
4.  Click the arrow to view the details for a particular log entry. **The Connection Logs** tab shows request and response information, which can be recorded for all APIs. The **Messages** tab is used for message logs, which can only be recorded for v4 message APIs.

    <figure><img src="../../.gitbook/assets/00 log.png" alt="A request&#x27;s detail page in the developer portal, showing its timestamp, API, plan, and transaction identifier above connection log panels for the request and response."><figcaption></figcaption></figure>

{% hint style="warning" %}
The API publisher determines which information is logged for a given API. To configure what information is logged and visible to an API subscriber, see [Modify logging information](../../analyze-and-monitor-apis/logging.md#modify-logging-information).
{% endhint %}
