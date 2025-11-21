# Create and Publish an API Using the Management API

## Overview

This guide uses the v4-Proxy API definition to create an HTTP Proxy API. The principles are the same for other types of APIs.

This example uses the Gravitee Echo API to set up an HTTP proxy API. The Gravitee Echo API returns JSON-formatted data through the following URL: [https://api.gravitee.io/echo](https://api.gravitee.io/echo)

{% hint style="info" %}
* If the `Enable API Review` option is enabled in your API Management settings, you need to use the "Ask for a review" and "Accept a review" requests to complete the API Review process.&#x20;
* The `Enable API Review` option ensures that someone other than the API creator reviews and approves an API before the API creator publishes the API to a Gateway or the Developer Portal.
{% endhint %}

To create, deploy, and publish your API to the Developer Portal, you must complete the steps outlined in this article.

## 1. Obtain a Personal Access Token

To authenticate with the Management API (mAPI), you must provide a set of credentials or a Personal Access Token (PAT). &#x20;

To generate a PAT, complete the following steps:

1. Log into your API Management Console
2. In the navigation menu, click `Organization` .
3. In the `User Management` section of the `Organization menu`, click `Users` .
4. Click your username, and then scroll to `Tokens`.
5.  Click `Generate a personal token`.  This (bearer) token is used in the `Authorization` header when you make requests to the Management API.


    <figure><img src="../../.gitbook/assets/00 firas (1).png" alt=""><figcaption></figcaption></figure>
6.  &#x20;Set the Personal Access Token and management API base URL to environment variables by using values appropriate for your environment:


    ```bash
    export PERSONAL_ACCESS_TOKEN="kd2l91mL01110F..."
    export MANAGEMENT_API_URL="localhost:8083"
    ```

## 2. Create the API definition in JSON

You can create the API definition manually for your API in JSON.&#x20;

{% hint style="info" %}
You can also create an API definition using the following methods:

* Exporting an existing API definition, and then modifying the API definition.
* Using a Kubernetes resource in Gravitee Kubernetes Operator (GKO).
{% endhint %}

If you craft the API definition manually, complete the following step:

* Insert the API data in a JSON file called `my-api.json`. Your `my-api.json` file should match the following example:

```json
{
    "name":"My First API",
    "apiVersion":"1.0.0",
    "definitionVersion":"V4",
    "type":"PROXY",
    "description":"Example of creating my first API using the Management API (mAPI)",
    "listeners": [
        {
            "type":"HTTP",
            "paths": [
                {
                    "path":"/myfirstapi"
                }
            ],
            "entrypoints": [
                {
                    "type":"http-proxy"
                }
            ]
        }
    ],
    "endpointGroups": [
        {
            "name":"default-group",
            "type":"http-proxy",
            "endpoints": [
                {
                    "name":"default",
                    "type":"http-proxy",
                    "weight":1,
                    "inheritConfiguration":false,
                    "configuration": {
                        "target":"https://api.gravitee.io/echo"
                    }
                }
            ]
        }
    ]
}
```

## 3. Create the API with a mAPI call

1. Run the the following `curl` command to create the API from the JSON definition:

{% hint style="info" %}
You can pass the full JSON definition in the data (`-d`) argument of the `curl` command.
{% endhint %}

```sh
curl -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d @my-api.json \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis
```

A successful request returns a `HTTP 201 Created` status and the full configuration of the API.

2. Capture the API `id` to use in subsequent calls.&#x20;

In future calls, you can set this `id` as an environment variable like the following example:

```bash
export API_ID="54593ae4-0e2e-41fe-993a-e40e2ee1fe61"
```

## 4. Create a plan for the API

Your API must have at least one Security/Consumer plan associated with it before it can be deployed to a Gateway. For more information about Plans, see [Broken link](broken-reference "mention"). The following procedure explains how to create a `KEYLESS` plan.

To create a `Keyless` plan, complete the following steps:

1. To create a plan using the mAPI, run the following command:

```bash
curl -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d '{"definitionVersion":"V4","name":"Keyless","description":"Keyless Plan","characteristics":[],"security":{"type":"KEY_LESS"},"mode":"STANDARD"}' \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/plans
```

If your request is successful, The API call returns a `HTTP 201 Created` status and a full configuration of your new plan.&#x20;

2. Capture the plan `id` to use in subsequent calls.&#x20;

In future calls, you can set this `id` as an environment variable like the following example:

```bash
export PLAN_ID="211jf90-dk211kl-9313-j9119-3k21t6leel19"
```

## 5. Publish the plan

{% hint style="info" %}
You must publish the Plan in accordance with the API lifecycle management guidelines.
{% endhint %}

* To publish the Plan, run the following command:

```bash
curl -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/plans/${PLAN_ID}/_publish
```

If you published your plan successfully, you receive a `HTTP 200 OK` status.

## 6. Start the API

To start the API using the mAPI, use the following command:

```bash
curl -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
     -X POST \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/_start
```

If the API starts successfully, you receive a `HTTP 204 No Content` status. &#x20;

You can now view your API in your Gravitee API Management Console. The API has the `KEYLESS` Plan published. Also, the API is deployed to the Gateway.

## 7. (Optional) Publish the API to the Developer Portal

If you  want to publish your API to the Developer Portal, you must modify its configuration. To modify the APIs configuration, complete the following steps:&#x20;

1. From the JSON response of the Create API Request, modify the `lifecycleState` attribute to value `PUBLISHED`, and then send the result in a `PUT` request like the following example:

```bash
curl -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X PUT \
     -d '${MODIFIED_RESPONSE_FROM_CREATE_API_REQUEST}' \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}

```

If the `PUT` request is successful, you receive a `HTTP 200 OK` status.&#x20;

2. Re-deploy the API configuration using the following command:

```bash
curl -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/deployments
```

A  `HTTP 202 Accepted` status informs you the deployment of your API configuration to the Gateway has been started.
