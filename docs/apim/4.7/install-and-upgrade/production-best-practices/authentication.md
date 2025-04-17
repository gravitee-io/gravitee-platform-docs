# Authentication

## Identity providers

**We highly recommend using your own corporate identity provider** (must be OAuth2/OIDC-compliant) to delegate authentication to your Management Console and Portal. You have several choices:

* [Gravitee Access Management](https://app.gitbook.com/s/BhTMKXIHEN2PB8YB6Fz5/getting-started/tutorial-getting-started-with-am)
* [GitHub](https://app.gitbook.com/s/BhTMKXIHEN2PB8YB6Fz5/guides/identity-providers/social-identity-providers/github)
* [Azure AD](https://app.gitbook.com/s/BhTMKXIHEN2PB8YB6Fz5/guides/identity-providers/social-identity-providers/azure-ad)
* [Any compliant OAuth/OIDC server](https://app.gitbook.com/s/BhTMKXIHEN2PB8YB6Fz5/guides/identity-providers/social-identity-providers/openid-connect)

Alternatively, you can rely on your [LDAP server](https://documentation.gravitee.io/apim/getting-started/configuration/authentication-and-sso#ldap-authentication).

It is preferable to rely on an external identity provider to handle security so you can easily comply with your internal company security policy. You can configure role mapping to automatically assign a role to a given user matching particular criteria. Refer to the [Gravitee documentation](https://documentation.gravitee.io/apim/getting-started/configuration/authentication-and-sso#gravitee-access-management-authentication) for an example of role or group mapping.

## Developer Portal authentication

If there are no strong business requirements, **we highly recommend forcing user authentication to access the Developer Portal**. This limits service exposure to authenticated users only:

```yaml
portal:
  authentication:
    forceLogin:
      enabled: true
```

The Developer Portal configuration can be fine-tuned to satisfy your needs. Additional details are in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/developer-portal/advanced-developer-portal-configuration).

## Users

### Roles, permissions, and groups

Gravitee offers the ability to fine-tune a permissions list and the concept of roles, which can be used to **restrict user access to only what is required**.

Some good practices to establish:

* Use groups and permissions to restrict a given user's access to only a necessary subset of APIs.
* Ensure each user only has the necessary permissions (e.g., assign the API\_PUBLISHER role instead of ADMIN).
* Assign permissions to a group instead of each user individually.
* Automatically associate a group with each new API or application to facilitate permission management.

You can find detail on roles, groups, and permissions in the [Gravitee documentation](https://documentation.gravitee.io/apim/guides/administration/user-management-and-permissions).

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

Furthermore, you can find an additional setting for controlling the built-in (memory) Admin account. By default, admin user will be added. If you want to remove the default admin, then set:

```bash
adminAccountEnable: false
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

Each APIM component user session is managed using a signed JWT cookie. Any user with the JWT secret can log in to APIM and update their permissions. Consider the options below to enforce security:

* **Adapt the session duration** to a shorter period of time to force users to reauthenticate more frequently.
* **Enforce the JWT secret.** Ensure it is unique and rely on a password generator.
* **Enable cookie-secure** to force the browser to send the session cookie over HTTPS only.

You can also **update cookie-path and cookie-domain** to adapt them to your own environment. The values you define must be specific to the domain and path where the API is running and must not apply to any other environment (e.g., `.gravitee.io` could apply to any domain called `xxx.gravitee.io`, such as `dev.gravitee.io` or `qa.gravitee.io`)

```yaml
jwt:
  secret: cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3ecf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3ecf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3ecf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e
  expire-after: 172800 # 2 days
  cookie-secure: true
  #cookie-path: /
  # Allows to define cookie domain (default "")
  #cookie-domain: .gravitee.io
  # Allows to define if cookie secure only (default false)
```

### Other user options

You can configure various user options:

* `user.login.defaultApplication`: Creates a new application for each new user (default: `true`). **Disable the default application creation** to avoid unnecessary application creation. Users will need to explicitly create an application prior to subscribing to an API.
* `user.creation.token.expire-after`: Number of seconds before the user registration or reset password token expires. The default is `86400`(1 day). **Do** **not exceed 1 day** and use the reset password feature in case of expiration.
* `user.reference.secret`: Secret used to generate a unique and anonymous user reference. The secret must be 32 characters long and **must be changed.**
* `user.anonymize-on-delete:enabled`: When a user is deleted, their access is revoked. The user data remains in the database for audit purposes. Depending on your privacy policy, you should enable this feature to anonymize the user's first name, last name, and email when they are deleted.
* `user.password.policy.pattern`: By default, Gravitee includes a strong password policy taken from OWASP recommendations. We highly recommend not decreasing the complexity of the password policy if you allow user registration.

{% hint style="info" %}
You can find other information related to user management in the [Gravitee documentation](https://documentation.gravitee.io/apim/getting-started/configuration/configure-apim-management-api/user-and-management-configuration).
{% endhint %}
