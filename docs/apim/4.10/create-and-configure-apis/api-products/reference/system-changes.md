
## UI Changes

The API Products feature introduces new navigation and display elements in the Console UI:

### Navigation

The side menu includes an "API Products" item with the `gio:folder` icon, routing to `./api-products`.

API Product detail pages provide three tabs:
- **Configuration** (`gio:settings` icon)
- **APIs** (`gio:cloud-settings` icon)
- **Consumers** (`gio:users` icon), subdivided into:
  - **Plans** (requires `api_product-plan-r` permission)
  - **Subscriptions** (requires `api_product-subscription-r` permission)

### Subscription List Display

The subscription list includes a "Reference Type" column displaying labels based on the subscription's `referenceType`:

| `referenceType` | Display Label |
|:----------------|:--------------|
| `API` | "API" |
| `API_PRODUCT` | "API Product" |

Default subscription filter statuses are `ACCEPTED`, `PAUSED`, and `PENDING`.

---

## Roles Upgrader

The roles upgrader runs at order `950` and creates the following roles:

- `ROLE_API_PRODUCT_USER`
- `ROLE_API_PRODUCT_OWNER`
- `PRIMARY_OWNER` (system role with all API Product permissions)

API Product permissions include:
- `api_product-definition-r`, `api_product-definition-u`, `api_product-definition-d`, `api_product-definition-c`
- `api_product-plan-r`, `api_product-plan-c`, `api_product-plan-u`, `api_product-plan-d`
- `api_product-subscription-r`, `api_product-subscription-u`

---

## Gateway Event System

### Event Types

The `ApiProductEventType` enum defines three event types:

```java
public enum ApiProductEventType {
    DEPLOY,   // API Product deployed
    UPDATE,   // API Product updated
    UNDEPLOY  // API Product undeployed
}
```

### Event Payload

The `ApiProductChangedEvent` class contains:

```java
public class ApiProductChangedEvent {
    private final String productId;        // API Product ID
    private final String environmentId;    // Environment ID
    private final Set<String> apiIds;      // API IDs needing security chain refresh
}
```

Events are published when API Products are deployed, updated, or undeployed. If the API Product contains APIs, the event triggers security chain refresh for the affected APIs.

---

## Repository Implementation

### Supported Backends

API Product repository implementations are available for:
- **JDBC**
- **MongoDB**

A **NoOp** implementation is provided for unsupported backends.

### Repository Methods

The `ApiProductsRepository` interface defines:

```java
Optional<ApiProduct> findByEnvironmentIdAndName(String environmentId, String name);
Set<ApiProduct> findByEnvironmentId(String environmentId);
Set<ApiProduct> findByApiId(String apiId);
```

Plan and subscription repositories include new methods supporting reference type queries:

```java
// PlanRepository
Set<Plan> findByReferenceIdAndReferenceType(String referenceId, Plan.PlanReferenceType planReferenceType);
List<Plan> findByReferenceIdsAndReferenceTypeAndEnvironment(List<String> referenceIds, Plan.PlanReferenceType planReferenceType, Set<String> environments);
Optional<Plan> findByIdAndReferenceIdAndReferenceType(String plan, String referenceId, Plan.PlanReferenceType planReferenceType);

// SubscriptionRepository
Set<Subscription> findByReferenceIdAndReferenceType(String referenceId, SubscriptionReferenceType referenceType);
Optional<Subscription> findByIdAndReferenceIdAndReferenceType(String subscriptionId, String referenceId, SubscriptionReferenceType referenceType);

// ApiKeyRepository
Optional<ApiKey> findByKeyAndReferenceIdAndReferenceType(String key, String referenceId, String referenceType);
```

---

## Testing Infrastructure

### E2E Test Annotation

The `@DeployApiProducts` annotation enables API Product deployment in E2E tests:

```java
@Target({ ElementType.TYPE, ElementType.METHOD })
@Retention(RetentionPolicy.RUNTIME)
@Inherited
public @interface DeployApiProducts {
    String[] value(); // Paths to API Product definition files
}
```

**Usage:**

```java
@DeployApiProducts({ "/api-products/product1.json", "/api-products/product2.json" })
public class MyGatewayTest extends AbstractGatewayTest { }
```

The annotation loads API Product definitions from JSON files and deploys them in the test environment.

### Test Deployer Interface

The `ApiProductDeployer` interface provides methods for managing API Products in tests:

```java
void setDeployApiProductCallback(Consumer<ReactableApiProduct> apiProductDeployer);
void setUndeployApiProductCallback(Consumer<String> apiProductUndeployer);
void deployApiProduct(ReactableApiProduct reactableApiProduct);
void undeployApiProduct(String apiProductId);
void redeployApiProduct(ReactableApiProduct reactableApiProduct);
```
