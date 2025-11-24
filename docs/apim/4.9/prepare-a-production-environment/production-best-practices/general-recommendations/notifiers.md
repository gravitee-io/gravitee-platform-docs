---
description: Documentation about notifiers in the context of APIs.
---

# Notifiers

By default, APIM allows an API publisher to send notifications related to its APIs. This includes sending notifications over HTTP, which can be useful for automation. However, we recommend disabling this feature if you don't expect to use it:

```yaml
notifiers:
  email:
    enabled: false
  webhook:
    enabled: false
```

Alternatively, if you need to keep the HTTP notification feature enabled, we recommend establishing a list of allowed URLs to send notifications to:

```yaml
notifiers:
  webhook:
    enabled: true
    # Empty whitelist means all urls are allowed.
    whitelist:
      - https://whitelist.domain1.com
      - https://restricted.domain2.com/whitelisted/path
```

Specifying a list of authorized URLs allows the administrator to restrict URL notifications. This is particularly useful for companies that need to rely on a corporate webhook system.
