# Typo-tolerant API search

## Overview

Gravitee API Management 4.12.0 introduces typo-tolerant API search for the Developer Portal catalog. When enabled, the search engine automatically expands queries with fuzzy matching clauses based on Levenshtein distance, so developers find APIs even when their search queries contain minor spelling errors. For example, a search for "paymnt" still returns "payment" APIs.

This feature is disabled by default. Enable it per environment from the Console or through the Management API. Enabling it requires the `ENVIRONMENT_SETTINGS` update permission.

## Enable typo-tolerant search in the Console

The toggle is part of the New Developer Portal settings, which are available with an Enterprise license.

1. In the Console, open **Settings**.
2. In the **Portal** section of the settings menu, click **Settings**.
3. Scroll to the **New Developer Portal** section.
4. Enable the **Approximate spelling for API search** toggle.

    <!-- TODO: Screenshot of the "Approximate spelling for API search" toggle in the New Developer Portal settings -->
    <figure><img src="../.gitbook/assets/PLACEHOLDER-approximate-spelling-toggle.png" alt=""><figcaption><p>The Approximate spelling for API search toggle in the New Developer Portal settings</p></figcaption></figure>
5. Click **Save**.

## Configuration reference

The following setting controls typo-tolerant search for an environment. It is also configurable through the Management API.

<table>
    <thead>
        <tr>
            <th width="320">Property</th>
            <th>Description</th>
            <th width="100">Default</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>portal.next.catalog.fuzzySearch.enabled</code></td>
            <td>Enables typo-tolerant search for the Developer Portal catalog. When <code>true</code>, query tokens of four or more characters are expanded with fuzzy matching clauses: tokens of four to seven characters tolerate one edit (Levenshtein distance 1), and tokens of eight or more characters tolerate two edits (Levenshtein distance 2). Tokens shorter than four characters are matched exactly, and queries longer than 512 characters skip fuzzy expansion. The setting is exposed in the Management API <code>GET /settings</code> response under <code>portalNext.catalog.fuzzySearch.enabled</code>. Scope: <code>ENVIRONMENT</code>.</td>
            <td><code>false</code></td>
        </tr>
    </tbody>
</table>

## Verification

To verify typo-tolerant search is working as expected, follow these steps:

1. Open the Developer Portal catalog.
2. Search for an API using a query with a minor spelling error, such as "paymnt" for an API named "payment".
3. Confirm the API appears in the search results.

    <!-- TODO: Screenshot of the Developer Portal catalog returning the expected API for a misspelled query -->
    <figure><img src="../.gitbook/assets/PLACEHOLDER-typo-tolerant-search-result.png" alt=""><figcaption><p>A misspelled query returning the expected API in the Developer Portal catalog</p></figcaption></figure>
