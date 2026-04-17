---
description: Complete reference of all available AM plugins from the Gravitee Marketplace.
hidden: true
noIndex: true
---

# AM Plugin Reference

This page catalogs all AM plugins available through the [Gravitee Marketplace](https://www.gravitee.io/plugins). Plugins that have dedicated documentation pages are linked directly. All other plugins include their full marketplace documentation inline.

## AM Reporter

### File

**Plugin ID**: `gravitee-am-reporter-file`

*No additional documentation available.*

### JDBC

**Plugin ID**: `gravitee-am-reporter-jdbc`

*No additional documentation available.*

### Kafka

**Plugin ID**: `gravitee-am-reporter-kafka`

*No additional documentation available.*

### Mongodb

**Plugin ID**: `gravitee-am-reporter-mongodb`

*No additional documentation available.*

## Bot Detection

### Bot Detection reCAPTCHA v3

**Plugin ID**: `gravitee-am-botdetection-recaptcha-v3`

→ [Full documentation](../../../guides/bot-detection.md)

## Certificate

### Certificate AWS

**Plugin ID**: `gravitee-am-certificate-aws`

→ [Full documentation](../../../guides/certificates/aws-certificate-plugin.md)

### Certificate HSM AWS

**Plugin ID**: `gravitee-am-certificate-hsm-aws`

→ [Full documentation](../../../guides/certificates/aws-cloudhsm-plugin.md)

### Certificate Javakeystore

**Plugin ID**: `gravitee-am-certificate-javakeystore`

*No additional documentation available.*

### Certificate PKCS12

**Plugin ID**: `gravitee-am-certificate-pkcs12`

*No additional documentation available.*

## Device Identifier

### Device Identifier FingerprintJS v3 Community

**Plugin ID**: `gravitee-am-deviceidentifier-fingerprintjs-v3-community`

→ [Full documentation](../../../guides/device-identifier.md)

### Device Identifier FingerprintJS v3 Pro

**Plugin ID**: `gravitee-am-deviceidentifier-fingerprintjs-v3-pro`

→ [Full documentation](../../../guides/device-identifier.md)

## Factor

### Authenticator CBA

**Plugin ID**: `gravitee-am-authenticator-cba`

→ [Full documentation](../../../guides/login/certificate-based-authentication.md)

### Authenticator Magic Link

**Plugin ID**: `gravitee-am-authenticator-magiclink`

→ [Full documentation](../../../guides/login/magic-link-authentication.md)

### Factor Call

**Plugin ID**: `gravitee-am-factor-call`

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/phone-call.md)

### Factor Email

**Plugin ID**: `gravitee-am-factor-email`

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/email.md)

### Factor FIDO2

**Plugin ID**: `gravitee-am-factor-fido2`

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/mfa-with-fido2.md)

### - Access Management - HTTP Factor

**Plugin ID**: `gravitee-am-factor-http` — Gravitee.io - Access Management - HTTP Factor

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/http-factor.md)

### Factor Mock

**Plugin ID**: `gravitee-am-factor-mock`

#### Gravitee.io - Access Management - Mock Factor


##### Description

With MFA Mock factor, you can easily test MFA feature

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the factor list `AM_UI -> Multifactor Auth -> Mock` to create and configure a new mock factor.

### Factor OTP

**Plugin ID**: `gravitee-am-factor-otp`

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/one-time-password-otp.md)

### Factor OTP Sender

**Plugin ID**: `gravitee-am-factor-otp-sender`

#### Gravitee.io - Access Management - OTP Sender Factor


##### Description

OTP Sender Factor allows user to verify identity security thanks to a code sent to their devices (SMS, Email, ...) during multi-factor authentication process.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

OTP Sender factor can be added as a MFA factor at: `AM_UI -> Settings -> Multifactor Auth -> OTP Sender Factor`.

### Factor Recovery Code

**Plugin ID**: `gravitee-am-factor-recovery-code`

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/recovery-codes.md)

### Factor SMS

**Plugin ID**: `gravitee-am-factor-sms`

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/sms.md)

## Identity Provider

### Identity Provider Azure AD

**Plugin ID**: `gravitee-am-identityprovider-azure-ad`

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/azure-ad.md)

### Identity Provider - CAS

**Plugin ID**: `gravitee-am-identityprovider-cas` — Gravitee.io AM - Identity Provider - CAS

→ [Full documentation](../../../guides/identity-providers/enterprise-identity-providers/cas.md)

### Identity Provider Facebook

**Plugin ID**: `gravitee-am-identityprovider-facebook`

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/facebook.md)

### Identity Provider FranceConnect

**Plugin ID**: `gravitee-am-identityprovider-franceconnect`

→ [Full documentation](../../../guides/identity-providers/legal-identity-providers/franceconnect.md)

### Identity Provider GitHub

