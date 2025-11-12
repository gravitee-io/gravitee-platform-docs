# Configure a Production-ready AM Environment

## Overview

During Gravitee Access Management (AM) installation, some default settings are created. While these default settings can be useful for testing your new installation, some of them may not be suitable for a production environment, where security is more of a consideration.

This how-to gives some tips on important settings to check in AM when preparing to move to a production environment. AM includes many other configuration options and every environment is unique. We recommend you also read the [Configuration Guide](../configuration/) to determine if you have completed all the configuration you need before you deploy AM in production.

{% hint style="info" %}
You can also read the [OAuth 2.0 best practices](docs/am/4.3/guides/auth-protocols/oauth-2.0/best-practices.md) for more details about configuring your AM environment.
{% endhint %}

You can configure AM settings in various ways — the `gravitee.yml` file, the AM Console settings, and environment and system variables. When you configure new settings, it is important to understand that one configuration type can override another. [Configure AM API](../configuration/configure-am-api/) gives a good overview of this topic.

## Step 1: Disable the internal APIs

AM API and AM Gateway include internal APIs which are enabled by default. If you do not intend to use them, we recommend you disable them.

Perform the following steps on both the AM API component and the AM Gateway component:

1. Open your `gravitee.yml` file.
2. In the `services:` section, set the `http:` `enabled` value to `false`:

{% code title="gravitee.yml" %}
````
```yaml
services:
  core:
    http:
      enabled: false
      port: 18093
      host: localhost
      authentication:
        # authentication type to be used for the core services
        # - none : to disable authentication
        # - basic : to use basic authentication
        # default is "basic"
        type: basic
        users:
          admin: adminadmin
```
````
{% endcode %}

To learn more about the internal APIs, see:

* [Configure the AM API internal API](docs/am/4.3/getting-started/configuration/configure-am-api/internal-api.md)
* [Configure the AM Gateway internal API](docs/am/4.3/getting-started/configuration/configure-am-gateway/internal-api.md)

## Step 2: Update the default users

Some default users are created for you during installation. We recommend you remove any users you do not need.

{% hint style="warning" %}
We strongly recommend that, regardless of the user management system you put in place, you keep the default **admin** user, so that you can recover AM in case of issues. Remember to change the default administrator password.
{% endhint %}

Perform the following steps on the AM API component:

1. Open your `gravitee.yml` file.
2. In the `security \ providers` section, remove any users you do not need:

{% code title="gravitee.yml" overflow="wrap" %}
````
```yaml
# Security section is used to defined organization users available on AM bootstrap
security:
  # If true create on AM bootstrap an inline identity provider with an admin user (login: admin)
  # this is the legacy mode
  defaultAdmin: false
  ## authentication providers
  ## currently, only "in memory" provider is supported
  providers:
    - type: memory
      enabled: false
      ## Name of IdentityProvider
      ## If missing the type will be used to create a generic name (ex: Memory users)
      #name:
      ## password encoding/hashing algorithm. One of:
      ## - BCrypt : passwords are hashed with bcrypt (supports only $2a$ algorithm)
      ## - none : passwords are not hashed/encrypted
      #default value is BCrypt
      password-encoding-algo: BCrypt
      users:
        - user:
          username: admin
          #email:
          firstname: Administrator
          lastname: Administrator
          ## Passwords are encoded using BCrypt
          ## Password value: adminadmin
          password: $2a$10$NG5WLbspq8V1yJDzUKfUK.oum94qL/Ne3B5fQCgekw/Y4aOEaoFZq
          role: ORGANIZATION_OWNER
```
````
{% endcode %}

3.  Update the default administrator password:

    <figure><img src="https://docs.gravitee.io/images/apim/3.x/how-tos/configure-apim/admin-pwd.png" alt=""><figcaption><p>Admin password</p></figcaption></figure>

## Step 3: Update the JWT secret

The JWT secret is used for multiple purposes :

* Sign session cookies in the AM API component
* Sign tokens used for the email verification process in the AM API and AM Gateway components
* Sign access and refresh tokens in the AM Gateway component if no certificate has been selected for your application (HMAC256)

