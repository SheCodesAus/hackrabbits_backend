from django.test import TestCase
from users.serializers import CommunityUserSerializer
from users.models import CustomUser

class CommunityUserSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "image": "http://example.com/image.jpg",
            "current_role": "Developer",
            "location": "PERTH",
            "password": "strongpassword123",
        }
        self.invalid_data = {
            "first_name": "",
            "last_name": "",
            "image": "",
            "current_role": "",
            "location": "",
            "password": "",
        }

    def test_valid_serializer(self):
        serializer = CommunityUserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.user_type, CustomUser.USER_TYPES["COMMUNITY_USER"])

    def test_invalid_serializer(self):
        serializer = CommunityUserSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
