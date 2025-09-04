---
noIndex: true
---

# Code Generation

Generating server or client code from an API specification allows you to interact with your API specification more efficiently during development and testing. Blackbird uses [OpenAPI Generator](https://openapi-generator.tech/) to generate code for the API description. However, you can use any of the available server or client generators. For more information, see the [OpenAPI Generators List](https://openapi-generator.tech/docs/generators).

## Using a sample template to generate code

Use a sample template to explore how Blackbird's code generation process works.

**To generate code using a sample template:**

1.  Download the sample [petstore.yaml](https://blackbird.a8r.io/assets/downloads/specs/petstore/openapi.yaml) file to use for testing.

    ```yaml
    openapi: "3.0.0"
    info:
      version: 1.0.0
      title: Swagger Petstore
      license:
        name: MIT
      contact:
        name: Swagger API Team
        email: fakeemail@fake.com
      description: This is a sample server Petstore server.
    tags:
      - name: pets
        description: Everything about your Pets
      - name: owners
        description: Everything about the owners
    paths:
      /pets:
        get:
          description: List all pets
          operationId: listPets
          tags:
            - pets
          parameters:
            - name: limit
              in: query
              description: How many items to return at one time (max 100)
              required: false
              schema:
                type: integer
                maximum: 100
                format: int32
          responses:
            '200':
              description: A paged array of pets
              headers:
                x-next:
                  description: A link to the next page of responses
                  schema:
                    type: string
              content:
                application/json:
                  schema:
                    $ref: "#/components/schemas/Pets"
            default:
              description: unexpected error
              content:
                application/json:
                  schema:
                    $ref: "#/components/schemas/Error"
        post:
          description: Create a pet
          operationId: createPets
          tags:
            - pets
          responses:
            '201':
              description: Null response
            default:
              description: unexpected error
              content:
                application/json:
                  schema:
                    $ref: "#/components/schemas/Error"
      /pets/{petId}:
        get:
          description: Info for a specific pet
          operationId: showPetById
          tags:
            - pets
          parameters:
            - name: petId
              in: path
              required: true
              description: The id of the pet to retrieve
              schema:
                type: string
          responses:
            '200':
              description: Expected response to a valid request
              content:
                application/json:
                  schema:
                    $ref: "#/components/schemas/Pet"
            default:
              description: unexpected error
              content:
                application/json:
                  schema:
                    $ref: "#/components/schemas/Error"
    components:
      schemas:
        Pet:
          type: object
          required:
            - id
            - name
          properties:
            id:
              type: integer
              format: int64
            name:
              type: string
            tag:
              type: string
        Pets:
          type: array
          maxItems: 100
          items:
            $ref: "#/components/schemas/Pet"
        Error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: integer
              format: int32
            message:
              type: string
    ```
2.  (Optional but recommended) Create a basic configuration for the template. While not required, this establishes a standard setup for multiple projects. For example, you can define a configuration file for the Go server template by creating a file named `blackbird-go-server-config.yaml` with the following content.

    ```yaml
    gitHost: github.com # or any other git host
    gitUserId: my-org # or any other user/org ID
    ```

    > **Note:** These options can be overwritten for different projects using the `--gen-config-values` flag with unique values like `name` or `version`. You can use multiple values by repeating the flag.
3.  Run the code generate command using one of the following options:

    If you didn't create a basic configuration for the template, use the following command.

    ```shell
    blackbird code generate server go-server -s petstore.yaml -o ~/Documents/new-project
    ```

    If you created a basic configuration for the template, use the `--gen-config-path` flag to specify the path to the configuration file.

    ```shell
    blackbird code generate server go-server -s petstore.yaml -o ~/Documents/new-project --gen-config-path blackbird-go-server-config.yam--gen-config-values gitRepoId=my-application
    ```
4.  Apply the variables prompted by the CLI. Provide the package version and package name.

    ```shell
    Enter the package name [swagger_petstore]:
    Enter the package version [1.0.0]:
    ```

When the API project is generated, it creates a new directory with all the necessary modules and Go files for the projects, including the Dockerfile you'll use to run and debug the code.

## Using an existing API in Blackbird to generate code

If you want to use an existing API in Blackbird to generate code, use one of the following options.

### Generate server code

Generate server-side boilerplate code to help backend developers implement and test API routes and endpoints.

**To generate the server code for the API:**

```shell
blackbird code generate server --api-name <slug name>
```

### Generate API client code

Generate client-side code to help frontend developers interact with and test API methods and endpoints.

**To generate API client code:**

```shell
blackbird code generate client --api-name <slug name>
```
