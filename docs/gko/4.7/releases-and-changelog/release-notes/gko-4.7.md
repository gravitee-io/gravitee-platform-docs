---
description: Gravitee Kubernetes Operator 4.7 Release Notes.
---

# GKO 4.7

The 4.7 release of the Gravitee Kubernetes Operator brings support for two new APIM resources: [Shared Policy Groups](/apim/policies/shared-policy-groups) and [User Groups](/apim/administration/user-management#users-and-user-groups). This not only increases the scope of what can now be managed as-code from your GitOps CI/CD pipeline, it also enables a new paradigm by which common API policies can be managed centrally by the platform team, with their own lifecycle, and easily applied to the many APIs that are created by different API development teams across your organization.

## Shared Policy Groups

Shared policy groups let you define a collection of policies in a central location and use them across multiple APIs.

\
To create a shared policy group with the Gravitee Kubernetes Operator, you can use the new dedicated CRD. Then you can refer to the shared policy group from a V4 API definition.

The example below shows a shared policy group that applies to the request phase of a proxy API, and includes a rate limit policy.

```yaml
apiVersion: gravitee.io/v1alpha1
kind: SharedPolicyGroup
metadata:
  name: simple-shared-policy-group
spec:
  contextRef:
    name: "context"
  name: "simple-shared-policy-grous"
  description: "Simple shared policy group"
  apiType: "PROXY"
  phase: "REQUEST"
  steps:
    - name: Rate Limit
      description: k8s rate limit
      enabled: true
      policy: rate-limit
      configuration:
        async: false
        addHeaders: true
        rate:
          useKeyOnly: false
          periodTime: 1
          limit: 10
          periodTimeUnit: MINUTES
          key: ""
```

Now I can reference this shared policy group from one of my API definitions. In the example API definition below, you can see that I’ve referenced the shared policy by its Kubernetes name “simple-shared-policy-group”, as part of a common flow:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: v4-api-shared-policy-group
spec:
  name: "v4 API Shared Policy Group"
  contextRef: 
    name: context
  description: "v4 API with a shared policy group"
  version: "1.0"
  type: PROXY
  flows:
    - name: "default"
      enabled: true
      selectors:
        - type: "HTTP"
          path: "/"
          pathOperator: "EQUALS"
      request:
        - sharedPolicyGroupRef:
            name: "simple-shared-policy-group"
          enabled: true
  listeners:
    - type: HTTP
      paths:
        - path: "/api-spg"
      entrypoints:
        - type: http-proxy
          qos: AUTO
  endpointGroups:
    - name: Default HTTP proxy group
      type: http-proxy
      endpoints:
        - name: Default HTTP proxy
          type: http-proxy
          inheritConfiguration: false
          configuration:
            target: https://api.gravitee.io/echo
          secondary: false
  flowExecution:
    mode: DEFAULT
    matchRequired: false
  plans:
    API_KEY:
      name: "API Key plan"
      description: "API key plan needs a key to authenticate"
      security:
        type: "API_KEY"
      flows:
        - enabled: true
          selectors:
            - type: HTTP
              path: "/"
              pathOperator: STARTS_WITH
```

You can reference a single shared policy from multiple APIs.&#x20;

The shared policy group has its own lifecycle, so you can update a shared policy and changes will apply immediately to all APIs that reference it, without needing to update or redeploy the APIs.

## Environment-level User Groups

As part of Gravitee’s role-based access control system (RBAC), users that have access to your API management control plane can be put into groups in order to simplify the way you define which users can access which APIs or applications in the control plane. \


Because an API definition can reference a group directly, we've have requests from users that want to also be able to manage the groups themselves declaratively using the Gravitee Kubernetes Operator.&#x20;

As of 4.7, this is now possible! In the example below, I’ve defined a group of users called **developers** and added a member to the group called **jonathanadmin**:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Group
metadata:
  name: developers
spec:
  contextRef:
    name: "context"
  name: "developers"
  notifyMembers: false
  members:
  - source: memory
    sourceId: jonathanadmin
    roles:
      API: OWNER
      APPLICATION: OWNER
      INTEGRATION: USER
```

The user I’ve added has been given a specific set of roles that will apply to different objects in Gravitee that the group gets added to.

I can now extend the API definition from the first part of this post to include a reference to this group of users.&#x20;

Below is a snippet that shows an added reference to the developers user group. All members of that group will now become members of this API.

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: v4-api-shared-policy-group
spec:
  name: "v4 API Shared Policy Group"
  contextRef: 
    name: context
  description: "v4 API with a shared policy group"
  version: "1.0"
  type: PROXY
  groups:
    - developers
```
