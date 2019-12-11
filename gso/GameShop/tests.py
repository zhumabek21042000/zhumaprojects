from django.test import TestCase, Client


# Create your tests here.
class MyViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()  # This sets up the test client

    def test_my_view(self):
        # A simple test that the view returns a 200 status code
        # In reality your test needs to check more than this depending on what your view is doing
        response = self.client.get('the/view/url')
        self.assertEqual(response.status_code, 200)
