import pytest
from django.test import TestCase
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

# Create your tests here.
class TestExample(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    # def setUp(self):
    #     self.client = APIClient()

    def test_route1(self):
        response = self.client.get('/app01/route1/')
        print(response.json())
        self.assertEqual(response.status_code, 200)

class Test01(TestCase):
    # 每一個測試方法執行前執行
    def setUp(self):
        print("======= start =======")

    def test01(self):
        print("run test01")

    def test02(self):
        print("run test02")

    # 每一個測試方法執行後執行
    def tearDown(self):
        print("======= end =======")


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        print("start===============!")

    def test01(self):
        print("run test01")

    def test02(self):
        print("run test02")

    @classmethod
    def tearDownClass(cls):
        print("end!===================")

# python manage.py test
# python manage.py test -v=2 # 顯示詳細資訊
