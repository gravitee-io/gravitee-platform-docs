# Subscription form database reference

## Table structure

The subscription forms table stores one form per environment.

**Table name:** `${gravitee_prefix}subscription_forms`

<table>
    <thead>
        <tr>
            <th width="167">Column</th>
            <th width="140">Type</th>
            <th width="180">Constraints</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>id</code></td>
            <td><code>nvarchar(64)</code></td>
            <td>NOT NULL, PRIMARY KEY</td>
            <td>Unique identifier</td>
        </tr>
        <tr>
            <td><code>environment_id</code></td>
            <td><code>nvarchar(64)</code></td>
            <td>NOT NULL, UNIQUE</td>
            <td>Environment identifier (one form per environment)</td>
        </tr>
        <tr>
            <td><code>gmd_content</code></td>
            <td><code>nclob</code></td>
            <td>NOT NULL</td>
            <td>Gravitee Markdown form content</td>
        </tr>
        <tr>
            <td><code>enabled</code></td>
            <td><code>boolean</code></td>
            <td>NOT NULL</td>
            <td>Whether the form is visible to consumers in the Developer Portal</td>
        </tr>
    </tbody>
</table>

This table is created automatically by the `4.11.0_08_add_subscription_forms_table` Liquibase migration during the APIM 4.11 upgrade.

For usage information, see [Subscription forms](../../secure-and-expose-apis/subscriptions/subscription-forms.md).
