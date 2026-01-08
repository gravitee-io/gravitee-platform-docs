---
description: An overview about ai - prompt token tracking.
metaLinks:
  alternates:
    - ai-prompt-token-tracking.md
---

# AI - Prompt Token Tracking

## Overview

This policy allows you to track of the number of tokens sent and received by an AI API.

## Usage

Here are some examples for how to use the AI - Prompt Token Tracking.

### Built-in support for OpenAI, Gemini, Claude, and Mistral

The plugin has built-in support for the following AI providers:

* OpenAI (ChatGPT)
* Google (Gemini)
* Anthropic (Claude)
* Mistral

Select the appropriate type in the configuration, and the plugin handles the token tracking automatically.

### Custom Provider

When the API provider is not one of the built-in providers, use the `CUSTOM` type. When you choose the `CUSTOM`, you must provide a custom response body parsing configuration that matches the structure of the API responses from your provider.

For example, the following configuration can be used to extract tokens usage and model from a custom AI API response:

```json
{
  "id": "a6775254-dc2f-4411-9b1c-415f3ba8ee8d",
  "my_model": "LLAAMA",
  "result": "a result",
  "my_usage": {
    "promptUsage": 100,
    "responseUsage": 8
  }
}
```

* Sent tokens count point: `my_usage.promptUsage`
* Receive tokens count point: `my_usage.responseUsage`
* Sent tokens count point: `my_model`

## Phases

The `ai-prompt-token-tracking` policy can be applied to the following API types and flow phases.

### Compatible API types

* `PROXY`

### Supported flow phases:

* Response

## Compatibility matrix

Strikethrough text indicates that a version is deprecated.

| Plugin version  | APIM            | Java version |
| --------------- | --------------- | ------------ |
| 1.0.0 and after | 4.8.x and after | 21           |

## Configuration options

| <p>Name<br><code>json name</code></p>                   | <p>Type<br><code>constraint</code></p> | Mandatory | Description                                     |
| ------------------------------------------------------- | -------------------------------------- | :-------: | ----------------------------------------------- |
| <p>Response body parsing<br><code>extraction</code></p> | object                                 |           | <p><br>See "Response body parsing" section.</p> |
| <p>Cost<br><code>pricing</code></p>                     | object                                 |           | <p><br>See "Cost" section.</p>                  |

**Response body parsing (Object)**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Description                                                                                                                                       |
| ------------------------------------- | -------------------------------------- | :-------: | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p>Type<br><code>type</code></p>      | object                                 |     ✅     | <p>Type of Response body parsing<br>Values: <code>GPT</code> <code>GEMINI</code> <code>CLAUDE</code> <code>MISTRAL</code> <code>CUSTOM</code></p> |

**Response body parsing: ChatGPT by OpenAI `type = "GPT"`**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description |
| ------------------------------------- | -------------------------------------- | :-------: | ------- | ----------- |
| No properties                         |                                        |           |         |             |

**Response body parsing: Gemini by Google `type = "GEMINI"`**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description |
| ------------------------------------- | -------------------------------------- | :-------: | ------- | ----------- |
| No properties                         |                                        |           |         |             |

**Response body parsing: Claude by Anthropic `type = "CLAUDE"`**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description |
| ------------------------------------- | -------------------------------------- | :-------: | ------- | ----------- |
| No properties                         |                                        |           |         |             |

**Response body parsing: Mistral `type = "MISTRAL"`**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description |
| ------------------------------------- | -------------------------------------- | :-------: | ------- | ----------- |
| No properties                         |                                        |           |         |             |

**Response body parsing: Custom provider `type = "CUSTOM"`**

| <p>Name<br><code>json name</code></p>                            | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description                                                                     |
| ---------------------------------------------------------------- | -------------------------------------- | :-------: | ------- | ------------------------------------------------------------------------------- |
| <p>Sent token count EL<br><code>inputTokenPointer</code></p>     | string                                 |     ✅     |         | A Gravitee Expression Language that represent number of tokens sent to LLM      |
| <p>Model pointer<br><code>modelPointer</code></p>                | string                                 |           |         | A Gravitee Expression Language that represent model of LLM                      |
| <p>Receive token count EL<br><code>outputTokenPointer</code></p> | string                                 |     ✅     |         | A Gravitee Expression Language that represent number of tokens receive from LLM |

**Cost (Object)**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Description                                                           |
| ------------------------------------- | -------------------------------------- | :-------: | --------------------------------------------------------------------- |
| <p>Type<br><code>type</code></p>      | object                                 |     ✅     | <p>Type of Cost<br>Values: <code>none</code> <code>pricing</code></p> |

**Cost: No cost calculation `type = "none"`**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description |
| ------------------------------------- | -------------------------------------- | :-------: | ------- | ----------- |
| No properties                         |                                        |           |         |             |

**Cost: Cost calculation `type = "pricing"`**

| <p>Name<br><code>json name</code></p>                            | <p>Type<br><code>constraint</code></p>  | Mandatory | Default | Description              |
| ---------------------------------------------------------------- | --------------------------------------- | :-------: | ------- | ------------------------ |
| <p>Input Token Price Unit<br><code>inputPriceUnit</code></p>     | <p>number<br><code>(0, +Inf]</code></p> |     ✅     |         | Input Token Price Unit   |
| <p>Input Token Price Value<br><code>inputPriceValue</code></p>   | <p>number<br><code>(0, +Inf]</code></p> |     ✅     |         | Input Token Price Value  |
| <p>Output Token Price Unit<br><code>outputPriceUnit</code></p>   | <p>number<br><code>(0, +Inf]</code></p> |     ✅     |         | Output Token Price Unit  |
| <p>Output Token Price Value<br><code>outputPriceValue</code></p> | <p>number<br><code>(0, +Inf]</code></p> |     ✅     |         | Output Token Price Value |

## Examples

Calculate usage cost for OpenAI ChatGPT API

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "AI - Prompt Token Tracking example API",
    "flows": [
      {
        "name": "Common Flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "STARTS_WITH"
          }
        ],
        "response": [
          {
            "name": "AI - Prompt Token Tracking",
            "enabled": true,
            "policy": "ai-prompt-token-tracking",
            "configuration":
              {
                  "extraction": {
                      "type": "GPT"
                  },
                  "pricing": {
                      "inputPriceValue": 0.4,
                      "inputPriceUnit": 1000000,
                      "outputPriceValue": 0.8,
                      "outputPriceUnit": 1000000
                  }
              }
          }
        ]
      }
    ]
  }
}

```

_Track tokens usage only on Custom API response_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "AI - Prompt Token Tracking example API",
    "flows": [
      {
        "name": "Common Flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "STARTS_WITH"
          }
        ],
        "response": [
          {
            "name": "AI - Prompt Token Tracking",
            "enabled": true,
            "policy": "ai-prompt-token-tracking",
            "configuration":
              {
                  "extraction": {
                      "type": "CUSTOM",
                      "inputTokenPointer": "/usage/custom_prompt_tokens",
                      "outputTokenPointer": "/usage/custom_completion_tokens",
                      "modelPointer": "/custom_model"
                  },
                  "pricing": {
                      "type": "none"
                  }
              }
          }
        ]
      }
    ]
  }
}

```

## Changelog

#### 1.0.0-alpha.1 (2025-06-17)

**Features**

* extract token sent, received and model of LLM queries ([f6182df](https://github.com/gravitee-io/gravitee-policy-ai-prompt-token-tracking/commit/f6182dfd4cd1ef172621e6f05f77807e38815bc2))
