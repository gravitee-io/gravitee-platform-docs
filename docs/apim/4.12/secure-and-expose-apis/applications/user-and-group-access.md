---
description: An overview about user and group access.
metaLinks:
  alternates:
    - user-and-group-access.md
---

# User and Group Access

## Overview

An application's **User and group access** page lets you manage user and group access to individual applications. Application membership management enables you to control who can access and manage applications. You can add members directly, invite external users by email, transfer application ownership, and assign role-based permissions. This feature supports both immediate member addition for existing platform users and invitation-based onboarding for new users.

## Key Concepts

### Application Members

Application members are platform users assigned to an application with a specific role. Members can view, modify, or manage the application based on their assigned permissions. Each application has one PRIMARY_OWNER and may have multiple members with other roles, such as USER or OWNER. Members are added either directly for existing users or through the invitation workflow for new users.

### Application Invitations

Application invitations enable you to onboard users who do not yet have platform accounts. When an invitation is created, the system sends an email containing a registration link with a JWT token. Recipients complete registration by providing their name and password, after which they are automatically added as application members with the invited role. Invitations remain pending until accepted or deleted.

### Roles and Permissions

Application roles define member capabilities within an application. Roles are organization-scoped and include both system roles, such as PRIMARY_OWNER, and custom roles. System roles and PRIMARY_OWNER cannot be assigned during member creation or invitation. The PRIMARY_OWNER role is unique per application and can only be transferred through the ownership transfer workflow. Role assignment is validated against the organization's role catalog.

### Membership Enrichment

User search results can include application membership status when the `includes.applicationMembership` parameter is provided. The response metadata contains a map keyed by user IDs indicating whether each user is already a member of the specified application. This enrichment enables you to filter out existing members when adding new ones.

## Prerequisites

Before managing application membership, ensure the following requirements are met:

* You must have `APPLICATION_MEMBER[CREATE]` permission to add members or create invitations
* You must have `APPLICATION_MEMBER[READ]` permission to view members or invitations
* You must have `APPLICATION_MEMBER[UPDATE]` permission to edit member roles, update invitations, resend invitations, or transfer ownership
* You must have `APPLICATION_MEMBER[DELETE]` permission to remove members or delete invitations
* `portal.next.applications.membership.enabled` must be set to `true` to access membership features
* `portal.next.applications.membership.invitations.enabled` must be set to `true` to access invitation features
* `portal.next.applications.membership.transferOwnership.enabled` must be set to `true` to access ownership transfer
* `jwt.secret` must be configured for invitation token generation and validation
* You must enable user registration using `PORTAL_USERCREATION_ENABLED` or `CONSOLE_USERCREATION_ENABLED` for invitation acceptance
* Default ORGANIZATION and ENVIRONMENT roles must be configured in organization settings

## Gateway Configuration

### Membership Feature Toggles

| Property | Description | Example |
|:---------|:------------|:--------|
| `portal.next.applications.membership.enabled` | Enables application membership settings in Portal Next. When disabled, the Members and Invitations tabs are hidden. | `true` |
| `portal.next.applications.membership.transferOwnership.enabled` | Enables the transfer ownership feature. When disabled, the Transfer Ownership button is hidden even if you are the current owner. | `false` |
| `portal.next.applications.membership.invitations.enabled` | Enables the application invitation feature. When disabled, the Invitations tab is hidden and invitation creation is disabled. | `false` |

All membership properties are scoped to `ENVIRONMENT` reference type.

### JWT Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `jwt.secret` | Secret key used to sign and verify JWT tokens for invitation links. Required for invitation functionality. | `your-secret-key` |
| `jwt.issuer` | Issuer claim value used during token verification. | `gravitee-management-auth` |

### User Registration Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `PORTAL_USERCREATION_ENABLED` | Enables the **Allow User Registration** setting in Portal. Required for invitation acceptance in Portal context. | `true` |
| `CONSOLE_USERCREATION_ENABLED` | Enables the **Allow User Registration** setting in Console. Required for invitation acceptance in Console context. | `true` |

## Configure user and group access

To configure user and group access, complete the following steps:

1. [create-an-application.md](create-an-application.md "mention").
2. Log in to your APIM Console, and then click **Applications**.
3.  Find the application you want to configure. Use the radio buttons to select either Active or Archived applications. Next, either scroll through the paginated lists of available applications or use the search field to find the application by name.

    <figure><img src="../../.gitbook/assets/00 groups added to applications 7.png" alt=""><figcaption></figcaption></figure>
4. Click on the application you want to configure.
5.  Click on **User and group access** in the Application menu.

    <figure><img src="../../.gitbook/assets/00 groups added to applications 8.png" alt=""><figcaption></figcaption></figure>

