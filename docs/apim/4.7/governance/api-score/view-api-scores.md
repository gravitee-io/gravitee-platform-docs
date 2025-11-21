# View API Scores

{% hint style="warning" %}
API Score is a technology preview. This feature is not recommended for production environments.&#x20;
{% endhint %}

## High-level API Score statistics

High-level API Score statistics are shown on the **API Score** page. To get to your API Score dashboard:

1. Ensure that API Score is enabled. For more information about enabling API Score, see [Enable API Score](enable-api-score.md).
2. Log in to your APIM Console.
3.  In the menu, click **API Score**. 


    <figure><img src="../../.gitbook/assets/image (207).png" alt=""><figcaption></figcaption></figure>

The **Overview** and **APIs** sections of the **API Score** page provide you with high-level metrics to understand the quality of your APIs. These metrics are:

* The average score of your API
* The number of errors in your API
* The number of warnings in your API
* The number of infos in your API
* The number of hints in your API

The **Overview** section shows these metrics across all of your APIs.

<figure><img src="../../.gitbook/assets/image (205).png" alt=""><figcaption></figcaption></figure>

The **APIs** section contains a list of your APIs to show these metrics for each API individually.&#x20;

<figure><img src="../../.gitbook/assets/image (206).png" alt=""><figcaption><p>Example API score dashboard</p></figcaption></figure>

## Individual API Score details

To view the API Score details for a specific API, click on the API in the **APIs** section of your API Score dashboard.

<figure><img src="../../.gitbook/assets/00 api 1.png" alt=""><figcaption></figcaption></figure>

This brings you to a page that shows the details of API metrics.&#x20;

<figure><img src="../../.gitbook/assets/00 api 2.png" alt=""><figcaption></figcaption></figure>

### Filter API Score issues

To filter your API's issues by category, select from the tabs of API Score metrics. By default, all issues are shown. If no information exists for a metric, it will be grayed out and you will not be able to select it.

You can also filter issues via the search function. You can search using information from the following columns:

* Severity
* Recommendation&#x20;
* Path

To filter using the search function, type your search query into the **Search** field. The table showing issue details is filtered as you type.

The table has the following columns:

* **Severity:** This gauges the severity of the issue. In order of increasing severity, the options are: hint, info, warning, error.
* **Line/Column:** The line and column of the issue location are shown in `[line]:[column]` format.&#x20;
* **Recommendation:** This column provides a recommendation for how to fix the issue.&#x20;
* **Path:** This column shows the path to the issue location.
