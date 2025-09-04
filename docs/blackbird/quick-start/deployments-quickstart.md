---
noIndex: true
---

# Deployments Quickstart

In this tutorial, we'll be using the Blackbird CLI to deploy our code to a dedicated environment.

## Before you get started

Before you get started:

* Download the CLI. For more information, see [#download-the-cli-and-log-in-optional](./#download-the-cli-and-log-in-optional "mention").
* Add or create an API. For more information, see [api-quickstart.md](api-quickstart.md "mention").
* Create a mock. For more information, see [mock-quickstart.md](mock-quickstart.md "mention").
* Test and debug your code. For more information, see [code-quickstart.md](code-quickstart.md "mention").
* Open your preferred IDE, such as Visual Studio Code.

## 1. Creating a Deployment

Now that we have a debugged and generated code project, we can use the `deployment create` command to override the mocked URL.

Note, similarly to when we containerized our code, we can use the generated Dockerfile for our deployment.

```shell
blackbird deployment create simple-api --dockerfile Dockerfile --context .
```

If you use your own Dockerfile, make sure that the image will not run as root. Refer to the limitations section in the Deployment user guide for more information.

Once the command is finished running, we should notice that our existing mocked URL has been used again with the containerized API code. This command is similar to `code run`, but instead of running locally, everything is deployed within a Blackbird environment.

If your deployment status doesn't switch to ready soon after it's created, check the troubleshooting section in the Deployment user guide for possible causes and solutions.

## 2. Testing our Deployment

Now that we have a deployed simple-api project, we can double-check the status of the deployment and curl to the mocked URL.

```shell
blackbird deployment status simple-api
```

```shell
curl https://<host-name>/simple-api/say-hello
```

Additionally, we can view the logs of the API with the addition of the `--logs` flag.

```shell
blackbird deployment status simple-api --logs
```

We should see our curled GET request now appearing in the Application logs.

Deployments can be used to replace mocks or run separately if a new name is provided. In the quickstart, we replaced our existing mock.

## 3. Next Steps

At this point you should have a good understanding of all the various Blackbird functionality and how Blackbird can help you accelerate your API development process. Please feel free to checkout other documentation such as how to [secure-instances-on-blackbird.md](../technical-reference/secure-instances-on-blackbird.md "mention") and our [user-management.md](../user-management.md "mention") guide.
