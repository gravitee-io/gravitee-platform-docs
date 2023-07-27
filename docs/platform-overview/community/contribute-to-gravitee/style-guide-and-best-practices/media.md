---
description: This page summarizes rules and best practices for docs media
---

# Media

## General

* Each media file must be uploaded with meaningful, descriptive name.
* If a single image is appropriate in several places, use the same file. This ensures consistent look and feel and facilitates image maintenance, e.g., one file must be replaced as opposed to several.
* When using Arcade to build interactive demos, give the video a meaningful, descriptive name and store it locally.
* When using Scribe or Dubble for how-to documentation, give screenshots meaningful, descriptive names and store them locally in a folder named after the article in which the Scribe/Dubble is used.
* Captions/alt text may consist solely of the file name where appropriate. Never include a figure number as a way to indicate image placement.

## Arcades

* Record in 1920 x 1080 for consistency and optimal UI appearance.
* Include an overlay page with a descriptive title.
* Enter a title that ensures the arcade is easy to find, reuse, and modify. The filename is shown as the URL above the arcade.
* Use the Gravitee organization defaults for fonts, colors, and background colors.
* Only add tooltips if they provide additional context, e.g., don't add a tooltip that says "click here."
* To show additional information, use the blue-colored hotspots with text that appears by default.&#x20;
  * Continue to use the Gravitee default hotspots to indicate the next area on which to click, but ensure the text does not appear by default to avoid confusing the reader.
* Use complete sentences for the tooltips.
* Delete frames where the cursor moves without showing anything useful, e.g., unnecessary scrolling.

Example:

{% @arcade/embed flowId="ditvkcx6pI6iFmYwQvt9" url="https://app.arcade.software/share/ditvkcx6pI6iFmYwQvt9" %}
