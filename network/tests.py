from django.test import TestCase, Client
from django.db.models import Max
from .models import *




class ClientTestCase(TestCase):
    def setUP(self):
        user135 = User.objects.create(username = 'neko36723' , password='neko3457', email='neko4373@example.com')
        post1 = Postovi.objects.create(title='neki titl', post1='samosaomsaosm' ,userid=user135, date='2022-05-05', likes=5, username='neko367' )
    """Tests that page can be accesesd """
    def test_valid_home_page(self):
        c = Client()
        response= c.get("")
        self.assertEqual(response.status_code, 200)
        """Tests that page can be accesesd """
    def test_valid_npost(self):
        c = Client()
        response= c.get("/login")
        self.assertEqual(response.status_code, 200)
        """Tests that page can be accesesd """
    def test_valid_following(self):
        c = Client()
        response= c.get("/register")
        self.assertEqual(response.status_code, 200)
        """Tests that page can be accesesd """
    def test_valid_following(self):
        c = Client()
        response= c.get("/npost")
        self.assertEqual(response.status_code, 302)
        """Tests that page cthrows 404 error for index out of range """
    def test_invalid_post_page(self):
        #max_id = Postovi.objects.all().order_by("-id")[0]
        c = Client()
        response = c.get(f"/post/{75}")
        self.assertEqual(response.status_code, 302)

class Follow4FollowTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username = 'neko19' , password='neko19', email='neko19@example.com')
        user2 = User.objects.create(username = 'neko2' , password='neko2', email='neko2@example.com')
        user3 = User.objects.create(username = 'neko3' , password='neko3', email='neko3@example.com')
        user4 = User.objects.create(username = 'neko4' , password='neko4', email='neko4@example.com')
        user5 = User.objects.create(username = 'neko5' , password='neko5', email='neko5@example.com')
        a1 = Follow4Follow.objects.create(kogaprate_id=1, pratioci_id=2)
        a2 = Follow4Follow.objects.create(kogaprate_id=1, pratioci_id=3)
        a3 = Follow4Follow.objects.create(kogaprate_id=1, pratioci_id=4)
        a4 = Follow4Follow.objects.create(kogaprate_id=3, pratioci_id=1)
        a5 = Follow4Follow.objects.create(kogaprate_id=3, pratioci_id=2)
    def test_valid_folow_count1(self):
        """ Tests that followers of user with an id 1 is equal to 3 """
        a = Follow4Follow.objects.filter(kogaprate_id=1).count()
        self.assertEqual(a , 3)
    def test_valid_folow_count2(self):
        """ Tests that followers of user with an id 3 is equal to 2 """
        b = Follow4Follow.objects.filter(kogaprate_id=3).count()
        self.assertEqual(b , 2)
    def test_valid_folow_count3(self):
        """ Test that user with an id of 2 follows 2 users """
        c = Follow4Follow.objects.filter(pratioci_id=2).count()
        self.assertEqual(c , 2)
    def test_valid_folow_count4(self):
        """ Test that user with and id of 5 doesn't follow anyone"""
        d = Follow4Follow.objects.filter(pratioci_id=5).count()
        self.assertEqual(d , 0)
    def test_invalid_following(self):
        a = Follow4Follow.objects.create(kogaprate_id=1, pratioci_id=1)
        self.assertFalse(a.is_valid_pratioci())