Any users with this secret can tamper AM sessions and tokens. For security reasons, we strongly advise you to change the default value when using AM.

{% hint style="info" %}
As the secret is used between AM API and AM Gateway, be sure to set the same value for both components.
{% endhint %}

Perform the following steps on the AM API and Gateway components:

1. Open your `gravitee.yml` file.
2. In the `jwt` section, update the `secret` value:

{% code title="gravitee.yml" overflow="wrap" %}
````
```yaml
# JWT used to generate signed token for management security mechanism (Bearer Token) and to verify emails
jwt:
  secret: s3cR3t4grAv1t3310AMS1g1ingDftK3y # jwt secret used to sign JWT tokens (HMAC algorithm)
  #kid: default-gravitee-AM-key # kid (key ID) Header Parameter is a hint indicating which key was used to secure the JWT
  #expire-after: 604800 # the end of validity of the token in seconds (default 604800 = a week)
  #issuer: https://gravitee.am # the principal that issued the JWT (default https://gravitee.am)
  #cookie-path: / # cookie context path (default /)
  #cookie-domain: .gravitee.io # cookie domain (default "")
  #cookie-secure: true # cookie secure flag (default false)
```
````
{% endcode %}

3. You can also update other values, such as:
   * the `expire-after` value, to change the validity period from the default value of one week
   * the `cookie-path` and `cookie-domain` values, to adapt them to your own environment; the values you define must be specific to the domain and path where the API is running and not apply to any another environment (for example, `.gravitee.io` could apply to any domain called `xxx.gravitee.io`, such as `dev.gravitee.io` or `qa.gravitee.io`)
   * the `cookie-secure` to adapt the Secure flag for the Session Cookie (should be set to true).

## Step 4: Update CORS policy

Cross-origin resource sharing (CORS) is a mechanism that allows restricted resources on a web page to be requested from another domain outside the domain from which the first resource was served.

Only selected and trusted domains should access AM (e.g. the AM console). Prefer allowing specific domains over any domains (do not use \* wildcard value).

Perform the following steps on the AM API component:

1. Open your `gravitee.yml` file.
2. In the `http` section, update the `cors` section:

{% code title="gravitee.yml" overflow="wrap" %}
```yaml
#http:
#  api:
     # Configure the listening path for the API. Default to /management
#    entrypoint: /management
#  cors:
#      Allows to configure the header Access-Control-Allow-Origin (default value: *)
#      '*' is a valid value but is considered as a security risk as it will be opened to cross origin requests from anywhere.
#    allow-origin: http://developer.mycompany.com
#      Allows to define how long the result of the preflight request should be cached for (default value; 1728000 [20 days])
#    max-age: 864000
#      Which methods to allow (default value: OPTIONS, GET, POST, PUT, DELETE, PATCH)
#    allow-methods: 'OPTIONS, GET, POST, PUT, DELETE, PATCH'
#      Which headers to allow (default values: Cache-Control, Pragma, Origin, Authorization, Content-Type, X-Requested-With, If-Match, X-Xsrf-Token)
#    allow-headers: 'X-Requested-With'
#  csrf:
    # Allows to enable or disable the CSRF protection (default is enabled).
#    enabled: true
```
{% endcode %}

## Step 5: Update URL Redirects policy

During login and logout operations AM API uses callback URLs to redirect the end-user back to the AM Console.

To avoid potential open-redirection vulnerabilities (be redirected to malicious websites), you can define a set of allowed URL callbacks.

Perform the following steps on the AM API component:

1. Open your `gravitee.yml` file.
2. In the `http` section, update the `login` and `logout` sections:

