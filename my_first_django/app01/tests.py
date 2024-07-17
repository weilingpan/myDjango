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
