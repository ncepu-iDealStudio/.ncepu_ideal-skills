import os
import allure
import pytest

from test.unit_test.common.decorators import allure_decorate
from test.unit_test.common.request_util import RequestUtil
from test.unit_test.utils.read_yaml import read_yaml

base_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.mark.resource
@allure.feature("XXXX接口")
class TestStudentSelectedCourseResource:

    @pytest.mark.parametrize("caseInfo", read_yaml(os.path.join(base_dir, "data/get.yaml")))
    @allure_decorate("注释信息")
    def test_get(self, caseInfo, env_dict):
        RequestUtil.test_body(caseInfo, env_dict)

    @pytest.mark.parametrize("caseInfo", read_yaml(os.path.join(base_dir, "data/post.yaml")))
    @allure_decorate("注释信息")
    def test_post(self, caseInfo, env_dict):
        RequestUtil.test_body(caseInfo, env_dict)

    @pytest.mark.parametrize("caseInfo", read_yaml(os.path.join(base_dir, "data/put.yaml")))
    @allure_decorate("注释信息")
    def test_update(self, caseInfo, env_dict):
        RequestUtil.test_body(caseInfo, env_dict)

    @pytest.mark.parametrize("caseInfo", read_yaml(os.path.join(base_dir, "data/delete.yaml")))
    @allure_decorate("注释信息")
    def test_delete(self, caseInfo, env_dict):
        RequestUtil.test_body(caseInfo, env_dict)
        