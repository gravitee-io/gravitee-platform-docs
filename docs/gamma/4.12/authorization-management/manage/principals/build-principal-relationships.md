---
hidden: false
noIndex: false
---

# Build principal relationships

Link principals into hierarchies using parent-child relationships. Relationships drive the `in` operator in GAPL: when a policy says `principal in Group::"engineering"`, it matches any user whose parents include that group.

## How relationships work

Every entity has a `parents` list — an ordered collection of references to other entities. A parent reference is a structured pair of `entityType` and `entityId` that maps to the canonical engine UID (for example, `Group::"engineering"`).

The relationship model supports:

| Pattern | Example | GAPL effect |
|---------|---------|-------------|
| **User → Group** | Alice is a member of Engineering | `principal in Group::"engineering"` matches Alice |
| **Group → Group** | Engineering is part of Product | `principal in Group::"product"` matches all Engineering members transitively |
| **ServiceAccount → Group** | CI Bot belongs to Automation | `principal in Group::"automation"` matches CI Bot |

## Setting parents during creation

When creating a new principal via **Add Principal**:

1. Scroll to the **Parents** section
2. Type in the combobox to search existing entities by name
3. Select one or more parents from the dropdown
4. Each selected parent appears as a chip; click the × to remove it

The parent picker only shows entities of the same kind. For example, when creating a `PRINCIPAL`, only other principal entities appear as parent options.

## Editing parents on existing entities

1. On the Entities page, find the entity in the Principals table
2. Click the **⋮** menu → **Edit**
3. In the Edit panel, modify the **Parents** combobox
4. Click **Save**

## Viewing relationships in the table

The Entities table includes a **Relationships** column that shows:

| Badge | Meaning |
|-------|---------|
| `in 1` | This entity is a child of 1 parent |
| `in 3` | This entity is a child of 3 parents |
| `contains 5 User` | This entity is a parent of 5 User entities |
| `contains 2 Group` | This entity is a parent of 2 Group entities |

Click on an entity name to open the **Entity Detail** panel, which includes a dedicated **Relationships** tab showing all parent and child entities.

## Relationship semantics in policies

GAPL supports two match modes for principal clauses:

| Mode | GAPL syntax | When to use |
|------|------------|-------------|
| **Exact** (`==`) | `principal == User::"alice"` | Match this specific principal |
| **Includes** (`in`) | `principal in Group::"engineering"` | Match this principal and all its descendants |

The visual policy editor automatically selects the appropriate default:
- **Groups and Roles** default to `includes` (membership containers)
- **Users, Service Accounts, and Agent Identities** default to `exact` (leaf principals)

{% hint style="info" %}
You can override the default match mode in the visual editor by clicking the match mode indicator on the statement card.
{% endhint %}

## Next steps

* [Create your first policy](../../get-started/create-your-first-policy.md) — Write policies using group membership
* [Build resource relationships](../resources/build-resource-relationships.md) — Apply the same parent-child pattern to resources
