### Membership Management

Protected Resource membership is managed via the `/protected-resources/{id}/members` endpoint.

#### List Members

Retrieve all members assigned to a Protected Resource:

**Endpoint:** `GET /protected-resources/{id}/members`

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[LIST]`

**Response:** Array of membership objects, each containing:
- `memberId`: Unique identifier for the member
- `memberType`: Type of member (`USER` or `GROUP`)
- `role`: Assigned role for the member

#### Add a Member

Assign a new member to a Protected Resource:

**Endpoint:** `POST /protected-resources/{id}/members`

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[CREATE]`

**Request Body:**

#### Remove a Member

Remove a member from a Protected Resource:

**Endpoint:** `DELETE /protected-resources/{id}/members/{member}`

**Permission Required:** `PROTECTED_RESOURCE_MEMBER[DELETE]`

**Response:** `204 No Content`

#### Retrieve Flattened Permissions

Retrieve the flattened permission map for the current user:

**Endpoint:** `GET /protected-resources/{id}/members/permissions`

**Permission Required:** `PROTECTED_RESOURCE[READ]`

**Response:** Flattened permission map showing the current user's effective permissions for the Protected Resource.
