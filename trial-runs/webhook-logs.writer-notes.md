# webhook logs.writer notes

## Questions requiring clarification

Please provide answers to the following so the article can be finalized.

<details>

<summary>1. Alternative configuration path</summary>

The draft states: "It is possible to configure this from the Webhook log page" and refers to a top-right button, but no screenshot was provided.

* Should this alternative configuration method be documented in this article?
* If yes, please provide a screenshot that shows the Webhook log page with the top-right button, and confirm the button label (e.g., "Configure", "Settings", or similar).

</details>

<details>

<summary>2. Sampling strategy details</summary>

The foreword mentions a "Count per time window" sampling strategy with specific defaults and limits (e.g., Count: 100/10, Temporal: PT10S/PT1S, etc.).

* Should these sampling-strategy defaults and limits be included here, or will they be documented in a separate logging-configuration article?
* If they belong here, please confirm the exact wording and numeric values to include.

</details>

<details>

<summary>3. gravitee.yml configuration</summary>

The draft references `reporting.logging.max_size` in gravitee.yml as controlling the message body size in logs.

* Should Helm chart equivalents and these gravitee.yml settings be documented in this article, or in a separate configuration reference?
* If included here, please provide the exact Helm chart values (key paths and default values) to document alongside the gravitee.yml example.

</details>

<details>

<summary>4. Read-only settings behavior</summary>

The foreword mentions that settings become read-only when configured in gravitee.yml with non-default values.

* Do you want this behavior documented in this article?
* If so, should we include a short explanation and an example (e.g., "When reporting.logging.max\_size is set to X in gravitee.yml, the corresponding UI fields on the Webhook log page are disabled") and where (this page or a configuration reference)?

</details>

<details>

<summary>5. Save button location / autosave behavior</summary>

The draft instructs: "Click **Save** to apply the configuration" but the screenshots do not show a Save button.

* Does the UI require an explicit Save action, or are changes auto-saved?
* If a Save button exists, please confirm its location and label (and provide a screenshot if possible). If changes are auto-saved, please confirm so the text can be adjusted.

</details>

***

## Content decisions made

{% hint style="info" %}
These decisions were applied while preparing the article draft.
{% endhint %}

* Excluded `image_3.jpg` (Gravitee branding image) as it provides no documentation value.
* Structured the article as a how-to following template guidelines.
* Combined viewing and configuring webhook logs into a single article because they are closely related tasks.
* Expanded "DLQ" to "Dead Letter Queue" on first use.
* Added a verification section (how to confirm configuration is applied) based on template requirements.
* Preserved all links and query parameters as found in the draft (no URLs were altered).
* Removed navigation elements and unrelated summaries present in the source.

If any of these decisions should be revisited, please indicate which ones.

***

## Next steps

* Provide answers/screenshots for the five clarification questions above.
* If you want sampling details, gravitee.yml/Helm values, or read-only behavior included, supply the precise configuration snippets or confirm they should be covered in a separate configuration reference page.
* Confirm whether to keep the combined view/configuration flow or split into separate pages.

Once clarified, I will produce the final GitBook-optimized markdown (including any stepper or tabs blocks if the UI flow warrants them).
