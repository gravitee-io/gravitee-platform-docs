---
hidden: false
noIndex: false
---

# Manage resources
<!-- GAP-STRUCTURAL: Missing procedural content source -->

Resources are shared, reusable components that API proxies reference at runtime. Common examples include OAuth2 token validation endpoints, cache stores, and authentication providers.

{% hint style="warning" %}
The Resources tab is marked **Coming soon** in the current build. No resource management UI is available yet. This page documents the planned capability. Source: `ApiDetailSidebarNav.tsx:L79` — `comingSoon: true`.
{% endhint %}

## Resource types
Gamma supports all existing APIM resource types. It inherits the API Management resource model rather than introducing a separate resource system. Available resources include: Cache, OAuth2 (Generic, Gravitee AM), Authentication Provider, Confluent Schema Registry, and Keycloak adapter.

## Create a resource
Resource creation forms use the same field definitions as the classic APIM Console.

1. From the Gamma console sidebar, select **API Management**.
2. Navigate to **Resources**.
3. Select **Create Resource**.
4. Choose a resource type and configure its fields.
5. Save the resource.

## Use a resource in an API proxy

{% hint style="warning" %}
**Not implemented**: Shared resource binding (as known in APIM) is not yet implemented in Gamma 4.12. API Proxies cannot currently be bound to these resources via the UI.
{% endhint %}

Resources are referenced by name in security plans and policies. For example, an OAuth2 plan references an OAuth2 resource for token introspection.

## Next steps

* [Secure your API proxy](../api-management/build/secure-your-api-proxy.md) — Attach security plans that reference OAuth2 or other authentication resources.
