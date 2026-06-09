---
hidden: true
noIndex: true
---

# Creating and Managing Templated Portal Pages

## Prerequisites

Before creating portal pages with templates, ensure the following:

* Gravitee API Management 4.x or later
* Developer Portal enabled
* Portal navigation structure configured (API pages or environment pages)
* For API pages: at least one published API with portal documentation enabled

## Gateway Configuration

## Creating Portal Pages with Templates

1. Navigate to the Developer Portal page editor for the target API or environment page.
2. Enter Gravitee Markdown content in the page editor.
3. Embed FreeMarker expressions using `${...}` syntax and FreeMarker directives (e.g., `<#if>`, `<#list>`).
4. Reference API properties using the `api` root variable (for API pages) or environment metadata using the `metadata` root variable (for environment pages).
5. Save the page.

    The system performs a dry-run template rendering with the appropriate model (API or environment metadata) to validate syntax and property references. If validation fails, the backend returns a specific error message describing the invalid template syntax or missing property reference.

### Example: Basic API information header

```markdown
# ${api.name} — ${api.version}

> ${api.description}

**Status:** ${api.lifecycleState}
**Visibility:** ${api.visibility}
**Owner:** ${api.primaryOwner.displayName} (${api.primaryOwner.email})
```

### Example: Conditional support contact block

```markdown
## Support

<#if api.metadata['email-support']?has_content>
Contact us at [${api.metadata['email-support']}](mailto:${api.metadata['email-support']}).
<#else>
No support contact configured.
</#if>
```

### Example: Listing categories and tags

```markdown
**Categories:** <#list api.categories as cat>${cat}<#sep>, </#list>

**Tags:** <#list api.tags as tag>`${tag}`<#sep>  </#list>
```

### Example: Deployment timestamp with date formatting

```markdown
<#if api.deployedAt??>
Last deployed: ${api.deployedAt?string['yyyy-MM-dd HH:mm']}
<#else>
Not yet deployed.
</#if>
```

### Example: Loop over V4 listeners (V4 HTTP / Native only)

```markdown
## Endpoints

<#list api.listeners as listener>
- **${listener.type}**
</#list>
```

### Example: Owner type check

```markdown
<#if api.primaryOwner.type == "GROUP">
Maintained by the **${api.primaryOwner.displayName}** team.
<#else>
Maintained by **${api.primaryOwner.displayName}**.
</#if>
```

### Example: Environment metadata (environment page)

```markdown
# Welcome to ${metadata['portal-name']!api.name}

For assistance, reach out to [support](mailto:${metadata['support-email']}).
```

## Managing Portal Page Errors

When saving portal page content fails with an HTTP error (status 400+), the Developer Portal displays the specific backend error message returned by the validation service. The generic client-side message `"Failed to update page content"` is suppressed to avoid replacing the specific backend message with a generic one. Non-HTTP errors (e.g., network failures) still display the generic message.

For details on the validator API changes that enable this behavior, see [Validator API Changes](../../portal-page-content-validator-api-changes.md#portal-page-content-validator-api-changes).
