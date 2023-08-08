# Configure a Production-ready APIM Environment

## Overview

The default settings created during APIM installation can be useful for testing your new instance. However, some may not be suitable for a production environment, where security is more of a consideration.

This guide highlights the APIM settings that require special attention while you prepare to move to a production environment. It is organized into the following sections:

* Security checklist
* Internal API
* Deployment
* Authentication
* Brute force protection
* [Disable internal APIs](configure-a-production-ready-apim-environment.md#disable-internal-apis)
* [Update default users](configure-a-production-ready-apim-environment.md#update-default-users)
* [Update the JWT secret](configure-a-production-ready-apim-environment.md#update-the-jwt-secret)
* [Update the default APIM settings](configure-a-production-ready-apim-environment.md#update-the-default-apim-settings)
* [Portal & Console default Nginx security config](configure-a-production-ready-apim-environment.md#portal-and-console-default-nginx-security-config)

{% hint style="warning" %}
**Configuring APIM**

APIM includes many other configuration options and every environment is unique. However you configure new settings (via the `gravitee.yml` file, APIM Console, or environment and system variables) it is important to understand that one configuration type can override another. [Configure APIM Gateway](components/the-gravitee-api-gateway.md) gives a good overview of this topic.
{% endhint %}

## Security checklist

Review and amend the following before going into production and exposing your APIs.&#x20;

The objective is not to apply all of the recommendations, but to ensure that all configurations have been made with caution.

* Disable or enforce the security of the internal API
* Review the exposition of the console and developer portal to the outside world
* Ensure the console and developer portal rest APIs are accessible through HTTPS
* Configure authentication using an Identity Provider
* Enable authentication to access the Developer Portal
* Remove all the default users
* Remove the admin user or enforce the admin user password
* Disable user self-registration for bot console and portal
* Disable auto-validation of self-registered users (if self-registration is enabled)
* Change the user session signing secret and validity duration
* Disable default application creation
* Set the registration link validity to 1 day
* Change the user reference secret
* Configure brute force protection (Recaptcha or Fail2ban)
* Enabled CSRF protection
* Configure CORS for Console and Portal REST APIs
* Change the property encryption secret
* Enable documentation page sanitizer
* Disable Webhook notifier or configure an authorized list of URLs
* Apply safe practices when designing and deploying APIs

## Internal APIs

APIM API and APIM Gateway include internal APIs that are enabled by default. These internal APIs permit the retrieval of monitoring and technical information pertaining to Gravitee components (more information [here](https://documentation.gravitee.io/apim/getting-started/configuration/configure-apim-management-api/internal-api-1)).

### Disabling internal APIs

If you do not intend to use an internal API, **we recommend you disable it**.

1. Open your `gravitee.yml` file.
2. In the `services:` section, set the `http:` `enabled` value to `false`:

```yaml
services:
  core:
    http:
      enabled: false
      ...
```

### Enforcing security

If you plan to keep the internal API enabled, please consider enforcing the security by following the next steps.

1. Ensure basic authentication:

```yaml
services:
  core:
    http:
      ...
      authentication:
        type: basic
        users:
          admin: adminadmin
```

2. Remove the default admin user and password.
3. Replace these with a username/password of your choosing, as shown in the example below. A good practice is to:
   1. Create a random username that is less obvious than a simple "admin" user.
   2. Define a strong password that follows security best practices. Ideally, you should use a password generator.

```yaml
services:
  core:
    http:
      ...
      authentication:
        type: basic
        users:
          kJCe9nxhNV: "k5/ya\S6*9dm2kT`dbnhr{jzyD)<u.<9"
```

4. It is highly recommended that you bind the internal API to make it accessible from localhost only:

```yaml
services:
  core:
    http:
      enabled: true
      port: 18083
      host: localhost
```

To learn more about internal APIs, see:

* [Configure the APIM Management API internal API](configure-apim-management-api/internal-api.md)
* [Configure the APIM Gateway internal API](the-gravitee-api-gateway/gateway-internal-api.md)

## Deployment

### Console and Portal APIs

Gravitee APIM Management API allows the simultaneous exposure of both Console and Developer Portal REST APIs. This enables quick setup when discovering the platform.

If the Console and Developer Portal are not intended to be used by the same category of users, it is **recommended to deploy them on distinct instances**.

You can deploy a couple of instances dedicated to the Management Console with the Portal API disabled on one side:

```yaml
http:
  api:
    console:
      enabled: true
    portal:
      enabled: false
```

On the other side, you can deploy another dedicated couple of instances for the Developer Portal by disabling the Console API:

```yaml
http:
  api:
    console:
      enabled: false
    portal:
      enabled: true
```

The Console REST API will remain inaccessible to the outside world if you decide to make your Developer Portal reachable from outside of your company. However, Gravitee recommends that you do not expose your Console or Developer Portal publicly if there is no particular business requirement.&#x20;

Refer to the [Gravitee documentation](https://documentation.gravitee.io/apim/getting-started/configuration/configure-apim-management-api/internal-api#configure-the-management-and-portal-apis) for more information about Console and Portal APIs.

### Enable HTTPS

Whatever solution you rely on, **make sure your REST APIs are only reachable over HTTPS** to protect against man-in-the-middle attacks.

There are several ways to configure TLS depending on your type of installation. One way is to let Gravitee manage the TLS connection directly by configuring it:

```yaml
jetty:
  secured: true
  ssl:
    keystore:
      type: jks # Supports jks, pkcs12
      path: <keystore_path>
      password: <keystore_secret>
```

You can find additional details regarding HTTPS support for the REST APIs in the[ Gravitee documentation](https://documentation.gravitee.io/apim/getting-started/configuration/configure-apim-management-api/internal-api#enable-https-support).

## Authentication

### Identity provider

**We highly recommend using your own corporate identity provider** (must be Oauth2/OIDC-compliant) to delegate authentication to your Management Console and Portal. You have several choices:

* [Gravitee Access Management](https://documentation.gravitee.io/apim/getting-started/configuration/authentication-and-sso#gravitee-access-management-authentication)
* [GitHub](https://documentation.gravitee.io/apim/getting-started/configuration/authentication-and-sso#github-authentication)
* [Google](https://documentation.gravitee.io/apim/getting-started/configuration/authentication-and-sso#google-authentication)
* [Any compliant OAuth/OIDC server](https://documentation.gravitee.io/apim/getting-started/configuration/authentication-and-sso#openid-connect-authentication)

Alternatively, you can rely on your [LDAP server](https://documentation.gravitee.io/apim/getting-started/configuration/authentication-and-sso#ldap-authentication).

It is preferable to rely on an external identity provider to handle security so you can easily comply with your internal company security policy. You can configure role mapping to automatically assign a role to a given user matching particular criteria. Refer to the [Gravitee documentation](https://documentation.gravitee.io/apim/getting-started/configuration/authentication-and-sso#gravitee-access-management-authentication) for an example of role or group mapping.

### Developer Portal authentication

If there are no strong business requirements, **we highly recommend forcing user authentication to access the Developer Portal**. This limits service exposure to authenticated users only:

```yaml
portal:
  authentication:
    forceLogin:
      enabled: true
```

The Developer Portal configuration can be fine-tuned to satisfy your needs. Additional details are in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/developer-portal/advanced-developer-portal-configuration).

### Default users

Some default users are created for you during installation. These users are mainly there to discover the platform's capabilities with respect to roles and permissions.

**We recommend you remove these users if you do not need them** (or change their default passwords).

In the `gravitee.yaml` file, remove the following users: `user`, `api1`, `application1`

```yaml
security:
  providers:
    - type: memory
      users:
        - user:
          username: user # <-- Remove these users
        - user:
          username: api1
        - user:
          username: application1
```

### Admin user

It is recommended to rely on an external IdP for authentication. Gravitee also recommends removing the default admin user and assigning proper admin roles and permissions to a restricted list of well-known users:

```yaml
security:
  providers:
    - type: memory
      users:
        - user:
          username: admin # <-- Remove the admin user
```

If removing the admin user is not an option, **we highly recommend replacing the default password** with a strong password of your choice:

```yaml
security:
  providers:
    - type: memory
        - user:
          username: admin
          password: <bcrypt password>
```

### User self-registration

We recommend **disabling the capability for a user to self-register** for both the Console and the Developer Portal to rely on your company IdP to manage your user provisioning. This dramatically decreases the risk of an external user unexpectedly accessing your system:

```yaml
console:
  userCreation:
    enabled: false

portal:
  userCreation:
    enabled: false
```

If disabling self-registration is not possible due to business considerations, we strongly advise that you **disable auto validation of self-registered users** and instantiate a human-based acceptance process:

```yaml
console:
  userCreation:
    enabled: true
    automaticValidation:
        enabled: false

portal:
  userCreation:
    enabled: true
    automaticValidation:
        enabled: false
```

Console and Developer Portal settings are independent, allowing you to apply different strategies.

### User session

User session is managed using a signed JWT cookie. Consider the options below to enforce security:

* **Adapt the session duration** to a shorter period of time to force users to reauthenticate more frequently.
* **Enforce the JWT secret.** Ensure it is unique and rely on a password generator.
* **Enable cookie-secure** to force the browser to send the session cookie over HTTPS only.

```yaml
jwt:
  secret: cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3ecf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3ecf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3ecf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e
  expire-after: 172800 # 2 days
  cookie-secure: true
```

### Other options

You can configure various user options:

* `user.login.defaultApplication`: Creates a new application for each new user (default: `true`). **Disable the default application creation** to avoid unnecessary application creation. Users will need to explicitly create an application prior to subscribing to an API.
* `user.creation.token.expire-after`: Number of seconds before the user registration or reset password token expires. The default is `86400`(1 day). **Do** **not exceed 1 day** and use the reset password feature in case of expiration.
* `user.reference.secret`: Secret used to generate a unique and anonymous user reference. The secret must be 32 characters long and **must be changed.**
* `user.anonymize-on-delete:enabled`: When a user is deleted, their access is revoked. The user data remains in the database for audit purposes. Depending on your privacy policy, you should enable this feature to anonymize the user's first name, last name, and email when they are deleted.
* `user.password.policy.pattern`: By default, Gravitee includes a strong password policy taken from OWASP recommendations. We highly recommend not decreasing the complexity of the password policy if you allow user registration.

You can find other information related to user management in the [Gravitee documentation](https://documentation.gravitee.io/apim/getting-started/configuration/configure-apim-management-api/user-and-management-configuration).

## Brute-force protection

### ReCaptcha

Ensure that ReCaptcha is configured to protect forms against bots and brute-force attempts:

```yaml
# Allows to enable or disable recaptcha (see https://developers.google.com/recaptcha/docs/v3). Currently, it only affect the user registration route.
reCaptcha:
  enabled: true
  siteKey: <your_site_key>
  secretKey: <your_secret_key>
  minScore: 0.5
  serviceUrl: https://www.google.com/recaptcha/api/siteverify
```

Gravitee relies on [ReCaptcha V3](https://developers.google.com/recaptcha/docs/v3?hl=en), which is non-intrusive for the end user. You can obtain your site key and secret key directly from your Google developer account ([https://www.google.com/recaptcha/admin/create](https://www.google.com/recaptcha/admin/create)).

### Fail2Ban

If your platform is particularly exposed to the outside world, we recommend adding additional protection against pure brute-force attacks by [setting up Fail2Ban](https://documentation.gravitee.io/apim/getting-started/configuration/configure-apim-management-api/security#fail2ban).

Fail2Ban scans log files and automatically bans IPs that show malicious signs, e.g., too many password failures, seeking an opportunity for exploitation, etc.

## Browser protection

### Enable CSRF protection

Cross-site request forgery (CSRF) is a web security vulnerability that allows an attacker to induce users to perform actions that they do not intend to perform. You can protect your end users by checking that the CSRF protection is enabled (enabled by default):

```yaml
http: 
  csrf:
    # Allows to enable or disable the CSRF protection. Enabled by default.
    enabled: true
```

We strongly recommend **NEVER** disabling CSRF protection unless you are absolutely sure of what you are doing and that your users may be exposed to [Cross Site Request Forgery attacks](https://fr.wikipedia.org/wiki/Cross-site\_request\_forgery).

### Configure CORS

CORS is one of the most important things to set up to protect your users and your system against malicious attackers. It allows the user's browser to enable native protection preventing unauthorized websites to perform a JavaScript HTTP call to the Console or REST API. Basically, when well-configured, you only allow your own Console website (e.g., [https://gio-console.mycompany.com)](https://gio-console.my-comany.com\)) and Dev Portal website (e.g., [https://gio-portal.mycompany.com)](https://gio-portal.mycompany.com\)) to make calls from a browser to their respective APIs.

Make sure CORS is well-configured for both the Console AND the Portal APIs:

```yaml
http:
  api:
    management:
      cors:
        allow-origin: 'https://gio-console.mycompany.com'
    portal:
      cors:
        allow-origin: 'https://gio-portal.mycompany.com'
```

`allow-origin: '*'` should be considered a security risk because it permits all cross-origin requests. **We highly recommend fine-tuning the allow-origin setting. Refer to** the [Gravitee documentation](https://documentation.gravitee.io/apim/getting-started/configuration/configure-apim-management-api/internal-api#cors-configuration) for other useful information related to CORS.

## Other configuration settings

### Property encryption

Gravitee allows attaching properties to an API and offers the capability to store encrypted property values. **You must change the default encryption secret** with a custom secret that can't be determined easily. You must consider the following when changing the secret:

* The secret must be **changed for both Management and Gateway** and have the same value.
* The secret must be **32 bytes in length**.
* The secret should ideally be generated with a password generation tool to enforce robustness.
* If you have several installations (e.g., one for dev, one for prod), make sure to **set up different secrets for each installation**.

```yaml
api:
  properties:
    encryption:
         secret: <32 byte length secret>
```

You can find additional details about property encryption in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/policy-design/v2-api-policy-design-studio#encryption).

### Documentation sanitizer

Gravitee offers the capability to attach and expose API documentation. Once published, these pages can be accessible to API consumers to discover and understand the purpose of an API. **We recommend enabling the sanitization of the documentation pages** to avoid any script injection that could have an impact on the API consumer when the page is published on the Developer Portal.

```yaml
documentation:
  markdown:
    sanitize: true
```

### Notifiers

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

Specifying a list of authorized URLs allows the administrator to restrict URL notifications. This is particularly useful for companies that need to rely on a corporate Webhook system.

## API management safe practices

### Roles, permissions, and groups

Gravitee offers the ability to fine-tune a permissions list and the concept of roles, which can be used to **restrict user access to only what is required**.

Some good practices to establish:

* Use groups and permissions to restrict a given user's access to only a necessary subset of APIs.
* Ensure each user only has the necessary permissions (e.g., assign the API\_PUBLISHER role instead of ADMIN).
* Assign permissions to a group instead of each user individually.
* Automatically associate a group with each new API or application to facilitate permission management.

You can find detail on roles, groups, and permissions in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/administration/user-management-and-permissions).

### API review & quality

You can **enable API review and quality** to avoid unexpected public exposure to the Developer Portal without strong security requirements or if you want a member of a quality team to review API designs prior to deploying the API and make it accessible from the API consumers. This can be a smooth way to put a good API strategy in place with strong requirements.

You will find more information about API review and quality in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/api-measurement-tracking-and-analytics/using-the-api-quality-feature).

### API design

There is no "rule of thumb" when it comes to designing and exposing your APIs. It always depends on the business requirements. However, here are some considerations to keep up on the list to avoid mistakes and open unexpected security breaches:

* Enable and configure Cors at API level. This ensures the best level of security when the API is consumed by browser-based applications. See [details here](https://documentation.gravitee.io/apim/guides/api-configuration/v2-api-configuration/configure-cors#configure-cors).
* Avoid exposing an API without security (ie keyless plan) when possible. Always prefer stronger security solutions such as JWT or Oauth2.
* Disable auto validation of API subscriptions to manually validate each of them. This ensures that you know your API consumers by reviewing each subscription.
* Require the API consumer to put a comment when subscribing to an API. It's a simple way to understand why a subscription has been made and helps in detecting malicious attempts to access an API.
* Regularly review the subscriptions and revoke those that are no longer used.

More information on how to manage API subscription are detailed in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/api-exposure-plans-applications-and-subscriptions/subscriptions).

##

##

##

## Disable internal APIs

APIM API and APIM Gateway include internal APIs which are enabled by default. If you do not intend to use them, we recommend you disable them.

Perform the following steps on both the APIM API component and the APIM Gateway component:

1. Open your `gravitee.yml` file.
2.  In the `services:` section, set the `http:` `enabled` value to `false`:

    ```yaml
    services:
      core:
        http:
          enabled: false
          port: 18083
          host: localhost
          authentication:
            # authentication type to be used for the core services
            # - none: to disable authentication
            # - basic: to use basic authentication
            # default is "basic"
            type: basic
            users:
              admin: adminadmin
    ```

To learn more about the internal APIs, see:

* [Configure the APIM Management API internal API](configure-apim-management-api/internal-api.md)
* [Configure the APIM Gateway internal API](the-gravitee-api-gateway/gateway-internal-api.md)

## Update default users

Some default users are created for you during installation. We recommend you remove any users you do not need.

{% hint style="info" %}
We strongly recommend that, regardless of the user management system you put in place, you keep the default **admin** user, so that you can recover APIM in case of issues. Remember to change the default administrator password.
{% endhint %}

Perform the following steps on the APIM API component:

1. Open your `gravitee.yml` file.
2.  In the `security \ providers` section, remove any users you do not need:

    ```yaml
    security:
      # When using an authentication providers, use trustAll mode for TLS connections
      # trustAll: false
      providers:  # authentication providers
        - type: memory
          # allow search results to display the user email. Be careful, It may be contrary to the user privacy.
    #      allow-email-in-search-results: true
          # password encoding/hashing algorithm. One of:
          # - bcrypt: passwords are hashed with bcrypt (supports only $2a$ algorithm)
          # - none: passwords are not hashed/encrypted
          # default value is bcrypt
          password-encoding-algo: bcrypt
          users:
            - user:
              username: user
              #firstname:
              #lastname:
              # Passwords are encoded using BCrypt
              # Password value: password
              password: $2a$10$9kjw/SH9gucCId3Lnt6EmuFreUAcXSZgpvAYuW2ISv7hSOhHRH1AO
              roles: ORGANIZATION:USER,ENVIRONMENT:USER
              # Useful to receive notifications
              #email:
            - user:
              username: admin
              #firstname:
              #lastname:
              # Password value: admin
              password: $2a$10$Ihk05VSds5rUSgMdsMVi9OKMIx2yUvMz7y9VP3rJmQeizZLrhLMyq
              roles: ORGANIZATION:ADMIN,ENVIRONMENT:ADMIN
              #email:
            - user:
              username: api1
              #firstname:
              #lastname:
              # Password value: api1
              password: $2a$10$iXdXO4wAYdhx2LOwijsp7.PsoAZQ05zEdHxbriIYCbtyo.y32LTji
              # You can declare multiple roles using comma separator
              roles: ORGANIZATION:USER,ENVIRONMENT:API_PUBLISHER
              #email:
            - user:
              username: application1
              #firstname:
              #lastname:
              # Password value: application1
              password: $2a$10$2gtKPYRB9zaVaPcn5RBx/.3T.7SeZoDGs9GKqbo9G64fKyXFR1He.
              roles: ORGANIZATION:USER,ENVIRONMENT:USER
    ```
3.  Update the default administrator password:

    <figure><img src="https://docs.gravitee.io/images/apim/3.x/how-tos/configure-apim/admin-pwd.png" alt=""><figcaption><p>Default admin password</p></figcaption></figure>

To learn more about configuring users, see [Authentication and SSO](../../guides/administration/authentication-and-sso.md).

## Update the JWT secret

The JWT secret is used for signing session cookies in the APIM UI components. Any users with this secret can log in to APIM and update their permissions.

Perform the following steps on the APIM API component:

1. Open your `gravitee.yml` file.
2.  In the `jwt` section, update the `secret` value:

    ```yaml
    jwt:
      secret: myJWT4Gr4v1t33_S3cr3t
      # Allows to define the end of validity of the token in seconds (default 604800 = a week)
      #expire-after: 604800
      # Allows to define the end of validity of the token in seconds for email registration (default 86400 = a day)
      #email-registration-expire-after: 86400
      # Allows to define issuer (default gravitee-management-auth)
      #issuer: gravitee-management-auth
      # Allows to define cookie context path (default /)
      #cookie-path: /
      # Allows to define cookie domain (default "")
      #cookie-domain: .gravitee.io
      # Allows to define if cookie secure only (default false)
      #cookie-secure: true
    ```
3. You can also update other values, such as:
   * the `expire-after` value, to change the validity period from the default value of one week
   * the `cookie-path` and `cookie-domain` values, to adapt them to your own environment; the values you define must be specific to the domain and path where the API is running and not apply to any other environment (for example, `.gravitee.io` could apply to any domain called `xxx.gravitee.io`, such as `dev.gravitee.io` or `qa.gravitee.io`)

## Update the default APIM settings

The most common settings are described below. Not all of these settings need to be changed in every environment.

Perform the following steps in APIM Console:

1. Log in to APIM Console.
2. Select **Settings**.
3.  In the **Portal** section:

    1. Select **Settings** in the inner sidebar.
    2. Update the **Company name.**

    <figure><img src="../../.gitbook/assets/Screenshot 2023-07-11 at 3.34.14 PM.png" alt=""><figcaption><p>Portal settings</p></figcaption></figure>
4.  In the Gateway section:

    1. Select **API Logging**.
    2. Update the maximum logging duration for APIM API logging to avoid flooding. In this example, we have configured a logging duration of 15 minutes:

    <figure><img src="../../.gitbook/assets/Screenshot 2023-07-11 at 3.42.12 PM.png" alt=""><figcaption><p>API logging settings</p></figcaption></figure>
5. Select **Organization** in the main sidebar:
   1. In the **Gateway** section:
      1. Select **Sharding Tags**.
      2.  In the **Entrypoint mappings** section of the page, update the **Entrypoint** field with your APIM API endpoint.

          <figure><img src="../../.gitbook/assets/Screenshot 2023-07-11 at 3.38.19 PM.png" alt=""><figcaption><p>Save sharding tag</p></figcaption></figure>
   2. Select **Settings** in the inner sidebar:
      * Update the **Title** of APIM Console to make it more appropriate for your own environment.
      * Update the **Management URL** to your APIM Console URL.

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-11 at 3.31.13 PM.png" alt=""><figcaption><p>Organization settings</p></figcaption></figure>

The recommended value depends on the type of logging you have enabled: the more information you log, the lower the value needs to be (although the value must be above zero to be taken into account).

## Portal & Console default Nginx security config

The APIM Console uses this default config:

```
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Content-Security-Policy "frame-ancestors 'self';" always;
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options nosniff;
    add_header X-Permitted-Cross-Domain-Policies none;
```

The APIM Portal uses this default config:

```
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options nosniff;
    add_header X-Permitted-Cross-Domain-Policies none;
```

It is recommended to complete these mechanisms to have better control over the resources the user agent is allowed to load for a given page.

For APIM Portal you can improve security to allow specific origins, with these headers:

```
add_header X-Frame-Options "ALLOW-FROM=my-domain.com" always;
add_header Content-Security-Policy "frame-ancestors my-domain.com;" always;
```

{% hint style="info" %}
APIM Management Console uses an iframe to preview the portal theme configuration, so it is necessary to add the Management Console in the Developer Portal nginx config. You can learn more about:

* Content-Security\_policy and framing [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors)
* X-Frame-Options [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)
{% endhint %}
