from django.test import TestCase
from django.shortcuts import reverse
# Create your tests here.


class LandingPageTest(TestCase):


    def test_get(self):
        # Todo some sort of test
        response = self.client.get(reverse("landing_page"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"landing.html")
        # print(response.content)
        # print(response.status_code)
    

    

    # def test_template_name(self):
    #     # todo some sort of test
    #     pass 



 

 