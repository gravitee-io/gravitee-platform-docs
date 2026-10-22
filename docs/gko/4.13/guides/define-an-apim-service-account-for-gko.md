---
description: Create an API Management service account so the Gravitee Kubernetes Operator 4.13 can authenticate through a ManagementContext. Follow the steps to set it up.
---

# Define an APIM service account for GKO

The best way to provide GKO with credentials to connect to your APIM installation through a `ManagementContext` is to create a service account for GKO in the Gravitee APIM Console.

To create a service account, go to the organization settings in APIM, create a new user, and choose **Service Account**. Entering the service account email is optional.

<figure><img src="../.gitbook/assets/guide-define-an-apim-service-accoun-6 (1).png" alt="The Pre-register a user form, where Service Name is the only required field for a service account."><figcaption></figcaption></figure>

Next, ensure that this service account has the ADMIN role on the organization, and the ADMIN role on the desired environment. The ADMIN role on the organization lets GKO manage every resource. To give GKO fewer permissions, see [Limit the permissions of the service account](#limit-the-permissions-of-the-service-account).

<figure><img src="../.gitbook/assets/guide-define-an-apim-service-accoun-15 (1).png" alt="The gko-sa account detail, with an organization Roles list and a Roles list per environment."><figcaption></figcaption></figure>

The screenshot below shows the environment-level permissions included in the API\_PUBLISHER role:

<figure><img src="../.gitbook/assets/guide-define-an-apim-service-accoun-5 (1).png" alt="Full create, read, update, and delete on API, Application, and Integration, and read on Group."><figcaption></figcaption></figure>

From the newly created service account, scroll to the **Tokens** section at the bottom of the page and create a new token:

<figure><img src="../.gitbook/assets/guide-define-an-apim-service-accoun-7 (1).png" alt="The Generate a token dialog, which asks only for a token name before generating."><figcaption></figcaption></figure>

{% hint style="warning" %}
Immediately copy your new personal access token. You won’t be able to see it again.
{% endhint %}

You can now use this token as credentials in a `ManagementContext`:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ManagementContext
metadata:
  name: dev-mgmt-ctx
spec:
  baseUrl: http://localhost:8083
  environmentId: DEFAULT
  organizationId: DEFAULT
  auth:
    bearerToken: xxxx-yyyy-zzzz
```

## Limit the permissions of the service account

Instead of the ADMIN role on the organization, give the service account roles that grant only the permissions in the following table. Each cell gives the scope of a role, then the permission and the action as a role on the **Roles** page of the organization settings shows them. The scope tells you which of the service account's roles grants the permission:

* An **Environment** permission comes from the service account's role on the environment.
* An **API** or **Application** permission comes from the service account's role on that API or application. When GKO creates an API from an `ApiV4Definition` or `ApiDefinition`, or an application from an `Application`, the service account becomes its primary owner and holds these permissions on it. To let GKO update an API or application that was created another way, add the service account to it as a member, with a role that grants these permissions.

| Resource | Create | Update | Delete | Read (drift detection) |
| --- | --- | --- | --- | --- |
| `ApiV4Definition` | Environment `API`: Create | API `DEFINITION`: Update, and Environment `API`: Create or Update | API `DEFINITION`: Delete | API `DEFINITION`: Read |
| `ApiDefinition` | Environment `API`: Create | API `DEFINITION`: Update, and Environment `API`: Create or Update | API `DEFINITION`: Delete | - |
| `Application` | Environment `APPLICATION`: Create | Application `DEFINITION`: Update, and Environment `APPLICATION`: Create or Update | Application `DEFINITION`: Delete | Application `DEFINITION`: Read |
| `Subscription` | API `SUBSCRIPTION`: Create, and Application `SUBSCRIPTION`: Create on the application | API `SUBSCRIPTION`: Update | API `SUBSCRIPTION`: Delete | API `SUBSCRIPTION`: Read |
| `Group` | Environment `GROUP`: Create | Environment `GROUP`: Update | Environment `GROUP`: Delete | Environment `GROUP`: Read |
| `SharedPolicyGroup` | Environment `SHARED_POLICY_GROUP`: Create | Environment `SHARED_POLICY_GROUP`: Update | Environment `SHARED_POLICY_GROUP`: Delete | Environment `SHARED_POLICY_GROUP`: Read |
| `Dictionary` | Environment `DICTIONARY`: Create | Environment `DICTIONARY`: Update | Environment `DICTIONARY`: Delete | Environment `DICTIONARY`: Read |
| `Portal`, `PortalListing`, and a `PortalLink` or `Documentation` of a portal | Environment `PORTAL`: Create | Environment `PORTAL`: Update | Environment `PORTAL`: Delete | Environment `PORTAL`: Read |
| `PortalTheme` | Environment `THEME`: Create | Environment `THEME`: Update | Environment `THEME`: Delete | Environment `THEME`: Read |
| A `PortalLink` or `Documentation` of an API | API `DOCUMENTATION`: Create | API `DOCUMENTATION`: Update | API `DOCUMENTATION`: Delete | API `DOCUMENTATION`: Read |
| `McpProxy` | Environment `API`: Create | Environment `API`: Update | Environment `API`: Delete | Environment `API`: Read |
| `CatalogMcpServer` | Environment `AI_CATALOG`: Create | Environment `AI_CATALOG`: Update | Environment `AI_CATALOG`: Delete | Environment `AI_CATALOG`: Read |

Some changes require more than the table shows:

* **Members.** Applying an `ApiV4Definition` or `Application` also requires the API or Application `MEMBER` permission with Update when its members differ from those of the API or application in APIM, apart from the primary owner and the service account. A resource that declares no members differs when the API or application has any other member. With this permission, applying the resource sets the members to the ones you declare and makes the service account the primary owner.
* **A deleted application.** Applying an `Application` again after you deleted it requires the ADMIN role on the organization.
* **A closed subscription.** Applying a `Subscription` again after its subscription was closed also requires Application `SUBSCRIPTION`: Create on the application.
* **The portal theme.** Applying a `Portal` that changes the active theme also requires Environment `THEME`: Update. A `Portal` that references no theme changes it when a theme is active.

GKO reads a resource from APIM only to detect drift, so the **Read** column applies only when drift detection is on. For more information, see [Drift detection](../overview/drift-detection.md).

When the service account lacks a permission, APIM refuses the change with a `403` status and the message `You do not have sufficient rights to access this resource`.
