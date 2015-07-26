from __future__ import unicode_literals
from shutil import rmtree

from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase
import factory
from faker import Faker

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
    @classmethod
    def setUp(cls):
        cls.user1 = UserFactory()
        cls.user1.set_password('secret')
        cls.user1.save()
        for i in range(10):
            PhotoFactory(user=cls.user1)

    def tearDown(cls):
        User.objects.all().delete()
        rmtree(settings.MEDIA_TEST)

    def test_photo_creation(self):
        self.assertEqual(Photo.objects.count(), 10)

    def test_photos_belong_to_user(self):
        pic1 = self.user1.photos.first()
        self.assertEqual(self.user1.photos.count(), 10)
        self.assertEqual(self.user1.username, pic1.user.username)

    def test_photo_do_not_belong_to_other_users(self):
        other_user = UserFactory()
        other_user.set_password('moresecret')
        other_user.save()
        self.assertEqual(other_user.photos.count(), 0)

    def test_photo_deletion_on_user_deletion(self):
        self.assertGreater(Photo.objects.count(), 0)
        self.user1.delete()
        self.assertEqual(Photo.objects.count(), 0)


class AlbumTestCase(TestCase):
    """Test albums can be created and assigned to users and albums."""
    @classmethod
    def setUp(cls):
        cls.user1 = UserFactory()
        cls.user1.set_password('secret')
        cls.user1.save()
        cls.album1 = AlbumFactory(user=cls.user1)
        cls.album2 = AlbumFactory(user=cls.user1)
        cls.pics = []
        for i in range(5):
            pic = PhotoFactory(user=cls.user1)
            pic.save()
            cls.pics.append(pic)

    def tearDown(cls):
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

