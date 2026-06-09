---
metaLinks:
  alternates:
    - https://app.gitbook.com/s/H4VhZJXn1S232OEmh8Wv/guides/identity-providers
---

# Identity Providers

An _identity provider_ is a service used to authenticate and communicate authorization and user information. AM comes with a set of default identity provider types, including social providers such as Facebook, Google, or Twitter, and enterprise providers such as Active Directory or database providers. You can also create your own custom providers.

Identity providers can be created and managed through the Access Management console or programmatically using the Automation API. The Automation API provides a machine-oriented HTTP interface for managing identity providers at the path `/organizations/{orgId}/environments/{envId}/domains/{domainKey}/identities`. System identity providers can be configured using the `domains.identities.default.*` settings in `gravitee.yml` and managed through the Automation API by setting `system: true` in the request body.