**Plugin ID**: `gravitee-am-identityprovider-github`

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/github.md)

### Identity Provider Google

**Plugin ID**: `gravitee-am-identityprovider-google`

*No additional documentation available.*

### Identity Provider Gravitee

**Plugin ID**: `gravitee-am-identityprovider-gravitee`

This Identity Provider is dedicated to organization users. This implementation is based on the OrganizationUserService in order to access user information through the repositories. The UserProvider implementation mostly provide "empty" methods to avoid collision with the regular method of the service layer (create, delete) excepted for the `update` one that allow the password update.

### Identity Provider HTTP

**Plugin ID**: `gravitee-am-identityprovider-http`

→ [Full documentation](../../../guides/identity-providers/enterprise-identity-providers/http-web-service.md)

### Identity Provider HTTP Flow

**Plugin ID**: `gravitee-am-identityprovider-http-flow`

→ [Full documentation](../../../guides/identity-providers/enterprise-identity-providers/http-web-service.md)

### Identity Provider Inline

**Plugin ID**: `gravitee-am-identityprovider-inline`

→ [Full documentation](../../../guides/identity-providers/database-identity-providers/inline.md)

### Identity Provider JDBC

**Plugin ID**: `gravitee-am-identityprovider-jdbc`

→ [Full documentation](../../../guides/identity-providers/database-identity-providers/jdbc.md)

### Identity Provider - Kerberos

**Plugin ID**: `gravitee-am-identityprovider-kerberos` — Gravitee.io AM - Identity Provider - Kerberos

→ [Full documentation](../../../guides/identity-providers/enterprise-identity-providers/kerberos.md)

### Identity Provider LinkedIn

**Plugin ID**: `gravitee-am-identityprovider-linkedin`

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/linkedin.md)

### Identity Provider Mongo

**Plugin ID**: `gravitee-am-identityprovider-mongo`

→ [Full documentation](../../../guides/identity-providers/database-identity-providers/mongodb.md)

### Identity Provider OAuth2 Generic

**Plugin ID**: `gravitee-am-identityprovider-oauth2-generic`

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/openid-connect.md)

### Identity Provider Salesforce

**Plugin ID**: `gravitee-am-identityprovider-salesforce`

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/salesforce.md)

### Identity Provider - SAML

**Plugin ID**: `gravitee-am-identityprovider-saml` — Gravitee.io AM - Identity Provider - SAML

→ [Full documentation](../../../guides/identity-providers/enterprise-identity-providers/saml-2.0.md)

### Identity Provider Twitter

**Plugin ID**: `gravitee-am-identityprovider-twitter`

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/twitter.md)

## Other

#### Secret provider

### Secret Provider AWS

**Plugin ID**: `gravitee-secret-provider-aws`

→ [Full documentation](../../../getting-started/configuration/secret-providers.md)

### Secret Provider HC Vault

**Plugin ID**: `gravitee-secret-provider-hc-vault`

→ [Full documentation](../../../getting-started/configuration/secret-providers.md)

### Secret Provider Kubernetes

**Plugin ID**: `gravitee-secret-provider-kubernetes`

→ [Full documentation](../../../getting-started/configuration/secret-providers.md)

## Policy

### Account Linking

**Plugin ID**: `gravitee-am-policy-account-linking`

→ [Full documentation](../../../guides/user-management/account-linking.md)

### Enrich Auth Flow

**Plugin ID**: `gravitee-am-policy-enrich-auth-flow`

#### Enrich Authentication Flow Profile

##### Description

You can use the `enrich-auth-flow` policy to persist some information between the authentication steps.
These data will be automatically loaded into the execution context attributes through the `authFlow` entry. (`{#context.attributes['authFlow']['my-additional-attribute']}`)

##### Configuration

| Property | Required | Description | Type | Default |
| --- | --- | --- | --- | --- |
| properties | Yes |  |  |  |
| The information to get from the execution context |  |  |  |  |
| List of properties | - |  |  |  |

### Enrich Profile

**Plugin ID**: `gravitee-am-policy-enrich-profile`

#### Enrich User Profile

##### Description

You can use the `enrich-profile` policy to add some information to the user profile based on the AM execution context.

##### Configuration

| Property | Required | Description | Type | Default |
| --- | --- | --- | --- | --- |
| properties | Yes |  |  |  |
| The information to get from the execution context |  |  |  |  |
| List of properties | - | exitOnError | No |  |
| Terminate the request if there are an error |  |  |  |  |
| boolean | false |  |  |  |

### Enroll MFA

**Plugin ID**: `gravitee-am-policy-enroll-mfa`

#### Enroll MFA policy

##### Description

You can use the `enroll-mfa` policy to automatically enroll MFA factors based on the user profile information and that way skip
the interactive MFA enrollment step.

##### Configuration

