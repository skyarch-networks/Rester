from logging import getLogger
from rester.exc import TestCaseExec
from rester.http import HttpClient
from rester.loader import TestSuite, TestCase
import yaml
import os.path
import codecs
import json

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
        case_name = os.path.basename(case.filename)
        res_dict = tc.get_dict(case_name)
        self._export_json(res_dict, case_name)
        # exportJSONで吐き出し
    def _export_json(self, res_dict, case_name):
        n = os.path.basename(case_name)
#        n.replace(r".yaml", r".json")
        f_name = "result_%s" %  n.replace(r".yaml", r".json")


        str = json.dumps(res_dict, indent=4, ensure_ascii=False)
        with open(f_name, 'w') as f:
            # JSONへの書き込み
            json.dump(res_dict, f,ensure_ascii=False,indent= 4)
        pass
        return

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

            print(c, "filename : %s " %(result.get('name')), end=' ')
            for k in ['passed', 'failed', 'skipped']:
                if k == 'passed':
                    c = bcolors.OKGREEN
                    print(c, end=' ')
                    for res in result.get(k):
                        print("\n %s: %s " % (k, res), end=' ')
                else:
                    c = bcolors.FAIL
                    print(c, end=' ')
                    for res in result.get(k):
                        print("\n %s: %s " % (k, res['name']), end=' ')
            print(bcolors.ENDC)



#TODO
# Support enums
# post processing
