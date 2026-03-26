---
description: Getting started with Mock Quickstart.
noIndex: true
---

# Mock Quickstart

In this tutorial, we'll be creating a mock server of an API in our catalog using the Blackbird CLI

## Before you get started

Before you get started:

* Download the CLI. For more information, see [#download-the-cli-and-log-in-optional](./#download-the-cli-and-log-in-optional "mention").
* Add or create an API. For more information, see [api-quickstart.md](api-quickstart.md "mention").
* Open your preferred IDE, such as Visual Studio Code.

## 1. Creating a Mocked Instance

Now that we have an entry in our API catalog, we can create a mock server using the `mock create` command.

```shell
blackbird mock create simple-api --api-name simple-api
```

This command may take a few seconds while our environment gets set up and the mock instance gets created.

Once the mock instance is ready, we should see an output with a hostname. This mocked hostname will be our new endpoint for this instance.

## 2. Listing a Mocked Instance

Once our Mock instance is created, we can view it using the `mock list` or `instance list` command.

```shell
blackbird mock list
```

```shell
blackbird instance list
```

## 3. Using our Mocked Instance

We can now send a request to our mocked instance to test the behavior. For the purposes of this tutorial we will use `curl`.

```shell
curl https://<host-name>/simple-api/say-hello
```

We should be returned with a message. Note that the value of the message is generated with a nonsense string. Similarly, if the value was expected to be an integer, we can expect a random integer.

## 4. Configuring our Mocked Instance

If you want to enable your mock instance to generate random data based on the schema objects defined in the OpenAPI specification, consider using dynamic data generation.

You can do this by using the `mock config <mock-name> set` command.

```shell
blackbird mock config simple-api set dynamic=true
```

To preview the configuration of your mock instance, use the `mock config <mock-name> get` command.

```shell
blackbird mock config simple-api get # to get the whole config
blackbird mock config simple-api get dynamic # to get a specific config value
```

At the moment, `dynamic` is the only configuration value that can be set.

## 5. Next Steps

Now that we have a working mocked instance and know what the outputs of our requests look like, the next step would be to generate a project using our API.

The next step in our tutorial should be to generate code. Please follow the [code-quickstart.md](code-quickstart.md "mention") guide.

## 6. Deleting our Mocked Instance

Once we are done using our mocked instance, we can spin down the environment and clean up our resources with the `mock delete` command.

```shell
blackbird mock delete simple-api
```
