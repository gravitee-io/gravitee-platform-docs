---
title: Examples Table
---

{% tabs %}
{% tab title="V4 API definition" %}
This snippet of a V4 API definition includes a flow that uses the JSON-to-JSON Transform policy (in the response phase) to rename the '\_id' to 'userId' key and remove the '\_\_v' field.

<pre class="language-json"><code class="lang-json">{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "JSON Transformation Example v4 API",
<strong>    "flows" : [ {
</strong>          "name" : "JSON Transformation",
          "enabled" : true,
          "selectors" : [ {
            "type" : "HTTP",
            "path" : "/",
            "pathOperator" : "STARTS_WITH"
          } ],
          "request" : [],
          "response" : [ {
            "name" : "JSON to JSON Transformation",
            "description": "Rename '_id' to 'userId', and remove '__v' field.",
            "enabled" : true,
            "policy" : "json-to-json",
            "configuration" : {
                "overrideContentType": true,
                "scope": "REQUEST",
                "specification": "[\n  {\n    \"operation\": \"shift\",\n    \"spec\": {\n      \"_id\": \"userId\",\n      \"*\": {\n        \"$\": \"&#x26;1\"\n      }\n    }\n  },\n  {\n    \"operation\": \"remove\",\n    \"spec\": {\n      \"__v\": \"\"\n    }\n  }\n]"
            }
          } ],
          "subscribe": [],
          "publish": []
  ...
  } ],
  ...
}
</code></pre>
{% endtab %}

{% tab title="V4 API CRD" %}
This snippet of a V4 API yaml manifest (for the Gravitee Kubernetes Operator) includes a flow that uses the JSON-to-JSON Transform policy (in the response phase) to rename the '\_id' to 'userId' key and remove the '\_\_v' field.

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "json-transformation-example-v4-gko-api"
spec:
  name: "JSON Transformation Example V4 GKO API"
  flows:
    name: "Common Flow"
    enabled: true
    selectors:
    - type: "HTTP"
      path: "/"
      pathOperator: "STARTS_WITH"
    response:
    - name: "JSON to JSON Transformation"
      enabled: true
      policy: "json-to-json"
      configuration:
        overrideContentType: true
        specification: "[\n  {\n    \"operation\": \"shift\",\n    \"spec\": {\n      \"_id\": \"userId\",\n      \"*\": {\n        \"$\": \"&1\"\n      }\n    }\n  },\n  {\n    \"operation\": \"remove\",\n    \"spec\": {\n      \"__v\": \"\"\n    }\n  }\n]"      
    ...
```
{% endtab %}
{% endtabs %}
