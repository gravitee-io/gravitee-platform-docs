---
description: Overview of ApiResource.
---

# ApiResource

Resources are objects that allow you to define pointers to external resources, such as authentication providers and caches, that can then be referenced from an API definition's policies. Learn more about Gravitee resources in the [APIM user guide](https://documentation.gravitee.io/apim/guides/api-configuration/resources#resource-descriptions).

## Create a reusable API resource

You can use GKO to create API resources, such as caches or authentication providers, that can be reused in other APIs. Updates to a shared resource are automatically propagated to all APIs that reference that resource.

Below is an example of an `ApiResource` cache resource:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiResource
metadata:
  name: reusable-resource-cache
  namespace: gravitee
spec:
  name: "cache-resource"
  type: "cache"
  enabled: true
  configuration:
      timeToIdleSeconds: 0
      timeToLiveSeconds: 0
      maxEntriesLocalHeap: 1000
```

The following example shows a Redis cache resource:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiResource
metadata:
  name: reusable-resource-cache-redis
  namespace: gravitee
spec:
  name: "redis-cache"
  type: "cache-redis"
  enabled: true
  configuration:
      releaseCache: false
      maxTotal: 8
      timeToLiveSeconds: 0
      timeout: 2000
      useSsl: true
      standalone:
          enabled: true
          host: "redis-cache.default.svc.cluster.local"
          port: 6379
      sentinel:
          enabled: false
          masterId: "sentinel-master"
      password: "change_me!"
```

## Referencing API resources in your API definitions

Once an API resource has been created, it can be referenced in one or more API definitions. The example below shows how to use the `reusable-resource-cache-redis` resource in an API definition via references to the resource name and namespace:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: reusable-resource-example
  namespace: gravitee
spec:
  name: "Reusable Resource Example"
  version: "1.0"
  description: "A simple API reusing a redis cache resource"
  proxy:
    virtual_hosts:
      - path: "/cached-with-redis"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
  resources:
    - ref:
        name: reusable-resource-cache-redis
        namespace: gravitee
  flows:
  - name: ""
    path-operator:
      path: "/"
      operator: "STARTS_WITH"
    condition: ""
    consumers: []
    methods: []
    pre:
    - name: "Cache"
      description: "Cache with Redis"
      enabled: true
      policy: "cache"
      configuration:
        timeToLiveSeconds: 600
        cacheName: "redis-cache"
        methods:
        - "GET"
        - "OPTIONS"
        - "HEAD"
        scope: "API"
        key: "cache-key"
    post: []
    enabled: true
```

Resources can also be defined inline in API definitions. The following API reuses the `reusable-resource-cache-redis` resource defined above and defines an in-memory authentication provider resource inline:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: reusable-resource-example
  namespace: gravitee
spec:
  name: "Reusable Resource Example"
  version: "1.0"
  description: "A simple API reusing a redis cache resource with an inlined authentication provider"
  proxy:
    virtual_hosts:
      - path: "/cached-with-redis"
    groups:
      - endpoints:
          - name: "Default"
            target: "https://api.gravitee.io/echo"
  resources:
    - ref:
        name: reusable-resource-cache-redis
        namespace: gravitee
    - name: "inline-auth"
      type: "auth-provider-inline-resource"
      enabled: true
      configuration:
          users:
            - username: "user"
              password: "password"
  # ...

```

{% hint style="info" %}
If a resource defined inline contains a reference to a reusable resource (via the `ref` property), the reusable resource will take precedence over the inline configuration.
{% endhint %}
