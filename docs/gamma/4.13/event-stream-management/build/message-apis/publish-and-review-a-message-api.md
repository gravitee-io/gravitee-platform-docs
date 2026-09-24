---
hidden: false
noIndex: false
description: Publish, unpublish, and deprecate a Message API in Event Stream Management, make it public or private, and take it through the API review workflow. Follow the steps to change its publication.
---

# Publish and review a Message API

The publication of a Message API is separate from its runtime state on the gateway. The **Publication** section of the **Settings** page publishes the Message API to the Developer Portal, deprecates it, and sets its visibility. When the environment uses the API review workflow, a banner above every page of the Message API tracks its review.

## Publish, unpublish, or deprecate the Message API

1. From the Gamma console, open **Event Stream Management**.
2. In the sidebar, click **Message APIs**.
3. Click the name of the Message API.
4. In the **General** group of the Message API sidebar, click **Settings**.
5. Scroll to the **Publication** section.
6. Click the action you need, then confirm it:

<table>
    <thead>
        <tr>
            <th width="160">Action</th>
            <th>Effect</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Publish</strong></td>
            <td>Publishes the Message API to the Developer Portal. Offered while the Message API is created or unpublished.</td>
        </tr>
        <tr>
            <td><strong>Unpublish</strong></td>
            <td>Removes the Message API from the Developer Portal. Offered while the Message API is published.</td>
        </tr>
        <tr>
            <td><strong>Deprecate</strong></td>
            <td>Marks the Message API as deprecated.</td>
        </tr>
        <tr>
            <td><strong>Make public</strong></td>
            <td>Makes the Message API publicly visible. Offered while it's private.</td>
        </tr>
        <tr>
            <td><strong>Make private</strong></td>
            <td>Makes the Message API private. The Developer Portal then shows it only to its members, to the members of its groups, and to the users whose applications subscribe to it. Offered while it's public.</td>
        </tr>
    </tbody>
</table>

The console confirms with **Message API updated**.

Once the Message API is deprecated, the **Publication** section disappears, and the console offers no way to undo the deprecation.

When the environment uses the API review workflow, **Publish** and **Unpublish** appear in two cases only. Either a reviewer has accepted the Message API, or the Message API was created before the environment turned on the review workflow.

## Submit a Message API for review

When the environment uses the API review workflow, the review banner above the pages of the Message API shows where the review stands.

1. Open the Message API.
2. In the review banner, click **Ask for review**.

The console confirms with **Message API submitted for review**. For users who aren't reviewers, the banner then reads **Waiting for a review**. Until a reviewer accepts it, you can't start or publish the Message API.

To submit the Message API for review as soon as you create it, turn on **Ask for review** in the last step of the creation wizard. See [Create a Message API](create-a-message-api.md).

## Review a Message API

Reviewers see **This review is yours to rule on** in the banner of a Message API under review.

1. Open the Message API.
2. In the review banner, click **Review changes**.
3. In the **Review Message API** dialog, tick the items of the **Quality checklist**. The checklist appears when the environment defines quality rules.
4. Optional: Enter **Review comments**, up to 500 characters.
5. Click **Accept** or **Reject**.

The console confirms with **Message API review accepted** or **Message API changes requested**. After a rejection, the Message API can't be published or started until it's reviewed again. Apply the requested changes, then click **Ask for review** again.

## Verification

To verify the publication of the Message API, follow these steps:

1. Open the Message API.
2. Check the lifecycle badge in the header of the Message API sidebar, for example **Published** or **Deprecated**.
3. When the environment uses the API review workflow, check the review badge, for example **In review** or **Review accepted**.
