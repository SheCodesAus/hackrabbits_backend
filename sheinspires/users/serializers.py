from rest_framework import serializers
from .models import CustomUser

class RoleModelSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    skills = serializers.StringRelatedField(many=True)
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        skills = validated_data.pop('skills', [])
        user = CustomUser.objects.create_user(**validated_data)
        user.categories.set(categories)
        user.skills.set(skills)
        return user

#BS added create method first exclude many to many fields from validated user after it's created they both set and be a part of the user

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
        validated_data['user_type'] = "COMMUNITY_USER"

        return CustomUser.objects.create_user(**validated_data)
    
