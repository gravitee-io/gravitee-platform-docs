# Configure Application Membership Features

## Prerequisites

Before configuring application membership features, ensure the following:

* User must have an active account on the Gravitee platform
* For member management: user must have `MEMBER[R]` permission to view members, `MEMBER[C]` to add members, `MEMBER[U]` to update roles or transfer ownership, `MEMBER[D]` to delete members
* For invitation management: `portal.next.applications.membership.invitations.enabled` must be `true` and user must have `MEMBER[R]` permission to view invitations
* For ownership transfer: `portal.next.applications.membership.transferOwnership.enabled` must be `true`, user must be the current primary owner, and user must have `MEMBER[U]` permission
* JWT secret must be configured (`jwt.secret` property, minimum 256 bits) for invitation token generation and validation
* Default organization and environment roles must be defined for new user registration
* User registration must be enabled (`Key.CONSOLE_USERCREATION_ENABLED` for organization context, `Key.PORTAL_USERCREATION_ENABLED` for environment context)

## Gateway Configuration

### Portal Next Feature Toggles

| Property | Description | Example |
|:---------|:------------|:--------|
| `portal.next.applications.membership.enabled` | Enables application membership settings in Portal Next. When `false`, the Members tab is hidden. | `true` |
| `portal.next.applications.membership.transferOwnership.enabled` | Enables transfer of application ownership feature. When `false`, the Transfer Ownership button is hidden. | `false` |
| `portal.next.applications.membership.invitations.enabled` | Enables application membership invitation feature. When `false`, the Invitations tab is hidden. | `false` |

Portal Next keys use `ENVIRONMENT` reference type with reference ID `"DEFAULT"`.

### JWT Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `jwt.secret` | JWT signing secret; must be at least 256 bits. Throws `IllegalStateException` with message "JWT secret is mandatory" if missing or empty. | (required) |
| `jwt.issuer` | JWT issuer claim used for token verification. | `DEFAULT_JWT_ISSUER` |
