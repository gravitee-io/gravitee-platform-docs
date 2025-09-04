---
hidden: true
noIndex: true
---

# Visualize your services' API

You can visualize and explore your service’s OpenAPI specification documentation from within Ambassador Cloud.

### Prerequisites

1. You must have **Edge Stack or Emissary-ingress version 2.0+ Developer Preview** [installed and connected to Ambassador Cloud](quick-start.md) in your Kubernetes cluster. This guide assumes you have deployed the `quote` application and resources from the [Service Catalog quick start](quick-start.md).
2. Enable reporting the `quote` service documentation by creating, or editing, the `quote-backend` Ambassador Mapping resource with the following docs path `/.ambassador-internal/openapi-docs`

{% hint style="warning" %}
In the below example, the hostname is wildcard but you should specify your own hostname, otherwise you will need to enter it manually in the Ambassador Cloud Dev Portal when you will want to try out your APIs directly in the UI.
{% endhint %}

```bash
kubectl apply -f - <<EOF
---
apiVersion: getambassador.io/v3alpha1
kind: Mapping
metadata:
  name: quote-backend
spec:
  hostname: "*"
  prefix: /backend/
  service: quote
  docs:
    path: "/.ambassador-internal/openapi-docs"
...
EOF
```

### Visualize the API Documentation

1. Navigate to [Ambassador Cloud](https://app.getambassador.io/cloud/services) to see your connected services.
2. Select the quote service from the Service Catalog page.
3. Click on the API tab to access the rendered OpenAPI documentation.
4. You can also see all your API documentation by clicking on the **Dev Portal** button in the side bar, documented [here](ambassador-cloud-developer-portal-overview.md).

### &#x20;What's next?

You've published your service documentation on Ambassador Cloud to enable collaboration with other teams and members of your organization, but you can extend your services AmbassadorMapping with [other Developer Portal docs options](technical-reference/api/developer-portal.md), and **Service Catalog annotations!** See the full list of service annotations [here](annotations-overview.md).
