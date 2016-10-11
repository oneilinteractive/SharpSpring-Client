import json
import uuid
import urllib
import logging

import requests


LOG = logging.getLogger(__name__)


class SharpSpringRequest(object):
    _uri = 'http://api.sharpspring.com/pubapi/v1/'

    def __init__(self, api_account_id, api_secret_key):
        self.api_account_id = api_account_id
        self.api_secret_key = api_secret_key

        self.reset()

    def reset(self):
        self._method = None
        self._where = {}
        self._data = {}
        self._params = {}
        self._limit = None
        self._offset = None

        return self

    def __setitem__(self, key, value):
        self._data[key] = value

        return self

    def __getitem__(self, key):
        return self._data.get(key, None)

    def __delitem__(self, key):
        del self._data[key]

    @property
    def data(self):
        data = self._data
        params = self._params
        params['where'] = self._where or {}
        params['limit'] = self._limit or ''
        params['offset'] = self._offset or ''
        data['params'] = params

        return data

    def where(self, key, value):
        self._where[key] = value

        return self

    def param(self, key, value):
        self._params[key] = value

        return self

    def method(self, method):
        self['method'] = method

        return self

    def _info(self, prepared):
        info = '{}\n{}\n----HEADERS----\n{}\n----BODY----\n{}'.format(
            '-----------START-----------',
            prepared.method + ' ' + prepared.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in 
                prepared.headers.items()),
            prepared.body,
        )
        LOG.info(info)

    def send(self):
        try:
            self['id'] = str(uuid.uuid4())
            params = {
                'accountID': self.api_account_id,
                'secretKey':  self.api_secret_key,
            }
            sess = requests.Session()
            req = requests.Request('post', self._uri, params=params,
                json=self.data)

            prepped = req.prepare()

            self._info(prepped)
            self.reset()

            return sess.send(prepped)
        except Exception as e:
            raise e


class SharpSpringRequestForm(SharpSpringRequest):
    """
    This class handles sending form data via the API instead of through
    JavaScript.

    In order to use this class you must collect a few params from the
    form embed code provided by SharpSpring

    'baseURI', 'https://app-aaaaaaaaaa.marketingautomation.services/webforms/receivePostback/dddddddddddd/'
    'endpoint', 'eeeeee-rrrr-llll-0000-ffffffff'

    Using the except from an embed code, we can extract the values are needed
        app_id is aaaaaaaaaa
        postback_id is dddddddddddd
        endpoint_id is eeeeee-rrrr-llll-0000-ffffffff
    """

    def __init__(self, app_id, postback_id, endpoint_id,
                 ss_tk_cookie=None):
        super(RequestForm, self).__init__()

        if not app_id or not postback_id or not endpoint_id:
            msg = 'The app_id, postback_id, and endpoint_ids are required'

            raise Exception(msg)

        self.app_id = app_id
        self.postback_id = postback_id
        self.endpoint_id = endpoint_id

        if ss_tk_cookie:
            self['trackingid__sb'] = ss_tk_cookie

        self.form_uri = ('https://app-{}.marketingautomation.services/'
                         'webforms/receivePostback/{}/{}/'
                         'jsonp/').format(self.app_id, self.postback_id,
                                          self.endpoint_id)

    def send_form(self, form_data=None):
        """"""
        form_data = form_data or {}

        for k, v in form_data.items():
            self[k] = v

        try:
            data = self.data

            del data['params']

            sess = requests.Session()
            req = requests.Request('post', self.form_uri, params=data)
            prepped = req.prepare()

            self._info(prepped)
            self.reset()

            return sess.send(prepped)
        except Exception as e:
            raise e