{% code title="gravitee.yml" overflow="wrap" %}
```yaml
#http:
#  api:
     # Configure the listening path for the API. Default to /management
#    entrypoint: /management
#  cors:
#      Allows to configure the header Access-Control-Allow-Origin (default value: *)
#      '*' is a valid value but is considered as a security risk as it will be opened to cross origin requests from anywhere.
#    allow-origin: http://developer.mycompany.com
#      Allows to define how long the result of the preflight request should be cached for (default value; 1728000 [20 days])
#    max-age: 864000
#      Which methods to allow (default value: OPTIONS, GET, POST, PUT, DELETE, PATCH)
#    allow-methods: 'OPTIONS, GET, POST, PUT, DELETE, PATCH'
#      Which headers to allow (default values: Cache-Control, Pragma, Origin, Authorization, Content-Type, X-Requested-With, If-Match, X-Xsrf-Token)
#    allow-headers: 'X-Requested-With'
#  csrf:
    # Allows to enable or disable the CSRF protection (default is enabled).
#    enabled: true
#  login:
#      Allows to configure the allowed callback urls during login process (default value: *)
#      '*' is a valid value but is considered as a security risk as it will be opened to open redirection issues.
#    allow-redirect-urls: https://am-console.mycompany.com/login/callback
#  logout:
#      Allows to configure the allowed callback urls during logout process (default value: *)
#      '*' is a valid value but is considered as a security risk as it will be opened to open redirection issues.
#    allow-redirect-urls: https://am-console.mycompany.com/logout/callback
```
{% endcode %}

## Step 6: Enable Secure Cookies

Cookies are used by AM API and AM Gateway to keep minimal information about user sessions. The "Secure" flag instructs a user’s browser to only send the cookie along with requests over HTTPS to in-scope addresses.

Perform the following steps on the AM API component:

1. Open your `gravitee.yml` file.
2. In the `jwt` section, update the `cookie-secure` value:

{% code title="gravitee.yml" overflow="wrap" %}
````
```yaml
# JWT used to generate signed token for management security mechanism (Bearer Token) and to verify emails
jwt:
  secret: s3cR3t4grAv1t3310AMS1g1ingDftK3y # jwt secret used to sign JWT tokens (HMAC algorithm)
  #kid: default-gravitee-AM-key # kid (key ID) Header Parameter is a hint indicating which key was used to secure the JWT
  #expire-after: 604800 # the end of validity of the token in seconds (default 604800 = a week)
  #issuer: https://gravitee.am # the principal that issued the JWT (default https://gravitee.am)
  #cookie-path: / # cookie context path (default /)
  #cookie-domain: .gravitee.io # cookie domain (default "")
  #cookie-secure: true # cookie secure flag (default false)
```
````
{% endcode %}

Perform the following steps on the AM Gateway component:

1. Open your `gravitee.yml` file.
2. In the `http.cookie` section, update the `secure` value:

{% code title="gravitee.yml" overflow="wrap" %}
````
```yaml
#http
##  cookie:
#    secure: false # Default is false for demonstration purpose but we highly recommend you to enable cookie secure.
#    sameSite: Lax
#    session:
#      name: session-name
#      timeout: 1800000 # (in milliseconds)
```
````
{% endcode %}

3\. You can also consider updating the \`sameSite\` to \[Strict]\(https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#syntax) and adapt the session timeout:

## Step 7: Mitigate Cross-Site Scripting (XSS) and Cross Site Framing

The AM Gateway implements [Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) and [X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options).

It is recommended to use these two mechanisms to have better control over the resources the user agent is allowed to load for a given page.

For example, if you don’t want to render a page in an `<iframe>` element, you can define the `X-Frame-Options` to `DENY` or use the `frame-ancestors` directive of CSP.

```yaml
http:
  # define the X-Frame-Options
  xframe:
    action: DENY
  # define CSP directives
  csp:
    directives:
    - frame-ancestors 'none';
```

## Step 8: Sending email

The AM Management API and the AM Gateway are able to send email via the `email` section in the `gravitee.yaml` of each service.&#x20;

As of AM version 4.0.2, the `allowedfrom` attribute has been added to restrict the FROM attribute a user can define in the AM UI when customizing the email form or when configuring the `Send Email` policy. It is highly recommended to update this value to restrict authorized domain names.

```yaml
# SMTP configuration used to send mails
email:
  enabled: false
  host: smtp.my.domain
  subject: "[Gravitee.io] %s"
  port: 587
  from: noreply@my.domain
  username: user@my.domain
  password: password
  # List of allowed from
  allowedfrom:
     - ${email.from}
     - *@mydomain.org
```
