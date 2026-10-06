---
description: An overview about policies.
---

# Policies

## Overview

The **Policies** section takes you to the Gravitee Policy Studio.

<figure><img src="../../.gitbook/assets/A 11 policy 1.png" alt="The Policies page of a native Kafka API, listing a default keyless flow and a Common group, with no flows yet selected."><figcaption></figcaption></figure>

You can use the Policy Studio to create and manage flows. Flows are policy enforcement sequences that protect or transform how APIs are consumed. You can create a flow for an existing plan that applies to only the subscribers of that plan, or a Common flow that applies to all users of the API. For a native Kafka API, only one Common flow is allowed, and only one flow is allowed per plan.

Policies are added to flows to enforce security, reliability, and proper data transfer. Policies can be added to the different request/response phases of a Kafka API transaction in policy chains of arbitrary length.

## Configuration

1. Click the **+** next to a plan's name to create a flow for that individual plan, or next to **Common** to create a Common flow.
2. Give your flow a name.
3.  Click **Create**.

    <figure><img src="../../.gitbook/assets/A 11 policy 0.png" alt="The Create a new flow dialog for a native API, with a flow name entered and a note that only one flow is allowed."><figcaption></figcaption></figure>
4.  In the Flow details panel, select the **Global** header to add a policy to the **Interact** phase of the Kafka API transaction.

    <figure><img src="../../.gitbook/assets/A 11 policy 2.png" alt="The Policies page with a new flow selected, showing the Connect phase marked coming soon and an empty Interact phase between the client and the broker."><figcaption></figcaption></figure>

    Choose either the Kafka ACL or [Kafka Topic Mapping](../policies/kafka-topic-mapping.md) policy.

    <figure><img src="../../.gitbook/assets/A 11 policy 3.png" alt="The Policies for Interact phase dialog, offering the Kafka ACL and Kafka Topic Mapping policies."><figcaption></figcaption></figure>

    Fill out the policy configuration details and click **Add policy**.

    <figure><img src="../../.gitbook/assets/AAA policy.png" alt="The Policies page with a Kafka Topic Mapping policy added to the Interact phase of the selected flow."><figcaption></figcaption></figure>
5.  In the Flow details panel, select the **Event messages** header to add a policy to the **Publish** and/or **Subscribe** phase of the Kafka API transaction.

    <figure><img src="../../.gitbook/assets/A 11 policy 4.png" alt="The Event messages tab of a flow, showing empty Publish and Subscribe phases between the client and the broker."><figcaption></figcaption></figure>

    Select the [Kafka Quota](../policies/kafka-quota.md) policy.

    <figure><img src="../../.gitbook/assets/A 11 policy 5.png" alt="The Policies for Publish phase dialog, offering the Kafka Quota policy."><figcaption></figcaption></figure>

    Fill out the policy configuration details and click **Add policy**.

    <figure><img src="../../.gitbook/assets/AAB policy.png" alt="The Event messages tab with a Kafka Quota policy added to the Publish phase of the selected flow."><figcaption></figcaption></figure>
6. Click **Save** and redeploy your API for changes to take effect.
