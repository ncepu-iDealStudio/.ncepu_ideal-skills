#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pytest

from test.unit_test.common.decorators import allure_decorate
from test.unit_test.common.request_util import RequestUtil
from test.unit_test.common.function_test_util import FunctionTestUtil
from test.unit_test.tools.read_yaml import read_yaml

base_url = os.path.dirname(os.path.abspath(__file__))


class TestSysDepartmentinfoService:
    @pytest.mark.parametrize("caseInfo", read_yaml(os.path.join(base_url, "data.yaml")))
    def test_sub_count(self, caseInfo):
        FunctionTestUtil.test_body(caseInfo)
        