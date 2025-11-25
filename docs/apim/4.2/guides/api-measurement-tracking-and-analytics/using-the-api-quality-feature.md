---
description: >-
  This article focuses on how to use the API Quality feature to govern your APIs
  and ensure that only high-quality APIs make it into production.
---

# Using the API Quality feature

### Introduction

The Gravitee **API Quality** feature enables you to create and automatically assign customizable scores based on certain variables that you feel impact an API's overall quality. When enabled, APIs that you create in Gravitee will automatically be assigned an API quality score. This feature is incredibly valuable for organizations interested in API governance, as it allows them to ensure that certain standards are met, where these standards are treated as score-relevant variables.

### Configure API Quality

{% @arcade/embed url="https://app.arcade.software/share/ditvkcx6pI6iFmYwQvt9" flowId="ditvkcx6pI6iFmYwQvt9" %}

API Quality is configured at the Portal Settings level. To access these settings:

1. Log in to your API Management Console.
2. Select **Settings** from the left-hand nav.
3. Under **Portal**, select **Quality.**

<figure><img src="../../.gitbook/assets/Access API Quality settings (1).gif" alt=""><figcaption><p>Access the API Quality settings</p></figcaption></figure>

The API Quality feature allows you to ensure that every API you publish or deploy to production is of high quality, based on your organization's standards. You can choose to use this feature as merely a way to measure and view the quality of your APIs, or, you can use it to actually introduce necessary friction into the API lifecycle.

To simply enable quality to be measured and viewable within an APIs details, check the **Enable API Quality Metrics** checkbox. If you want to build API Quality review into your workflow, and not allow an API to be published without first having undergone review (which gives a reviewer a chance to review the quality score), check the **Enable API review** checkbox.

<figure><img src="../../.gitbook/assets/Enabnle API Quality (1).gif" alt=""><figcaption><p>Enable API quality metrics and API quality review</p></figcaption></figure>

Your API Quality scores will be dependent on weighted values that you give either pre-built quality characteristics or custom rules that you can enforce manually. You can define these weights and rules in the API Quality settings page. The pre-built characteristics that come built-in to the Gravitee platform are:

* Description: what is the overall quality of the API description? You can add further nuance by adding weight to the following sub categories of the API description:
  * **Description length**: choose a minimum description length and enter that into the **Description minimum length** field
  * **Logo**: add weight to whether or not the API description includes a logo
  * **Categories**: add weight to whether or not the description includes categories
  * **Labels**: add weight to whether or not the description includes labels
* **Documentation**: does the API come with:
  * Functional documentation
  * Technical documentation
* **Endpoint**: is there a health check set up for the API?

If you leverage the pre-built rules, quality scores will be assigned automatically, as the Gravitee API Management solution can takes those rules and measure API quality against them automatically.

However, In addition to these pre-built rules, you can also add your own manual rules. To add a manual rule, follow these steps:

1. In the **API Quality** settings, select the + **Add a new quality rule** icon in the bottom right corner of the page.
2. Define your rule by giving it a name, a description, and a weight.

Once created, you can enforce this custom rule manually across your APIs.

<figure><img src="../../.gitbook/assets/Create custom API quality rule (1).gif" alt=""><figcaption><p>Create custom API quality rule</p></figcaption></figure>

### View and review APIs based on API Quality scoring

An APIs quality score is visible in its **General** details page. To view an API Quality score, follow these steps:

1. Log in to the API Management Console.
2. On the APIs page, select the API for which you want to view a Quality score.
3. Select General under Portal.

You'll see the Quality score along with the various Quality rules that are impacting the score.

<figure><img src="../../.gitbook/assets/View quality score (1).gif" alt=""><figcaption></figcaption></figure>
