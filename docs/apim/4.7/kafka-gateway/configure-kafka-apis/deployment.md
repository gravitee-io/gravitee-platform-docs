---
description: An overview about deployment.
---

# Deployment

## Overview

In the **Deployment** section, you can manage sharding tags and track changes to your API.

## Configuration

From the **Configuration** header you can control where your API is deployed through the use of [sharding tags](../../gravitee-gateway/sharding-tags.md). Sharding tags are configured at the Organization level.

<figure><img src="../../.gitbook/assets/1 shard 1.png" alt="The Deployment configuration tab of a Kafka API, with an empty sharding tags selector."><figcaption></figcaption></figure>

Multiple sharding tags can be assigned to your API. Once you've saved your selections, you must redeploy your API for the changes to take effect.

<figure><img src="../../.gitbook/assets/1 shard 2.png" alt="The Deployment configuration tab with two sharding tags selected and an out-of-sync banner offering to deploy the API."><figcaption></figcaption></figure>

## Deployment History

Selecting the **Deployment History** header displays the history of changes to your API deployment. These are the changes to your API definition from the perspective of the Kafka Gateway.

If your API is out of sync, you can click **View version to be deployed** to view the current API definition.

<figure><img src="../../.gitbook/assets/1 deploy 1.png" alt="The Deployment History tab, listing four versions with their date, user, and label, the newest marked in use."><figcaption></figcaption></figure>

Use the checkboxes to select two API definitions you'd like to compare. The comparison is automatically generated.

<figure><img src="../../.gitbook/assets/1 deploy 2.png" alt="A side-by-side comparison of two API definition versions, with the plan identifier, name, and security type highlighted as changed."><figcaption></figcaption></figure>

{% hint style="info" %}
Only two API definitions can be selected at a time. If you close the comparison and check a third API definition, the first API definition you selected will be compared with the third selection. Any new selections will always be compared with your first selection. To reset comparisons, uncheck all boxes.
{% endhint %}

Click on the eye icon to view the JSON of the API definition. You can then click the page icon on the right to copy it to the clipboard.

<figure><img src="../../.gitbook/assets/1 deploy 3.png" alt="A version detail dialog showing the date, user, and label above the JSON API definition for a native Kafka API."><figcaption></figcaption></figure>