| Property | Required | Description | Type | Default |
| --- | --- | --- | --- | --- |
| MFA Factor ID |  |  |  |  |
| Yes |  |  |  |  |
| The MFA factor to enroll |  |  |  |  |
| String |  |  |  |  |
| - |  |  |  |  |
| Value |  |  |  |  |
| Yes (except the HTTP MFA factor) |  |  |  |  |
| The value used to enroll the MFA factor (email, phone number, ...). Support EL. |  |  |  |  |
| String |  |  |  |  |
| - |  |  |  |  |
| Primary |  |  |  |  |
| Yes |  |  |  |  |
| Set this factor as a primary method for the end-user |  |  |  |  |
| boolean |  |  |  |  |
| false |  |  |  |  |

### MFA Challenge

**Plugin ID**: `gravitee-am-policy-mfa-challenge`

#### MFA Challenge policy


##### Description

You can use the `mfa-challenge` policy to enforce users to confirm their identity by using another factor.

> **Warning:** Enabling `Enroll factor if user has no MFA device` expects an authenticated user. This is why this option has to be disabled for `Reset Password` flow as it can lead to user error.

##### Configuration

| Property | Required | Description | Type |
| --- | --- | --- | --- |
| MFA Factor ID |  |  |  |
| Yes |  |  |  |
| The MFA factor to challenge |  |  |  |
| String |  |  |  |

### Send Email

**Plugin ID**: `gravitee-am-policy-send-email`

*No additional documentation available.*

## Protocol

### Protocol - SAML 2.0 Identity Provider

**Plugin ID**: `gravitee-am-gateway-handler-saml2-idp` — Gravitee.io AM - Protocol - SAML 2.0 Identity Provider

→ [Full documentation](../../../guides/auth-protocols/saml-2.0.md)

## Resource

### HTTP

**Plugin ID**: `gravitee-am-resource-http`

#### Gravitee.io - Access Management - HTTP Resource


##### Description

With HTTP Resource, send messages to all your customers, collaborators, via the media of your choice: sms, enriched sms, email, voice or fax.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the resource list `AM_UI -> Services -> HTTP` to create and configure a new resource.
This resource is used as a SMS/Email provider to send verification codes during multifactor authentication process.

### HTTP Factor

**Plugin ID**: `gravitee-am-resource-http-factor`

#### Gravitee.io - Access Management - HTTP Factor Resource


##### Description

HTTP Factor resource facilitates to send HTTP requests to and endpoint to receive response which can be used as per the user needs.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the resource list `AM_UI -> Services -> HTTP Factor` to create and configure a new HTTP Factor resource.
This resource can be used with SMS provider to complete send and check verification steps during multifactor authentication process.

### Infobip

**Plugin ID**: `gravitee-am-resource-infobip`

To use the plugin, create an account at [infobip site](https://www.infobip.com/), follow the instructions.
To create the resource at AM, you will need:
* Api Key: the authorization from the service
* Api Key prefix: Basic, App, IBSSO, Bearer
* base url: base url provided
* app id: id of the app
* message id: id of the message.

Any doubt, check the docs [here](https://www.infobip.com/docs/api)

### MFA Mock

**Plugin ID**: `gravitee-am-resource-mfa-mock`

#### Gravitee.io - Access Management - Mock Resource


##### Description

With MFA Mock resource, you can easily test factors like SMS, Email without third party services.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the resource list `AM_UI -> Services -> Mock` to create and configure a new resource.
This resource is used as a SMS, Email provider to validate a static code defined into the plugin configuration.

### - Access Management - Resource - Orange Contact Everyrone

**Plugin ID**: `gravitee-am-resource-orange-contact-everyone`

#### Gravitee.io - Access Management - Orange Contact Everyone Resource


##### Description

With Orange Contact Everyone service, send messages to all your customers, collaborators, via the media of your choice: sms, enriched sms, email, voice or fax.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the resource list `AM_UI -> Services -> Orange Contact Everyone` to create and configure a new resource.
This resource is used as a SMS provider to send verification codes during multifactor authentication process.

### SFR

**Plugin ID**: `gravitee-am-resource-sfr`

#### Gravitee.io - Access Management - SFR DMC API Resource


##### Description

With SFR DMC API, send messages to all your customers, collaborators, via the media of your choice: sms, enriched sms, email, voice or fax.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the resource list `AM_UI -> Services -> SFR DMC API` to create and configure a new resource.
This resource is used as a SMS provider to send verification codes during multifactor authentication process.

### SMTP

**Plugin ID**: `gravitee-am-resource-smtp`

*No additional documentation available.*

### Twilio

**Plugin ID**: `gravitee-am-resource-twilio`

#### Gravitee.io - Access Management - HTTP Twilio Resource

##### Description

HTTP Twilio resource facilitates integration with Twilio.

⚠️ This plugin is compatible with Gravitee.io Access Management v4.0.0 and above.
