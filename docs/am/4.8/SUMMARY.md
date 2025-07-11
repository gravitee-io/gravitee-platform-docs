# Table of contents

## Overview

* [Introduction to Gravitee Access Management (AM)](README.md)
* [AM Architecture](overview/am-architecture/README.md)
  * [Control Plane & Data Plane](overview/am-architecture/control-plane-and-data-plane.md)
* [Plugins](overview/plugins/README.md)
  * [Compatibility Matrices](overview/plugins/compatibility-matrices.md)
* [Gravitee AM Enterprise Edition](overview/open-source-vs-enterprise-am/README.md)
  * [Enterprise Edition Licensing](https://documentation.gravitee.io/platform-overview/gravitee-essentials/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing)

## Getting Started

* [Install & Upgrade Guides](getting-started/install-and-upgrade-guides/README.md)
  * [Quick Install](getting-started/install-and-upgrade-guides/quick-install.md)
  * [Run in Docker](getting-started/install-and-upgrade-guides/run-in-docker/README.md)
    * [Docker Images Install](getting-started/install-and-upgrade-guides/run-in-docker/docker-images-install.md)
    * [Docker Compose Install](getting-started/install-and-upgrade-guides/run-in-docker/docker-compose-install.md)
  * [Install with .ZIP](getting-started/install-and-upgrade-guides/install-with-.zip.md)
  * [Install on Red Hat](getting-started/install-and-upgrade-guides/install-on-red-hat.md)
  * [Install on Amazon](getting-started/install-and-upgrade-guides/install-on-amazon.md)
  * [Deploy in Kubernetes](getting-started/install-and-upgrade-guides/deploy-in-kubernetes.md)
  * [Configure a Production-ready AM Environment](getting-started/install-and-upgrade-guides/configure-a-production-ready-am-environment.md)
  * [4.5 Upgrade Guide](getting-started/install-and-upgrade-guides/upgrade-guide.md)
  * [4.7 Upgrade Guide](getting-started/install-and-upgrade-guides/4.7-upgrade-guide.md)
  * [Configure Gateway Resilience Mode](getting-started/install-and-upgrade-guides/configure-gateway-resilience-mode.md)
  * [Configure Multiple Data Planes](getting-started/install-and-upgrade-guides/configure-multiple-data-planes.md)
  * [Breaking changes for Access Management](getting-started/install-and-upgrade-guides/breaking-changes-for-access-management.md)
* [Configuration](getting-started/configuration/README.md)
  * [AM Gateway](getting-started/configuration/configure-am-gateway/README.md)
    * [Internal API](getting-started/configuration/configure-am-gateway/internal-api.md)
  * [AM API](getting-started/configuration/configure-am-api/README.md)
    * [Internal API](getting-started/configuration/configure-am-api/internal-api.md)
  * [AM Console](getting-started/configuration/configure-am-console.md)
  * [Repositories & DataPlane](getting-started/configuration/configure-repositories.md)
  * [Reporters](getting-started/configuration/configure-reporters.md)
  * [Monitoring](getting-started/configuration/configure-monitoring.md)
  * [Secret Providers](getting-started/configuration/secret-providers.md)
* [Tutorial: Getting Started with AM](getting-started/tutorial-getting-started-with-am/README.md)
  * [Log in to AM Console](getting-started/tutorial-getting-started-with-am/login-to-am-console.md)
  * [Set Up Your First Application](getting-started/tutorial-getting-started-with-am/set-up-your-first-application.md)
  * [Get User Profile Information](getting-started/tutorial-getting-started-with-am/get-user-profile-information.md)
  * [Secure Your APIs](getting-started/tutorial-getting-started-with-am/secure-your-apis/README.md)
    * [Configure Generic OAuth2 Authorization Server](getting-started/tutorial-getting-started-with-am/secure-your-apis/configure-generic-oauth2-authorization-server.md)
    * [Configure Gravitee.io Access Management](getting-started/tutorial-getting-started-with-am/secure-your-apis/configure-gravitee.io-access-management.md)
  * [Configure a Flow](getting-started/tutorial-getting-started-with-am/configure-a-flow.md)
  * [Add Custom Claims to Tokens](getting-started/tutorial-getting-started-with-am/add-custom-claims-to-tokens.md)

## Guides

* [Prologue](guides/prologue.md)
* [Auth Protocols](guides/auth-protocols/README.md)
  * [OAuth 2.0](guides/auth-protocols/oauth-2.0/README.md)
    * [Which Flow Should I Use?](guides/auth-protocols/oauth-2.0/which-flow-should-i-use.md)
    * [Proof Key for Code Exchange (PKCE)](guides/auth-protocols/oauth-2.0/proof-key-for-code-exchange-pkce.md)
    * [Best Practices](guides/auth-protocols/oauth-2.0/best-practices.md)
    * [Refresh Tokens](guides/auth-protocols/oauth-2.0/refresh-tokens.md)
    * [Extension Grants](guides/auth-protocols/oauth-2.0/extension-grants.md)
    * [Dynamic Redirect URI Parameters](guides/auth-protocols/oauth-2.0/dynamic-redirect-uri-parameters.md)
  * [OpenID Connect](guides/auth-protocols/openid-connect.md)
  * [UMA 2.0](guides/auth-protocols/uma-2.0.md)
  * [SCIM 2.0](guides/auth-protocols/scim-2.0.md)
  * [Open Banking](guides/auth-protocols/open-banking.md)
  * [CIBA](guides/auth-protocols/ciba.md)
  * [SAML 2.0](guides/auth-protocols/saml-2.0.md)
* [Security Domains](guides/security-domains.md)
* [Identity Providers](guides/identity-providers/README.md)
  * [Create an Identity Provider](guides/identity-providers/create-an-identity-provider.md)
  * [User, Role and Group Mapping](guides/identity-providers/user-and-role-mapping.md)
  * [Enterprise Identity Providers](guides/identity-providers/enterprise-identity-providers/README.md)
    * [Active Directory/LDAP](guides/identity-providers/enterprise-identity-providers/active-directory-ldap.md)
    * [HTTP (web service)](guides/identity-providers/enterprise-identity-providers/http-web-service.md)
    * [Kerberos](guides/identity-providers/enterprise-identity-providers/kerberos.md)
    * [SAML 2.0](guides/identity-providers/enterprise-identity-providers/saml-2.0.md)
    * [CAS](guides/identity-providers/enterprise-identity-providers/cas.md)
  * [Social Identity Providers](guides/identity-providers/social-identity-providers/README.md)
    * [OpenID Connect](guides/identity-providers/social-identity-providers/openid-connect.md)
    * [Azure AD](guides/identity-providers/social-identity-providers/azure-ad.md)
    * [Facebook](guides/identity-providers/social-identity-providers/facebook.md)
    * [Github](guides/identity-providers/social-identity-providers/github.md)
    * [Twitter](guides/identity-providers/social-identity-providers/twitter.md)
    * [LinkedIn](guides/identity-providers/social-identity-providers/linkedin.md)
    * [Salesforce](guides/identity-providers/social-identity-providers/salesforce.md)
  * [Legal Identity Providers](guides/identity-providers/legal-identity-providers/README.md)
    * [FranceConnect](guides/identity-providers/legal-identity-providers/franceconnect.md)
  * [Database Identity Providers](guides/identity-providers/database-identity-providers/README.md)
    * [JDBC](guides/identity-providers/database-identity-providers/jdbc.md)
    * [MongoDB](guides/identity-providers/database-identity-providers/mongodb.md)
    * [Inline](guides/identity-providers/database-identity-providers/inline.md)
* [Applications](guides/applications/README.md)
  * [Client Secrets](guides/applications/client-secrets.md)
* [Branding](guides/branding/README.md)
  * [CSS Custom Variables Reference](guides/branding/css-custom-variables-reference.md)
  * [Language Default Properties Reference](guides/branding/language-default-properties-reference.md)
* [Bot Detection](guides/bot-detection.md)
* [Device Identifier](guides/device-identifier.md)
* [Login](guides/login/README.md)
  * [Step-up Authentication](guides/login/step-up-authentication.md)
  * [Adaptive Multi-factor Authentication](guides/login/adaptive-multi-factor-authentication.md)
  * [Risk-based MFA](guides/login/risk-based-mfa.md)
  * [Remember Authentication Device](guides/login/remember-authentication-device.md)
  * [Passwordless (W3C Webauthn)](guides/login/passwordless-w3c-webauthn.md)
  * [Silent Reauthentication](guides/login/silent-reauthentication.md)
  * [Identifier-first Login Flow](guides/login/identifier-first-login-flow.md)
  * [Hide Login Form](guides/login/hide-login-form.md)
  * [Redirect Users After Login](guides/login/redirect-users-after-login.md)
* [Multi-factor Authentication](guides/multi-factor-authentication/README.md)
  * [Managing Factors](guides/multi-factor-authentication/managing-factors/README.md)
    * [Email](guides/multi-factor-authentication/managing-factors/email.md)
    * [One-time-password (OTP)](guides/multi-factor-authentication/managing-factors/one-time-password-otp.md)
    * [SMS](guides/multi-factor-authentication/managing-factors/sms.md)
    * [Phone Call](guides/multi-factor-authentication/managing-factors/phone-call.md)
    * [MFA with FIDO2](guides/multi-factor-authentication/managing-factors/mfa-with-fido2.md)
    * [Alternative Methods](guides/multi-factor-authentication/managing-factors/alternative-methods.md)
    * [Recovery Codes](guides/multi-factor-authentication/managing-factors/recovery-codes.md)
    * [HTTP Factor](guides/multi-factor-authentication/managing-factors/http-factor.md)
  * [Configure MFA for an Application](guides/multi-factor-authentication/configure-mfa-for-an-application.md)
  * [MFA Brute Force and Rate Limit](guides/multi-factor-authentication/mfa-brute-force-and-rate-limit.md)
  * [Manage User MFA](guides/multi-factor-authentication/manage-user-mfa.md)
  * [MFA Policies](guides/multi-factor-authentication/mfa-policies.md)
* [Resources](guides/resources.md)
* [Certificates](guides/certificates/README.md)
  * [AWS Certificate plugin](guides/certificates/aws-certificate-plugin.md)
  * [AWS CloudHSM plugin](guides/certificates/aws-cloudhsm-plugin.md)
* [User Management](guides/user-management/README.md)
  * [Users](guides/user-management/users/README.md)
    * [Password Options](guides/user-management/users/password-options.md)
  * [User attributes](guides/user-management/user-attributes.md)
  * [Groups](guides/user-management/groups.md)
  * [Roles](guides/user-management/roles.md)
  * [User Registration](guides/user-management/user-registration.md)
  * [Account Linking](guides/user-management/account-linking.md)
  * [SCIM 2.0](guides/user-management/scim-2.0.md)
  * [User Consent](guides/user-management/user-consent.md)
  * [Password Policy](guides/user-management/password-policy.md)
  * [Self-service Account Management](guides/user-management/self-service-account-management.md)
* [Session Management](guides/session-management.md)
* [Audit Trail](guides/audit-trail.md)
* [Alerts](guides/alerts/README.md)
  * [Manage Alerts](guides/alerts/manage-alerts.md)
  * [Notification Channels](guides/alerts/notification-channels.md)
* [Flows](guides/flows.md)
* [Administration](guides/administration.md)
* [AM Expression Language](guides/am-expression-language.md)
* [Developer Contributions](guides/developer-contributions.md)

## Reference

* [API Reference](reference/am-api-reference.md)

## Releases & Changelog

* [Release Notes](releases-and-changelog/release-notes/README.md)
  * [AM 4.8](releases-and-changelog/release-notes/am-4.8.md)
  * [AM 4.7](https://documentation.gravitee.io/am/4.7/releases-and-changelog/release-notes/am-4.7)
  * [AM 4.6](https://documentation.gravitee.io/am/releases-and-changelog/release-notes/am-4.6)
  * [AM 4.5](https://documentation.gravitee.io/am/4.5/releases-and-changelog/release-notes/am-4.5)
  * [AM 4.4](https://documentation.gravitee.io/am/4.4/releases-and-changelog/release-notes/am-4.4)
  * [AM 4.3](https://documentation.gravitee.io/am/4.3/releases-and-changelog/release-notes/am-4.3)
  * [AM 4.2](https://documentation.gravitee.io/am/4.2/releases-and-changelog/release-notes/am-4.2)
  * [AM 4.1](https://documentation.gravitee.io/am/4.1/releases-and-changelog/release-notes/am-4.1)
  * [AM 4.0](https://documentation.gravitee.io/am/4.0/releases-and-changelog/release-notes/am-4.0)
* [Changelog](releases-and-changelog/changelog/README.md)
  * [AM 4.8.x](releases-and-changelog/changelog/am-4.8.x.md)
  * [AM 4.7.x](https://documentation.gravitee.io/am/4.7/releases-and-changelog/changelog/am-4.7.x)
  * [AM 4.6.x](https://documentation.gravitee.io/am/4.6/releases-and-changelog/changelog/am-4.6.x)
  * [AM 4.5.x](https://documentation.gravitee.io/am/4.5/releases-and-changelog/changelog/am-4.5.x)
  * [AM 4.4.x](https://documentation.gravitee.io/am/4.4/releases-and-changelog/changelog/am-4.4.x)
  * [AM 4.3.x](https://documentation.gravitee.io/am/4.3/releases-and-changelog/changelog/am-4.3.x)
  * [AM 4.2.x](https://documentation.gravitee.io/am/4.2/releases-and-changelog/changelog/am-4.2.x)
  * [AM 4.1.x](https://documentation.gravitee.io/am/4.1/releases-and-changelog/changelog/am-4.1.x)
  * [AM 4.0.x](https://documentation.gravitee.io/am/4.0/releases-and-changelog/changelog/am-4.0.x)

## Community & Support

* [Enterprise Support](community-and-support/enterprise-support.md)
* [Community](community-and-support/community/README.md)
  * [Support](https://community.gravitee.io/c/support/11)
  * [Roadmap & Feedback](https://www.gravitee.io/user-feedback)
  * [Announcements & Events](https://community.gravitee.io/c/announcements/5)
