---
description: An overview about General Info Settings.
---

# General Info Settings

{% hint style="info" %}
Only v2 APIs support the API Quality feature
{% endhint %}

## Overview

The general settings for a Gravitee v2 API are grouped into 3 sections: [general information](general-info-settings.md#general-information), [Quality](general-info-settings.md#quality), and [Danger Zone](general-info-settings.md#danger-zone).

<figure><img src="broken-reference" alt=""><figcaption><p>v2 API general settings</p></figcaption></figure>

{% tabs %}
{% tab title="General information" %}
* **Name**, **Version**, **Description**: Editable basic information
* **Labels:** Enter a label
* Choose one or more **Categories** from the drop-down menu
* Upload an **API picture** and/or **API background**
* **Owner**, **Created**, **Last connection**: Informative only
* **Emulate v4 engine:** Toggle ON or OFF to use or not use the reactive execution engine
* **Export** your API definition and/or **Import** an API definition to update your API
* **Duplicate** or **Promote** your API
{% endtab %}

{% tab title="Quality" %}
The metrics in this section describe how well your API conforms to rules set for the [API Quality ](../../api-measurement-tracking-and-analytics/using-the-api-quality-feature.md)feature.
{% endtab %}

{% tab title="Danger Zone" %}
Mission-critical (and potentially dangerous) actions:

* **Start the API:** Deploy the API to all Gateways, or the Gateways specified using [Sharding tags](../../../getting-started/configuration/apim-gateway/sharding-tags.md)
* **Publish the API:** Publish the API to the Developer Portal
* **Make Public:** Make the API public so that everybody can see it
* **Deprecate this API:** Unpublish it from the Developer Portal
* **Delete:** Delete the API
{% endtab %}
{% endtabs %}

## Access and edit general settings

To access the general settings of a v2 API:

1. Log in to your APIM Console
2. Select APIs from the left nav
3. Select your API
4. From the inner left nav, select **Info** under the **General** section
5. Modify editable settings as desired
6. Click **Save**
