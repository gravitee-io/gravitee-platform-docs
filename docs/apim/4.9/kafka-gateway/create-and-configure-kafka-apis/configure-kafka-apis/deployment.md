# Deployment

## Overview

In the **Deployment** section, you can manage sharding tags and track changes to your API.

## Configuration

From the **Configuration** header you can control where your API is deployed through the use of [sharding tags](docs/apim/4.9/configure-and-manage-the-platform/gravitee-gateway/sharding-tags.md). Sharding tags are configured at the Organization level.

<figure><img src="../../../../4.7/.gitbook/assets/1 shard 1.png" alt=""><figcaption></figcaption></figure>

Multiple sharding tags can be assigned to your API. Once you've saved your selections, you must redeploy your API for the changes to take effect.

<figure><img src="../../../../4.7/.gitbook/assets/1 shard 2.png" alt=""><figcaption></figcaption></figure>

## Deployment History

Selecting the **Deployment History** header displays the history of changes to your API deployment. These are the changes to your API definition from the perspective of the Kafka Gateway.

If your API is out of sync, you can click **View version to be deployed** to view the current API definition.

<figure><img src="../../../../4.7/.gitbook/assets/1 deploy 1.png" alt=""><figcaption></figcaption></figure>

Use the checkboxes to select two API definitions you'd like to compare. The comparison is automatically generated.

<figure><img src="../../../../4.7/.gitbook/assets/1 deploy 2.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Only two API definitions can be selected at a time. If you close the comparison and check a third API definition, the first API definition you selected will be compared with the third selection. Any new selections will always be compared with your first selection. To reset comparisons, uncheck all boxes.
{% endhint %}

Click on the eye icon to view the JSON of the API definition. You can then click the page icon on the right to copy it to the clipboard.

<figure><img src="../../../../4.7/.gitbook/assets/1 deploy 3.png" alt=""><figcaption></figcaption></figure>
