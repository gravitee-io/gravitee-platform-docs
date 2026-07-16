# Generate an API Score

## Overview

API Score doesn't generate scores automatically. After you enable API Score, each API's score stays **Not available** until you run an evaluation on that API. Scores are also static: once an API is evaluated, its score doesn't change when you edit the API, update its documentation, or import a new ruleset. To reflect any change in the score, run the evaluation again.

When you evaluate an API, API Score sends the following assets to the scoring service:

* The Gravitee API definition for that API
* Every OpenAPI documentation page attached to the API
* Every AsyncAPI documentation page attached to the API

Each asset is scored against Spectral's default OpenAPI and AsyncAPI rulesets, plus any custom rulesets and functions configured for the environment. The score, issues, and assets that were evaluated are stored and shown on the API's **API Score** page, replacing any previous result. For more information about what gets scored, see [Types of Assets](types-of-assets.md). For more information about rulesets, see [Rulesets and Functions.](rulesets-and-functions.md)

## Prerequisites

Before you can generate a score, confirm the following:

* API Score is enabled for the environment. For more information, see [Enable API Score.](enable-api-score.md)
* The API that you want to evaluate is one of the supported types: Gravitee v2, v4 proxy, v4 message, v4 native Kafka, or federated.

## Evaluate an API

To generate a score for an API, follow these steps:

1. Log in to your APIM Console.
2. Open **APIs**.&#x20;
3. Click the API that you want to evaluate.
4. In the API's left sidebar, click **API Score**.
5. Click **Evaluate**.

The evaluation runs asynchronously. While the request is processing, the page shows the following banner:

{% hint style="info" %}
A request is currently processing, updated result will appear below once completed.
{% endhint %}

When the evaluation completes, the page shows the API's score as a percentage badge, the **Last evaluated** timestamp, and the issues raised by the rulesets, grouped by severity. For more information about interpreting the results, see View API Scores.

## Re-evaluate an API after changes

API Score results are static. Editing the API, changing its policies, adding or removing OpenAPI or AsyncAPI documentation pages, or importing a new ruleset doesn't refresh an existing score. To update an API's score after any change, open the API's **API Score** page and click **Evaluate** again. The new result replaces the previous one, and the **Last evaluated** timestamp updates.

## Possible evaluation outcomes

After an evaluation completes, the API's **API Score** page shows one of the following states.

<table><thead><tr><th width="220">State</th><th>What it means</th></tr></thead><tbody><tr><td>Score badge with issues</td><td>The API was scored against at least one ruleset and issues were raised. The page lists each issue with its severity, line and column, recommendation, and path.</td></tr><tr><td>All clear</td><td>The API was scored against at least one ruleset and no issues were raised. The score is 100%.</td></tr><tr><td>No scorable assets</td><td>The API's assets didn't match any ruleset. For example, the API has no OpenAPI or AsyncAPI documentation pages, and no custom ruleset applies to its API type.</td></tr></tbody></table>

If the evaluation fails or times out, a snackbar shows the error. Click **Evaluate** again once the issue is resolved.

## Verification

To verify that API Score evaluation is working as expected, follow these steps:

1. Open the API's **API Score** page before evaluating. The page shows `This API has never been scored before`, with a prompt to click the **Evaluate** button.
2. Click **Evaluate**. The pending banner appears below the header.
3. Wait for the evaluation to complete. The score badge, the **Last evaluated** timestamp, and the list of issues appear on the page.
4. Open **API Score** from the main menu to view the environment-wide dashboard. The API appears in the **APIs** table with its new score, and the **Overview** section reflects the updated average.
