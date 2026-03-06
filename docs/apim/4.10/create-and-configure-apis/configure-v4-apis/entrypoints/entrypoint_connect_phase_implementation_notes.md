### Related Changes

{% hint style="info" %}
This section documents internal implementation details for the Entrypoint Connect phase. This content is intended for release notes or internal implementation documentation and is out of scope for user-facing feature documentation.
{% endhint %}

The UI policy studio now displays the Entrypoint Connect phase before the Interact phase, reflecting the actual execution order. The phase is labeled "Entrypoint Connect phase" in the policy catalog and flow designer.

Backend APIs and database schemas have been updated to store `entrypointConnect` flow steps alongside `interact`, `publish`, and `subscribe` steps. The OpenAPI schema for Native APIs includes the `entrypointConnect` array field.

UI libraries have been updated to version 17.6.1 to support the new phase:

* `@gravitee/ui-policy-studio-angular`
* `@gravitee/ui-particles-angular`
