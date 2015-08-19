from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client, TestCase
from django.test.utils import override_settings

import factory
from faker import Faker
from shutil import rmtree
from splinter import Browser
from time import sleep

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
        sleep(3)

    def setUp(self):
        self.user1 = UserFactory()
        self.user1.set_password('secret')
        self.user1.save()
        self.album1 = AlbumFactory(user=self.user1)
        for i in range(10):
            pic = PhotoFactory(user=self.user1)
            self.album1.photos.add(pic)
            pic.save()
        self.album1.save()
        pic.save()

    def login_helper(self, username, password):
        self.browser.visit('%s%s' % (self.live_server_url, '/accounts/login/'))

        self.browser.fill('username', username)
        self.browser.fill('password', password)
        self.browser.find_by_value('Log in').first.click()

    def test_library_view(self):
        self.login_helper(self.user1.username, 'secret')
        self.browser.visit('%s%s' % (self.live_server_url, '/images/library/'))
        images = self.browser.find_by_tag('img')
        self.assertEqual(len(images), 11)


"""The following tests were completed with reference to the work of Nick Draper
and Megan Slater. Original found at:
https://github.com/ndraper2/django-imager/blob/master/imagersite/imager_images/tests.py
"""


class LibraryViewTestCase(TestCase):
    def setUp(self):
        user1 = UserFactory.create(username='alice')
        user1.set_password('secret')
        user1.save()
        user2 = UserFactory.create(username='bob')
        user2.set_password('secret')
        user2.save()
        pic = PhotoFactory.create(user=user1)
        pic.save()
        album = AlbumFactory.create(user=user1)
        album.save()
        album.photos.add(pic)

    def test_library_view(self):
        photo = Photo.objects.all()[0]
        album = Album.objects.all()[0]
        client = Client()
        client.login(username='alice', password='secret')
        response = client.get('/images/library/')
        # Check for truncated titles
        self.assertContains(response, photo.title[:20])
        self.assertContains(response, album.title[:20])

    def test_library_view_different_user(self):
        photo = Photo.objects.all()[0]
        album = Album.objects.all()[0]
        client = Client()
        client.login(username='bob', password='secret')
        response = client.get('/images/library/')
        self.assertNotContains(response, photo.title[:20])
        self.assertNotContains(response, album.title[:20])

    def test_library_unauthenticated(self):
        client = Client()
        response = client.get('/images/library/', follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertContains(response, 'input type="submit" value="Log in"')


class PhotoAddTestCase(TestCase):
    def setUp(self):
        user = UserFactory.create(username='alice')
        user.set_password('secret')
        user.save()
        pic = PhotoFactory.create(user=user)
        pic.save()
        album = AlbumFactory.create(user=user)
        album.save()
        album.photos.add(pic)

    def test_add_photo(self):
        client = Client()
        client.login(username='alice', password='secret')
        with open('imagersite/static/images/django_thumb.jpg', 'rb') as fh:
            response = client.post(
                '/images/photos/add/',
                {'file': fh, 'title': 'test title', 'published': 'private'},
                follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test title')

    def test_photo_add_unauthenticated(self):
        client = Client()
        response = client.get('/images/photos/add', follow=True)
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertContains(response, 'input type="submit" value="Log in"')


class PhotoEditTestCase(TestCase):
    def setUp(self):
        user = UserFactory.create(username='alice')
        user.set_password('secret')
        user.save()
        user2 = UserFactory.create(username='bob')
        user2.set_password('secret')
        user2.save()
        photo = PhotoFactory.create(user=user)
        photo.save()

    def test_edit_photo(self):
        client = Client()
        client.login(username='alice', password='secret')
        photo = Photo.objects.all()[0]
        response = client.get('/images/photos/{}/edit/'.format(photo.id))
        self.assertContains(response, photo.title[:20])
        with open('imagersite/static/images/django_thumb.jpg', 'rb') as fh:
            response = client.post(
                '/images/photos/{}/edit/'.format(photo.id),
                {
                    'file': fh,
                    'title': 'new test title',
                    'published': 'private'
                },
                follow=True
            )
        self.assertContains(response, 'new test title')
        response = client.get('/images/photos/{}/'.format(photo.id))
        self.assertContains(response, 'new test title')

    def test_edit_other_user(self):
        # what you end up with is a create form for yourself.
        client = Client()
        client.login(username='bob', password='secret')
        photo = Photo.objects.all()[0]
        with open('imagersite/static/images/django_thumb.jpg', 'rb') as fh:
            response = client.post(
                '/images/photos/{}/edit/'.format(photo.id),
                {
                    'file': fh,
                    'title': 'other user',
                    'published': 'private'
                },
                follow=True
            )
        self.assertEqual(response.status_code, 404)
        # alice = User.objects.get(username='alice')
        # self.assertEqual(photo.user, alice)
        # self.assertNotIn(photo.title, 'other user')

    def test_photo_edit_unauthenticated(self):
        client = Client()
        photo = Photo.objects.all()[0]
        response = client.get(
            '/images/photos/{}/edit/'.format(photo.id), follow=True
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertContains(response, 'input type="submit" value="Log in"')


class AlbumAddTestCase(TestCase):
    def setUp(self):
        user = UserFactory.create(username='alice')
        user.set_password('secret')
        user.save()
        user2 = UserFactory.create(username='bob')
        user2.set_password('secret')
        user2.save()
        photo = PhotoFactory.create(user=user)
        photo.save()

    def test_add_album(self):
        client = Client()
        client.login(username='alice', password='secret')
        photo = Photo.objects.all()[0]
        response = client.post(
            '/images/album/add/',
            {
                'title': 'new album title',
                'photos': photo.id,
                'published': 'private',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'new album title')
        album = Album.objects.all()[0]
        self.assertIn(photo, album.photos.all())

    def test_album_add_unauthenticated(self):
        client = Client()
        response = client.get('/images/album/add/', follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertContains(response, 'input type="submit" value="Log in"')


class AlbumEditTestCase(TestCase):
    def setUp(self):
        user = UserFactory.create(username='alice')
        user.set_password('secret')
        user.save()
        user2 = UserFactory.create(username='bob')
        user2.set_password('secret')
        user2.save()
        pic = PhotoFactory.create(user=user)
        pic.save()
        album = AlbumFactory.create(user=user)
        album.save()
        album.photos.add(pic)

    def test_edit_other_user(self):
        client = Client()
        client.login(username='bob', password='secret')
        album = Album.objects.all()[0]
        response = client.post(
            '/images/album/{}/edit/'.format(album.id),
            {
                'title': 'other user',
                'published': 'private'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 404)

    def test_album_edit_unauthenticated(self):
        client = Client()
        album = Album.objects.all()[0]
        response = client.get(
            '/images/album/{}/edit/'.format(album.id), follow=True
        )
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertContains(response, 'input type="submit" value="Log in"')
