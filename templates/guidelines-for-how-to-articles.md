# GUIDELINES for How-To Articles

## Introduction

A how-to article provides your users with a set of instructions to follow to solve a specific problem or complete a specific task. A task is an action that your users can take towards accomplishing a goal using your product. Multiple tasks may be involved in achieving a goal.

The purpose of how-to articles:

* **Demonstrate the different capabilities of a product.** Specifically, how to use the product to satisfy certain criteria or implement certain use cases.
* **Familiarize users with product features and improve UX.** This promotes cost reduction by lowering the number of support requests.

## Best practices

### General

* **Determine the single best path to completion.** Do not provide the user with options. Options place an undue burden upon the user to evaluate and choose between different paths.
* **Anticipate probable challenges and errors.**
  * Cite system recommendations to ensure dependencies, alert the user to functional boundaries, and protect against excessive resource consumption.
  * Include hints, cautions, and warnings to guide or unblock the user.
  * Troubleshoot common issues the user may encounter.
* **Do not explain concepts.** Assume that the user has a working knowledge of the background information and technologies referenced by the instructions.
* **Target 90% of users.** Write for a core audience that targets 90% of product users. Avoid documenting edge cases that are rarely used and test the limits of product capabilities.
* **Practice link hygiene.**&#x20;
  * Use relative links to internal documentation when possible. Avoid linking to external sites.
  * Use links sparingly to promote a self-contained, single page flow and a linear experience.
* **Test your documentation.** Ensure there are no omissions or inaccuracies and that all necessary actions are stated explicitly.

### Format and structure

* **One task per page.** Address one logical goal (task) per how-to article.
* **Orient the user.**&#x20;
  * Explicitly state if the user needs to navigate to a different screen or open a file prior to completing the next action.
  * Add contextual information first, before the action. For example, "Navigate to **X section**, and then click **Y**."&#x20;
* **One step, one action.** Limit each step to one action unless it's logical that those steps are performed together. For example, "Navigate to **X**, and then click **Y**."
* **10 steps maximum.** Enforce a 10 step limit for individual tasks. For 10+ steps, logically group steps in sub-sections or sub-steps.&#x20;
* **Numbered lists for ordered steps.** Use numbered steps for actions that must be completed sequentially.&#x20;
* **Bullet points for unordered steps or options.** Use bullet points for actions that can be completed in any order, or for options that the user can select between.
* **Begin optional steps with (Optional).** For example, "(Optional) Click Save."
* **Provide sample output.** Benchmark user progress with examples of expected output or behaviors to validate step completion.
* **Add visual aids and references.** Add [code samples](https://developers.google.com/style/code-samples) or [screenshots](https://developers.google.com/style/images) where appropriate. For screenshots:
  * Blur any sensitive data.&#x20;
  * Place a red box around the UI element that the user needs to look for or click.

### Language

* **Write in the present tense and use** [**base form**](https://en.wikipedia.org/wiki/English_verbs#Base_form) **verbs.**
  * For example, "connect", "set up", or "build." Do not use the "-ing" form of the verb.
  * Begin titles and headings with the base form of a verb and express a complete thought. For example, "Install Gravitee APIM with Docker."
* **Do not use** [**intensifiers**](https://app.gitbook.com/s/ySqSVpDHfKA0fNml1fVO/overview/am-architecture)**.** Intensifiers are adverbs that strengthen the meaning of another word. For example, "very" or "really."&#x20;
* **Define terminology and acronyms.** Definitions should occur alongside first usage.
* **Use English words only.** Do not use Latin abbreviations such as etc., e.g, and i.e. To cite examples, use “for example.” Do not use parentheses.
* **Be concise and use a neutral tone.** Be brief and direct and do not add personality. The writing styles of multiple authors should be indistinguishable.
