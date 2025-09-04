---
noIndex: true
---

# The Envoy Filter Type

## The Envoy Filter Type (v3alpha1)

The `EnvoyFilter` custom resource works in conjunction with the [EnvoyFilterPolicy](envoyfilterpolicy.md) custom resource to define when and how Ambassador Edge Stack modifies or intercepts incoming and outgoing traffic, similar to the `Filter` resource. `EnvoyFilter` applies certain [Envoy HTTP filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/http_filters) configurations, and you can use it to configure a WebAssembly (Wasm) filter to implement custom logic for your specific needs.

This document provides an overview of all the fields on the `EnvoyFilter` custom resource, including their purpose, type, and default values. This page is specific to the `getambassador.io/v3alpha1` version of the `EnvoyFilter` resource.

### Envoy Filter API Reference

To create an Envoy Filter, the `spec.type` must be set to `EnvoyFilter`, and the `EnvoyFilter` field must contain the configuration for your Envoy filter.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: EnvoyFilter
metadata:
  name: "example-envoy-filter"
  namespace: "example-namespace"
spec:
  ambassador_id: []string
  filterType:  Enum             # required, "wasm"
  wasm: WasmFilter              # required
    filePath: string            # required
    failureModeAllow: bool      # optional
    allowPrecompiledWASM: bool  # optional
    customConfig: string        # optional
    rootID: string              # required
    vmID: string                # required
    runtime: Enum               # required, "envoy.wasm.runtime.v8", "envoy.wasm.runtime.wavm"
```

#### EnvoyFilter

| **Field**    | **Type**     | **Description**                                    |
| ------------ | ------------ | -------------------------------------------------- |
| `filterType` | `Enum`       | Specifies the filter type.                         |
| `wasm`       | `WasmFilter` | Contains the configuration for a Wasm filter type. |

#### WasmFilter

**Appears On**: \[EnvoyFilter]\[]

| **Field**              | **Type** | **Description**                                                                                                                                                        |
| ---------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `filePath`             | `string` | Defines the path to a `.wasm` file on the Edge Stack pod filesystem.                                                                                                   |
| `failureModeAllow`     | `bool`   | When set to `true`, allows requests in the event of a fatal error when running the Wasm filter.                                                                        |
| `allowPrecompiledWASM` | `bool`   | Determines whether or not to allow precompiled Wasm files.                                                                                                             |
| `customConfig`         | `string` | (Optional) Passes custom context or configurations to the Wasm filter.                                                                                                 |
| `rootID`               | `string` | Sets the `root_id` of the virtual machine created for the Wasm filter. The field can't be empty and can only include alphanumeric characters, hyphens, or underscores. |
| `vmID`                 | `string` | Sets the `vm_id` of the virtual machine created for the Wasm filter. The field can't be empty and can only include alphanumeric characters, hyphens, or underscores.   |
| `runtime`              | `Enum`   | Specifies which of the supported Wasm runtimes to use. The runtime is constrained to known supported runtimes.                                                         |
