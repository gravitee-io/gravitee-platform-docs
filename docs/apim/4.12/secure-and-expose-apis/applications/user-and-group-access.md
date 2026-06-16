---
description: An overview about user and group access.
metaLinks:
  alternates:
    - user-and-group-access.md
---

# User and Group Access

## Overview

An application's **User and group access** page lets you manage user and group access to individual applications. Application membership management enables API platform administrators to control who can access and manage applications in the Gravitee Portal. Administrators can add members directly, invite external users via email, assign roles, and transfer application ownership. This feature provides granular access control for application-level operations through both the Portal UI and REST API.

## Key Concepts

### Invitations

Invitations are email-based requests to join an application. When an invitation is created, the system checks whether the recipient already has a platform account. Existing users are added directly as members; unknown recipients receive a pending invitation. Each invitation includes the recipient's email address, the assigned role, creation and update timestamps, and an optional confirmation page URL for the registration workflow.

### Roles

Application roles define the permissions granted to members and invitees. Roles are organization-specific and include both custom and system-defined roles. The `PRIMARY_OWNER` role cannot be assigned through standard member addition or invitation workflows — it is reserved for ownership transfer operations. When a role is omitted during member creation, the system assigns .

### Application Membership Enrichment

The user search API supports application membership enrichment through the `includes.applicationMembership` parameter. When provided, the response metadata includes a per-user membership map indicating whether each user is already a member of the specified application. This capability requires `APPLICATION_MEMBER[READ]` permission on the referenced application and excludes users without valid identifiers from the lookup.

## Prerequisites

* The `portal.next.applications.membership.enabled` configuration property must be set to `true` to enable application membership settings in Portal Next.
* The `jwt.secret` configuration property must be set (throws `"JWT secret is mandatory"` if missing).
* Users must have appropriate permissions:
  * `APPLICATION_MEMBER[READ]` to view members and invitations
  * `APPLICATION_MEMBER[CREATE]` to add members
  * `APPLICATION_MEMBER[UPDATE]` to edit member roles
  * `APPLICATION_MEMBER[DELETE]` to remove members
  * `APPLICATION_INVITATION[CREATE]` to create invitations
  * `APPLICATION_INVITATION[UPDATE]` to edit or resend invitations
  * `APPLICATION_INVITATION[DELETE]` to delete invitations
  * `MANAGEMENT_USERS[READ]` to search platform users
* For ownership transfer, `portal.next.applications.membership.transferOwnership.enabled` must be `true`, and the user must be the current application owner with `APPLICATION_MEMBER[UPDATE]` permission.
* For invitation acceptance, either `CONSOLE_USERCREATION_ENABLED` (ORGANIZATION scope) or `PORTAL_USERCREATION_ENABLED` (ENVIRONMENT scope) must be `true`.

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

Under the **Members** tab, you can add users or groups as members of your application and define their roles to manage and perform tasks and operations. The **Members** tab displays a searchable, paginated list of all users who have been granted access to the application. Each member entry shows the user's display name, email address, assigned role, and action buttons for editing or removing the member.

<figure><img src="../../.gitbook/assets/00 groups added to applications 3.png" alt=""><figcaption></figcaption></figure>

#### Search for members

To search for members, enter at least one character in the **Display Name** search field. The search performs a case-insensitive substring match against member display names.

{% hint style="info" %}
When you change the search term, the page resets to 1. When you change the page size, the active search filter is preserved. Clearing the search input sends an empty filter object to the API.
{% endhint %}

#### Add a new member

