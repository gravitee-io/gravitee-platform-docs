---
description: >-
  This page focuses on improvements to Gravitee EL error handling, parsing, and
  definitions
---

# Expression Language

## EL condition evaluation

### Legacy execution engine behavior

With the legacy execution engine, the Gateway returns a `500` error with an obscure message when the Gateway provides a valid Gravitee Expression Language (EL) expression that fails to be evaluated because it is trying to access missing data.

For example:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-1.png" alt=""><figcaption><p>Sample EL condition evaluation error with legacy engine</p></figcaption></figure>

### Reactive execution engine improvements

With the reactive execution engine, the policy (or flow) is executed when a valid EL expression is evaluated as `true`. Otherwise, it is skipped.

A policy is skipped when:

* The EL expression is evaluated as `false`.
* The EL expression evaluation fails because the expected data tested is missing.

This is shown in the example below:

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-2.png" alt=""><figcaption><p>Sample EL condition skipping behavior with reactive engine</p></figcaption></figure>

Mastering EL expressions can be challenging. The new mode eases the learning curve by ensuring EL expressions that attempt to access missing data are evaluated as `false` instead of returning an obscure error. For example, `{#request.headers['X-Test'][0] == 'something'}` will skip execution even if the request header `X-Test` is not specified.

However, the execution will fail and throw an error if the provided EL expression cannot be parsed (for example, if it is syntactically invalid). The error message details why the EL expression cannot be parsed.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-condition-evaluation-3.png" alt=""><figcaption><p>Sample EL condition error with reactive engine</p></figcaption></figure>

## EL expression parsing

### Legacy execution engine behavior

With the legacy execution engine, an EL expression is parsed each time it is evaluated.

### Reactive execution engine improvements

With the reactive execution engine, a new caching mechanism allows the Gateway to cache the parsed EL expression for reuse and thereby improve performance.

## EL body expressions

### Legacy execution engine behavior

With the legacy execution engine, using an EL expression such as `{#request.content == 'something'}` is limited to policies working at `REQUEST_CONTENT` or `RESPONSE_CONTENT` phases (e.g. Assign Metrics, Assign Content, Request Validation, etc.).

However, defining a policy or a flow condition based on the request or response body is not supported.

### Reactive execution engine improvements

With the reactive execution engine, it is possible to define a condition based on the request or response body. For example, you can create a condition such as `{#request.content == 'something'}`.

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

Use this feature with caution - an EL body-based expression is resource heavy and should be avoided when performance is a concern. Working with request or response content can significantly degrade performance and consumes substantially more memory on the Gateway.
