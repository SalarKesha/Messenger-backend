from django.db.models import Q
from rest_framework import serializers

from account.models import UserModel
from django.conf import settings

from private.models import PrivateChat


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password')
        required_fields = fields
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return UserModel.objects.create_user(validated_data.get('username'), validated_data.get('password'))


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'image')
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return settings.ORIGIN_URL + obj.image.url
        return None


class UserUpdateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'image')
        extra_kwargs = {
            'id': {'read_only': True},
        }
        # required_fields = ('image',)


class UserExploreSerializer(UserSerializer):
    private_chat = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'image', 'private_chat')
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def get_private_chat(self, obj):
        request = self.context.get('request')
        pc = PrivateChat.objects.filter(Q(owner=request.user, user=obj) | Q(owner=obj, user=request.user)).first()
        if pc:
            return pc.id
        return None
