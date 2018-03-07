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
        req_header = "Response Headers: \n  {\n"
        for key, value in headers.items():
            req_header += ('    {}: {}\n'.format(key, value))
        req_header += "  }"
        self.logger.info(
            '\n Invoking REST Call... \n  api_url: %s,\n  method: %s,\n  headers: %s', api_url, method, req_header)

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
            emit = self.logger.warn
        Header = "Response Headers: \n{\n"
        for key, value in response.headers.items():
            Header += ('  {}: {}\n'.format(key, value))
        emit(Header + "}")
        if is_raw:
            emit('Response:\n%s\n' + response.text)
            print(response.text)
        else:
            emit('Response:\n' + json.dumps(payload, sort_keys=True, indent=2) + '\n')
            print(json.dumps(payload, sort_keys=True, indent=2))

        return ResponseWrapper(response.status_code, payload, response.headers)

    # Add aws request

    def aws_request(self, api_url, method, headers, params, auth, is_raw):
        req_header = "Response Headers: \n  {\n"
        for key, value in headers.items():
            req_header += ('    {}: {}\n'.format(key, value))
        req_header += "  }"
        self.logger.info(
            '\n Invoking REST Call... \n  api_url: %s,\n  method: %s,\n  headers: %s,\n  authrization: %s',
            api_url, method, req_header, auth)

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
        if is_raw or 'json' not in response.headers['content-type']:
            payload = {"__raw__": response.text}
        else:
            payload = response.json()

        if response.status_code < 300:
            emit = self.logger.debug
        else:
            emit = self.logger.warn
        Header = "Response Headers: \n{\n"
        for key, value in response.headers.items():
            Header += ('  {}: {}\n'.format(key, value))
        emit(Header + "}")
        if is_raw:
            emit('Response:\n%s\n' + response.text)
            print(response.text)
        else:
            emit('Response:\n' + json.dumps(payload, sort_keys=True, indent=2) + '\n')
            print(json.dumps(payload, sort_keys=True, indent=2))

        return ResponseWrapper(response.status_code, payload, response.headers)
