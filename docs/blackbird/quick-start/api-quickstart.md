---
noIndex: true
---

# API Quickstart

In this tutorial, we'll be adding an entry to our API catalog using the Blackbird CLI.

## Before you get started

Before you get started:

* Download the CLI and log in. For more information, see [#download-the-cli-and-log-in-optional](./#download-the-cli-and-log-in-optional "mention").
* Open your preferred IDE, such as Visual Studio Code.

## 1. Creating an API

For the purposes of this tutorial we are going to use the sample [simpleapi.yaml](https://blackbird.a8r.io/assets/downloads/specs/simpleapi/openapi.yaml) file.

```yaml
openapi: 3.0.1
info:
  title: Simple API
  version: 1.0.0
paths:
  "/say-hello":
    get:
      summary: Get a hello message
      operationId: getHello
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Hello, World!
                required:
                - message
                additionalProperties: false
        4XX:
          description: Client Error
        5XX:
          description: Server Error
  "/echo":
    post:
      summary: Echo back the message
      operationId: postEcho
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  echoedMessage:
                    type: string
                required:
                - echoedMessage
                additionalProperties: false
        4XX:
          description: Client Error
        5XX:
          description: Server Error
components:
  schemas:
    ErrorMessage:
      type: object
      properties:
        error:
          type: string
      required:
      - error
      additionalProperties: false
```

Once the file is downloaded, we are going to add an API to our catalog using the `api create` command.

```shell
blackbird api create "Simple API" --spec-path ./simpleapi.yaml
```

## 2. Listing an API

Once our API is created, we can view it using the `api list` command.

```shell
blackbird api list simple-api
```

## 3. Using our API

Now that we have an API in our catalog, there are a few different Blackbird tools that we can now use.

The next step in our tutorial should be to mock our API. Please follow the [mock-quickstart.md](mock-quickstart.md "mention") guide.

## 4. Deleting our API

Once we are done using our API, we can delete it from our catalog using the `api delete` command.

```shell
blackbird api delete simple-api
```

This command will also ask us if we should delete all deployments associated with our API as well.
