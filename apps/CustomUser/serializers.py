from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Profile, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    avatar = serializers.SerializerMethodField(read_only=True)
    coverImage = serializers.SerializerMethodField(read_only=True)

    def __init__(self, instance=None,customizeFields:list=[],customizeDepth:int=None, **kwargs):
        super().__init__(instance=instance, **kwargs)
        self.Meta.depth = customizeDepth if customizeDepth is not None else None
        for field_name in set(self.fields) - set(customizeFields) : self.fields.pop(field_name) if len(customizeFields) > 0 else None
    

    class Meta:
        depth=0
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        user_obj = User.objects.create_user(**user_data)
        my_group,created = Group.objects.get_or_create(name='customer')
        my_group.user_set.add(user_obj)

        profile = Profile.objects.create(user=user_obj, **validated_data)

        return profile