# Subscription Form Database Schema

## Database Schema

The subscription form feature requires a new database table. Apply the migration file `08_add_subscription_forms_table.yml` to create the schema before enabling the feature.

### Table Structure

**Table name**: `${gravitee_prefix}subscription_forms`

| Property | Type | Constraints | Description |
|:---------|:-----|:------------|:------------|
| `id` | nvarchar(64) | NOT NULL | Unique identifier |
| `environment_id` | nvarchar(64) | NOT NULL | Environment identifier |
| `gmd_content` | nclob | NOT NULL | Gravitee Markdown form content |
| `enabled` | boolean | NOT NULL | Whether form is visible to API consumers |

### Constraints

- **Primary key**: `pk_${gravitee_prefix}subscription_forms` on `id`
- **Unique constraint**: `uc_${gravitee_prefix}subscription_forms_environment_id` on `environment_id`

Each environment can have only one subscription form. The unique constraint on `environment_id` enforces this rule at the database level.
