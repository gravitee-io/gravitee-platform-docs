# Example Resource Configurations

## Overview

Terraform defines resources as basic infrastructure elements. It creates and manages these resources as part of its Infrastructure as Code (IaC) workflow. This lets you use configuration files to automate reproducible and version controlled APIs.

Resources are classified by type, where a resource type is associated with a particular provider. Gravitee's Terraform provider supports several different resource types, such as v4 APIs and Shared Policy Groups.

To create a resource, you need to add a resource definition to your Terraform configuration file. The definition includes settings such as the resource type, a Human-readable Identifier (hrid) to uniquely identify the resource by name, and arguments to specify other resource parameters.

Terraform uses your configuration files to track the state of your infrastructure. When you update your configuration, Terraform detects the differences between your existing and desired states. It then creates and executes a plan to apply your changes. This is a fully automated alternative to manually updating your APIs in the APIM Console or with mAPI scripts.

## Gravitee resources

The Gravitee Terraform provider supports the following Gravitee resource types:&#x20;

* v4 HTTP proxy API
* v4 message API
* v4 Native Kafka API
* Shared Policy Group

Terraform can create, update, or delete these resources as part of its workflow.&#x20;

## Lifecycle

Each resource is identified by the unique value assigned to its `hrid` field. This field can be referenced by other resources to enable object dependency. For example, an API that invokes a Shared Policy Group can refer to a particular Shared Policy Group resource using its `hrid` value.

{% hint style="info" %}
For consistency, we recommend that you use the same value for a resource's name and `hrid`. We also recommend that you choose meaningful resource names / `hrid` values, and only modify them when it is compulsory.
{% endhint %}

If the name or `hrid` of a resource is modified, Terraform does not recognize it as an existing entity. Instead, Terraform considers the resource to be a new entity. To avoid dangling objects that were created by Terraform but are no longer managed by it, Gravitee deletes a resource whose `hrid` was modified, and then creates a new resource with the modified `hrid` value.&#x20;

{% hint style="info" %}
If you modify the `hrid` of an API resource, its analytics data is no longer accessible. If you then reapply the original `hrid`, analytics are accessible in the state prior to the `hrid` change.
{% endhint %}

## Plugin configuration

Gravitee includes a powerful plugin system that lets you extend its capabilities.&#x20;

You can create plugins for your APIs using custom schema, because from the perspective of the Management API, plugins are schema-less. This forces you to use the `jsonencode(any)` function repeatedly in Terraform resources. The schema-less properties that require this are all named `configuration`.

The `configuration` naming conventions used by Terraform and Gravitee differ. Terraform uses conventional `snake_case`, whereas Gravitee API uses `lowerCamelCase`. The following example illustrates this difference:

```hcl
endpoints = [
  {
    name = "Default Kafka"
    type = "kafka"
    # configuration => Gravitee plugin
    configuration = jsonencode({
      # camelCase
      bootstrapServers = "localhost:8082"
    })
    # snake_case
    inherit_configuration = true
  }
]
```

## Examples

The following examples configure resources for specific use cases:

