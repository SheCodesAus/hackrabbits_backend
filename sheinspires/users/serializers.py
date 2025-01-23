from rest_framework import serializers
from .models import CustomUser

class RoleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    

class CommunityUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'image', 'current_role', 'location']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'image': {'required': True},
            'current_role': {'required': True},
            'location': {'required': True},
        }

    def create(self, validated_data):
        validated_data['user_type'] = CustomUser.USER_TYPES["COMMUNITY_USER"]
        return CustomUser.objects.create_user(**validated_data)
