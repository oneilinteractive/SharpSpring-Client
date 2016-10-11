# SharpSpring-Client

SharpSpring API client for Python.


## Requirements

* Python 2.7+
* Requests

## Quick Start

Here is a simple example on how to grab all of the leads for your given account_id and secret.

```python
from sharpsprinclient import SharpSpringRequest


account_id = 'account-id'
secret = 'some_secret'
request = SharpSpringRequest(account_id, secret)
response = request.method('getLeads').send()

print(response.json()) # {'id': <SomeID>, 'result': {[<Lead>, <Lead>, ...]}}
```

You can also submit a form with all of its fileds to the SharpSpring API.

```python
import urllib

from sharpsprinclient import SharpSpringRequestForm


app_id = 'aaaaaaaaaa'
postback_id = 'dddddddddddd'
endpoint_id = 'eeeeee-rrrr-llll-0000-ffffffff'
ss_tk_cookie = urllib.unquote(get_the_cookie_somehow())
form_data = {
    'first_name': 'mark',
    'last_name': 'testing',
    'email': 'mark@testing.test'
}
request = SharpSpringRequestForm(app_id=app_id, postback_id=postback_id,
        endpoint_id=endpoint_id, ss_tk_cookie=ss_tk_cookie)
response = request.send_form(form_data=form_data)

print(response) # jsonp callback function
```

If you wanted to update a lead with values that included a custom field defined in the SharpSpring dashboard, you would have to first get the field's `systemName` and then set it on the `updateLeads` call:

```python
from sharpspringclient import SharpSpringRequest

account_id = 'account-id'
secret = 'some_secret'
request = SharpSpringRequest(account_id, secret)

# get custom field 'Interested item' from SharpSpring
request.method('getFields')
request.where('label', 'Interested item')
interested_item_field = None

resp = api.send()

if resp.status_code == 200:
    data = resp.json()
    field = data['result']['field'][0]
    interested_item_field = field['systemName'] # this doesnt change so you can store it locally and save a lookup

# now update a specific lead
lead_data = {
    'emailAddress': 'some@email.address',
}

if interested_item_field:
    lead_data[interested_item_field] = interested_item_value

request.method('updateLeads') # we can reuse the same request instance
request.param('objects', [lead_data,])

resp = request.send()

print(resp)
````