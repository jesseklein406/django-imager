from __future__ import unicode_literals
from shutil import rmtree

from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase
import factory
from faker import Faker
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser
from django.test.utils import override_settings
from .models import Album, Photo

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Create a fake user."""
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user{}'.format(n))
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()


class PhotoFactory(factory.django.DjangoModelFactory):
    """Create a fake photo."""
    class Meta:
        model = Photo

    photo = factory.django.ImageField()
    title = fake.sentence()
    description = fake.text()
    user = factory.SubFactory(UserFactory)


class AlbumFactory(factory.django.DjangoModelFactory):
    """Create a fake album."""
    class Meta:
        model = Album

    title = fake.sentence()
    description = fake.text()
    user = factory.SubFactory(UserFactory)


class PhotoTestCase(TestCase):
    """Test photos can be created and assigned to users."""

    def setUp(self):
        self.user1 = UserFactory()
        self.user1.set_password('secret')
        self.user1.save()
        for i in range(10):
            PhotoFactory(user=self.user1)

    def tearDown(self):
        User.objects.all().delete()
        rmtree(settings.MEDIA_TEST)

    def test_photo_creation(self):
        self.assertEqual(Photo.objects.count(), 10)

    def test_photos_belong_to_user(self):
        pic1 = self.user1.photos.first()
        self.assertEqual(self.user1.photos.count(), 10)
        self.assertEqual(self.user1.username, pic1.user.username)

    def test_photos_do_not_belong_to_other_users(self):
        other_user = UserFactory()
        other_user.set_password('moresecret')
        other_user.save()
        self.assertEqual(Photo.objects.count(), 10)
        self.assertEqual(other_user.photos.count(), 0)

    def test_photo_deletion_on_user_deletion(self):
        self.assertGreater(Photo.objects.count(), 0)
        self.user1.delete()
        self.assertEqual(Photo.objects.count(), 0)


class AlbumTestCase(TestCase):
    """Test albums can be created and assigned to users and albums."""

    def setUp(self):
        self.user1 = UserFactory()
        self.user1.set_password('secret')
        self.user1.save()
        self.album1 = AlbumFactory(user=self.user1)
        self.album2 = AlbumFactory(user=self.user1)
        self.pics = []
        for i in range(5):
            pic = PhotoFactory(user=self.user1)
            pic.save()
            self.pics.append(pic)

    def tearDown(self):
        User.objects.all().delete()
        rmtree(settings.MEDIA_TEST)

    def test_album_creation(self):
        self.assertEqual(Album.objects.count(), 2)

    def test_albums_belong_to_user(self):
        self.assertEqual(self.user1.albums.count(), 2)
        self.assertEqual(self.user1.username, self.album1.user.username)

    def test_albums_do_not_belong_to_other_users(self):
        other_user = UserFactory()
        other_user.set_password('moresecret')
        other_user.save()
        self.assertEqual(other_user.albums.count(), 0)

    def test_add_photos_to_albums(self):
        self.assertEqual(self.album1.photos.count(), 0)
        self.album1.photos.add(*self.pics[:3])
        self.album2.photos.add(*self.pics[3:])
        self.assertEqual(self.album1.photos.count(), 3)
        self.assertEqual(self.album2.photos.count(), 2)

    def test_set_album_cover_photo(self):
        self.assertIsNone(self.album1.cover)
        self.album1.cover = self.pics[0]
        self.assertIsInstance(self.album1.cover, Photo)

    def test_album_deletion_on_user_deletion(self):
        self.assertGreater(Album.objects.count(), 0)
        self.user1.delete()
        self.assertEqual(Album.objects.count(), 0)


@override_settings(DEBUG=True)
class LiveServerTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(LiveServerTest, cls).setUpClass()
        cls.browser = Browser()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(LiveServerTest, cls).tearDownClass()

    def setUp(self):
        self.user1 = UserFactory()
        self.user1.set_password('secret')
        self.user1.save()
        self.album1 = AlbumFactory(user=self.user1)
        for i in range(10):
            pic = PhotoFactory(user=self.user1)
            self.album1.photos.add(pic)
            pic.save()
        # self.album1.cover = pic
        self.album1.save()
        pic.save()

    def login_helper(self, username, password):
        self.browser.visit('%s%s' % (self.live_server_url, '/accounts/login/'))

        self.browser.fill('username', username)
        self.browser.fill('password', password)
        self.browser.find_by_value('Log in').first.click()

    def test_library(self):
        self.login_helper(self.user1.username, 'secret')
        self.browser.visit('%s%s' % (self.live_server_url, '/images/library/'))
        images = self.browser.find_by_tag('img')
        self.assertEqual(len(images), 11)

    def test_edit(self):
        self.login_helper(self.user1.username, 'secret')
        self.browser.visit('%s%s' % (self.live_server_url, '/images/library/'))
        self.browser.find_by_tag('button')[8].click()
        self.browser.execute_script(
            'document.getElementById("title").value="Hijacked"'
        )
        self.browser.execute_script(
            'document.getElementById("description").value="hijacked"'
        )
        self.browser.find_by_id('submit').click()
        self.assertTrue(self.browser.is_text_present('Hijacked'))
