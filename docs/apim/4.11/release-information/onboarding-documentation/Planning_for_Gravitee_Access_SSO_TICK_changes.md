# Planning for Gravitee Access and SSO

This page outlines the strategy for securing the Gravitee ecosystem. While we recommend delegating authentication to an external identity provider (IdP) for production environments, you can also manage users locally. Learn how to transition to a federated identity model (SSO) and how to manage and harden local authentication for specific use cases or air-gapped deployments.

## Deliverables

* **Authentication Strategy:** Selection of federated SSO (OIDC or SAML) or managed local authentication.
* **Automated Provisioning:** SCIM or Just-In-Time (JIT) provisioning for SSO users.
* **Access Control Model:** Defined RBAC mapping for both local and external users.
* **Security Hardening:** Removal of default credentials and configuration of account recovery paths.

## Stakeholders

Involve the following stakeholders in access planning:

* **IAM Team:** To provide IdP credentials if using SSO.
* **Security and CISO Office:** To approve password policies for local users or MFA for SSO.
* **Platform Engineers:** To configure `gravitee.yml` and manage system installation.
* **Support and Help Desk:** To define the workflow for password resets and account recovery.

## Prerequisites

* **License:** Gravitee Enterprise Edition is required for advanced IdP and SCIM features.
* **People:** An administrator with access to the server filesystem to make `gravitee.yml` changes.
* **Knowledge:** Understanding of OIDC or SAML for SSO or Bcrypt hashing for local users.

## Anticipated Duration

* **Days 1 to 2:** Requirement gathering (SSO versus local) and security policy definition.
* **Days 3 to 4:** Implementation of the chosen provider and attribute and role mapping.
* **Day 5:** Security hardening, removal of default accounts, and failover testing.

## Potential Risks and Challenges

* **Local User Overhead:** Managing users locally increases administrative burden and the risk of orphan accounts.
* **Single Point of Failure:** If the IdP is unavailable, SSO users are locked out.
* **Security Gaps:** Local accounts often lack the advanced MFA and threat detection provided by modern IdPs.
* **Credential Exposure:** Improperly secured local passwords or default accounts, such as `admin/admin`, pose a significant breach risk.

## Actions and Activities

### Select Your Identity Source
Decide whether to use an external IdP or manage users within Gravitee:

* **External IdP:** Register Gravitee as an application in your corporate IdP, such as Microsoft Entra ID or Okta.
* **Local Users:** Define your user list within the security section of your configuration.

### Configure Authentication in Gravitee
Update your `gravitee.yml` file based on your selection:

* **For SSO:** Provide the Client ID, secret, and discovery endpoint. Disable `localLogin` to enforce SSO-only access.
* **For Local Authentication:** Ensure all users have a secure, hashed password using Bcrypt.

### Establish Role and Group Mapping
Ensure users have the correct permissions immediately upon login:

* **SSO:** Map IdP attributes, such as `department`, to Gravitee groups.
* **Local Authentication:** Manually assign users to the appropriate groups and roles, such as `API_PUBLISHER`.

### Remove or Secure Default Accounts
Address default accounts created during installation, such as `admin`, `user`, and `api1`, before production:

1. Change the default `admin` password using a secure hash.
2. Disable the account entirely by setting `adminAccountEnable: false`.

### Define the Emergency Access Path
Regardless of your SSO choice, maintain one emergency local account:

* **Emergency Admin:** Create a local account that is not linked to SSO. Store the 32-character password in a secure location to ensure access if the IdP is unavailable.

## Best Practices

{% hint style="info" %}
If you have multiple sources, such as some users in a database and others in LDAP, Gravitee can federate them into a single login layer. This allows you to support different types of users simultaneously.
{% endhint %}

### Use Local Authentication Appropriately
While Gravitee recommends SSO for production, local authentication is appropriate for:
* Initial discovery phases or proofs of concept (PoCs).
* Air-gapped environments with no connection to an external IdP.
* Creating emergency "break-glass" administrator accounts.

### Define Password Reset Workflows
Local users do not have a self-service password reset feature by default. You must define a workflow where users contact an administrator to update their password hash in the configuration or database. An external IdP is preferred for a better user experience.
