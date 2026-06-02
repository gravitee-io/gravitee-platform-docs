# Portal Navigation FreeMarker Template Validation

## Overview

Portal navigation templating enables dynamic content in Gravitee Markdown portal pages using FreeMarker expressions. The system validates template syntax and variable references when saving page content, providing context-aware error messages to prevent runtime rendering failures.

## Key Concepts

### FreeMarker Template Validation

When updating Gravitee Markdown portal page content, the system performs a dry-run render to validate FreeMarker template syntax and variable references before persisting changes. Validation uses the API model if the page is nested under an API node; otherwise, it uses environment metadata. The system walks the `parentId` chain upward until finding a portal navigation API node to determine the appropriate template context.

### Enclosing API Resolution

The portal navigation system resolves the enclosing API for each navigation item by traversing the parent hierarchy. This resolution determines which template variables are available during validation and rendering. Pages under an API node receive an `api` object in the template context; pages at the environment level receive a `metadata` map.

### Error Handling

The system distinguishes between template validation errors (invalid FreeMarker syntax or missing variables) and HTTP transport errors. Template validation errors are reported with specific messages identifying the problematic expression. HTTP errors are handled by the global error interceptor to avoid duplicate or generic error messages in the user interface.

## Prerequisites

Before using portal navigation templating, ensure the following:

* Gravitee API Management platform with portal navigation enabled
* Portal pages configured as Gravitee Markdown content type
* Navigation items linked to portal page content records

## Creating Portal Page Content with Templates

When editing Gravitee Markdown portal page content, FreeMarker template expressions are validated on save. If the page is nested under an API node in the portal navigation tree, the template context includes the API model. For environment-level pages, the context includes environment metadata.

Template validation errors display the specific expression or variable that failed:

* `"Invalid expression or value is missing for <expression>"` — FreeMarker template references undefined variable
* `"Invalid template: <detail>"` — FreeMarker parse failure (syntax error)

Pages without a linked navigation item are not validated.

## Managing Template Validation Errors

When a template validation error occurs, the system returns a specific error message identifying the problematic FreeMarker expression. HTTP error responses (status 400, 500, etc.) are handled by the global HTTP error interceptor and displayed in the user interface. Generic client-side error messages are suppressed when the server provides a specific validation message to avoid replacing detailed backend feedback with generic text like `"Failed to update page content"`.

## Restrictions

* Template validation occurs only when the navigation page is linked to a portal page content record; orphaned content is not validated
* Pages without a linked navigation item skip validation entirely
* FreeMarker error messages expose internal variable names to end users
* Custom implementations of `PortalPageContentValidator` must update method signatures to include the `existingContent` parameter (breaking change):
  ```java
  // Before
  void validate(UpdatePortalPageContent updateContent);

  // After
  void validate(PortalPageContent<?> existingContent, UpdatePortalPageContent updateContent);
  ```

{% hint style="info" %}
This feature was introduced in APIM 4.12.
{% endhint %}

## Related Changes

The validator interface signature changed to accept both existing and updated content parameters, requiring updates to custom validator implementations:

```java
// Before
void validate(UpdatePortalPageContent updateContent);

// After
void validate(PortalPageContent<?> existingContent, UpdatePortalPageContent updateContent);
```

Error handling in the portal navigation UI component now suppresses generic error messages when HTTP errors are already handled by the global interceptor, preventing duplicate or conflicting error notifications.
