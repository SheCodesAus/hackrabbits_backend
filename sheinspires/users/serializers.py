from rest_framework import serializers
from .models import CustomUser, Category, Skill, Invitation

class RoleModelSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all(), required=False)
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), required=False)


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
# BS: changed the catergories and skills fields to be able to handle many-to-many as they can't done by drf automatically, need customisation
# `PrimaryKeyRelatedField` allows the serializer to accept a list of primary keys for the related objects.
# The `queryset` ensures that only valid `Category` and `Skill` objects can be assigned to a user.
# The `many=True` parameter indicates that multiple related objects can be provided in the request.
# These fields will only validate the input and are handled separately in the `create` method for assignment.


class CommunityUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'image', 'current_role', 'location', 'phone_number', 'linkedin']

        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
            'first_name': {'required': True},
            'last_name': {'required': True},
            'image': {'required': True},
            'current_role': {'required': True},
            'location': {'required': True},
        }

        
    def create(self, validated_data):
        validated_data['user_type'] = "COMMUNITY_USER"

        return CustomUser.objects.create_user(**validated_data)
    
class InvitationSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source='full_name')
    currentRole = serializers.CharField(source='current_role')
    whyInspiring = serializers.CharField(source='why_inspiring')

    class Meta:
        model = Invitation
        fields = ['fullName', 'email', 'industry', 'currentRole', 'whyInspiring']

    def create(self, validated_data):
        # Convert camelCase to snake_case
        full_name = validated_data.pop('full_name')
        current_role = validated_data.pop('current_role')
        why_inspiring = validated_data.pop('why_inspiring')
        
        return Invitation.objects.create(
            full_name=full_name,
            current_role=current_role,
            why_inspiring=why_inspiring,
            **validated_data
        )