from logging import getLogger
from rester.http import HttpClient
from rester.struct import DictWrapper
from testfixtures import log_capture
from rester.aws import AWSLogin
import collections
import re
import traceback
from rester.report import ResultReport

Failure = collections.namedtuple("Failure", "errors output")


class TestCaseExec(object):
    logger = getLogger(__name__)

    def __init__(self, case, options):
        self.case = case
        self.options = options
        self.passed = []
        self.failed = []
        self.skipped = []
        self.reports = []

    def __call__(self):
        # What was this?
        #skip_all_subsequent_tests = False
        auth = ""
        token = ""
        access_token = ""
        values = self.case.variables._variables
        if values.keys() >= {'username', 'password', 'client_id', 'account_id', 'region_name', 'identity_pool_id',
                             'user_pool_id'}:
            auth, token, access_token = AWSLogin.cognito_login(values['username'], values['password'],
                                                               values['identity_pool_id'],values['client_id'],
                                                               values['region_name'], values['account_id'],
                                                               values['user_pool_id'])
        elif values.keys() >= {'region_name', 'identity_pool_id'}:
           auth, token = AWSLogin.cognito_auth(values['region_name'], values['identity_pool_id'])

        self.case.variables._variables['__token'] = token
        self.case.variables._variables['__access_token'] = access_token

        for step in self.case.steps:
            self.step_report = ResultReport()
            self.step_report.name = step.name
            self.step_report.method = step.method
            self.logger.debug('Test Step Name : %s', step.name)
            if step.get('skip', False):
                self.logger.info('\n=======> Skipping test case : ' + step.name)
                self.skipped.append(step)
                continue

            @log_capture()
            def _run(l):

                failures = self._execute_test_step(step, auth, token, self.step_report)
                return failures, l

            f, logs = _run()
            if f:
                self.failed.append((step, Failure(f.errors, "".join(self._format_logs(logs)))))
            else:
                self.passed.append(step)
            self.reports.append(self.step_report)

        return self._result()

    def _result(self):
        d = dict(name=self.case.filename,
                 passed=sorted([step.name for step in self.passed]),
                 failed=None,
                 skipped=sorted([step.name for step in self.skipped]))
        d['failed'] = f = []
        for step, failure in self.failed:
            f.append(dict(name=step.name, errors=failure.errors, logs=failure.output))
        return d

    def _format_logs(self, lc):
        for r in lc.actual():
            yield "%s: %s - %s\n" % (r[1], r[0], r[2])

    def _build_param_dict(self, test_step):
        params = {}
        if hasattr(test_step, 'params') and test_step.params is not None:
            # JSON は String のまま
            if isinstance(test_step.params, str):
                return test_step.params
            for key, value in test_step.params.items().items():
                params[key] = self.case.variables.expand(value)
        return params

    def _build_data_dict(self, test_step):
        data = {}
        if hasattr(test_step, 'payload') and test_step.payload is not None:
            for key, value in test_step.payload.items().items():
                data[key] = self.case.variables.expand(value)
                self.logger.info(data[key])
        return data

    def _execute_test_step(self, test_step, auth, token, report):
        http_client = HttpClient(**self.case.request_opts)
        failures = Failure([], None)
        try:
            method = getattr(test_step, 'method', 'get')
            is_raw = getattr(test_step, 'raw', False)
            self.logger.info('\n=======> Executing TestStep : %s, method : %s', test_step.name, method)

            # process and set up headers
            headers = {}
            if hasattr(test_step, 'headers') and test_step.headers is not None:
                self.logger.debug('Found Headers')
                for key, value in test_step.headers.items().items():
                    headers[key] = self.case.variables.expand(value)


            # process and set up params
            params = self._build_param_dict(test_step)
            url = self.case.variables.expand(test_step.apiUrl)
            self.logger.debug('Evaluated URL : %s', url)

            # レポートの処理
            report.header = headers
            if isinstance(params, dict):
                report.query = params
            else:
                report.body = params
            report.url = url

            print("\n", test_step.name)

            # Add Aws Token from cognito

            if token is not None and auth is not None:
                headers.setdefault("x-amz-security-token", token)
                response_wrapper = http_client.aws_request(url, method, headers, params, auth, is_raw)
            else:
                response_wrapper = http_client.request(url, method, headers, params, is_raw)

            headers = response_wrapper.headers.items()
            try:
                report.response_header = headers
            except AttributeError:
                report.response_header = ""
            pass

            # expected_status = getattr(getattr(test_step, 'asserts'), 'status', 200)
            # if response_wrapper.status != expected_status:
            #     failures.errors.append("status(%s) != expected status(%s)" % (response_wrapper.status, expected_status))

            if hasattr(test_step, "asserts"):
                asserts = test_step.asserts
                if hasattr(asserts, "headers"):
                    self._assert_element_list('Header', failures, test_step, response_wrapper.headers, test_step.asserts.headers.items().items())

                if hasattr(asserts, "payload"):
                    self.logger.debug('Evaluating Response Payload')
                    self._assert_element_list('Payload', failures, test_step, response_wrapper.body, test_step.asserts.payload.items().items())
            else:
                self.logger.warn('\n=======> No "asserts" element found in TestStep %s', test_step.name)

        except Exception as inst:
            failures.errors.append(traceback.format_exc())
            self.logger.error('ERROR !!! TestStep %s Failed to execute !!!  %s \
                        \n !!! Will ignore all assignment statements as part of TestStep', test_step.name, inst)
            self.logger.exception('Exception')

        if failures.errors:
            return failures
        
        # execute all the assignment statements
        if hasattr(test_step, 'postAsserts') and test_step.postAsserts is not None:          
            for key, value in test_step.postAsserts.items().items():
                self._process_post_asserts(response_wrapper.body, key, value)

        return None

    def _assert_element_list(self, section, failures, test_step, response, assert_list):
        self.logger.debug("Inside assert_element_list: %s", response)

        test_step.assertResults = []

        for key, value in assert_list:
            self.logger.debug('key : %s, value : %s', key, value)
            json_eval_expr = getattr(response, key, '')
            if json_eval_expr is None:
                assert_message = 'assert statement :%s not found in target response', key
                self.logger.error('%s', assert_message)
                failures.errors.append(assert_message)
                continue

            self.logger.debug('---> json_eval_expr : %s and type : %s', json_eval_expr, type(json_eval_expr))

            # check for basic JSON types
            json_types = {'Integer':'int', 'String':'str', 'Array':'list', 'Float':'float', 'Boolean':'bool', 'Object':'dict'}
            if value in json_types:
                self.logger.info('Found json type : %s ', value)

                if type(json_eval_expr) == DictWrapper:
                    value = 'Object'
                    json_eval_expr = {}

                if type(json_eval_expr) == str:
                    json_eval_expr = ''

                value = eval(json_types[value])
                json_eval_expr = type(json_eval_expr)


            # Check for logical operators
            logic_ops = {'-gt':'>', '-ge':'>=', '-lt':'<', '-le':'<=', '-ne':'!=', '-eq':'==',
                         'exec': 'exec', '-in': 'in'}
            lg_op_expr = check_for_logical_op(value)
            if lg_op_expr:
                self.logger.debug("---> Found lg_op_expr : " + lg_op_expr)

            if lg_op_expr in logic_ops:
                final_lg_op = logic_ops[lg_op_expr]
                value = value[len(lg_op_expr):]
                self.logger.debug("     -----> Rest of the expression : " + value)
            else:
                # - If no operators found then assume '=='
                final_lg_op = logic_ops['-eq']

            self.logger.debug("---> Final final_lg_op : " + final_lg_op)

            # do variable expansion...
            value = self.case.variables.expand(value)
            self.logger.debug(' ---> final evaluated expression  : %s and type %s ', value, type(value))

            if isinstance(json_eval_expr, str):
                value = str(value)
            # construct the logical assert expression
            if final_lg_op != 'exec' and final_lg_op != 'in':
                assert_expr = 'json_eval_expr {0} value'.format(final_lg_op)
                assert_literal_expr = "{}:{{{}}} {} {}".format(key, json_eval_expr, final_lg_op, value)
                self.logger.debug('     ---> Assert_expr : ' + assert_expr)
                assert_result = eval(assert_expr)
            elif final_lg_op == 'in':
                assert_literal_expr = "{}:{{{}}} {} {}".format(key, json_eval_expr, final_lg_op, value)
                li = value.split(',')
                num = 0
                for item in li:
                    if json_eval_expr.find(item) != -1:
                        num += 1
                if num == len(li):
                    assert_result = True
                else:
                    assert_result = False
            else:
                assert_expr = 'exec_result = {0}'.format(value)
                assert_literal_expr = '"f({0}) <- {1}"'.format(json_eval_expr, value)
                exec(assert_expr)
                assert_result = _evaluate(value, json_eval_expr)

            self.logger.debug('assert evaluation result  : %s', assert_result)

            if not assert_result:
                assert_message = '{} Assert Statement : {}   ---> Fail!'.format(section, assert_literal_expr)
                self.logger.error('%s', assert_message)
                failures.errors.append(assert_message)
            else:
                assert_message = '{} Assert Statement : {}  ----> Pass!'.format(section, assert_literal_expr)
                self.logger.info('%s', assert_message)

    def _process_post_asserts(self, response, key, value):
        self.logger.debug("evaled value: {}".format(getattr(response, value, '')))
        self.case.variables.add_variable(key, getattr(response, value, ''))

def _evaluate(clause, value):
    assert_expr = 'result = {0}'.format(clause)
    #self.logger.debug('     ---> Assert_exec : ' + assert_expr)
    exec(assert_expr)
    return result #@UndefinedVariable


def check_for_logical_op(expression):
    if expression and isinstance(expression, str):
        #self.logger.debug("_check_for_logical_op : expression %s", expression)
        oprtr_regex = re.compile("-lt|-le|-gt|-ge|-eq|-ne|exec|-in")
        match = re.match(oprtr_regex, expression)
        if match:
            return match.group()
