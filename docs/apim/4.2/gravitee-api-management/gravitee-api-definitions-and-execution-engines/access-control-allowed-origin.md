---
description: This page discusses the improved response to origin validation
---

# Access-Control-Allowed-Origin

## Legacy execution engine behavior

When using the legacy execution engine, you can configure Cross-Origin Resource Sharing (CORS) to allow a specific subset of origins. Regardless of the actual configuration, the Gateway properly validates the origin but returns `Access-Control-Allowed-Origin: *` in the response header.

## Reactive execution engine improvements

When using the reactive execution engine, the allowed origin(s) you specify is returned instead of `*`. For example, in the configuration shown below, `Access-Control-Allowed-Origin: https://test.gravitee.io`.

<figure><img src="https://docs.gravitee.io/images/apim/3.x/event-native/event-native-api-management-cors.png" alt=""><figcaption><p>Sample CORS configuration</p></figcaption></figure>
