from logging import getLogger
from rester.exc import TestCaseExec
from rester.http import HttpClient
from rester.loader import TestSuite, TestCase
import yaml

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class ApiTestCaseRunner:
    logger = getLogger(__name__)

    def __init__(self, options={}):
        self.options = options
        self.results = []

    def run_test_suite(self, test_suite_file_name):
        test_suite = TestSuite(test_suite_file_name)
        for test_case in test_suite.test_cases:
            self._run_case(test_case)

    def run_test_case(self, test_case_file):
        case = TestCase(None, test_case_file)
        self._run_case(case)

    def _run_case(self, case):
        tc = TestCaseExec(case, self.options)
        self.results.append(tc())

    def display_report(self):
        for result in self.results:
            if not result['failed']:
                continue
            print("\n\n ############################ FAILED ############################")
            for e in result['failed']:
                print(bcolors.FAIL, result.get('name'), ":", e['name'])
                print(bcolors.ENDC)
                for i, error in enumerate(e['errors']):
                    print("%d." % i)
                    print(error)
                    print()
                print("-------- LOG OUTPUT --------")
                print(e['logs'])
                print("---------------------------")

        print("\n\n ############################ RESULTS ############################")
        for result in self.results:
            c = bcolors.OKGREEN
            if result.get('failed'):
                c = bcolors.FAIL

            print(c, result.get('name'), end=' ')
            for k in ['passed', 'failed', 'skipped']:
                if k == 'passed':
                    for res in result.get(k):
                        print("\n%s: %s \n" % (k, res), end=' ')
                else:
                    for res in result.get(k):
                        print("\n%s: %s \n" % (k, res['name']), end=' ')
            print(bcolors.ENDC)
            #print c, yaml.dump(result, default_flow_style=False,), bcolors.ENDC


            

            #self.logger.info("name: {}\n{}\n", name, )
#            test_case = exc.case
#            print "\n\n ===> TestCase : {0}, status : {1}".format(test_case.name, "Passed" if test_case.passed == True else "Failed!")
#            for test_step in test_case.testSteps:
#                #self.logger.info('\n     ====> Test Step name : %s, status : %s, message : %s', test_step.name, test_step.result.status, test_step.result.message)
#                print "\n\n     ====> Test Step : {0}".format(test_step.name)
#
#                if hasattr(test_step, 'result'):
#                    print "\n\n         ====> {0}!".format(test_step.result.message)
#
#                if hasattr(test_step, 'assertResults'):
#                    for assert_result in test_step.assertResults:
#                        #self.logger.debug('\n assert_result : ' + str(assert_result))
#                        print "\n        ---> {0}".format(assert_result['message'])




#TODO
# Support enums
# post processing
