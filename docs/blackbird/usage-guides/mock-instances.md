---
description: Overview of Mock Instances.
noIndex: true
---

# Mock Instances

A mock instance is a simulated version of your OpenAPI specification that replicates the behavior in a controlled environment.

Using mocks enhances productivity, facilitates testing, and improves the overall quality of your application by allowing you to design and test your application without accessing the actual API. It also allows for parallel development for frontend and backend components by allowing developers to work on their respective parts simultaneously.

You can use and manage mock instances in the Blackbird UI and CLI, but the functionality varies. You can use and manage mock instances in the Blackbird UI and CLI, but the functionality varies. Use the following sections to learn about the differences.

## Using mock instances in the UI

The [Blackbird UI](https://blackbird.a8r.io/dashboard) provides a user-friendly interface to help you interact with Blackbird mock instances.

### Create a mock instance in the UI

You can create a mock instance by using an existing API in your Blackbird catalog, uploading your own API specification, or choosing a third-party API specification.

**To create a mock:**

1. Open the [Blackbird UI](https://blackbird.a8r.io/dashboard).
2. In the left pane, choose **Mocks** under **Instances**.
3. Choose the **Create Mock** button.
4.  Choose one of the following options:

    * **Mock Existing API** – Choose an existing API from your Blackbird catalog.
    * **Upload Existing API** – Upload your own OpenAPI specification.
    * **Third-Party API** – Choose an external API to start designing your API with pre-built functionality. For example, use OpenAPI, Zoom API, or Google Analytics API.

    After you choose which API specification to mock, your mock instance displays on the Mocks page.

### View mock instances in the UI

You can view your mock instances in the following ways:

* In the left pane, choose **Mocks** and then choose the **mock** you want to view.
* In the left pane, choose **APIs** under **Catalog** and then choose the **View Mock Instance** button in the API tile.

### Configure a mock instance in the UI

You can configure the following mock options in the UI:

* **Dynamic mocking:** Toggle between dynamic and static mocking. Dynamic mocking generates responses based on input parameters, whereas static mocking returns fixed, predefined responses based on hardcoded data. If you have your own examples in your OpenAPI specification, consider using static mocking.
* **Response delay range:** Set the range for the response delay. The delay is calculated in milliseconds and randomized between the minimum and maximum numbers you set.
* **Simulated error rate:** Return randomized simulated error codes based on the specified rate.

**To configure a mock instance:**

1. Open the **mock** you want to configure.
2. Under **Instance Actions**, choose **Mock Configuration**.
3. Under **Dynamic Mocking**, slide the **toggle switch** on to use dynamic mocking or turn it off to use static mocking.
4. Under **Response Delay Range**, drag the sliders to define the range of the response delay you want to set. To reset the range, choose the **Reset Delay**.
5.  Under **Simulated Error Rate**:

    a. Slide the **toggle switch** on to use a simulated error rate.

    b. Select one or more **HTTP error codes** from the list.

    c. Define the **error rate**.
6. When your configuration is set, choose **Close** to close the window. The mock configuration selections display in the mock details area.

### Delete a mock instance in the UI

You can delete a mock instance in the following ways:

* In the left pane, choose **Mocks** and then choose the **Delete Instance** icon next to the mock you want to delete.
* In the left pane, choose **APIs** under **Catalog**, choose the **View Mock Instance** button in the API tile, and then choose the **Remove API** icon.

## Using mock instances with the CLI

The Blackbird CLI provides a fast and flexible way to interact with your API specs directly from the command line.

> **Note:** For a full list of CLI commands, see [mock.md](../technical-reference/blackbird-cli/mock.md "mention") in the _Blackbird CLI Reference_.

### Create a mock instance with the CLI

You can use one of the following API specification options when creating a mock using the CLI:

* An existing API specification in the Blackbird catalog.
* Your own API specification file.
* A sample API specification file ([Swagger Petstore](https://blackbird.a8r.io/assets/downloads/specs/petstore/openapi.yaml)).

> **Note:** For information on creating an API in the Blackbird catalog, see [apis.md](apis.md "mention").

To create a mock using an existing API specification in the Blackbird catalog, use its slug name in the following command.

```shell
blackbird mock create --api-name <slug-name>
```

To create a mock using your own API specification or the sample API specification, use the file name in the following command.

```shell
blackbird mock create --spec-path=petstore.yaml <name>
```

### View a mock instance with the CLI

You can use the CLI to view details about your mock instances in the following ways:

To view a list of all active mocks, use the following command.

```shell
blackbird mock list
```

### Configure a mock instance with the CLI

You can use the CLI to configure your mock to be dynamic or static. Dynamic mocking generates responses based on input parameters, whereas static mocking returns fixed, predefined responses based on hardcoded data. If you have your own examples in your OpenAPI specification, consider using static mocking.

To configure dynamic or static mocking, use the following command where `<config-parameter>` is `dynamic=true` or `dynamic=false`.

```shell
blackbird mock config set name <config-parameter>
```

To preview the configuration of your mock instance, use the following command.

```shell
blackbird mock config simple-api get # to get the whole config
blackbird mock config simple-api get dynamic # to get a specific config value
```

### Update a mock instance with the CLI

You can update a mock using an existing API specification in the Blackbird catalog or by uploading a new API specification to replace the existing one.

To update a mock using an existing API specification, use the API specification’s slug name in the following command.

```shell
blackbird mock update --api-name <slug-name>
```

To upload a new API specification, use the OpenAPI file name in the following command.

```shell
blackbird mock update --spec-path=simple-api.yaml <name>
```

### Secure a mock instance with the CLI

By default, mock endpoints are publicly available. However, you can secure the endpoints by using API keys or creating and automatically applying API keys when you create a mock.

To create and apply an API key when you create a mock, use the API key header flag in the following command.

```shell
blackbird mock create --api-name <slug-name> --apikey-header <HeaderKey>
```

> **Note:** For information on how to secure an existing mock endpoint, see [secure-instances-on-blackbird.md](../technical-reference/secure-instances-on-blackbird.md "mention").

### Delete a mock instance with a CLI

You can use the CLI to delete a mock instance.

To delete a mock, use the mock name in the following command.

```shell
blackbird mock delete <name>
```
