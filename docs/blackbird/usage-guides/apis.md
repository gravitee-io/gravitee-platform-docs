---
noIndex: true
---

# APIs

Blackbird provides tools for developing and managing your APIs, whether you're building a new API or iterating on an existing specification. It supports OpenAPI Specifications, which are JSON or YAML documents that follow the OpenAPI standard. After you add an API specification to your Blackbird catalog, it can be used to create mock instances, generate code, and deploy to hosted, non-production environments for testing and iteration.

You can use and manage APIs in the Blackbird UI and CLI, but the functionality varies. Use the following sections to learn about the differences.

## Using API specifications in the UI

The [Blackbird UI](https://blackbird.a8r.io/) provides a user-friendly interface to help you interact with API specifications.

### Discover and generate API specifications

Blackbird integrates with Git to simplify how you discover, generate, and manage your APIs. You can import existing API specifications from your Git repositories or analyze a repository to detect services and automatically generate new OpenAPI specifications based on your routes, handlers, and service structure. For more information, see [git.md](../technical-reference/integrations/git.md "mention") in _Integrations_.

### Create an API specification using AI in the UI

You can use an AI chatbot to describe the type of API you want to create and generate a specification based on your request.

**To create an API specification using AI:**

1. Open the [Blackbird UI](https://blackbird.a8r.io/).
2. In the left pane, choose **APIs**.
3. Choose the **Add API** button.
4. Choose the **Create An API** tile.
5.  In the prompt, provide a description of the API you want to create. For example, you could provide the following description for a payment processing API:

    _I want to create a new API for processing payments. Use OpenAPI 3.1.0. The service should have paths and operations related to accepting user payment requests, processing payments, and handling payment errors._
6.  (Optional) After reviewing the content, provide additional prompts to refine the API specification before adding it to your API catalog. For example, you can make changes to existing paths, add new paths, or update schemas.

    > **Note:** You can edit your API after adding it to your API catalog. For more information, see [#edit-an-api-specification-in-the-ui](apis.md#edit-an-api-specification-in-the-ui "mention").
7. When you’re ready, choose the **Accept** button.
8. (Optional) On the **Review Specification** page, update the following:
   * API Name – Provide a name for your API specification.
   * API Description – Provide a description for your API specification.
   *   API tags – Add tags that you can use to identify your resources.

       > **Note:** The Tags feature displays in the UI but isn't available, yet. We'll support tags in a future release.
   *   Mock Instance – Create a simulated version of your API specification that replicates the behavior in a controlled environment for testing purposes.

       > **Note:** For more information on mocking, see [mock-instances.md](mock-instances.md "mention").
9. Choose the **Create API** button.

**Next steps**

Now that you have an API in your Blackbird catalog, you can:

* Generate server or client code from your API specification. For more information, see [code-generation.md](code/code-generation.md "mention").
* Create a new mock instance based on your API specification. For more information, see [mock-instances.md](mock-instances.md "mention").

### Upload an existing API specification in the UI

If you already have an API specification, you can upload it directly into your API catalog.

**To upload an API specification:**

1. Open the [Blackbird UI](https://blackbird.a8r.io/).
2. In the left pane, choose **APIs**.
3. Choose the **Upload An API** tile.
4. In the **Upload API** section, you can either drag and drop a file into the area or click it to browse and select a file.
5. (Optional) On the **Review Specification** page, update the following:
   * API Name – Provide a name for your API specification.
   * API Description – Provide a description for your API specification.
   *   API tags – Add tags that you can use to identify your resources.

       > **Note:** The Tags feature displays in the UI but isn't available, yet. We'll support tags in a future release.
   *   Mock Instance – Create a simulated version of your API specification that replicates the behavior in a controlled environment for testing purposes.

       > **Note:** For more information on mocking, see Mock instances.
6. Choose the **Create API** button.

**Next steps**

Now that you have an API in your Blackbird catalog, you can:

* Generate server or client code from your API specification. For more information, see Code generation.
* Create a new mock instance based on your API specification. For more information, see Mock instances.

### Edit an API specification in the UI

You can modify an existing API specification as your API design evolves.

**To edit an API specification:**

1. Open the [Blackbird UI](https://blackbird.a8r.io/).
2. In the left pane, choose **APIs**.
3. Choose the **name of an API** in your catalog.
4. In the API Actions pane, choose **Edit API Specification**. Your API specification opens in an editor where you can edit it either manually or using AI prompts.
5.  In the **Request Changes** field, provide a description of the change you want to make. For example, you could provide the following description for a payment processing API:

    Update the /payments/process endpoint to accept an optional retry boolean field in the request body to indicate if the payment should be retried on failure.
6. (Optional) Make additional modifications to your API specification.
7. Choose **Accept Changes** to apply the patches, and then **Save** to confirm your updates.

### Remove an API specification in the UI

You can remove API specifications from the catalog. When you remove an API, the API and its data are permanently deleted from your catalog. This operation deallocates the API instance, so you can create a new instance in its place.

**To remove an API specification:**

1. Open the [Blackbird UI](https://blackbird.a8r.io/).
2. In the left pane, choose **APIs**.
3. In the tile of the API you want to remove, choose the **three vertical dots** to expand the menu.
4. Choose **Remove**.

## Using API specifications in the CLI

The [blackbird-cli](../technical-reference/blackbird-cli/ "mention") provides a fast and flexible way to interact with your API specs directly from the command line.

### Add an API to the Blackbird catalog with the CLI

You can create a new API in your Blackbird catalog by providing an API name and the path to the API specification:

```shell
blackbird api create <name> –-spec-path=STRING
```

For more information on your options, see API in the Blackbird CLI Reference.

> **Notes:** If you want to import APIs from Git or create an API using AI, you must use the [Blackbird UI](https://blackbird.a8r.io/). For more information, see [#using-api-specifications-in-the-ui](apis.md#using-api-specifications-in-the-ui "mention").

**Next steps**

Now that you have an API in your Blackbird catalog, you can:

* Generate server or client code from your API specification. For more information, see [code-generation.md](code/code-generation.md "mention").
* Create a new mock instance based on your API specification. For more information, see [mock-instances.md](mock-instances.md "mention").

## Update an existing API with the CLI

You can update an API specification by providing a new API name and path to the API specification:

```shell
blackbird api update <name> --spec-path=STRING
```

## View APIs with the CLI

You can list the details of your API specifications. Each listing includes the API name, slug name, specification file, and creator's name.

To list the details for all API specifications, use the following command.

```shell
blackbird api list
```

To list the details for one specification, use the following command and provide the API’s slug name:

```shell
blackbird api list [<slug-name>]
```

## Remove an API specification with the CLI

You can use the CLI to remove an API specification from your Blackbird catalog.

To delete an API specification, use the following command and provide the API’s slug name:

```shell
blackbird api delete <slug-name>
```

You’ll be prompted to choose whether to delete its associated instances. If you confirm, the instances will be permanently removed from the system. If not, the instances will remain, but the API will be removed from your catalog.
