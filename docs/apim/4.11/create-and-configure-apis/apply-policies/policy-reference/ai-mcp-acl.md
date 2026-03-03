# AI - MCP ACL

## Overview

The `mcp-acl` policy allows you to control access to MCP (Model Context Protocol) server functionalities using an Access Control List (ACL).

You can add this policy to an MCP Proxy API from the Policy Studio to restrict access to MCP features such as the list of tools, resources, and prompts.

## Usage

Here are some usage examples of using MCP ACL.

### 1. Default Behavior (Implicit Deny)

If you add the ACL policy without specifying any rules, the system adopts a restrictive "Deny All" approach by default.

**Action:** Add the policy to an MCP API, save, and deploy.

**Result:**

* All server functionalities will be inaccessible.
* An MCP client will be able to connect to the server via the Gateway, but the lists of tools, resources, and prompts will appear empty.

### 2. Authorizing Only Tool Listing

To allow a client to see available tools without being able to execute them:

* Add a rule (ACL) in the policy configuration.
* Select the `Tools` feature option.
* Check the `tools/list` box.
* Leave the `Name Pattern Type` field on `ANY` (default value).

**Result:** If you configure an MCP client, it will only be able to list available tools, but any attempt to call (execute) them will be rejected.

### 3. Authorizing the Call and Listing of a Specific Tool

To restrict access and execution to a single specific tool (e.g., `get_weather`):

* Add or modify an ACL in the policy configuration.
* In the `Tools` feature option:
  * Check `tools/list` AND `tools/call`.
* In the `Name Pattern Type` field, select `Literal`.
* In the `Name Pattern` field, enter the exact name of the tool (for example: `get_weather`).

**Result:** From now on, only this specific tool is visible to the MCP client and can be called. All other tools remain hidden and inaccessible.

### 4. Execution Conditions

Each ACL rule has a `Trigger Condition` field. This field allows you to add conditional logic to determine if the rule should be applied or ignored.

This is particularly useful for applying context-based security policies.

**Usage Example:** You can condition access to certain tools based on a specific property (claim) present in the user's token or a request attribute.

**Note:** The field generally expects a Gravitee EL (Expression Language) expression.

## Phases

The `mcp-acl` policy can be applied to the following API types and flow phases.

### Compatible API types

* `MCP PROXY`

### Supported flow phases:

* Request

## Compatibility matrix

Strikethrough text indicates that a version is deprecated.

| Plugin version | APIM             | UI Dependencies |
| -------------- | ---------------- | --------------- |
| 1.x            | 4.10.x to latest | 17.6.1          |

## Configuration options

| <p>Name<br><code>json name</code></p>      | <p>Type<br><code>constraint</code></p> | Mandatory | Description                                                                                                                            |
| ------------------------------------------ | -------------------------------------- | :-------: | -------------------------------------------------------------------------------------------------------------------------------------- |
| <p>ACLs<br><code>authorizations</code></p> | array                                  |           | <p>Define ACLs (Access Control Lists) in order to determine what users are having access to what resources.<br>See "ACLs" section.</p> |

### **ACLs (Array)**

| <p>Name<br><code>json name</code></p>              | <p>Type<br><code>constraint</code></p>         | Mandatory | Description                                                                      |
| -------------------------------------------------- | ---------------------------------------------- | :-------: | -------------------------------------------------------------------------------- |
| <p>Features<br><code>authorizedFeatures</code></p> | <p>array<br><code>[1, +Inf], unique</code></p> |     ✅     | <p><br>See "Features" section.</p>                                               |
| <p>Condition<br><code>condition</code></p>         | string                                         |           | The condition for which the following ACL should be be applicable (supports EL). |

### **Features (Array)**

| <p>Name<br><code>json name</code></p> | <p>Type<br><code>constraint</code></p> | Mandatory | Description                                                                              |
| ------------------------------------- | -------------------------------------- | :-------: | ---------------------------------------------------------------------------------------- |
| <p>Type<br><code>type</code></p>      | object                                 |     ✅     | <p>Type of<br>Values: <code>TOOLS</code> <code>RESOURCES</code> <code>PROMPTS</code></p> |

### &#x20;**:** **Tools `type = "TOOLS"`**

| <p>Name<br><code>json name</code></p>                | <p>Type<br><code>constraint</code></p>              | Mandatory | Default        | Description                          |
| ---------------------------------------------------- | --------------------------------------------------- | :-------: | -------------- | ------------------------------------ |
| <p>Tool methods<br><code>methods</code></p>          | <p>array (enum (string))<br><code>unique</code></p> |     ✅     | `[TOOLS_LIST]` |                                      |
| <p>Name Pattern Type<br><code>patternType</code></p> | enum (string)                                       |           | `ANY`          | Values: `ANY` `LITERAL` `EXPRESSION` |

### **: Resources `type = "RESOURCES"`**

