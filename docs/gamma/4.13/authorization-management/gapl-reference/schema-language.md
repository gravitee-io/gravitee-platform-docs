---
hidden: false
noIndex: false
description: The syntax of GAPL schema documents, covering entity types, attribute types, common types, actions, action groups, and namespaces.
---

# Schema language

The **Schema text** of a schema document declares the entity types, the actions, and the relationships that your policies are written against. A document is a sequence of declarations, each ending with `;`:

```
entity Team;

entity User in [Team] {
  email: String,
  department?: String
};

entity Document {
  owner: User,
  labels: Set<String>
};

action "read", "comment" appliesTo {
  principal: [User],
  resource: [Document]
};
```

Comments use `//` for the rest of a line and `/* ... */` for a block, as in policies. For how documents reach the gateways, see [Schema documents](../manage/schemas/schema-generation.md).

## Entity types

An entity type is declared with `entity`, a name, and an optional list of attributes between braces:

```
entity Group;
entity User { email: String, active: Bool };
entity Device = { platform: String };
```

The `=` before the braces is optional. Several types with the same attributes can be declared at once: `entity Invoice, CreditNote { amount: Long };`.

### Attributes

Each attribute is a name, `:`, and a [type](#attribute-types). A `?` after the name makes the attribute optional. Attributes are separated by commas, and a trailing comma is allowed:

```
entity User {
  email: String,
  department?: String,
  roles: Set<String>,
};
```

### Parents

`in [...]` lists the entity types that an entity of this type can have as parents, such as the teams a user belongs to. The parents themselves are set on each entity, and the `in` operator of policies follows them:

```
entity Team;
entity Department;
entity User in [Team, Department];
```

### Enumerated types

`enum [...]` lists every ID of an entity type. Each value appears once:

```
entity Region enum ["eu", "us", "apac"];
```

Policies refer to these entities like any other, such as `Region::"eu"`.

## Attribute types

| Type | Values |
|------|--------|
| `String` | Strings |
| `Long` | 64-bit integers |
| `Bool` | `true` or `false` |
| `decimal` | Decimals. See [`decimal`](extension-functions.md#decimal) |
| `datetime` | Instants. See [`datetime`](extension-functions.md#datetime) |
| `duration` | Lengths of time. See [`duration`](extension-functions.md#duration) |
| `ipaddr` | IP addresses and ranges. See [`ip`](extension-functions.md#ip) |
| `Set<T>` | Sets of values of type `T`, such as `Set<String>` or `Set<User>` |
| `{ ... }` | Records with the listed fields, such as `{ city: String, zip?: String }` |
| An entity type | A reference to an entity of that type, such as `owner: User` |
| A common type | The type the name stands for. See [Common types](#common-types) |

The names are case-sensitive. GAPL has no `Int`, `Integer`, or `Boolean` type: use `Long` and `Bool`.

## Common types

`type` gives a name to a type, so that several declarations can share it:

```
type Address = { street: String, city: String, zip?: String };

entity Customer { billing: Address, shipping?: Address };
```

A common type can use a common type declared later in the document. Two common types that refer to each other are refused.

## Actions

An action is declared with `action` and one or more names. A name is a string, or an identifier when it has only letters, digits, and `_`:

```
action "read";
action approve;
action "list", "export";
```

`appliesTo` says which principal types and resource types the action connects, and which data its requests carry in `context`. Each entry is optional, but `appliesTo` needs at least one:

```
action "transfer" appliesTo {
  principal: [User, ServiceAccount],
  resource: [Account],
  context: { amount: Long, channel?: String }
};
```

An action can be declared only once in a namespace.

## Action groups

An action declared with `in [...]` is a member of the actions listed there. A group is itself an action, declared in the same document:

```
action "manage";
action "read", "update", "delete" in ["manage"] appliesTo {
  principal: [User],
  resource: [Document]
};
```

In a policy, `action in Action::"manage"` then matches `manage`, `read`, `update`, and `delete`:

```
permit (principal in Group::"admins", action in Action::"manage", resource is Document);
```

Groups can nest: a group can be a member of another group. A group must be declared as an action, and groups can't form a cycle. A group in another namespace is written in full, such as `in [Admin::Action::"manage"]`.

Action groups apply on the gateways that receive the schema document. On a gateway without the document, `action in Action::"manage"` matches only the `manage` action itself.

## Namespaces

`namespace` groups declarations under a name. Inside the braces, declarations end with `;`. The `;` after the closing brace is optional:

```
namespace Sales {
  entity Order { region: String };
  action "refund" appliesTo { principal: [User], resource: [Order] };
}

entity User;
```

Outside its namespace, a type is written with the namespace in front, such as `Sales::Order`, and an action has the type `Sales::Action`, such as `Sales::Action::"refund"`. A namespace name can have several parts, such as `namespace Sales::Europe { ... }`, and namespaces can nest.

Inside a namespace, a name without `::` refers to the declaration of that namespace when there's one, and otherwise to the declaration outside any namespace. In the example, `Order` is `Sales::Order` and `User` is the top-level `User`. This fallback applies to type names only: an action group written inside a namespace always refers to an action of that namespace.

## What the gateway does with a schema

The gateways that receive a schema document use it for the following:

* **Action groups**. `action in ...` follows the groups the document declares.
* **Action search**. The `search/action` route of an AuthZEN endpoint returns the actions that your policies permit for the principal and resource of the request, among the declared actions whose `appliesTo` covers their types and the actions that exist as `Action` entities. An action without a `principal` or a `resource` entry in `appliesTo` covers every type.

A schema doesn't validate requests or policies. A request with a type, an action, or an attribute that the schema doesn't declare is still evaluated, and a policy that uses undeclared names saves and deploys.

## Rules a document must follow

The editor refuses a document that breaks the following rules:

* Every entity type that the document uses, in attributes, `in [...]`, or `appliesTo`, is declared in it.
* Every action group is declared as an action, and groups don't form a cycle.
* An action is declared once per namespace.
* An enumerated type lists each value once.
* Every common type can be resolved.

For the messages the editor shows, see [Validate schema changes](../manage/schemas/validate-schema-changes.md).
