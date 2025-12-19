---
title: Examples Table
---

{% tabs %}
{% tab title="V4 API definition" %}
This snippet of a V4 API definition includes a flow that contains a Data Masking policy.

<pre class="language-json"><code class="lang-json">{
  "api": {
    "name": "Data Masking v4 API",
<strong>    "flows" : [ {
</strong>          "id" : "e8d01c12-7fc8-4d57-901c-127fc8bd5766",
          "name" : "Data-masking",
          "enabled" : true,
          "selectors" : [ {
            "type" : "HTTP",
            "path" : "/get",
            "pathOperator" : "EQUALS",
            "methods" : [ ]
          } ],
          "request" : [ {
            "name" : "Data Logging Masking",
            "enabled" : true,
            "policy" : "policy-data-logging-masking",
            "configuration" : {
              "headerRules" : [ {
                "path" : "reqHeaderToHide",
                "replacer" : "*"
              } ],
              "scope" : "REQUEST_CONTENT",
              "bodyRules" : [ ]
            }
          } ],
          "response" : [ {
            "name" : "Data Logging Masking",
            "enabled" : true,
            "policy" : "policy-data-logging-masking",
            "configuration" : {
              "headerRules" : [ {
                "path" : "reqHeaderToHide",
                "replacer" : "*"
              } ],
              "scope" : "RESPONSE_CONTENT",
              "bodyRules" : [ ]
            }
          } ],
  ...
  }
  ...
}
</code></pre>
{% endtab %}

{% tab title="V4 API CRD" %}
This snippet of a V4 API yaml manifest for the Gravitee Kubernetes Operator includes a flow that contains a Data Masking policy.

```yaml
apiVersion: "gravitee.io/v1alpha1"
kind: "ApiV4Definition"
metadata:
  name: "data-masking-v4-gko-api"
spec:
  name: "Data Masked V4 GKO API"
  flows:
    - id: "e8d01c12-7fc8-4d57-901c-127fc8bd5766"
    name: "Data-masking"
    enabled: true
    selectors:
    - type: "HTTP"
      path: "/get"
      pathOperator: "EQUALS"
    request:
    - name: "Data Logging Masking"
      enabled: true
      policy: "policy-data-logging-masking"
      configuration:
        headerRules:
        - path: "reqHeaderToHide"
          replacer: "*"
        scope: "REQUEST_CONTENT"
        bodyRules: []
    response:
    - name: "Data Logging Masking"
      enabled: true
      policy: "policy-data-logging-masking"
      configuration:
        headerRules:
        - path: "reqHeaderToHide"
          replacer: "*"
        scope: "RESPONSE_CONTENT"
        bodyRules: []        
    ...
```
{% endtab %}
{% endtabs %}
