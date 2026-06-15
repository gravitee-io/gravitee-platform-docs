# Application Membership Concepts and Configuration

## Overview

Application membership management enables application owners and authorized members to control who has access to an application directly from the Developer Portal. Users can add registered platform users, invite new users by email, adjust member roles, transfer ownership, and manage pending invitations without administrator intervention. Administrators control feature availability through configuration toggles.

## Key Concepts

### Application Members

Application members are registered platform users who have been granted a role within a specific application. Members can view application details, manage subscriptions, and perform other actions based on their assigned role. The member list displays each user's display name, email, role, and membership timestamps. Users with `APPLICATION_MEMBER[READ]` permission can view the member list; users with `APPLICATION_MEMBER[CREATE]`, `APPLICATION_MEMBER[U]`, or `APPLICATION_MEMBER[D]` permissions can modify memberships.

### Application Invitations

Application invitations allow users to grant application access to people who are not yet members by entering their email address and selecting a role. When an invitation targets an email address that already belongs to a registered user, the system adds that user directly as an application member instead of creating a pending invitation. For unknown email addresses, the system creates a pending invitation and optionally sends a notification email with a confirmation URL. Invited users accept the invitation through the Developer Portal, which creates or updates their user account, assigns the invited role, and grants default organization and environment roles required for portal access.

### Application Roles

Application roles define the permissions a member has within an application. Roles are configured at the organization level and include both system roles (e.g., `PRIMARY_OWNER`) and custom roles. The `PRIMARY_OWNER` role identifies the application owner and cannot be assigned via direct member addition (only via invitation or ownership transfer). System roles and roles with empty names are excluded from role selection dropdowns. Each application must have exactly one primary owner at all times. Assignable roles are filtered to exclude roles where `name` is empty, `system` is `true`, or `name` equals `APPLICATION_PRIMARY_OWNER_ROLE_NAME`.

### Ownership Transfer

Ownership transfer allows the current primary owner to designate a new primary owner for the application. The transfer can target an existing application member or any other registered platform user. During the transfer, the current owner is reassigned to a different role (selected by the user), and the new owner receives the `PRIMARY_OWNER` role. This supports team continuity when ownership changes without requiring administrator intervention.

### JWT Token Structure

Invitation and registration tokens use JWT with HMAC256 signing. The token contains the following claims:

| Claim | Type | Description |
|:------|:-----|:------------|
| `ACTION` | String | Action type: `USER_REGISTRATION`, `GROUP_INVITATION`, `APPLICATION_INVITATION`, `RESET_PASSWORD`, or `USER_CREATION` |
| `EMAIL` | String | User email address |
| `subject` | `Optional<String>` | Existing user ID (present for invitation acceptance, absent for new user registration) |
| `issuer` | String | JWT issuer claim (validated against `jwt.issuer` configuration value) |

The decoded token is represented as:

```java
public record DecodedToken(
    String action,           // ACTION enum name
    String email,            // User email
    Optional<String> subject // Existing user ID (if any)
)
```

Token verification uses `Algorithm.HMAC256(jwt.secret)` and validates the issuer claim against the `jwt.issuer` configuration property. Verification failures throw `JWTVerificationException`.

### Invitation Repository

The invitation repository supports two search methods:

- `findByEmail(String email)`: Returns `List<Invitation>` for all invitations matching the email address
- `search(InvitationCriteria criteria, Sortable sortable, Pageable pageable)`: Returns `Page<Invitation>` with pagination and sorting

**InvitationCriteria:**

```java
public record InvitationCriteria(
    String referenceId,
    String referenceType,
    String email
)
```

**Sortable Columns:**

- Supported fields: `id`, `referenceType`, `referenceId`, `email`, `apiRole`, `applicationRole`, `createdAt`, `updatedAt`
- Default sort field: `email`
- Case-insensitive sorting applies to: `id`, `referenceType`, `referenceId`, `email`, `apiRole`, `applicationRole`

**MongoDB Index:**

- Collection: `invitations`
- Index name: `ri1rt1e1`

**JDBC Search:** Invitation search on MariaDB and MySQL uses LIKE clause escaping to prevent `BadSqlGrammarException` (fixed in PR #16907).

## Prerequisites

- User must have `APPLICATION_MEMBER[READ]` permission to view members and invitations
- User must have `APPLICATION_MEMBER[CREATE]` permission to add members or create invitations
- User must have `APPLICATION_MEMBER[U]` permission to update member roles, edit invitations, resend invitations, or transfer ownership
- User must have `APPLICATION_MEMBER[D]` permission to delete members or invitations
- User must be the current application owner to transfer ownership
- `jwt.secret` configuration property must be set (required for invitation token generation and verification)
- `portal.next.applications.membership.enabled` must be `true` to enable application membership features
- `portal.next.applications.membership.invitations.enabled` must be `true` to enable invitation creation and management
- `portal.next.applications.membership.transferOwnership.enabled` must be `true` to enable ownership transfer
- User registration must be enabled (checked via `Key.PORTAL_USERCREATION_ENABLED` or `Key.CONSOLE_USERCREATION_ENABLED`) for invitation acceptance

## Gateway Configuration

### JWT Token Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `jwt.secret` | HMAC256 secret for JWT token signing and verification. Required for invitation token generation. System throws `IllegalStateException` with message "JWT secret is mandatory" if missing or empty. | `your-secret-key` |
| `jwt.issuer` | JWT issuer claim used in token verification. Defaults to `DEFAULT_JWT_ISSUER` if not configured. | `gravitee-management-auth` |

### Portal Next Feature Toggles

| Property | Description | Example |
|:---------|:------------|:--------|
| `portal.next.applications.membership.enabled` | Enable application membership settings in Portal Next. When `false`, the Members tab is hidden from application details. | `false` (default) |
| `portal.next.applications.membership.invitations.enabled` | Enable application membership invitations in Portal Next. When `false`, the Invitations tab and invitation creation actions are hidden. | `false` (default) |
| `portal.next.applications.membership.transferOwnership.enabled` | Enable transfer of application ownership in Portal Next. When `false`, the Transfer Ownership button is hidden from the Members tab. | `false` (default) |
