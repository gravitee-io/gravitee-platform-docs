---
description: API Management 4.10 can sanitize published API documentation pages. Learn what the sanitizer removes and why that matters.
metaLinks:
  alternates:
    - documentation-sanitizer.md
---

# Documentation Sanitizer

Gravitee offers the capability to attach and expose API documentation. Once published, these pages can be accessible to API consumers to discover and understand the purpose of an API. **We recommend enabling the sanitization of the documentation pages** to avoid any script injection that could have an impact on the API consumer when the page is published on the Developer Portal.

```yaml
documentation:
  markdown:
    sanitize: true
```