### Members

Under the **Members** tab, you can add users or groups as members of your application and define their roles to manage and perform tasks and operations. The Members tab is visible when `portal.next.applications.membership.enabled` is `true` and you have `APPLICATION_MEMBER[READ]` permission.

<figure><img src="../../.gitbook/assets/00 groups added to applications 3.png" alt=""><figcaption></figcaption></figure>

* Click **+ Add members** to add members to your application. You can search for users by name or email.
* Use the **Role** drop-down menu to select member roles, which grant specific permissions. For more information on roles, please refer to the [Roles](../../configure-and-manage-the-platform/manage-organizations-and-environments/user-management.md#roles) documentation.

#### Creating Application Members

1. Click **Add Member** to open the member creation dialog.
2. Search for users by typing in the **User** autocomplete field. The search queries platform users and displays results with name, email, and avatar.
3. Select one or more users from the autocomplete results. Selected users appear as chips below the input field and cannot be re-selected.
4. Select a **Role** from the dropdown. Only assignable roles, excluding system roles and PRIMARY_OWNER, are available.
5. Click **Add** to create the memberships.

The system validates that selected users are not already members of the application. If a user is already a member, the request returns a `409 Conflict` error. If no role is specified, the system assigns the lowest application role by default.

The member creation dialog includes the following fields:

| Field | Description | Required |
|:------|:------------|:---------|
| **User** | Platform user(s) to add as members. Supports multi-select autocomplete with search. | Yes |
| **Role** | Application role to assign. Excludes system roles and PRIMARY_OWNER. | Yes |

#### Searching Members

Enter a search term in the search bar to filter members by display name. The search performs case-insensitive substring matching with a 300ms debounce. If no members match the search, the table displays "No members match your search."

The members table displays the following columns: user display name with avatar, email address, assigned role, and action buttons. Pagination controls appear when the member count exceeds the page size, which defaults to 10.

#### Editing Member Roles

1. Click the **Edit** button next to a member to open the role editor dialog.
2. Select a new **Role** from the dropdown.
3. Click **Save** to update the member's role.

The Edit button is visible only for members who are not the PRIMARY_OWNER and when you have `APPLICATION_MEMBER[UPDATE]` permission. Role validation ensures the selected role exists and is assignable.

#### Removing Members

Click the **Delete** button next to a member to remove them from the application. The Delete button is visible when you have `APPLICATION_MEMBER[DELETE]` permission and is disabled when the member is yourself. The Delete button is not rendered for members with the PRIMARY_OWNER role.

### Groups

Click the **Groups** tab to see which groups have access to your application. Use the drop-down menu to change group selections.

<figure><img src="../../.gitbook/assets/00 groups added to applications 4.png" alt=""><figcaption></figcaption></figure>

Selecting a group gives all members of that group access to your application.

### Invitations

Navigate to the application's Invitations tab in Portal Next. The Invitations tab is visible when both `portal.next.applications.membership.enabled` and `portal.next.applications.membership.invitations.enabled` are `true` and you have `APPLICATION_MEMBER[READ]` permission.

#### Creating Invitations

1. Click **Invite Members** to open the invitation creation dialog.
2. Enter one or more email addresses in the **Email** field. Press Enter or Tab after each email to add it as a chip. Emails are automatically trimmed and converted to lowercase.
3. Select a **Role** from the dropdown. Only assignable roles, excluding system roles and PRIMARY_OWNER, are available.
4. Toggle **Notify** to enable or disable email notifications. When enabled, recipients receive an email with a registration link. This toggle is enabled by default.
5. Enter a **Confirmation Page URL** in the text field. This URL is included in the invitation email and should point to the registration confirmation page in your portal, for example `https://portal.example.com/user/invitation/confirm`.
6. Click **Invite** to create the invitations.

The system validates each email address and checks for duplicates within the request. If a recipient email matches an existing platform user, that user is added directly as an application member and no invitation is created. If a recipient email matches multiple users, the request returns a `409 Conflict` error. If a pending invitation already exists for a recipient email, the request returns a `409 Conflict` error. If the role is PRIMARY_OWNER and any recipient matches an existing user, the request returns a `409 Conflict` error.

The response contains only pending invitations. If all recipients matched existing users, the response data array is empty.

The invitation creation dialog includes the following fields:

| Field | Description | Required |
|:------|:------------|:---------|
| **Email** | Email address(es) of users to invite. Supports multiple entries. | Yes |
| **Role** | Application role to assign upon invitation acceptance. Excludes system roles and PRIMARY_OWNER. | Yes |
| **Notify** | When enabled, sends invitation email to recipients. Enabled by default. | No |
| **Confirmation Page URL** | URL included in invitation email for registration completion. | Yes, when **Notify** is enabled |

#### Searching Invitations

Enter a search term in the search bar to filter invitations by email address. The search performs case-insensitive partial matching with a 300ms debounce.

The invitations table displays the following columns: recipient email address, assigned role, creation date, and action buttons. Pagination controls appear when the invitation count exceeds the page size, which defaults to 10.

#### Editing Invitation Roles

1. Click the **Edit** button next to an invitation to open the role editor dialog.
2. Select a new **Role** from the dropdown.
3. Click **Save** to update the invitation's role.

The Edit button is visible when you have `APPLICATION_MEMBER[UPDATE]` permission. Role validation ensures the selected role exists and is assignable.

#### Resending Invitations

1. Click the **Resend** button next to an invitation to open the resend dialog.
2. Enter a **Confirmation Page URL** in the text field.
3. Click **Resend** to send a new invitation email.

The Resend button is visible when you have `APPLICATION_MEMBER[UPDATE]` permission. The system generates a new JWT token and sends a new invitation email to the recipient.

#### Deleting Invitations

Click the **Delete** button next to an invitation to remove it. The Delete button is visible when you have `APPLICATION_MEMBER[DELETE]` permission. Deleted invitations cannot be accepted.

#### Accepting Invitations

When you receive an invitation email, click the registration link containing a JWT token. The link navigates to `/user/invitation/confirm/:token` in the portal. The confirmation page displays a registration form with the following fields:

1. **Email.** This field is pre-filled and disabled. It shows your email address extracted from the token.
2. **First Name.** This field is editable and empty by default. Enter your first name.
3. **Last Name.** This field is editable and empty by default. Enter your last name.
4. **Password.** This field is required. It must meet platform password requirements.
5. **Confirm Password.** This field is required. Re-enter your password to confirm it.

When you submit the form, the system calls the finalize registration endpoint with the token, first name, last name, and password. The backend decodes the JWT token and validates the token action, which must be `USER_REGISTRATION`, `GROUP_INVITATION`, or `APPLICATION_INVITATION`. It then creates or finalizes your account, processes all pending invitations for your email, assigns default `ORGANIZATION` and `ENVIRONMENT` roles, and adds you to the application with the invitation role. Upon success, the confirmation page displays "Invitation accepted" with a link to the login page.

### Transfer ownership

Under the **Transfer ownership** tab, you can grant complete application access to an application member or other user. The Transfer Ownership button is visible only when you are the current owner, have `APPLICATION_MEMBER[UPDATE]` permission, and `portal.next.applications.membership.transferOwnership.enabled` is `true`.

Click **Application member** and use the drop-down menu to select a user who is already a member of your application.

<figure><img src="../../.gitbook/assets/00 groups added to applications 5.png" alt=""><figcaption></figcaption></figure>

Click **Other user** to search for someone who is not a member of your application. You can enter either their name or email into the search field. Once you've selected a new primary owner for your application, use the drop-down to assign their role.

<figure><img src="../../.gitbook/assets/00 groups added to applications 6.png" alt=""><figcaption></figcaption></figure>

#### Transferring Ownership

1. Click **Transfer Ownership** to open the transfer dialog.
2. Select a **New Primary Owner** from the user autocomplete. The current owner cannot be selected.
3. Select a **Primary Owner Newrole** from the dropdown to assign to the current owner after the transfer. The PRIMARY_OWNER role is excluded from this dropdown.
4. Click **Transfer** to complete the ownership transfer.

The system validates that the new role is assignable and is not PRIMARY_OWNER. If validation fails, the request returns a `400 Bad Request` error.

The ownership transfer dialog includes the following fields:

| Field | Description | Required |
|:------|:------------|:---------|
| **New Primary Owner** | Platform user to receive PRIMARY_OWNER role. Cannot be the current owner. | Yes |
| **Primary Owner Newrole** | Role to assign to the current owner after transfer. Cannot be PRIMARY_OWNER. | Yes |

## Enforce group ownership of applications

You can enforce group ownership of applications by requiring that at least one group is added to an application. Each member of a group has a default role for applications. When that group is added to an application, all members inherit access to the application with the role they have been assigned.

To require an application to have at least one group added to it, complete the following steps:

1. Log in to your APIM Console, and then click **Settings**.
2. From the **Settings** menu, scroll down to the User Management section, and then click **Groups**.
3.  Turn on the toggle that requires an application to have at least one group before it can be created or updated

    <figure><img src="../../.gitbook/assets/00 groups 4.png" alt=""><figcaption></figcaption></figure>

By default, this setting is false. If it is set to true, group selection is required during application creation, and the Management API sends a 400 error in response to an attempt to create an application without a group.

{% hint style="info" %}
If the setting is enabled and there are existing applications without groups, those applications are not impacted. The APIs, subscriptions, and analytics of all applications continue to function properly.
{% endhint %}

## Management API

Base path: `/applications/{applicationId}`

### Search Members

**POST** `/members/_search`

Search application members with optional display name filtering and pagination.

**Request Body:**
```json
{
  "filters": {
    "displayName": "alice"
  }
}
```

**Query Parameters:**
- `page`. Integer. Defaults to 1.
- `size`. Integer. Defaults to 10.

**Response:** `200 OK`
```json
{
  "data": [
    {
      "id": "member-id",
      "user": {
        "id": "user-id",
        "display_name": "Alice Smith",
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "_links": {
          "avatar": "https://..."
        }
      },
      "role": "USER",
      "created_at": "2020-02-01T20:22:02.00Z",
      "updated_at": "2020-02-01T20:22:02.00Z"
    }
  ],
  "metadata": {
    "pagination": {
      "current_page": 1,
      "total": 1,
      "size": 10
    }
  }
}
```

**Error Responses:**
- `400 Bad Request`. Invalid search input.
- `403 Forbidden`. Missing `APPLICATION_MEMBER[READ]` permission.
- `404 Not Found`. Application not found.

### Create Member

**POST** `/members`

Add an existing platform user as an application member.

**Request Body:**
```json
{
  "user": "user-id",
  "reference": "optional-reference",
  "role": "USER"
}
```

**Response:** `201 Created`
```json
{
  "id": "member-id",
  "displayName": "Alice Smith",
  "role": "USER"
}
```

**Error Responses:**
- `400 Bad Request`. User required, role required, or role not assignable.
- `403 Forbidden`. Missing `APPLICATION_MEMBER[CREATE]` permission.
- `404 Not Found`. Application not found.
- `409 Conflict`. User is already a member.

### Update Member

**PUT** `/members/{memberId}`

Update an application member's role.

**Request Body:**
```json
{
  "role": "OWNER"
}
```

**Response:** `200 OK`
```json
{
  "id": "member-id",
  "displayName": "Alice Smith",
  "role": "OWNER"
}
```

**Error Responses:**
- `400 Bad Request`. Role required or role not assignable.
- `403 Forbidden`. Missing `APPLICATION_MEMBER[UPDATE]` permission.
- `404 Not Found`. Application or member not found.

### Delete Member

**DELETE** `/members/{memberId}`

Remove a member from the application.

**Response:** `204 No Content`

**Error Responses:**
- `403 Forbidden`. Missing `APPLICATION_MEMBER[DELETE]` permission.
- `404 Not Found`. Application or member not found.

### Transfer Ownership

**POST** `/members/_transfer_ownership`

Transfer PRIMARY_OWNER role to another member and assign a new role to the current owner.

**Request Body:**
```json
{
  "new_primary_owner_id": "user-id",
  "new_primary_owner_reference": "optional-reference",
  "primary_owner_newrole": "USER"
}
```

**Response:** `204 No Content`

**Error Responses:**
- `400 Bad Request`. Role not assignable or role is PRIMARY_OWNER.
- `403 Forbidden`. Missing `APPLICATION_MEMBER[UPDATE]` permission or you are not the current owner.
- `404 Not Found`. Application not found.

### Create Invitations

**POST** `/invitations`

Create one or more application invitations. Recipients matching existing users are added directly as members.

**Request Body:**
```json
{
  "recipients": [
    { "email": "alice@example.com" },
    { "email": "bob@example.com" }
  ],
  "role": "USER",
  "notify": true,
  "confirmation_page_url": "https://portal.example.com/user/invitation/confirm"
}
```

**Response:** `201 Created`
```json
{
  "data": [
    {
      "id": "00000000-0000-0000-0000-000000000001",
      "email": "alice@example.com",
      "role": "USER",
      "created_at": "2020-02-01T20:22:02.00Z",
      "updated_at": "2020-02-01T20:22:02.00Z"
    }
  ]
}
```

The response contains only pending invitations. If all recipients matched existing users, the data array is empty.

**Error Responses:**
- `400 Bad Request`. Invalid email format, duplicate email, or role not assignable.
- `403 Forbidden`. Missing `APPLICATION_MEMBER[CREATE]` permission.
- `404 Not Found`. Application not found.
- `409 Conflict`. Pending invitation exists, email matches multiple users, or PRIMARY_OWNER role with existing user.

### Search Invitations

**POST** `/invitations/_search`

Search application invitations with optional email filtering and pagination.

**Request Body:**
```json
{
  "filters": {
    "email": "alice"
  }
}
```

**Query Parameters:**
- `page`. Integer. Defaults to 1.
- `size`. Integer. Defaults to 10.

**Response:** `200 OK`
```json
{
  "data": [
    {
      "id": "invitation-id",
      "email": "alice@example.com",
      "role": "USER",
      "created_at": "2020-02-01T20:22:02.00Z",
      "updated_at": "2020-02-01T20:22:02.00Z"
    }
  ],
  "metadata": {
    "pagination": {
      "current_page": 1,
      "size": 10,
      "total": 1
    }
  }
}
```

**Error Responses:**
- `400 Bad Request`. Invalid search input.
- `403 Forbidden`. Missing `APPLICATION_MEMBER[READ]` permission.
- `404 Not Found`. Application not found.

### Update Invitation

**PUT** `/invitations/{invitationId}`

Update an invitation's role.

**Request Body:**
```json
{
  "role": "OWNER"
}
```

**Response:** `200 OK`
```json
{
  "id": "invitation-id",
  "email": "alice@example.com",
  "role": "OWNER",
  "created_at": "2020-02-01T20:22:02.00Z",
  "updated_at": "2020-02-01T20:22:02.00Z"
}
```

**Error Responses:**
- `400 Bad Request`. Role blank or role not assignable.
- `403 Forbidden`. Missing `APPLICATION_MEMBER[UPDATE]` permission.
- `404 Not Found`. Application or invitation not found.

### Delete Invitation

**DELETE** `/invitations/{invitationId}`

Delete a pending invitation.

**Response:** `204 No Content`

**Error Responses:**
- `403 Forbidden`. Missing `APPLICATION_MEMBER[DELETE]` permission.
- `404 Not Found`. Application or invitation not found.

### Resend Invitation

**POST** `/invitations/{invitationId}/_resend`

Resend an invitation email with a new JWT token.

**Request Body:**
```json
{
  "confirmation_page_url": "https://portal.example.com/user/invitation/confirm"
}
```

**Response:** `204 No Content`

**Error Responses:**
- `400 Bad Request`. Confirmation page URL required.
- `403 Forbidden`. Missing `APPLICATION_MEMBER[UPDATE]` permission.
- `404 Not Found`. Application or invitation not found.

## Portal API: Platform Users

### Search Users

**POST** `/users/_search`

Search platform users with optional membership enrichment for a specific application.

**Request Body:**
```json
{
  "filters": {
    "query": "alice"
  },
  "includes": {
    "applicationMembership": "application-id"
  }
}
```

**Query Parameters:**
- `page`. Integer. Defaults to 1.
- `size`. Integer. Defaults to 20.

**Response:** `200 OK`
```json
{
  "data": [
    {
      "id": "user-id",
      "display_name": "Alice Smith",
      "first_name": "Alice",
      "last_name": "Smith",
      "email": "alice@example.com",
      "reference": "ref",
      "editableProfile": true,
      "_links": {
        "avatar": "https://..."
      }
    }
  ],
  "metadata": {
    "data": {
      "total": 1
    },
    "applicationMembership": {
      "user-id": false
    }
  }
}
```

When `includes.applicationMembership` is provided, the response metadata includes an `applicationMembership` map keyed by user IDs. Users without IDs or with blank IDs are excluded from membership enrichment.

**Error Responses:**
- `400 Bad Request`. Invalid search input.
- `403 Forbidden`. Missing `MANAGEMENT_USERS[READ]` permission, or missing `APPLICATION_MEMBER[READ]` when `includes.applicationMembership` is provided.
- `404 Not Found`. Application not found when `includes.applicationMembership` is provided.

### Finalize Registration

**POST** `/user/registration/_finalize`

Accept an invitation and complete user registration.

**Request Body:**
```json
{
  "token": "jwt-token",
  "password": "secure-password",
  "firstname": "Alice",
  "lastname": "Smith"
}
```

**Response:** `200 OK`

**Error Responses:**
- `400 Bad Request`. Invalid token or password format invalid.
- `409 Conflict`. Token action is `RESET_PASSWORD` or user already finalized.

The JWT token contains the following claims:
- `action`. Set to `USER_REGISTRATION`, `GROUP_INVITATION`, or `APPLICATION_INVITATION`.
- `email`. The user email address.
- `sub`. The user ID. This claim is optional.

The token is verified using the `jwt.secret` configuration property and must have an issuer matching `jwt.issuer` (default: `gravitee-management-auth`).
