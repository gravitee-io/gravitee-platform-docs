# Vale workflow test page

This file contains deliberate writing errors so the Vale GitHub workflow can be
exercised end-to-end. **Delete this file after the test PR is reviewed.**

Add the `vale integration` label to the test PR to trigger the workflow.

## docs.Spelling — curated common typos (button expected)

teh quick brown fox. and the lazy dog. jsut a moment. thier setup. tihs is taht
problem. dat is the wrong word. wiht no warning. wnat the system to respond.

## docs.Spelling — typos resolved via pyspellchecker (button expected)

You can enbale the feature. For exmaple, see the table below. The handler will
recieve and process the request. Keep these values seperate. The error occured
during startup.

## docs.Spelling — typos resolved via accept.txt vocab (button expected, canonical casing)

Configure Opentelemtry tracing. Deploy on the kuberentes cluster. The graviteee
gateway forwards requests. The OTl shorthand also works.

## docs.Spelling — no candidate, no button (comment-only)

Garbage strings to confirm the no-suggestion path: xqzpzpz, qwzxmnb, plzvxc.

## Vale.Terms — preferred casing (existing rule, button expected)

We send the payload as protobuf over the network. Use the JavaScript SDK.

## Microsoft.Contractions — contraction expansion (existing rule, button expected)

You can not perform this action. The service does not respond. This is not the
correct value.

## Microsoft.We — first-person plural (existing rule, comment only)

We recommend enabling logging. Our gateway processes the request. Let us know.

## Microsoft.Adverbs — adverb removal (existing rule, button expected)

This is really easy to configure. The setup is very simple. The change is just
straightforward.

## Vale.Repetition — duplicate words (existing rule, button expected)

The the gateway forwards the the request to to the endpoint.
