# ApiResource CRD

## Creating a reusable API resource

You can use the GKO to create reusable [API resources](../../api-configuration/resources.md) by applying the [ApiResource CRD](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/docs/api/reference.md#apidefinitionspecresourcesindex). This allows you to define resources (cache or authentication providers, etc.) a single time and maintain them in a single place, then reuse these resources in multiple APIs. Subsequent updates to a resource will be automatically propagated to all APIs that reference that resource.

The example below shows a [Redis cache resource](../../api-configuration/resources.md#cache-redis) that can be applied using the `ApiResource` CRD:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiResource
metadata:
  name: reusable-resource-cache-redis
  namespace: default
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
  namespace: default
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
        namespace: default
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

Resources can also be defined inline in API definitions. The following API reuses the `reusable-resource-cache-redis` resource defined above and defines an in-memory authentication provider inline:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: reusable-resource-example
  namespace: default
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
        namespace: default
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
If a resource defined inline contains a reference to a reusable resource (using the `ref` property), the reusable resource will take precedence over the inline configuration.
{% endhint %}
