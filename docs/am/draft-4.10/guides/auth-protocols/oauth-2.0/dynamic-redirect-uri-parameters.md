# Dynamic Redirect URI Parameters

## Overview

The Dynamic Redirect URI Parameters feature in the OAuth2 flow enhances flexibility and control over redirection behavior by letting you append dynamic parameters to the final `redirect_uri`. These parameters are resolved using [Gravitee Expression Language (EL)](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/ySqSVpDHfKA0fNml1fVO/), which lets you insert custom logic and data into the redirect URL. Dynamic Redirect URI Parameters improves the adaptability and precision of user authentication flows by empowering applications to dynamically adjust redirect targets based on context, such as user-specific attributes or session data.

## Enable redirect URI parameters

To enable Gravitee Expression Language and dynamic parameters for redirect URIs, follow these steps:

1. Navigate to the **Domain** section in the Gravitee AM Console.
2. Go to the **Settings** tab.
3. Select **Client Registration**.
4. Toggle **Enable/Disable EL and dynamic parameters for redirect URIs** to ON.

<figure><img src="../../../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

Once enabled, you can use EL in redirect URIs to create personalized user experiences.

## Use Dynamic Redirect URIs

To use dynamic redirect URIs with query parameters, complete the following steps:

1. Navigate to the **Domain** section in the Gravitee AM Console.
2. Go to **Application** settings.
3. In the **Settings** tab, navigate the **Redirect URI** field.
4. Specify the `redirect_uris` with query parameters, embedding values using Gravitee Expression Language. For more information about available EL objects and their usage, refer to [am-expression-language.md](../../am-expression-language.md "mention").

<figure><img src="../../../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>

### Example

1.  Specify a `redirect_uri` in your application configuration. For example:

    ```
    https://callback?username={#context.attributes['user'].username}
    ```

    User-specific data is dynamically included in the redirection.
2. Initiate the login flow using `redirect_uri=https://callback`.

With this setup, `{#context.attributes['user'].username}` is evaluated and replaced with the actual username to tailor the redirection for the individual user.

### Limitations

When you configure redirect URIs, you cannot register two redirect URIs that have the same schema, hostname, and path, and differ only in their query parameters. This limitation is due to the validation logic that checks for uniqueness based on the combination of these components, without evaluating query parameters.

#### **Example:**

* Allowed: `https://example.com/callback`
*   Not Allowed:

    * `https://callback?param1=one&user={#context.attributes['user'].username}`
    * `https://callback?param1=two&user={#context.attributes['user'].username}`

    Both redirect URIs would be considered identical, causing conflicts in registration.
