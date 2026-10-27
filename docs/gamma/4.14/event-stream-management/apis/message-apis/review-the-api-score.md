---
hidden: false
noIndex: false
description: Evaluate the quality of a Message API in Event Stream Management against the scoring rulesets of the environment, and read the findings. Follow the steps to run an evaluation.
---

# Review the API Score

The API Score rates the quality of a Message API against the scoring rules of the environment. An evaluation produces a percentage and a list of findings, each with a severity: error, warning, info, or hint.

## Prerequisites

* API Score turned on for the environment. Otherwise, the **API Score** item doesn't appear in the Message API sidebar.
* To run an evaluation, permission to change the Message API's definition.

## Run an evaluation

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **Monitoring** group of the Message API sidebar, click **API Score**.
5. Click **Run evaluation**.

The console confirms with **API Score evaluation triggered** and shows **Evaluation in progress…** until the evaluation completes. The score then appears, with the date of the evaluation.

## Read the findings

The **API Score** card shows the score as a percentage, the total number of findings, `Violations`, and the number of findings per severity: `Errors`, `Warnings`, `Infos`, and `Hints`.

Under the card, each evaluated asset lists its findings with the **Severity**, the **Line/Column**, the **Recommendation**, and the **Path** of each one.

* To show one severity only, select it in the severity filter above the assets.
* To find a finding, search its message, path, or rule.

The evaluation applies every custom ruleset of the environment. Custom rulesets are imported and deleted on the **Rulesets** tab of **API Score**, in the **Observability** group of the Event Stream Management sidebar.

## Verification

To verify the evaluation, follow these steps:

1. Open **API Score** for the Message API.
2. Check that the card shows a score and the date of the last evaluation.
