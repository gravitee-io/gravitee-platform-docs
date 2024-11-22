---
description: >-
  This section walks you through creating and publishing your first API with the
  Gravitee Management API (mAPI).
---

# Creating and publishing an API with the Management API

This guide uses the v4-Proxy API definition, creating an HTTP Proxy API. The principles are the same for other types of APIs.

{% hint style="info" %}
In this example we will use the [Gravitee Echo API](https://api.gravitee.io/echo) to set up our first HTTP proxy API. The Gravitee Echo API returns JSON-formatted data via the following URL: [https://api.gravitee.io/echo](https://api.gravitee.io/echo)
{% endhint %}

{% hint style="info" %}
If the `Enable API Review` option is enabled in your API Management Settings, you will need to use the "Ask for a review" and "Accept a review" requests to complete the API Review process.

The [Enable API Review](../api-measurement-tracking-and-analytics/using-the-api-quality-feature.md) option enforces someone (other than the API Creator) to review & approve an API before it can be published to a Gateway or to the Developer Portal.
{% endhint %}

There are a few steps needed to fully create, deploy, and (optionally) publish your API to the Developer Portal:

* [Obtain a Personal Access Token](creating-and-publishing-an-api-with-the-management-api.md#obtaining-a-personal-access-token)
* [Create the API definition in JSON](creating-and-publishing-an-api-with-the-management-api.md#create-the-api-definition-in-json)
* [Create API via a mAPI call](creating-and-publishing-an-api-with-the-management-api.md#creating-the-api-via-a-mapi-call)
* [Create a plan for the API](creating-and-publishing-an-api-with-the-management-api.md#create-a-plan-for-the-api)
* [Publish the plan](creating-and-publishing-an-api-with-the-management-api.md#publish-the-plan)
* [Start the API](creating-and-publishing-an-api-with-the-management-api.md#start-the-api)
* [(Optionally) Publish the API to the developer portal](creating-and-publishing-an-api-with-the-management-api.md#optionally-publish-the-api-to-the-developer-portal)

## Obtain a Personal Access Token

In order to authenticate with the Management API, you must provide a set of credentials or a Personal Access Token (PAT). &#x20;

Use these steps to generate a personal access token:

1. Log into your API Management Console
2. Click on the `Organization` menu option
3. Under `User Management`, click on the `Users` option
4. Click on your username, and scroll down to `Tokens`
5. Finally, click on `Generate a personal token`.  This (bearer) token will be used in the `Authorization` header when making requests to the Management API.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXevKrd-eEwy0weN9zG1LDc-gb00Q6Et0vnp3rSVq0BWgIqN5CuMXoGBPU6VDPCHrU2SnWoQZQoU1E7LC_qsdAWpI-1bqhti2QawjPQ3v343WGCUhrItm2daeniAdeF5FlK_w-4I-fm5UAJ4q4u6b-7YG_hf?key=ct5dl3MgXSqTMSd4JX9ipQ" alt=""><figcaption></figcaption></figure>

To continue following this guide, set the Personal Access Token and management API base URL to enviornment variables, using values appropriate for your environment:

```bash
export PERSONAL_ACCESS_TOKEN="kd2l91mL01110F..."
export MANAGEMENT_API_URL="localhost:8083"
```

## Create the API definition in JSON

You can create the API definition for your API in JSON. Typically, you would get this by exporting an existing API definition and modifying it, or via a Kubernetes resource in GKO. However, in this case, we'll assume you are crafting the API definition manually. In that case, put the API data in a JSON file called `my-api.json`. The content should be like so:

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

## Create the API via a mAPI call

Now, run the `curl` command to create the API from the JSON definition:

```sh
curl -H "Authorization: ${PERSONAL_ACCESS_TOKEN}" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d @my-api.json \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis
```

You can also pass the full JSON definition above in the data (`-d`) argument of the `curl` command.

If your request is successful, you should receive a `HTTP 201 Created` status returned, as well as the full configuration of your new API. You now want to capture the API `id` to use in subsequent calls. You can set this again as an environment variable like so:

```bash
export API_ID="54593ae4-0e2e-41fe-993a-e40e2ee1fe61"
```

## Create a plan for the API

Every API must have at least one Security/Consumer [Plan](../../using-the-gravitee-api-management-components/general-configuration/plans-and-policies/) associated with it before it can be deployed to a Gateway.  The following example shows how to create a `KEYLESS` plan.

To create a plan via the mAPI, run the following, replacing the&#x20;

```bash
curl -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d '{"definitionVersion":"V4","name":"Keyless","description":"Keyless Plan","characteristics":[],"security":{"type":"KEY_LESS"},"mode":"STANDARD"}' \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/plans
```

As above, if your request is successful, you should receive a `HTTP 201 Created` status returned, as well as the full configuration of your new plan. You now want to capture the API `id` to use in subsequent calls. You can set this again as an environment variable like so:

```bash
export PLAN_ID="211jf90-dk211kl-9313-j9119-3k21t6leel19"
```

## Publish the plan

Now we need to publish the Plan (in accordance with the API lifecycle management guidelines). To do so, run:

```bash
curl -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/plans/${PLAN_ID}/_publish
```

This time you should receive a `HTTP 200 OK` status that confirms your Plan was published successfully.

## Start the API

Now the last mandatory step in creating your first API (using the Management API) is to actually **start** your API.

```bash
curl -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
     -X POST \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/_start
```

This time you should receive a `HTTP 204 No Content` status. &#x20;

Switch over to your Gravitee API Management Console and you should now see your API.  It will have the `KEYLESS` Plan published, and it’ll already be deployed to your API Gateway, so go ahead and test it out.

## (Optionally) Publish the API to the Developer Portal

If you also want to publish your API to the Developer Portal then you will need to modify its configuration.  From the JSON response of the Create API Request, modify the `lifecycleState` attribute to value `PUBLISHED` and send the result in a `PUT` request.

```bash
curl -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X PUT \
     -d '${MODIFIED_RESPONSE_FROM_CREATE_API_REQUEST}' \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}

```

This time you should receive a `HTTP 200 OK` status that confirms your API configuration was updated successfully. But since we made this change, we also need to re-deploy the API configuration again:

```bash
curl -H "Authorization: Bearer ${PERSONAL_ACCESS_TOKEN}" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
https://${MANAGEMENT_API_URL}/management/v2/organizations/DEFAULT/environments/DEFAULT/apis/${API_ID}/deployments
```

A status of `HTTP 202 Accepted` informs you the deployment (of your API configuration to the Gateway) has been started.

You have now created your first API using Gravitee’s Management API!
