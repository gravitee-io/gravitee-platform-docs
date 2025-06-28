---
hidden: true
---

# Assign Metrics

## Phases <a href="#user-content-phases" id="user-content-phases"></a>

### V3 engine <a href="#user-content-v3-engine" id="user-content-v3-engine"></a>

| onRequest | onResponse | onRequestContent | onResponseContent |
| --------- | ---------- | ---------------- | ----------------- |
| X         | X          | X                | X                 |

### V4 engine <a href="#user-content-v4-engine" id="user-content-v4-engine"></a>

| onRequest | onResponse | onMessageRequest | onMessageResponse |
| --------- | ---------- | ---------------- | ----------------- |
| X         | X          | X                | X                 |

## Description <a href="#user-content-description" id="user-content-description"></a>

You can use the `assign-metrics` policy to push extra metrics in addition to the natively provided request metrics.

These metrics can then be used from analytics dashboards to create custom widgets and, optionally, apply aggregations based on their value.

| Plugin version | APIM version  |
| -------------- | ------------- |
| 1.x            | Up to 3.17    |
| 2.x            | 3.18 to 3.20  |
| 3.x            | 4.0 to latest |

## Policy identifier <a href="#user-content-policy-identifier" id="user-content-policy-identifier"></a>

You can enable or disable the policy with policy identifier `policy-assign-metrics`.

## Example <a href="#user-content-example" id="user-content-example"></a>

### On a Request header <a href="#user-content-on-a-request-header" id="user-content-on-a-request-header"></a>

To display your request distribution based on a particular HTTP header in your dashboards, create the custom metric shown below.

```
"assign-metrics": {
    "metrics": [
        {
            "name": "myCustomHeader,
            "value": "{#request.headers['X-MyCustomHeader'] != null ? #request.headers['X-MyCustomHeader'][0] : null}"
        }
    ]
}
```
