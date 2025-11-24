---
description: An overview about shared policy groups.
---

# Shared Policy Groups

{% hint style="warning" %}
Shared policy groups only work with the Gravitee v4 API definition.
{% endhint %}

## Overview

With shared policy groups, you can define a collection of policies in a central location and use them across multiple APIs. Also, you can complete the following actions:

* Define a standard set of policies to shape traffic
* Enforce security standards
* Transform messages

The deployment of a shared policy group to the gateway is independent of the deployment lifecycle of the APIs the shared policy group is used in. If you make a change to the shared policy group, and then deploy it to the gateway, all APIs will pick up the changes when the next connection begins, without requiring the APIs to be restarted. When using this feature at scale, inform your team of any changes you make, and test your changes before deploying to a higher environment.

## Create a shared policy group

1. Navigate to the shared policy groups by completing the following sub-steps:
   1. Navigate to **Settings**, and then click **Gateway**.
   2. Click **Shared Policy Group**.
2. Click **Add Shared Policy Group**.
3. Depending on the chain that you want execute on, select either **proxy APIs** or **message APIs**.
4. Select the phase of API execution you want the chain to execute on.

{% hint style="warning" %}
This choice cannot be changed later. To change the phase of the API execution that you want to execute on, you must add another policy.
{% endhint %}

5. In the **Add Shared Policy Group for API** window, provide the following information for your API:

* Name
* Description
* Prerequisite message. When the group is used in an API, the prerequisite message is a text warning that is shown in the policy studio. This message indicates to users that the shared policy group requires additional configuration in the API to function. For example, context attributes.

6. Click **Save**.

## Add a shared policy group

Before you begin, you must create an API flow.

1. To add a policy flow, click **the plus button** to see the policies that are applicable to the phase.
2. (Optional) To filter the result for shared policy groups, click **Shared Policy Group**.

{% hint style="info" %}
You can see only deployed shared policy groups.
{% endhint %}

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXc49eNncnilBcCaupXY123kIumNnlez_NNk0YpMlO8EZhOJrMgcwdp5H8IjBYPno0fvkjW24zQ35hJNSrLF1oaZnOybddq13K-443sunBJXjjqXeLrMxrzAklPdofqGd-hQnV_zSEcHm-x9kx7KSgJ84go?key=PrMp2J0zWBtqrsqO75zcMw" alt="Policies for request phase screenshot"><figcaption><p>Policies for Request phase screen with the Shared Policy group filter appiled</p></figcaption></figure>

3. Click **Select** for the shared policy group that you want to add to the chain.
4. (Optional) In the **Policies for Request phase**, add a description and trigger condition. If you added a prerequisite message for your policy chain, it is shown here.

{% hint style="info" %}
The trigger condition works the same as for a regular policy. But when the trigger condition evaluates to false, all policies in the shared policy group are skipped.
{% endhint %}

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXdBSOmAx2_odvERZdo9W0byoOS_o9Clx_dsaJa_pWGZWHrirXdt9KXPo8sdcvOn2huz_9IalLRCPjpRA_8yge669fWn8CPGX0zPXFt9QfqkSsh7n4U1LxqxtyhkeL82MUtRHlHVJnvCvk7D2fZ7CaIis15d?key=PrMp2J0zWBtqrsqO75zcMw" alt="Policy for Request phase  screen with a shared policy group selected"><figcaption><p>Policies for Request phase screen with a shared policy group selected</p></figcaption></figure>

5. Click **Add policy**.

## Add a policy chain

1. Navigate to the light version of the Gravitee policy studio,
2. In the policy chain, click the **plus symbol**. You see a list of policies filtered to those are compatible with the phase the shared policy group executes on.
3. Add the policies to the chain, and then configure the policies.
4. To persist the changes, click **Save**.
5. To deploy the shared policy group to the gateway, click **Deploy.**

You can now use the shared policy group in an API flow.

## Edit a shared policy group

You can edit the shared policy group, complete the following steps:

1. Navigate to the policy chain.
2. On the **shared policy group tile**, click the three vertical dots.
3. From here, you can complete the following actions:
   * Edit the policy group's name and condition.
   * Review the prerequisite message.
   * Edit the group.
   * Disable the group.
   * Delete the group.
4. Save, and then deploy your API within the regular flow of the API.

## Version history

### View

