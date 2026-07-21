---
hidden: false
noIndex: false
---

# AuthZEN PDP synchronization

Gamma Authorization Management features a native, multi-tenant Policy Decision Point (PDP) that conforms to the AuthZEN standard. This allows your Gamma environment to synchronize authorization policies down to the API Gateway, enabling localized, high-performance evaluation of authorization requests.

## How it works

When you deploy authorization policies in the Gamma console, the control plane compiles those rules into an AuthZEN-compatible representation. The Gateway continuously synchronizes this state.

During runtime, when an API proxy or MCP proxy receives a request:
1. The proxy triggers an authorization check against the localized AuthZEN PDP.
2. The PDP evaluates the principal, action, and resource against the synchronized policies.
3. The PDP returns a standard permit or deny decision.

By evaluating authorization rules locally at the Gateway (the Policy Enforcement Point), Gamma avoids the latency of calling back to the central console for every request.

## Multi-tenant isolation

Gamma's AuthZEN PDP is fully multi-tenant. If you run multiple environments or tenants on the same Gateway, the PDP strongly isolates the policies and authorization data, ensuring that decisions are always scoped strictly to the calling tenant.

<!-- Source: AimResourceIntegrationTest.java — gravitee-gamma-module-aim -->
