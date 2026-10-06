---
description: >-
  This article focuses on how to use the API Quality feature to govern your APIs
  and ensure that only high-quality APIs enter production
---

# API Quality

{% hint style="warning" %}
The API Quality feature is only available to v2 APIs
{% endhint %}

## Overview

The Gravitee API Quality feature enables API governance by allowing you to create and automatically assign customizable scores based on certain variables determined to impact API quality. If API Quality is enabled, APIs that you create in Gravitee will automatically be assigned an API quality score.

## Configure API Quality

API Quality is configured at the Portal Settings level. To access these settings:

1. Log in to your API Management Console.
2. Select **Settings** from the left nav.
3. Select **API Quality** from the inner left nav
4.  Configure pre-built quality characteristics that Gravitee automatically enforces:

    <figure><img src="../../.gitbook/assets/api quality.png" alt="The API Quality settings page, with API review disabled, quality metrics enabled, and weighting fields for description, logo, categories, labels, and documentation."><figcaption><p>API Quality settings</p></figcaption></figure>

    * **Enable API review:** Toggle ON to build API Quality review into your workflow and not allow an API to be published without review
    * **Enable API Quality Metrics:** Toggle ON to enable quality to be measured and viewable within an APIs details
    * **Description:** **Description weight** assigns a weight to the overall description, while **Description minimum length**, **Logo weight**, **Categories weight**, and **Labels weight** assign weights to description characteristics
    * **Documentation:** Specify **Functional documentation weight** and **Technical documentation weight**
    * **Endpoint:** Specify **Healthcheck weight**
5.  Click **+ Add new quality rule** to configure a custom rule that will be enforced manually:

    <figure><img src="../../.gitbook/assets/api quality_manual rule.png" alt="The lower part of the API Quality settings page, showing a Manual rules table with one rule and its weight."><figcaption><p>Create a manual custom rule</p></figcaption></figure>

    * Specify the rule name, description, and weight
    * Click **Create**

## API Quality view and review

To view an API Quality score:

1. Log in to the API Management Console
2. Select **APIs** from the left nav
3. Select your API
4. From the inner left nav, select **Info** under **General**
5.  Scroll to the **Quality** section to view the API Quality score and rules that are impacting it

    <figure><img src="../../.gitbook/assets/api quality_applied.png" alt="The Info page of an API showing a Quality panel scored at 7 percent, listing the rules met and not met, above the Danger Zone."><figcaption><p>View the API Quality score</p></figcaption></figure>
