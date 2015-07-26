from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.test import TestCase
import factory
from faker import Faker

from .models import Album, Photo

# Create your tests here.
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
    """docstring for PhotoTestCase"""
    @classmethod
    def setUp(cls):
        user1 = UserFactory()
        user1.set_password('secret')
        user1.save()
        for i in range(100):
            PhotoFactory(user=user1)

    def test_photo_creation(self):
        self.assertTrue(Photo.objects.count() == 100)

    def test_photos_belong_to_user(self):
        user1 = User.objects.first()
        pic1 = user1.photos.first()
        self.assertEqual(user1.photos.count(), 100)
        self.assertEqual(user1.username, pic1.user.username)

    def test_photo_do_not_belong_to_other_users(self):
        other_user = UserFactory()
        other_user.set_password('moresecret')
        other_user.save()
        self.assertEqual(other_user.photos.count(), 0)
