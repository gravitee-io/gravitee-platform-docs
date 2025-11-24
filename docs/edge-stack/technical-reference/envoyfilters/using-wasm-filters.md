---
description: Step-by-step tutorial for Using Wasm Filters.
noIndex: true
---

# Using Wasm Filters

The WebAssembly (Wasm) filter type implements Envoy's [Wasm filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/wasm_filter), and it can be used to apply an HTTP filter with a Wasm plugin. The Wasm filter is used in conjunction with the [EnvoyFilter](../../crd-api-references/getambassador.io-v3alpha1/the-envoy-filter-type.md) and [EnvoyFilterPolicy](../../crd-api-references/getambassador.io-v3alpha1/envoyfilterpolicy.md) custom resources to introduce additional processing for incoming or outgoing traffic while maintaining the flow of requests. This allows you to implement highly specific, custom logic.

## The EnvoyFilterPolicy Resource

Similar to the `FilterPolicy` resource, you can use the `EnvoyFilterPolicy` resource to determine how to apply Envoy filters to HTTP requests.

For example:

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: EnvoyFilterPolicy
metadata:
  name: "example-wasm-filter-policy"
  namespace: "example-namespace"
spec:
  rules:
  - precedence: 1                        # optional
    envoyFilters:                        # required
    - name: "example-envoy-filter"       # required
      namespace: "example-namespace"     # required
```

> **Note:** For information on all supported fields, see [EnvoyFilterPolicy](../../crd-api-references/getambassador.io-v3alpha1/envoyfilterpolicy.md).

## The Wasm Resource

To use the Wasm filter type, you must mount a `.wasm` file to Ambassador Edge Stack's pod by creating a `configMap` with the `--from-file` flag and then referencing that `configMap` from Ambassador Edge Stack's deployment spec.

First, create the `configMap` that references your Wasm filter.

```shell
kubectl create configmap -n ambassador example-envoy-filter-config --from-file=example-wasm-filter.wasm
```

Second, edit the deployment to add a `volumeMount` that references the `configmap`.

```yaml
  volumeMounts:
  - name: wasmFilterVolumeMount
    mounthPath: /etc/envoy/example-wasm-filter.wasm
    subPath: example-wasm-filter.wasm
volumes:
  - name: wasmFilterVolume
    configMap:
      name: example-envoy-filter-config
      items:
        - key: example-envoy-filter-config
          path: example-envoy-filter-config
```

Finally, configure the `EnvoyFilter` to reference the `Wasm` filter that you mounted.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: EnvoyFilter
metadata:
  name: "example-wasm-filter"
  namespace: "example-namespace"
spec:
  filterType: "wasm"
  wasm:
    filePath: /etc/envoy/example-wasm-filter.wasm
    rootID: "my_root_id"
    runtime: "envoy.wasm.runtime.v8"
    vmID: "my_vm_id"
```