1. Click **+ Add members** to open the Add Member dialog.
2. Search for platform users by entering at least one character in the search field. The user search returns a list of platform users with their display names, email addresses, and membership status for the current application.
3. Select a user from the search results.
4. Use the **Role** drop-down menu to select a role, which grants specific permissions. For more information on roles, refer to the [Roles](../../configure-and-manage-the-platform/manage-organizations-and-environments/user-management.md#roles) documentation.
5. Confirm the addition.

The system adds the user as a member with the selected role. If you omit the role, the system assigns .

{% hint style="warning" %}
If the selected user is already a member, the system returns a `409 Conflict` error with the message `"Already exists"`. Member creation requests are limited to 3 concurrent operations.
{% endhint %}

#### Edit a member's role

1. Click the edit button next to the member entry.
2. Select a new role from the **Role** dropdown in the Edit Member dialog.
3. Save the changes.

The system updates the member's role and refreshes the member list.

#### Remove a member

1. Click the delete button next to the member entry.
2. Confirm the deletion.

{% hint style="info" %}
The delete button is hidden for members with the `PRIMARY_OWNER` role and disabled when the member is the current user. The delete button is visible only when you have `APPLICATION_MEMBER[DELETE]` permission.
{% endhint %}

### Groups

Click the **Groups** tab to see which groups have access to your application. Use the drop-down menu to change group selections.

<figure><img src="../../.gitbook/assets/00 groups added to applications 4.png" alt=""><figcaption></figcaption></figure>

Selecting a group gives all members of that group access to your application.

### Transfer ownership

Under the **Transfer ownership** tab, you can grant complete application access to an application member or other user.

Click **Application member** and use the drop-down menu to select a user who is already a member of your application.

<figure><img src="../../.gitbook/assets/00 groups added to applications 5.png" alt=""><figcaption></figcaption></figure>

Click **Other user** to search for someone who is not a member of your application. You can enter either their name or email into the search field. Once you've selected a new primary owner for your application, use the drop-down to assign their role.

<figure><img src="../../.gitbook/assets/00 groups added to applications 6.png" alt=""><figcaption></figcaption></figure>

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

## Member Search API

**Endpoint:** `POST /applications/{applicationId}/members/_search`

**Request Parameters:**
* `page` (query, integer): Page number (default: 1)
* `size` (query, integer): Page size (default: 10)

**Request Body:**
```json
{
  "filters": {
    "displayName": "string"
  }
}
```

**Response:**
```json
{
  "data": [
    {
      "id": "string",
      "user": {
        "id": "string",
        "display_name": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string"
      },
      "role": "string",
      "isCurrentUser": true,
      "isPrimaryOwner": false,
      "created_at": "2026-01-01T00:00:00Z",
      "updated_at": "2026-01-01T00:00:00Z"
    }
  ],
  "metadata": {
    "pagination": {
      "current_page": 1,
      "total": 42,
      "size": 10
    }
  }
}
```

**Permissions Required:** `APPLICATION_MEMBER[READ]`

**Error Responses:**
* `400`: Bad Request
* `403`: Permission Error
* `404`: Application Not Found

### User Search with Membership Enrichment API

**Endpoint:** `POST /users/_search`

**Request Parameters:**
* `page` (query, integer): Page number (default: 1)
* `size` (query, integer): Page size (default: 20)

**Request Body:**
```json
{
  "filters": {
    "query": "string"
  },
  "includes": {
    "applicationMembership": "application-id"
  }
}
```

**Response:**
```json
{
  "data": [
    {
      "id": "string",
      "display_name": "string",
      "email": "string"
    }
  ],
  "metadata": {
    "applicationMembership": {
      "user-1": true,
      "user-2": false
    },
    "data": {
      "total": 42
    }
  }
}
```

**Permissions Required:**
* `MANAGEMENT_USERS[READ]` (base permission)
* `APPLICATION_MEMBER[READ]` on the referenced application (when `includes.applicationMembership` is provided)

**Error Responses:**
* `400`: Bad Request (when both `q` query parameter and request body are provided)
* `403`: Permission Error
* `404`: Application Not Found (when `includes.applicationMembership` references nonexistent application)

**Behavior:**
* When `includes.applicationMembership` is provided, the response `metadata.applicationMembership` is enriched with per-user membership flags for that application.
* The deprecated query parameter `q` and request body `filters.query` cannot be used together (returns 400).
* When no query is provided, the system defaults to a wildcard query (`*`).
* Results are sorted by last name (case-insensitive, nulls last).
* Users without valid identifiers (null or blank) are excluded from membership lookup queries. If all users in a search result lack identifiers, the membership map returns empty.

### Member Management API

**Create Member:** `POST /applications/{applicationId}/members`

**Request Body:**
```json
{
  "userId": "string",
  "role": "string"
}
```

**Response:** `201 Created`

**Permissions Required:** `APPLICATION_MEMBER[CREATE]`

**Error Responses:**
* `400`: Bad Request
* `403`: Permission Error
* `404`: Application Not Found
* `409`: Conflict (user is already a member; error message: `"Already exists"`)

---

**Update Member:** `PUT /applications/{applicationId}/members/{memberId}`

**Request Body:**
```json
{
  "role": "string"
}
```

**Response:** `200 OK`

**Permissions Required:** `APPLICATION_MEMBER[UPDATE]`

**Error Responses:**
* `400`: Bad Request
* `403`: Permission Error
* `404`: Application Not Found or Member Not Found

---

**Delete Member:** `DELETE /applications/{applicationId}/members/{memberId}`

**Response:** `204 No Content`

**Permissions Required:** `APPLICATION_MEMBER[DELETE]`

**Error Responses:**
* `403`: Permission Error
* `404`: Application Not Found or Member Not Found
