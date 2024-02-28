---
description: >-
  This page focuses on improvements to Gravitee EL error handling, parsing, and
  definitions
---

# Expression Language

## EL condition evaluation

### Legacy execution engine behavior

The Gateway returns a `500` error with an obscure message when the legacy execution engine fails to evaluate a valid Gravitee Expression Language (EL) expression because it is trying to access missing data.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-1.png" alt=""><figcaption><p>Sample EL condition evaluation error with legacy engine</p></figcaption></figure>

### Reactive execution engine improvements

The reactive execution engine executes a policy (or flow) when a valid EL expression evaluates as `true`. Otherwise, the policy is skipped because the EL expression evaluates as `false`.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-2.png" alt=""><figcaption><p>Sample EL condition skipping behavior with reactive engine</p></figcaption></figure>

The reactive execution engine ensures EL expressions that attempt to access missing data are evaluated as `false`. For example, `{#request.headers['X-Test'][0] == 'something'}` will skip execution even if the request header `X-Test` is not specified.

The execution will fail and throw an error if the provided EL expression cannot be parsed, e.g., if it is syntactically invalid. The error message details why the EL expression cannot be parsed.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-3.png" alt=""><figcaption><p>Sample EL condition error with reactive engine</p></figcaption></figure>

## EL expression parsing

### Legacy execution engine behavior

The legacy execution engine parses an EL expression each time it is evaluated.

### Reactive execution engine improvements

The reactive execution engine employs a new caching mechanism that allows the Gateway to cache the parsed EL expression for reuse, thereby improving performance.

## EL body expressions

### Legacy execution engine behavior

The legacy execution engine limits use of EL expressions such as `{#request.content == 'something'}` to policies working at the `REQUEST_CONTENT` or `RESPONSE_CONTENT` phases (e.g., Assign Metrics, Assign Content, Request Validation, etc.).

However, defining a policy or a flow condition based on the request or response body is not supported.

### Reactive execution engine improvements

Using the reactive execution engine, it is possible to define a condition based on the request or response body. For example, you can create a condition such as `{#request.content == 'something'}`.

Depending on the expected content type, it is also possible to define a condition based on JSON such as `{#request.jsonContent.foo.bar == 'something'}` where the request body looks like this:

```json
{
  "foo": {
      "bar": "something"
  }
}
```

The same applies to XML content using `{#request.xmlContent.foo.bar == 'something'}`:

```xml
<foo>
  <bar>something</bar>
</foo>
```

### Migration considerations

Use this feature with caution. EL body-based expressions are resource-heavy and should be avoided when performance is a concern. Working with request or response content can significantly degrade performance and consumes substantially more memory on the Gateway.
