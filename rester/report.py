class ResultReport(object):
    '''
    テストケース(ステップ）の結果
    '''

    def __init__(self):
        pass
        self.__name = ""
        self.__url = ""
        self.__method = ""
        self.__params_header = {}  # パラメタの辞書が入る配列
        self.__params_query = []  # パラメタの辞書が入る配列
        self.__params_string = ""  # postのクエリ（文字列）
        self.__response_header = {}  # レスポンスの辞書が入る配列
        self.__response_body = []  # レスポンスの辞書が入る配列
        self.__evaluation = []  # 評価結果が入る配列
        self.__test_result = ""  # Pass or Fail or Skip

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, test_name: str):
        self.__name = test_name

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url: str):
        self.__url = url

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, method: str):
        self.__method = method

    @property
    def header(self):
        return self.__params_header

    @header.setter
    def header(self, header: dict):
        self.__params_header = header

    @property
    def query(self):
        return self.__params_query

    @query.setter
    def query(self, query_param: dict):
        self.__params_query = query_param

    @property
    def body(self):
        return self.__params_string

    @body.setter
    def body(self, body_string: str):
        self.__params_string = body_string

    @property
    def response_header(self):
        return self.__response_header

    @response_header.setter
    def response_header(self, response_header: dict):
        self.__response_header = response_header

    @property
    def test_result(self):
        return self.__test_result

    @test_result.setter
    def test_result(self, test_result: str):
        self.__test_result = test_result