| <p>Name<br><code>json name</code></p>                | <p>Type<br><code>constraint</code></p>              | Mandatory | Default            | Description                          |
| ---------------------------------------------------- | --------------------------------------------------- | :-------: | ------------------ | ------------------------------------ |
| <p>Resource methods<br><code>methods</code></p>      | <p>array (enum (string))<br><code>unique</code></p> |     ✅     | `[RESOURCES_LIST]` |                                      |
| <p>Name Pattern Type<br><code>patternType</code></p> | enum (string)                                       |           | `ANY`              | Values: `ANY` `LITERAL` `EXPRESSION` |

### **: Prompts `type = "PROMPTS"`**

| <p>Name<br><code>json name</code></p>                | <p>Type<br><code>constraint</code></p>              | Mandatory | Default          | Description                          |
| ---------------------------------------------------- | --------------------------------------------------- | :-------: | ---------------- | ------------------------------------ |
| <p>Prompt methods<br><code>methods</code></p>        | <p>array (enum (string))<br><code>unique</code></p> |     ✅     | `[PROMPTS_LIST]` |                                      |
| <p>Name Pattern Type<br><code>patternType</code></p> | enum (string)                                       |           | `ANY`            | Values: `ANY` `LITERAL` `EXPRESSION` |

## Examples

_Configure the MCP ACL policy to allow only the `get_weather` tool to be listed and called_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "MCP_PROXY",
    "name": "MCP ACL example API",
    "flows": [
      {
        "name": "All plans flow",
        "enabled": true,
        "selectors": [
          {
            "type": "MCP",
             "methods" : []
          }
        ],
        "request": [
          {
            "name": "MCP ACL",
            "enabled": true,
            "policy": "mcp-acl",
            "configuration":
              {
                  "authorizations": [
                      {
                          "authorizedFeatures": [
                              {
                                  "type": "TOOLS",
                                  "methods": ["TOOLS_LIST", "TOOLS_CALL"],
                                  "patternType": "LITERAL",
                                  "patternValue": "get_weather"
                              }
                          ]
                      }
                  ]
              }
          }
        ]
      }
    ]
  }
}

