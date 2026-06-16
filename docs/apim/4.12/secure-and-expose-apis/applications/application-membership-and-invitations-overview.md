# Application Membership and Invitations Overview

## Overview

Application membership and invitations enable application owners and authorized members to manage team access directly from the Developer Portal. Users can add registered platform users as application members, invite external users by email, adjust member roles, transfer ownership, and manage pending invitations—all without administrator intervention. Administrators control feature availability through environment-level configuration toggles.

## Key Concepts

### Application Members

Application members are registered platform users who have been granted a role on a specific application. Each member has a single application role (e.g., USER, OWNER) that determines their permissions. Members can view application details, manage subscriptions, and—depending on their role—modify application settings or manage other members. The primary owner is the user with ultimate control over the application, including the ability to transfer ownership.

### Application Invitations

Application invitations are pending membership grants sent to users via email. When an invitation is created, the system checks whether the recipient email matches an existing registered user. If the email matches exactly one user, that user is added directly as an application member. If the email matches no registered user, a pending invitation is created and optionally sent via email notification. Invitations include a role assignment and a confirmation URL. When the recipient accepts the invitation, the system creates or updates their user account, grants the specified application role, and assigns default organization and environment roles required for portal access.

### Ownership Transfer

Ownership transfer reassigns the primary owner role from the current owner to another registered application member. The current owner selects a target member and assigns themselves a new application role (e.g., USER). This operation is atomic: the target becomes the new primary owner, and the former owner assumes the specified role. Only the current primary owner can initiate a transfer, and the target must already be an application member.

### JWT Token Actions

JWT tokens encode invitation and registration actions using the `ACTION` claim. Supported actions include `USER_REGISTRATION` (new user registration), `GROUP_INVITATION` (group membership invitation), `APPLICATION_INVITATION` (application membership invitation), `RESET_PASSWORD` (password reset flow), and `USER_CREATION` (user creation flow). Each token includes an `EMAIL` claim and an optional `subject` claim for existing user IDs. Tokens are signed using HMAC256 with the `jwt.secret` configuration property and verified against the `jwt.issuer` claim.

### Invitation Search and Sorting

Invitation search supports filtering by email address using case-insensitive partial matching. The repository search method accepts sortable columns: `id`, `referenceType`, `referenceId`, `email`, `apiRole`, `applicationRole`, `createdAt`, and `updatedAt`. The default sort order is by `email` ascending. Case-insensitive sortable columns use the SQL pattern `ORDER BY CASE WHEN <field> IS NULL THEN 1 ELSE 0 END, LOWER(<field>) ASC`, which sorts NULL values first followed by case-insensitive ascending order. The MongoDB invitation index uses case-insensitive collation (SECONDARY strength, English locale) on `referenceId`, `referenceType`, and `email` fields.

## Prerequisites

* The Gravitee API Management platform must be deployed and accessible.
* The `jwt.secret` configuration property must be set to a value of at least 256 bits for invitation token signing and verification. The system throws an `IllegalStateException` if this value is missing or empty.
* User registration must be enabled for invitation acceptance to create new user accounts. For portal context, the `PORTAL_USERCREATION_ENABLED` parameter (ENVIRONMENT scope) must be enabled. For console context, the `CONSOLE_USERCREATION_ENABLED` parameter (ORGANIZATION scope) must be enabled. If disabled, the system throws a `UserRegistrationUnavailableException`.
* Users must have the `MEMBER[R]` permission on the application to view the Members or Invitations tabs.
* Users must have the `MEMBER[C]` permission to add members or create invitations.
* Users must have the `MEMBER[U]` permission to update member roles, update invitation roles, or transfer ownership.
* Users must have the `MEMBER[D]` permission to delete members or invitations.
* Users must have the `APPLICATION_MEMBER[R]` permission to enrich user search results with application membership metadata. If this permission is missing when application membership enrichment is requested, the system returns `403 Forbidden`.

## Gateway Configuration

### JWT Token Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `jwt.secret` | HMAC256 secret for signing and verifying invitation and registration tokens. Must be at least 256 bits long. The system throws an `IllegalStateException` if this value is missing or empty. | `your-256-bit-secret-key` |
| `jwt.issuer` | Issuer claim included in JWT tokens. Used during token verification. If not configured, the system uses the `DEFAULT_JWT_ISSUER` constant. | `gravitee-management-auth` |

### Portal Next Feature Toggles

| Property | Description | Default |
|:---------|:------------|:--------|
| `portal.next.applications.membership.enabled` | Enable application membership management in Portal Next. When `false`, the Members and Invitations tabs are hidden. | `false` |
| `portal.next.applications.membership.invitations.enabled` | Enable application membership invitations in Portal Next. When `false`, the Invitations tab and invitation creation actions are hidden. Requires `portal.next.applications.membership.enabled` to be `true`. | `false` |
| `portal.next.applications.membership.transferOwnership.enabled` | Enable ownership transfer in Portal Next. When `false`, the transfer ownership button is hidden. Requires `portal.next.applications.membership.enabled` to be `true`. | `false` |

All `portal.next.*` properties use `ENVIRONMENT` reference scope with reference ID `"DEFAULT"`.