* [#example-1-create-a-simple-v4-http-proxy-api-that-transforms-headers](example-resource-configurations.md#example-1-create-a-simple-v4-http-proxy-api-that-transforms-headers "mention")
* [#example-2-create-a-v4-message-api-that-fetches-kafka-messages](example-resource-configurations.md#example-2-create-a-v4-message-api-that-fetches-kafka-messages "mention")
* [#example-3-create-a-v4-native-kafka-proxy-api-that-assigns-a-custom-attribute](example-resource-configurations.md#example-3-create-a-v4-native-kafka-proxy-api-that-assigns-a-custom-attribute "mention")
* [#example-4-use-a-shared-policy-group-to-rate-limit-a-v4-http-proxy-api](example-resource-configurations.md#example-4-use-a-shared-policy-group-to-rate-limit-a-v4-http-proxy-api "mention")
* [#example-5-use-a-shared-policy-group-to-curate-the-headers-of-a-v4-http-proxy-api](example-resource-configurations.md#example-5-use-a-shared-policy-group-to-curate-the-headers-of-a-v4-http-proxy-api "mention")

{% hint style="info" %}
Example resource configurations, including the examples shown here, can be found in Gravitee's [Terraform provider repository](https://github.com/gravitee-io/terraform-provider-apim/tree/main/examples/use-cases) on GitHub.
{% endhint %}

### Example 1: Create a simple v4 HTTP proxy API that transforms headers

The following example configures the v4 HTTP proxy API resource to create a simple v4 HTTP proxy API with a Keyless plan and publish it to the Developer Portal as a public API. This resource uses the Gravitee [Transform Headers policy](../create-and-configure-apis/apply-policies/policy-reference/transform-headers.md) on the Request phase to add an extra header called "X-Hello."

```hcl
resource "apim_apiv4" "simple-api" {
  # should match the resource name
  hrid            = "simple-api"
  name            = "[Terraform] Simple PROXY API"
  description     = <<-EOT
    A simple API that routes traffic to gravitee echo API with an extra header.
    It is published to the API portal as public API and
    deployed to the Gateway
  EOT
  version         = "1.0"
  type            = "PROXY"
  state           = "STARTED"
  visibility      = "PUBLIC"
  lifecycle_state = "PUBLISHED"
  listeners = [
    {
      http = {
        type = "HTTP"
        entrypoints = [
          {
            type = "http-proxy"
          }
        ]
        paths = [
          {
            path = "/simple-api/"
          }
        ]
      }
    }
  ]
  endpoint_groups = [
    {
      name = "Default HTTP proxy group"
      type = "http-proxy"
      load_balancer = {
        type = "ROUND_ROBIN"
      }
      endpoints = [
        {
          name   = "Default HTTP proxy"
          type   = "http-proxy"
          weight = 1
          inherit_configuration = false
          # Configuration is JSON as is depends on the type schema
          configuration = jsonencode({
            target = "https://api.gravitee.io/echo"
          })
        }
      ]
    }
  ]
  flow_execution = {
    mode           = "DEFAULT"
    match_required = false
  }
  flows = [
    {
      enabled = true
      selectors = [
        {
          http = {
            type         = "HTTP"
            path         = "/"
            pathOperator = "STARTS_WITH"
            methods = []
          }
        }
      ]
      request = [
        {
          enabled = true
          name      = "Add 1 header"
          policy = "transform-headers"
          # Configuration is JSON as the schema depends on the policy used
          configuration = jsonencode({
            scope = "REQUEST"
            addHeaders = [
              {
                name  = "X-Hello"
                value = "World!"
              }
            ]
          })
        }
      ]
    }
  ]

  analytics = {
    enabled = false
  }
  definition_context = {}
  plans = {
    KeyLess = {
      name        = "KeyLess"
      type        = "API"
      mode        = "STANDARD"
      validation  = "AUTO"
      status      = "PUBLISHED"
      description = "This plan does not require any authentication"
      security = {
        type = "KEY_LESS"
      }
    }
  }
}
```

### Example 2: Create a v4 message API that fetches Kafka messages

The following example configures the v4 message API resource to create a v4 message API with a Keyless plan. This API has a WebSocket entrypoint and Kafka endpoint. It fetches messages from a Kafka cluster and publishes them to a client's WebSocket connection.

```hcl
resource "apim_apiv4" "message-api" {
  # should match the resource name
  hrid            = "message-api"
  name            = "[Terraform] Websocket to Kafka message API"
  description     = "Message API that publishes message fetch a Kafka cluster to a websocket."
  version         = "1,0"
  type            = "MESSAGE"
  state           = "STOPPED"
  visibility      = "PRIVATE"
  lifecycle_state = "UNPUBLISHED"
  listeners = [
    {
      http = {
        type = "HTTP"
        entrypoints = [
          {
            type = "websocket"
            configuration = jsonencode({
              publisher = {
                enabled = true
              }
              subscriber = {
                enabled = true
              }
            })
          }
        ]
        paths = [
          {
            path = "/message-api/"
          }
        ]
      }
    }
  ]
  endpoint_groups = [
    {
      name = "Default Kafka group"
      type = "kafka"
      endpoints = [
        {
          name = "Default Kafka"
          type = "kafka"
          configuration = jsonencode({
            bootstrapServers = "localhost:8082"
          })
          inherit_configuration = true
        }
      ]
      shared_configuration = jsonencode({
        consumer = {
          enabled               = true
          autoOffsetReset       = "latest"
          checkTopicExistence   = false
          encodeMessageId       = true
          removeConfluentHeader = false
          topics = [
            "test"
          ]
        }
        security = {
          protocol = "PLAINTEXT"
        }
      })
    }
  ]
  flow_execution = {
    match_required = false
    mode           = "DEFAULT"
  }
  flows = []
  analytics = {
    enabled = true
    sampling = {
      type  = "COUNT"
      value = 10
    }
  }
  definition_context = {}
  plans = {
    KeyLess = {
      name       = "KeyLess"
      type       = "API"
      mode       = "STANDARD"
      validation = "AUTO"
      status     = "PUBLISHED"
      description = "This plan does not require any authentication"
      security = {
        type = "KEY_LESS"
      }
    }
  }
}
```

### Example 3: Create a v4 Native Kafka proxy API that assigns a custom attribute

The following example configures the v4 Native Kafka proxy API resource to create a Native Kafka proxy  API with a Keyless plan. This resource uses the Gravitee [Assign Attributes policy](../create-and-configure-apis/apply-policies/policy-reference/assign-attributes.md) to assign a custom static attribute.

```hcl
resource "apim_apiv4" "kafka_native_api" {
  # should match the resource name
  hrid            = "kafka_native_api"
  name            = "[Terraform] Kafka Native proxy API"
  description     = "Connect to a local kafka cluster with a simple flow"
  version         = "1,0"
  type            = "NATIVE"
  state           = "STOPPED"
  visibility      = "PRIVATE"
  lifecycle_state = "UNPUBLISHED"
  listeners = [
    {
      kafka = {
        type = "KAFKA"
        entrypoints = [
          {
            type = "native-kafka"
          },
        ]
        host = "kafka.local"
        port = 9092
      }
    }
  ]
  endpoint_groups = [
    {
      name = "Default Native endpoint group"
      type = "native-kafka"
      endpoints = [
        {
          configuration = jsonencode({
            bootstrapServers = "kafka.local:9001"
          })
          inherit_configuration = true
          name                  = "Default Native proxy"
          secondary             = false
          type                  = "native-kafka"
          weight                = 1
        },
      ]
      shared_configuration = jsonencode({
        security = {
          protocol = "PLAINTEXT"
        }
      })
    },
  ]
  flows = [
    {
      name = "default"
      enabled : true,
      interact = [
        {
          enabled = true
          name    = "Assign custom static attribute as an example"
          policy  = "policy-assign-attributes"
          configuration = jsonencode({
            attributes = [
              {
                name  = "my.attribute"
                value = "example value"
              }
            ]
          })
        }
      ]
    },
  ]
  definition_context = {}
  plans = {
    KeyLess = {
      name       = "KeyLess"
      type       = "API"
      mode       = "STANDARD"
      validation = "AUTO"
      status     = "PUBLISHED"
      security = {
        type = "KEY_LESS"
      }
    }
  }
}
```

### Example 4: Create a Shared Policy Group for rate limiting

The following example configures the Shared Policy Group resource to use the Gravitee [Rate Limit policy](../create-and-configure-apis/apply-policies/policy-reference/rate-limit.md). It applies rate limiting on the Request phase to limit traffic to 10 requests per minute.

```hcl
resource "apim_shared_policy_group" "ratelimit-policy" {
  # should match the resource name
  hrid        = "ratelimit-policy"
  name        = "[Terraform] Rate limit shared policy"
  api_type    = "PROXY"
  description = "Single step rate limiting policy group"
  phase       = "REQUEST"
  steps = [
    {
      enabled     = true
      description = "Limit traffic to 10 request per minute"
      name        = "Rate Limit 10"
      policy      = "rate-limit"
      configuration = jsonencode({
        addHeaders = true
        async      = false
        rate = {
          key            = ""
          limit          = 10
          periodTime     = 1
          periodTimeUnit = "MINUTES"
          useKeyOnly     = false
        }
      })
    },
  ]
}
```

### Example 5: Use a Shared Policy Group to curate the headers of a v4 HTTP proxy API

The following example configures the Shared Policy Group resource to use the Gravitee [Transform Headers policy](../create-and-configure-apis/apply-policies/policy-reference/transform-headers.md) on the Request phase of a v4 HTTP proxy API. The resource removes the header "User-Agent" and adds a header named "X-Content-Path" that contains the API's context path.

```hcl
resource "apim_shared_policy_group" "curate_headers" {
  # should match the resource name
  hrid        = "curate_headers"
  name        = "[Terraform] Curated headers"
  description = "Simple Shared Policy Group that contains one step to remove User-Agent header and add X-Content-Path that contains this API context path"
  api_type    = "PROXY"
  phase       = "REQUEST"
  steps = [
    {
      enabled = true
      name    = "Curate headers"
      policy = "transform-headers"
      configuration = jsonencode({
        scope = "REQUEST"
        addHeaders = [
          {
            name  = "X-Context-Path"
            value = "{#request.contextPath}"
          }
        ],
        removeHeaders = ["User-Agent"]
      })
    }
  ]
}

resource "apim_apiv4" "simple-api-with-spg" {
  # should match the resource name
  hrid            = "simple-api-with-spg"
  name            = "[Terraform] Simple PROXY API With Shared Policy Group"
  description     = "A simple API that routes traffic to gravitee echo API. It curates headers using curate_headers Shared Policy Group."
  version         = "1"
  type            = "PROXY"
  state           = "STARTED"
  visibility      = "PRIVATE"
  lifecycle_state = "UNPUBLISHED"
  listeners = [
    {
      http = {
        type = "HTTP"
        entrypoints = [
          {
            type = "http-proxy"
          }
        ]
        paths = [
          {
            path = "/simple-api-with-spg/"
          }
        ]
      }
    }
  ]
  endpoint_groups = [
    {
      name = "Default HTTP proxy group"
      type = "http-proxy"
      load_balancer = {
        type = "ROUND_ROBIN"
      }
      endpoints = [
        {
          name   = "Default HTTP proxy"
          type   = "http-proxy"
          weight = 1
          inherit_configuration = false
          configuration = jsonencode({
            target = "https://api.gravitee.io/echo"
          })
        }
      ]
    }
  ]
  flow_execution = {
    mode           = "DEFAULT"
    match_required = false
  }
  flows = [
    {
      enabled = true
      selectors = [
        {
          http = {
            type         = "HTTP"
            path         = "/"
            pathOperator = "STARTS_WITH"
            methods = []
          }
        }
      ]
      request = [
        {
          enabled = true
          name   = "[Terraform] Curated headers"
          policy = "shared-policy-group-policy",
          configuration = jsonencode({
            hrid = apim_shared_policy_group.curate_headers.hrid
          })
        }
      ]
    }
  ]
  analytics = {
    enabled = false
  }
  definition_context = {}
  plans = {
    KeyLess = {
      name        = "KeyLess"
      type        = "API"
      mode        = "STANDARD"
      validation  = "AUTO"
      status      = "PUBLISHED"
      description = "This plan does not require any authentication"
      security = {
        type = "KEY_LESS"
      }
    }
  }
}
```

## Known limitations

The following known limitations apply to the 0.2.11 version of the Gravitee Terraform provider:

* APIs created with Terraform are shown in the Console with the 'Kubernetes' icon because they are read-only.
* In the `flows` section of the API resource definition, the `name` of the request should match the name of the Shared Policy Group to avoid inconsistencies when `terraform plan` is executed.
* In the `plans` section of the API resource definition, the `name` of the plan should match the key to avoid inconsistencies when `terraform plan` is executed.
* An API that uses a Shared Policy Group in its flow has a field named `sharedPolicyGroupId`  in its state, instead of `hrid`. This has no implications and will be fixed in upcoming releases.
* The `definition_context` section of the API resource definition will be removed in future versions, as it is deprecated but still mandatory.
* `pages` are not yet supported, but will be in an upcoming minor release. Examples will be added.