To view the version history of a shared policy group, click **Version History**. A list of the version will be displayed in reverse chronological order.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXeEUJqnB93yGrb2O9YQ4sy0F6yMD106fqwIRUe3wPq1dhQFxN9g7KDZIqqbjyr7bQJpVLdy7SINcFfk_-EDPnvbvEQ5fRm0v4fAOtxt78FbmxfN9WUJqf5rEZgJCHDkxsdy9tbKsMIUFSN0sfCuoo3_OQof?key=PrMp2J0zWBtqrsqO75zcMw" alt="Version of Transform Headers Demo screen"><figcaption><p>Version of Transform Headers Demo screen</p></figcaption></figure>

### Compare

To compare two versions, select two versions to compare. You can compare the versions using any of the following methods:

* To compare the versions using the raw JSON file, click **Raw**.
* To compare the versions side by side, click **Diff Side by Side**.
* To compare the versions line by line, click **Diff LIne by Line**.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXfddK75sJLiyXQoIQGSkr5QqpagaOUmsHX4g_52623NIaAJeEA6f2lBvAifQ5eirAVHPi9ZCEqDE5h1k5Dy3F0o94Tj0bse_YQD1XojIzszqjLlKuaE0RL4yxTjx_Imtv21-FHB1akgJKhjikEP6B0WYS1-?key=PrMp2J0zWBtqrsqO75zcMw" alt=""><figcaption></figcaption></figure>

### Restore

To restore a previous version, click **Restore version i**n the **version details** window. This action creates a pending version that you must deploy.

## AI flows

By default, Gravitee APIM 4.5 has three shared policy groups that empowers AI use cases. These policy groups can be chained together to support LLM proxy use cases. For example, prompt templating, prompt security, and LLM rate limiting.

Here are the default shared policy groups:

* **Rate Limit & Request token limit**: This policy limits the number of requests and number of tokens sent in a request. To use this policy, set context attributes prompt, maxTokens, and maxRequests.
* **Prompt Templating Example**: Uses the Assign Content policy to create and enhance a prompt from external data.
  * In this example, the shared policy group takes an input field of **ip** in the request body and adds it as an attribute.
  * It runs an HTTP Callout policy to find the IP address set in the context attribute and return its country and city as context attributes.
  * From the context attributes, it crafts a prompt in the Assign Attributes policy.
* **Redirect to HuggingFace**: This policy group crafts the body of a request to HuggingFace, which includes model parameters and options, and then it sends that request to a Dynamic Routing policy that redirects to HuggingFace.

You can use these shared policy groups together to build an LLM proxy for prompt templating and rate limiting. Also, you can edit these shared policy groups to match your needs.

You can delete these shared policy groups if you do not wish to have them. If you delete them, they will not return in that environment.

## Limitations

Shared policy groups have the following limitations:

* You cannot export a shared policy group. As a workaround, if you have a valid personal access token and the APIM\_HOST environment variable set, you can download the definition through the management API using the following command (editing environment variables and environment ID as needed):

```bash
curl --request GET \
  --url https://${MAPI_URL}/management/v2/environments/DEFAULT/shared-policy-groups/${GROUP_ID} \
  --header 'Accept: application/json' \
  --header 'Authorization: Basic ${PERSONAL_ACCESS_TOKEN}'

```

* You cannot import a shared policy group. As a workaround, if you have a valid personal access token and the APIM\_HOST environment variable set, you can create a shared policy group through the management API using the following command, with the `data` field containing the group definition:

```bash
curl --request POST \
  --url https://${MAPI_URL}/management/v2/environments/DEFAULT/shared-policy-groups \
  --header 'Accept: application/json' \
  --header 'Authorization: Basic ${PERSONAL_ACCESS_TOKEN}' \
  --header 'Content-Type: application/json' \
  --data '{
  "crossId": "5e2b3b3b-3b3b-3b3b-3b3b-3b3b3b3b3b3b",
  "name": "My Shared Policy Group",
  "description": "This is a shared policy group",
  "prerequisiteMessage": "The resource cache \"my-cache\" is required",
  "apiType": "MESSAGE",
  "phase": "REQUEST",
  "steps": [
    {
      "name": "string",
      "description": "string",
      "enabled": true,
      "policy": "string",
      "configuration": {},
      "condition": "string",
      "messageCondition": "string"
    }
  ]
}'
```

* If you import an API with a shared policy group reference that does not exist in the higher environment, the API executes with no issues. Future versions of Gravitee will allow the platform administrator to configure whether to allow APIs to run or be imported with missing shared policy groups.
