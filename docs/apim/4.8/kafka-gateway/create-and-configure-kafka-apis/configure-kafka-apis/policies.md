# Policies

## Overview

Gravitee policies are customizable rules or logic the Gateway executes during an API transaction. They modify the behavior of the request or response handled by the APIM Gateway to fulfill business rules during request/response processing. Policies are used to secure APIs, transform data, route traffic, restrict access, customize performance, or monitor transactions.&#x20;

Gravitee supports the following Kafka policies, which can be applied to Kafka APIs.

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td><a href="../../../create-and-configure-apis/apply-policies/policy-reference/kafka-acl.md">Kafka ACL</a></td><td></td><td></td></tr><tr><td><a href="../../../create-and-configure-apis/apply-policies/policy-reference/kafka-topic-mapping.md">Kafka Topic Mapping</a></td><td></td><td></td></tr><tr><td><a href="../../../create-and-configure-apis/apply-policies/policy-reference/kafka-quota.md">Kafka Quota</a></td><td></td><td></td></tr></tbody></table>

## Policy phases

The request and response of a Kafka API transaction are broken up into the following phases:

* **Connect:** Policies are executed after plan selection and authentication on the Gateway, but before the client connects to the upstream broker.&#x20;
* **Interact:** Policies with a global scope (e.g., topic mapping) are executed on all interactions between the client and the Gateway.&#x20;
* **Publish:** Specific policies acting at the message level are applied to each produced record.
* **Subscribe:** Specific policies acting at the message level are applied to each fetched record.

Which Kafka policies can be applied to each phase is summarized below:

<table><thead><tr><th>Policy</th><th data-type="checkbox">Connect</th><th data-type="checkbox">Interact</th><th data-type="checkbox">Publish</th><th data-type="checkbox">Subscribe</th></tr></thead><tbody><tr><td>Kafka ACL</td><td>false</td><td>true</td><td>false</td><td>false</td></tr><tr><td>Kafka Topic Mapping</td><td>false</td><td>true</td><td>false</td><td>false</td></tr><tr><td>Kafka Quota</td><td>false</td><td>false</td><td>true</td><td>true</td></tr></tbody></table>

Kafka policies can be applied to these phases in policy chains of arbitrary length.

## Gravitee Policy Studio

The **Policies** section takes you to the Gravitee Policy Studio.&#x20;

<figure><img src="../../../.gitbook/assets/A 11 policy 1.png" alt=""><figcaption></figcaption></figure>

You can use the Policy Studio to create and manage flows. Flows are policy enforcement sequences that protect or transform how APIs are consumed. They control where, and under what conditions, one or more policies act on an API transaction.

Policies are scoped to different API consumers through flows. You can create a flow for an existing plan that applies to only the subscribers of that plan, or a Common flow that applies to all users of the API. For a native Kafka API, only one Common flow is allowed, and only one flow is allowed per plan.

Policies are added to flows to enforce security, reliability, and proper data transfer. Policies can be added to the different request/response phases of a Kafka API transaction in policy chains of arbitrary length.

## Create a policy

1. Click the **+** next to a plan's name to create a flow for that individual plan, or next to **Common** to create a Common flow.
2. Give your flow a name.
3.  Click **Create**.\


    <figure><img src="../../../.gitbook/assets/A 11 policy 0.png" alt=""><figcaption></figcaption></figure>
4.  In the Flow details panel, select the **Global** header to add a policy to the **Interact** phase of the Kafka API transaction.\


    <figure><img src="../../../.gitbook/assets/A 11 policy 2.png" alt=""><figcaption></figcaption></figure>

    Choose either the Kafka ACL or [Kafka Topic Mapping](../../../create-and-configure-apis/apply-policies/policy-reference/kafka-topic-mapping.md) policy. \


    <figure><img src="../../../.gitbook/assets/A 11 policy 3.png" alt=""><figcaption></figcaption></figure>

    Fill out the policy configuration details and click **Add policy**.\


    <figure><img src="../../../.gitbook/assets/AAA policy.png" alt=""><figcaption></figcaption></figure>
5.  &#x20;In the Flow details panel, select the **Event messages** header to add a policy to the **Publish** and/or **Subscribe** phase of the Kafka API transaction.\


    <figure><img src="../../../.gitbook/assets/A 11 policy 4.png" alt=""><figcaption></figcaption></figure>

    Select the [Kafka Quota](../../../create-and-configure-apis/apply-policies/policy-reference/kafka-quota.md) policy. \


    <figure><img src="../../../.gitbook/assets/A 11 policy 5.png" alt=""><figcaption></figcaption></figure>

    Fill out the policy configuration details and click **Add policy**.\


    <figure><img src="../../../.gitbook/assets/AAB policy.png" alt=""><figcaption></figcaption></figure>
6. Click **Save** and redeploy your API for changes to take effect.