```

### Changelog

[**1.0.2**](https://github.com/gravitee-io/gravitee-policy-mcp-acl/compare/1.0.1...1.0.2) **(2025-12-17)**

**Bug Fixes**

* ignore events without data ([95334cd](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/95334cde5172d6bd136048e12a37459ce5fa051c))

[**1.0.1**](https://github.com/gravitee-io/gravitee-policy-mcp-acl/compare/1.0.0...1.0.1) **(2025-12-15)**

**Bug Fixes**

* clean pom.xml ([82c96bb](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/82c96bbabee9470e21ea6c2fb39c1f89cfe3604e))

#### 1.0.0 (2025-12-11)

**Bug Fixes**

* allow special characters in patternValue ([d9a7259](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/d9a72592f04a203a080a6ca5da0baf1df25fb5e8))
* bump apim to fix addActionOnResponse ([315ed38](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/315ed381037e6e1eaf689e02d9b84a97e62893d4))
* can only be used on request phase ([52cceb5](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/52cceb530d6432fcfc0751bc34b0a8d8618a4cc4))
* force common-mcp version to make artifactory release work ([29ec5e5](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/29ec5e5cbb66794a192b4a0d4044ea827ac7ce67))
* ignore event without message event type ([ee3d7d1](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/ee3d7d18c4345aed286a42765e5ff76cb8f958df))
* import for common.mcp ([82b7760](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/82b776037200db2988a585b93cac80deda3f9550))
* update CONTENT\_LENGTH when policy modify response json ([9c62a6e](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/9c62a6ea14a28c43eeb93df1dfac1f3a3fc2b44d))
* use right method enum value ([8aa90ca](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/8aa90ca17fae1a454de0af692f0ccb0d79a495ee))

**Features**

* add ActionFilter to filter authorized MCP actions ([44a448f](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/44a448fdd9010b2fb93339f2912c5cb30e15cf05))
* add feature key in plugin.properties ([0855fb2](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/0855fb23be7fa4a1fac992e062ab03da65062b06))
* complete policy documentation with docgen ([3e39b07](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/3e39b07c2d721ee7ce06476880e7524e9e4485f9))
* handle event-stream and non event response ([d5437d6](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/d5437d6f7205e4c24b40cd95f6ce817327b909d5))
* impl ACL for PROMPTS\_GET MCP Method ([335622c](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/335622c38fcb1a3144554fc53b2d150e20bcd923))
* impl ACL for PROMPTS\_LIST MCP Method ([77678e1](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/77678e1a1c655e9330a174754b9992fb4608de70))
* impl ACL for RESOURCES\_LIST MCP Method ([3add58b](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/3add58b03b8b1659ab636a5b44db57eeb456219c))
* impl ACL for RESOURCES\_READ MCP Method ([377f37e](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/377f37ecec1ee4e77672b50f5315000a780c02d4))
* impl ACL for RESOURCES\_SUBSCRIBE MCP Method ([8ce04fa](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/8ce04fafb7fe896b4c161c265b10a4aa5cf0fbca))
* impl ACL for RESOURCES\_TEMPLATES\_LIST MCP Method ([32ca595](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/32ca5951f1f14bf20431fd71069491f582f2515d))
* impl ACL for ToolsCall MCP Method ([612b131](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/612b13110aed06eb025e984babcb03a6bfd324de))
* impl ToolsListStrategy to validate ACL ([798f984](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/798f984ceed10015f929257479ca151793fa94a2))

#### [1.0.0-alpha.8](https://github.com/gravitee-io/gravitee-policy-mcp-acl/compare/1.0.0-alpha.7...1.0.0-alpha.8) (2025-12-10)

**Bug Fixes**

* update CONTENT\_LENGTH when policy modify response json ([69864d0](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/69864d089f38a1662bcea40f57f8dd6799d4eb3a))

#### [1.0.0-alpha.7](https://github.com/gravitee-io/gravitee-policy-mcp-acl/compare/1.0.0-alpha.6...1.0.0-alpha.7) (2025-12-09)

**Features**

* add feature key in plugin.properties ([6cbb99e](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/6cbb99e4a45a37f561347a94ef127ec2ad5eb1c8))

#### [1.0.0-alpha.6](https://github.com/gravitee-io/gravitee-policy-mcp-acl/compare/1.0.0-alpha.5...1.0.0-alpha.6) (2025-12-08)

**Bug Fixes**

* bump apim to fix addActionOnResponse ([200c3fa](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/200c3fa285ea00921b33e1170e545c99829c10c0))
* ignore event without message event type ([6eb2617](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/6eb2617fd19781ce44119e59319eff9f51ef16ee))

#### [1.0.0-alpha.5](https://github.com/gravitee-io/gravitee-policy-mcp-acl/compare/1.0.0-alpha.4...1.0.0-alpha.5) (2025-12-04)

**Bug Fixes**

* force common-mcp version to make artifactory release work ([f6de3c9](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/f6de3c9cf0f817a935890e58999934ae4d338b8e))

#### [1.0.0-alpha.4](https://github.com/gravitee-io/gravitee-policy-mcp-acl/compare/1.0.0-alpha.3...1.0.0-alpha.4) (2025-12-04)

**Bug Fixes**

* import for common.mcp ([7d1c9a3](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/7d1c9a39a4e709a98be2ac1212f2fdba19d789b6))

#### [1.0.0-alpha.3](https://github.com/gravitee-io/gravitee-policy-mcp-acl/compare/1.0.0-alpha.2...1.0.0-alpha.3) (2025-12-04)

**Bug Fixes**

* allow special characters in patternValue ([13a4c3c](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/13a4c3c0a665469592aa1bae9ba9f17551392000))

**Features**

* complete policy documentation with docgen ([853ba3b](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/853ba3b1f519b768f39cb9fd091164a7ed03a413))
* handle event-stream and non event response ([46c90c3](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/46c90c302374995b0604e60d4c9b7e4e49718a47))
* impl ACL for PROMPTS\_GET MCP Method ([e64ebe8](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/e64ebe8156f88ecefb74ea88990a85933aec6cff))
* impl ACL for PROMPTS\_LIST MCP Method ([f2f23f1](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/f2f23f1a2b4f9640c4eb3df1ff82bcac71859549))
* impl ACL for RESOURCES\_LIST MCP Method ([e17cce8](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/e17cce84ee3fd2eac7bc2f09fa41aacf379d4374))
* impl ACL for RESOURCES\_READ MCP Method ([94f400d](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/94f400d71c7c0f1fb05ea8b5957f440599a9a088))
* impl ACL for RESOURCES\_SUBSCRIBE MCP Method ([9e06ac3](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/9e06ac3db59ccf2995102b900242e3274f3b747d))
* impl ACL for RESOURCES\_TEMPLATES\_LIST MCP Method ([f55ce44](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/f55ce445e20fc8e7bb7583042f51869155ff7a4c))
* impl ACL for ToolsCall MCP Method ([6c36839](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/6c3683980ede66aa0d2adf5a50d990d56abc5511))

#### [1.0.0-alpha.2](https://github.com/gravitee-io/gravitee-policy-mcp-acl/compare/1.0.0-alpha.1...1.0.0-alpha.2) (2025-11-28)

**Features**

* impl ToolsListStrategy to validate ACL ([bb0e761](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/bb0e76150d43952ab6cdcbe6a107e57930be1b97))

#### 1.0.0-alpha.1 (2025-11-19)

**Bug Fixes**

* can only be used on request phase ([5a6d4dc](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/5a6d4dce5c1a41910abbd483e3721f1d2a4d8c5d))
* use right method enum value ([268a7ae](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/268a7aeb66484a4d201036f2723bbc0a6e359f80))

**Features**

* add ActionFilter to filter authorized MCP actions ([d61f460](https://github.com/gravitee-io/gravitee-policy-mcp-acl/commit/d61f4604507c1fd9f4738717cccfdfe6965d1820))
