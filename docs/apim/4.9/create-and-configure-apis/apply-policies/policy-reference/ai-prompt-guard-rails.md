---
description: An overview about ai - prompt guard rails.
metaLinks:
  alternates:
    - ai-prompt-guard-rails.md
---

# AI - Prompt Guard Rails

## Overview

This policy uses an AI-powered text classification model to evaluate user prompts for potentially inappropriate or malicious content. It can detect a wide range of violations, such as profanity, sexually explicit language, harmful intent, and jailbreak prompt injections, which are adversarial inputs crafted to bypass AI safety mechanisms.

Depending on configuration, when a prompt is flagged:

* **Blocked and flagged** – the request is denied at the gateway
* **Allowed but flagged** – the request proceeds but is logged for monitoring

{% hint style="info" %}
You may face an error when using this policy using the Gravitee's docker image. This is due to the fact that the default image are based on Alpine Linux, which does not support the ONNX Runtime. To resolve this issue you need to use the Gravitee's docker image based on Debian, which is available at graviteeio/apim-gateway:4.8.0-debian.
{% endhint %}

## Content Checks

The Content Checks property specifies the classification labels that are applied to evaluate prompts. You should choose Labels in alignment with the selected model's capabilities and the intended filtering goals. For example, filtering for profanity while omitting toxicity checks.

Supported labels are documented in the model’s card or configuration file.

## AI Model Resource

The policy requires an **AI Model Text Classification Resource** to be defined at the API level. This resource serves as the classification engine for evaluating prompts' content during policy execution.

For more information about creating and managing resources, go to [Resources](https://documentation.gravitee.io/apim/policies/resources)

After the resource is created, the policy must be configured with the corresponding name using the **AI Model Resource Name** property.

> _**NOTE**_: The policy will load the model while handling the first request made to the API. Therefore, this first call will take longer than usual, as it includes the model loading time. Subsequent requests will be processed faster.

## Notice

This plugin allows usage of models based on meta LLama4:

* [gravitee-io/Llama-Prompt-Guard-2-22M-onxx](https://huggingface.co/gravitee-io/Llama-Prompt-Guard-2-22M-onnx)
* [gravitee-io/Llama-Prompt-Guard-2-86M-onxx](https://huggingface.co/gravitee-io/Llama-Prompt-Guard-2-86M-onnx)

> Llama 4 is licensed under the Llama 4 Community License, Copyright © Meta Platforms, Inc. All Rights Reserved.

## Phases

The `ai-prompt-guard-rails` policy can be applied to the following API types and flow phases.

### Compatible API types

* `PROXY`

### Supported flow phases

* Request

## Compatibility matrix

Strikethrough text indicates that a version is deprecated.

| Plugin version  | APIM            | Java version |
| --------------- | --------------- | ------------ |
| 1.0.0 and after | 4.8.x and after | 21           |

## Configuration options

| <p>Name<br><code>json name</code></p>                             | <p>Type<br><code>constraint</code></p> | Mandatory | Default       | Description                                                                          |
| ----------------------------------------------------------------- | -------------------------------------- | :-------: | ------------- | ------------------------------------------------------------------------------------ |
| <p>Content Checks<br><code>contentChecks</code></p>               | string                                 |           |               | Comma-separated list of model labels (e.g., TOXIC,OBSCENE)                           |
| <p>Prompt Location<br><code>promptLocation</code></p>             | string                                 |           |               | Prompt Location                                                                      |
| <p>Request Policy<br><code>requestPolicy</code></p>               | enum (string)                          |           | `LOG_REQUEST` | <p>Request Policy<br>Values: <code>BLOCK_REQUEST</code> <code>LOG_REQUEST</code></p> |
| <p>Resource Name<br><code>resourceName</code></p>                 | string                                 |           |               | The resource name loading the Text Classification model                              |
| <p>Sensitivity threshold<br><code>sensitivityThreshold</code></p> | number                                 |           | `0.5`         |                                                                                      |

## Examples

Only log the request when inappropriate prompt detected

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "AI - Prompt Guard Rails example API",
    "resources": [
      {
        "name": "ai-model-text-classification-resource",
        "type": "ai-model-text-classification",
        "configuration": "{\"model\":{\"type\":\"MINILMV2_TOXIC_JIGSAW_MODEL\"}}",
        "enabled": true
      }
    ],
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
        "request": [
          {
            "name": "AI - Prompt Guard Rails",
            "enabled": true,
            "policy": "ai-prompt-guard-rails",
            "configuration":
              {
                  "resourceName": "ai-model-text-classification-resource",
                  "promptLocation": "{#request.jsonContent.prompt}",
                  "contentChecks": "identity_hate,insult,obscene,severe_toxic,threat,toxic",
                  "requestPolicy": "LOG_REQUEST"
              }
          }
        ]
      }
    ]
  }
}

```

_Block request when inappropriate prompt detected_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "AI - Prompt Guard Rails example API",
    "resources": [
      {
        "name": "ai-model-text-classification-resource",
        "type": "ai-model-text-classification",
        "configuration": "{\"model\":{\"type\":\"MINILMV2_TOXIC_JIGSAW_MODEL\"}}",
        "enabled": true
      }
    ],
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
        "request": [
          {
            "name": "AI - Prompt Guard Rails",
            "enabled": true,
            "policy": "ai-prompt-guard-rails",
            "configuration":
              {
                  "resourceName": "ai-model-text-classification-resource",
                  "promptLocation": "{#request.jsonContent.prompt}",
                  "contentChecks": "identity_hate,insult,obscene,severe_toxic,threat,toxic",
                  "requestPolicy": "BLOCK_REQUEST"
              }
          }
        ]
      }
    ]
  }
}

```

_Provide a custom sensitivity threshold for inappropriate prompts_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "AI - Prompt Guard Rails example API",
    "resources": [
      {
        "name": "ai-model-text-classification-resource",
        "type": "ai-model-text-classification",
        "configuration": "{\"model\":{\"type\":\"MINILMV2_TOXIC_JIGSAW_MODEL\"}}",
        "enabled": true
      }
    ],
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
        "request": [
          {
            "name": "AI - Prompt Guard Rails",
            "enabled": true,
            "policy": "ai-prompt-guard-rails",
            "configuration":
              {
                  "resourceName": "ai-model-text-classification-resource",
                  "promptLocation": "{#request.jsonContent.prompt}",
                  "sensitivityThreshold": 0.1,
                  "contentChecks": "identity_hate,insult,obscene,severe_toxic,threat,toxic",
                  "requestPolicy": "BLOCK_REQUEST"
              }
          }
        ]
      }
    ]
  }
}

```

## Changelog

#### 1.0.0-alpha.1 (2025-06-18)

#### **Features**

* implementation of AI prompt guard rails policy ([b101445](https://github.com/gravitee-io/gravitee-policy-ai-prompt-guard-rails/commit/b1014451356cf708dab05f9df1d7a67eaa9fb63b))
