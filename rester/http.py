from logging import getLogger
from rester.struct import ResponseWrapper
import json
import requests


class HttpClient(object):
    logger = getLogger(__name__)
    ALLOWED_METHODS = ["get", "post", "put", "delete", "patch"]

    def __init__(self, **kwargs):
        self.extra_request_opts = kwargs

    def request(self, api_url, method, headers, params, is_raw):
        self.logger.info(
            '\n Invoking REST Call... api_url: %s, method: %s, headers: %s ', api_url, method, headers)

        try:
            func = getattr(requests, method)
        except AttributeError:
            self.logger.error('undefined HTTP method!!! %s', method)
            raise

        # String なら JSON として data に載せる
        if isinstance(params, str):
            try:
                json.loads(params)
                data = params
                params = None
            except json.decoder.JSONDecodeError:
                data = None
        else:
            data = None

        response = func(api_url, headers=headers, params=params, data=data, **self.extra_request_opts)

        if is_raw or 'json' not in response.headers['content-type']:
            payload = {"__raw__": response.text}
        else:    
            payload = response.json()

        if response.status_code < 300:
            emit = self.logger.debug
        else:
            emit = self.logger.warning
        emit('Response Headers: %s', str(response.headers))
        if is_raw:
            emit('Response:\n%s\n' + response.text)
        else:
            emit('Response:\n%s\n' + json.dumps(payload, sort_keys=True, indent=2))

        return ResponseWrapper(response.status_code, payload, response.headers)

    # Add aws request

    def aws_request(self, api_url, method, headers, params, auth, is_raw):
        self.logger.info(
            '\n Invoking REST Call... api_url: %s, method: %s, headers: %s, authrization: %s',
            api_url, method, headers, auth)

        try:
            func = getattr(requests, method)
        except AttributeError:
            self.logger.error('undefined HTTP method!!! %s', method)
            raise

        # String なら JSON として data に載せる
        if isinstance(params, str):
            try:
                json.loads(params)
                data = params
                params = None
            except json.decoder.JSONDecodeError:
                data = None
        else:
            data = None

        response = func(api_url, headers=headers, params=params, data=data, auth=auth, **self.extra_request_opts)
        self.logger.info(response.text)
        if is_raw or 'json' not in response.headers['content-type']:
            payload = {"__raw__": response.text}
        else:
            payload = response.json()

        if response.status_code < 300:
            emit = self.logger.debug
        else:
            emit = self.logger.warn
        emit('Response Headers: %s', str(response.headers))
        if is_raw:
            emit('Response:\n%s\n' + response.text)
        else:
            emit('Response:\n%s\n' + json.dumps(payload, sort_keys=True, indent=2))

        return ResponseWrapper(response.status_code, payload, response.headers)
