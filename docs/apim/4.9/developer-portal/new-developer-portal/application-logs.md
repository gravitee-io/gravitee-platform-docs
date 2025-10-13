# Application Logs

{% hint style="warning" %}
This feature is in tech preview.
{% endhint %}

As an API subscriber, you can view paginated logs for all of the APIs your application has subscribed to. The list of logs displays the name, timestamp, HTTP method, and response status of each API.

If you have [set the new Developer Portal as your default Developer Portal](broken-reference), you can access it from the Developer Portal button in your APIM Console header. If you have not set the new Developer Portal as your default, follow the instructions to [enable the new Developer Portal](broken-reference).

The Developer Portal opens in a new browser tab. To view the logs for an API:

1.  Click **Applications** from its header menu.\


    <figure><img src="../../.gitbook/assets/00 apps.png" alt=""><figcaption></figcaption></figure>
2. Click on an application, then select the **Analytics & Logs** tab.
3.  Use the filters to set constraints on which API logs are shown.\


    <figure><img src="../../.gitbook/assets/00 logs.png" alt=""><figcaption></figcaption></figure>
4.  Click the arrow to view the details for a particular log entry. **The Connection Logs** tab shows request and response information, which can be recorded for all APIs. The **Messages** tab is used for message logs, which can only be recorded for v4 message APIs.\


    <figure><img src="../../.gitbook/assets/00 log.png" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
The API publisher determines which information is logged for a given API. To configure what information is logged and visible to an API subscriber, see [Modify logging information](broken-reference).
{% endhint %}
