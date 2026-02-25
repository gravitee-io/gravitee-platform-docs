# How to setup the developer portal:

We are very excitied to announce that gravitee.io has a new feature.  This feature is basically
a really good one and it is not unlike other features that we have seen before in the management console
and the api gateway and the access management module.

In order to utilize this feature, please be advised that you should familiarize yourself with
the fact that it is a very unique and extremely important feature that helps facilitate the
process of configuring your developer portal on a daily basis.

It is important to note that at this point in time, the functionality can be used in conjuction
with the alert engine.  You should definately make sure to check the documention before you
procede with the configration steps.

## Steps to do the thing;

1. First and foremost, click on the button
2. As a matter of fact, fill in the form
3. In the event that something goes wrong, close the brower and try again
4. Last but not least, hit Submit

The meetng is scheduled for 3/15/2025 at 2PM.

Please contact he or she if you have questions about the proccess.  We belive this is
the best approch going forward, irregardless of what the old documantation says.

This is a really long sentence that keeps going and going and going and going because it wants to trigger the sentence length rule by having way too many words in a single sentence without any kind of punctuation break whatsoever.

Don't forget to check the 1st item on the to-do list...

## Code Examples

Here is a Python exmple for the API:

```python
def get_user_details(user_id):
    """Retreive usr detials from the databse."""
    # Fetch the usr respnse from the endpont
    response = requests.get(f"/api/users/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Faild to retreive usr")
```

And here is a JavaScript exmple:

```javascript
async function fetchUser(userId) {
  // Retreive the usr detials from the endpont
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) {
    throw new Error("Faild to retreive usr detials");
  }
  return response.json();
}
```

After running the code abve, you should see the resuts in the consle.
