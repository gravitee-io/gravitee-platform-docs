---
description: Configuration and usage guide for creating shared policy groups.
---

# Creating shared policy groups

1. Navigate to the shared policy groups by completing the following sub-steps:

a. Navigate to **Settings**, and then click **Gateway**.

b. Click **Shared Policy Group**.

2. Click **Add Shared Policy Group**.
3. Depending on the chain that you want execute on, select either **proxy APIs** or **message APIs**.
4. Select the phase of API execution you want the chain to execute on.

{% hint style="warning" %}
This choice cannot be changed later. To change the phase of the API execution that you want to execute on, you must add another policy.
{% endhint %}

5. In the **Add Shred Policy Group for API** window, provide the following information for your API:

* Name
* Description
* Prerequisite message. When the group is used in an API, the prerequisite message is a text warning that is shown in the policy studio. This message indicates to users that the shared policy group requires additional configuration in the API to function. For example, context attributes.

6. Click **Save**.
