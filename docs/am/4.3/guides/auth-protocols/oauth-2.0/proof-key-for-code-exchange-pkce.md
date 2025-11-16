# Proof Key for Code Exchange (PKCE)

[Proof Key for Code Exchange (PKCE)](https://datatracker.ietf.org/doc/html/rfc7636) is an extension to the [authorization code](README.md#authorization-code) flow to prevent interception attacks from public clients.

{% hint style="info" %}
Force PKCE for public clients who cannot securely store their client secret. PKCE must be used for single-page applications (SPA) and mobile/native applications.
{% endhint %}

The PKCE extension introduces two temporary secrets:

* A **code\_verifier** that will be sent to the token endpoint `oauth/token`
* A **code\_challenge** that will be sent to the authorization endpoint `oauth/authorize`

{% hint style="info" %}
These codes are cryptographically-random values that your application has to create.
{% endhint %}

## How it works

As an extension of the authorization code flow, the steps to request access tokens are very similar:

1. The end user clicks **Sign in** in the application.
2. The application generates the code\_challenge and the code\_verifier.
3. The end user is redirected to the AM authorization server `/oauth/authorize?response_type=code&code_challenge=myChallenge`.
4. The end user authenticates using one of the configured identity providers and login options (MFA for example).
5. (Optional) A consent page is displayed to ask for user approval.
6. AM redirects the end user back to the application with an authorization code.
7. The application calls the AM authorization server `/oauth/token?code_verifier=myVerifier` to exchange the code for an access token (and optionally, a refresh token).
8. The application can use the access token to make secure API calls for the end user.

{% hint style="info" %}
The PKCE extension prevents potential attackers from exchanging the authorization code for an access token because it requires the code verifier.
{% endhint %}

## Examples

You can use the following examples as a guideline for generating the code\_verifier and code\_challenge if you want to build your application from scratch.

{% hint style="info" %}
Third-party libraries or SDKs can also be used for this purpose.
{% endhint %}

### JavaScript example

```javascript
// utils
function base64URLEncode(str) {
  btoa(str)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
}

function bufferToString(buffer: Uint8Array) {
  const CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const state = [];
  for (let i = 0; i < buffer.byteLength; i += 1) {
    const index = buffer[i] % this.CHARSET.length;
    state.push(this.CHARSET[index]);
  }
  return state.join('');
}
```

```javascript
// generate the code_verifier
const array = new Uint8Array(32);
window.crypto.getRandomValues(array);
const codeVerifier = base64URLEncode(bufferToString(array));
```

```java
// generate the code_challenge
const encoder = new TextEncoder();
const data = encoder.encode(codeVerifier);
window.crypto.subtle.digest('SHA-256', data)
  .then(buffer => {
      const bufferToString = String.fromCharCode.apply(null, new Uint8Array(buffer));
      return base64URLEncode(bufferToString);
  })
  .then(str => {
      const codeChallenge = str;
  });
```

### Java example

```java
// generate the code_verifier
SecureRandom secureRandom = new SecureRandom();
byte[] code = new byte[32];
secureRandom.nextBytes(codeVerifier);
String codeVerifier = Base64.getUrlEncoder().withoutPadding().encodeToString(code);
```

{% code overflow="wrap" %}
```java
// generate the code_challenge
byte[] bytes = codeVerifier.getBytes("US-ASCII");
MessageDigest md = MessageDigest.getInstance("SHA-256");
String codeChallenge = Base64.getUrlEncoder().withoutPadding().encodeToString(md.digest(bytes));
```
{% endcode %}
