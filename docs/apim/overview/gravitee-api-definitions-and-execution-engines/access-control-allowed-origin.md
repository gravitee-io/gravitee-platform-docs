---
description: This page discusses the improved response to origin validation
---

# Access-Control-Allowed-Origin

## Overview

With the legacy execution engine, you can configure Cross-Origin Resource Sharing (CORS) to allow a specific subset of origins. The Gateway properly validates the origin but returns `Access-Control-Allowed-Origin: *` in the response header regardless of the actual configuration.

## Reactive execution engine improvements

With the reactive execution engine, the allowed origin(s) you specify is returned instead of `*` - for example, `Access-Control-Allowed-Origin:` [`https://test.gravitee.io`](https://test.gravitee.io/) for the configuration shown below.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-cors.png" alt=""><figcaption><p>Sample CORS configuration</p></figcaption></figure>
