---
hidden: false
noIndex: false
description: Take a Kafka Service in Event Stream Management through the API review workflow, from the request for a review to the reviewer's decision, and read its publication state. Follow the steps to submit or review one.
---

# Review a Kafka Service

When the environment uses the API review workflow, a reviewer accepts a Kafka Service before it can be started. A banner above every page of the Kafka Service shows where the review stands and holds the review actions.

## Publication and visibility

The publication of a Kafka Service is separate from its runtime state on the gateway. The Kafka Service pages show its publication but don't change it: the **Details** section of the **Settings** page shows the **Visibility** and the **Lifecycle** of the Kafka Service, read-only. See [Manage general settings](manage-general-settings.md).

## Read the review state

When the environment uses the API review workflow, the header of the Kafka Service sidebar shows a review badge next to the state and deployment badges:

* **Draft**. The Kafka Service has never been submitted for review.
* **In review**. A reviewer hasn't decided yet.
* **Changes requested**. A reviewer rejected the Kafka Service.
* **Review accepted**. A reviewer accepted the Kafka Service.

The banner above the pages says what the state means for you:

<table>
    <thead>
        <tr>
            <th width="260">Banner</th>
            <th>Shown when</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>This is a draft</strong></td>
            <td>The Kafka Service has never been reviewed. Starting it stays locked until a reviewer accepts it.</td>
        </tr>
        <tr>
            <td><strong>Waiting for a review</strong></td>
            <td>The Kafka Service is under review, and you aren't a reviewer.</td>
        </tr>
        <tr>
            <td><strong>This review is yours to rule on</strong></td>
            <td>The Kafka Service is under review, and you can review APIs.</td>
        </tr>
        <tr>
            <td><strong>A reviewer asked for changes</strong></td>
            <td>A reviewer rejected the Kafka Service. Reviewers see <strong>Changes were asked for on this API</strong> instead.</td>
        </tr>
        <tr>
            <td><strong>You accepted the changes on this API</strong></td>
            <td>Reviewers only, after an acceptance. Other users see no banner once the review is accepted.</td>
        </tr>
        <tr>
            <td><strong>Never reviewed</strong></td>
            <td>The Kafka Service was created before the environment turned on the review workflow, and you can submit it. Nothing holds it back.</td>
        </tr>
    </tbody>
</table>

While the Kafka Service is a draft, under review, or rejected, the **Start** and **Stop** actions disappear from the page header and from the **Settings** page.

## Submit a Kafka Service for review

1. From the Gamma console, open **Event Stream Management**.
2. In the **APIs** group of the sidebar, click **Kafka Services**.
3. Click the name of the Kafka Service.
4. In the review banner, click **Ask for review**.

**Ask for review** appears for a draft, for a rejected Kafka Service, and for one that was never reviewed, when you have permission to change the Kafka Service. The console confirms with **Kafka Service submitted for review**.

To submit the Kafka Service for review as soon as you create it, select **Ask for review** in the **Review** step of the creation wizard. See [Create a Kafka Service with a registered cluster](create-a-kafka-service-with-a-registered-cluster.md#review).

## Review a Kafka Service

Reviewers need permission to review the APIs of the environment.

1. Open the Kafka Service.
2. In the review banner, click **Review changes**.
3. In the **Review Kafka Service** dialog, select the items of the **Quality checklist**. The checklist appears when the environment defines quality rules.
4. Optional: Enter **Review comments**, up to 500 characters. The comments are recorded in the audit trail, but the author doesn't see them, so tell the author directly as well.
5. Click **Accept** or **Reject**.

The console confirms with **Kafka Service review accepted** or **Kafka Service changes requested**. After a rejection, the Kafka Service can't be started until it's reviewed again. The author applies the requested changes, then clicks **Ask for review** again.

A reviewer can come back to a decision: **Review changes** stays in the banner after an acceptance or a rejection.

## Verification

To verify the review state of the Kafka Service, follow these steps:

1. Open the Kafka Service.
2. Check the review badge in the header of the Kafka Service sidebar, for example **In review** or **Review accepted**.
3. On the **Settings** page, check the **Review** row of the **Details** section.
