---
description: Create a copy of an existing Kafka Service with a new name, version, and listener host prefix.
hidden: false
noIndex: false
---

# Duplicate a Kafka service

When you operate several Kafka Services with a consistent configuration, duplicating an existing service is faster than creating each one with the wizard. The **Duplicate** action creates a new Kafka Service from the source service's configuration and prompts you for a name, a version, and a new listener host prefix.

## What the copy includes

The duplicated Kafka Service reuses the following configuration from the source service:

* The description, visibility, tags, and groups.
* The listener configuration, with the host prefix replaced by the value that you provide.
* The endpoint binding that determines how the service reaches Kafka.

The copy doesn't include the source service's labels, categories, plans, or policies. The new service is created in a stopped state, and you become its primary owner.

{% hint style="info" %}
Configure a **Plan** for the new service before clients consume from or produce to it.
{% endhint %}

## Duplicate the service

1. From the Gamma console sidebar, select **Event Stream Management**.
2. Navigate to **Kafka Services**.
3. Select the Kafka Service that you want to copy.
4. In the service sidebar, select **General**.
5. Select **Duplicate**.
6. In the **Duplicate Kafka Service** dialog, complete the following fields:

| Field           | Description                                                                                                                                                                                                                                                     |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Name**        | The name of the new service. Pre-filled with the source service's name followed by `(copy)`.                                                                                                                                                                     |
| **Version**     | The version of the new service. Pre-filled with the source service's version.                                                                                                                                                                                    |
| **Host prefix** | The listener host prefix of the new service. A single DNS label of lowercase letters, digits, and hyphens, up to 49 characters. Enter a prefix that isn't in use by any other API in the environment. The source service's own prefix counts as already in use. |

7. Select **Duplicate**.

The console creates the new Kafka Service and redirects you to its overview page.

If the host prefix is already in use, the service isn't created and the dialog shows the error message. Enter a different prefix and select **Duplicate** again.

## Next steps

After duplicating the service, prepare the copy to serve traffic:

* Configure a **Plan** to allow clients to consume from or produce to the new service. See [Create a Kafka service with a registered cluster](create-a-kafka-service-with-a-registered-cluster.md).
* Review the endpoint binding from the service's **Configuration** page if the new service targets different backend infrastructure.
* Start the service from its **General** page when it's ready to accept connections.
