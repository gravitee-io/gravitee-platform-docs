---
description: >-
  Learn how to create your Gravitee APIs using the Gravitee Management Console
  UI
---

# How-to

## Different options for creating your APIs

Gravitee offers two main ways for you to create your APIs in the Management Console UI:

* From scratch, via the API creation wizard
* Via import

This how-to guide will focus on _how_ to do the above. If you want to learn more about the various API creation options and concepts, please refer to the [Create APIs Concepts article.](concepts.md)

## Create your Gravitee API

To access the API creation flow, follow these steps:

## Create an API using Gravitee: HTTP GET over Kafka advanced

***

* Created by Alex Drag on 3/3/2023
* [Edit original on dubble](https://dubble.so/guides/create-an-api-using-gravitee-http-get-over-kafka-advanced-arzz7upr6bbxcnb1ulpp)

***

This is how you use the Gravitee API creation wizard to create an API. This API makes use of Gravitee's protocol mediation capabilities. We create an API that allows consumer to "GET" messages and events from a Kafka topic.

#### [1. We'll start in the dashboard. Find the APIs tab on the left.](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/)

![](https://dubble-prod-01.s3.amazonaws.com/assets/d1ba790b-0125-490a-9023-f2d8e0606747.png?0)

#### [2. Click on APIs in the left-hand nav.](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/1832f6d1-dcf1-4c5a-9472-6433cbb10b04/2.5/0.83333333333333/20.433436532508?0)

#### 3. Click on add Add API to add an API.

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/c3c953e6-aeb6-4a09-8c18-730774d68086/2.5/97.083333333333/11.351909184727?0)

#### [4. Click on Continue in the wizard](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/3eea0e89-b577-468c-a8b8-dc1eba32a0e6/2.5/30.416666666667/65.94427244582?0)

#### [5. It's time to fill in your basic details and API metadata. I'll start by filling in my name.](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/b875f67b-dd8c-466a-ab31-5301e4182869/2.5/57.578125/32.939886480908?0)

#### [6. Then I'll give the API a version number.](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/f3e33539-2056-4556-a657-497cd5a8806c/2.5/86.875/32.939886480908?0)

#### [7. Then, I'll give it a description.](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/ebdd340f-1de7-47fa-8435-4843393aaa32/1.6843003412969/63.984375/42.047213622291?0)

#### [8. Click on Validate my API details](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/b62c7ea2-5b4c-4cf4-ae6f-c89a347c6c30/2.5/86.588541666667/59.313725490196?0)

#### [9. Here, you're going to choose the kind of proxy and API that you want to create. We'll create a "message-based"](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

The general tule of

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/b85659f8-1470-4327-947e-09feaf3cfebf/2.5/41.484375/55.94523993808?0)

#### [10. Click on Select my API architecture](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/feb81b71-9f5d-4586-bd0f-874ec7e74546/2.5/86.588541666667/68.421052631579?0)

#### [11. Click on highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/24cec7f1-3b59-4ba9-acc0-ee51374dd0dc/2.5/41.484375/34.984520123839?0)

#### [12. Click on Select my entrypoints](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/3c6cb8b5-33fa-4fc6-a401-f527c42fa7d0/2.5/86.588541666667/89.886480908153?0)

#### [13. Type in highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/43adc2d6-b63b-4d46-a14e-b024927209dd/1.9242424242424/62.526041666667/50.554695562436?0)

#### [14. Click on highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/32ec8ccf-fdaf-4734-8725-cca4a0cf2542/1.9242424242424/62.526041666667/59.268575851393?0)

#### [15. Click on highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/0971992f-5f96-49e4-b62f-7d09aea98d98/1.8216444981862/63.984375/12.725748194014?0)

#### [16. Click on highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/863e2c6a-32dc-4906-a7c2-3dc13e4a6b59/1.8216444981862/63.984375/32.359391124871?0)

#### [17. Click on highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/f11b51b3-964f-4f37-b0e4-00207aa7e07f/2.5/42.447916666667/54.676212590299?0)

#### [18. Click on highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/cc602af3-5d8b-4922-8a92-b5dd788e7acc/2.5/42.447916666667/75.574045407637?0)

#### [19. Click on Validate my entrypoints](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/bf554a99-18b3-4eea-bfdf-87dc764eacf2/2.5/87.421875/90.879772961816?0)

#### [20. Click on highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/cef2174a-bcec-43a7-b2d5-d2fc63ee7867/2.5/41.484375/33.952528379773?0)

#### [21. Click on Select my endpoints](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/1baaac39-bf46-42ed-aa48-c34fb750323a/2.5/86.588541666667/87.409700722394?0)

#### [22. Type in highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/dbc637c4-d577-41b6-b1d6-bef1e99e0816/1.8216444981862/63.984375/39.338235294118?0)

#### [23. Click on +](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/4491f913-4a65-4a13-8244-d20487947c64/2.5/42.369791666667/58.642930856553?0)

#### [24. Type in highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/c02aab39-f463-4edf-8804-7a0375c9ff96/1.8733003708282/63.984375/60.287667698658?0)

#### [25. Click on PLAINTEXT](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/f2475562-5e40-4ed4-99c7-82d51764e03d/1.9273072060683/63.515625/55.050309597523?0)

#### [26. Click on SSL](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/dbaee55a-069c-478e-a9d1-d70002f901eb/1.8733003708282/63.984375/69.420794633643?0)

#### [27. Click on GSSAPI](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/db674ba4-5613-4560-b7c1-ef4d51c4b25e/1.98382923674/63.515625/56.004901960784?0)

#### [28. Click on OAUTHBEARER](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/f58c32b1-f835-4eff-82e7-200332f733ab/1.9273072060683/63.984375/61.706656346749?0)

#### [29. Click on sasl.jaas.config \*](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/e662ae09-4664-463b-a2ca-53f72a37fb20/1.9273072060683/63.984375/59.539473684211?0)

#### [30. Type in highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/fb446110-a878-4f50-ad7b-22de04b82625/1.9273072060683/63.984375/58.094685242518?0)

#### [31. Click on highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/4af58e06-bfd2-4abe-bec8-6c4a95d23217/2.0430463576159/63.515625/69.05959752322?0)

#### [32. Click on PEM](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/d9b853c4-e1c7-40f8-b5a3-1ee2c809592e/1.98382923674/63.984375/74.761351909185?0)

#### [33. Type in highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/c2e9fc38-6402-4468-8829-9cf87613c431/1.98382923674/63.984375/64.441434468524?0)

#### [34. Type in highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/f6dfd031-5dc1-4f07-8b50-1c41bccede95/1.98382923674/63.984375/70.865583075335?0)

#### [35. Click on ssl.trustStore.certificates](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/b93668ab-ea70-4474-9790-701e08e42ebf/1.98382923674/63.984375/78.115325077399?0)

#### [36. Type in highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/88952cd5-33b8-47a9-b0ae-705c12329911/1.98382923674/63.984375/76.670536635707?0)

#### [37. Click on highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/97899d8d-7da6-4485-9898-82c4cfa32475/2.0430463576159/63.515625/70.201238390093?0)

#### [38. Click on PEM](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/418a2ba8-fc67-4e1c-b3f6-73bff709b822/1.98382923674/63.984375/75.902992776058?0)

#### [39. Click on ssl.keystore.location](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/670b2f98-236b-4ed8-aec3-1d4562b9a2db/1.98382923674/63.984375/68.885448916409?0)

#### [40. Type in highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/0015e899-0211-47e7-8185-c27efa8e7214/1.98382923674/63.984375/67.440660474716?0)

#### [41. Type in highlight](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/f79705a5-2c33-4873-893a-ad693566dfa8/1.98382923674/63.984375/54.463364293086?0)

#### [42. Click on ssl.keystore.certificate.chain](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/ecc3cf50-6ed9-4911-875f-1bd0e09988c4/1.98382923674/63.984375/61.40350877193?0)

#### [43. Click on Validate my endpoints](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/3534fa03-a40e-4f05-91ea-5bface9e51fe/2.5/86.588541666667/89.880030959752?0)

#### [44. Click on Validate my plans](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/4b392f7e-ba3f-4ab2-8dda-f4eef463826d/2.5/86.588541666667/39.009287925697?0)

#### [45. Click on Validate my documentation](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/ced136a6-2eec-46a8-a7c3-418dd3f86385/2.5/86.588541666667/34.881320949432?0)

#### [46. Click on Create my API](https://apim-master-console.team-apim.gravitee.dev/#!/environments/DEFAULT/apis/new/create/v4)

![](https://d3q7ie80jbiqey.cloudfront.net/media/image/zoom/e7cc5989-411c-4d76-aacc-857cdf1c7a53/2.5/41.380208333333/86.171310629515?0)

