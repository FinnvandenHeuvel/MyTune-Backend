from rest_framework import serializers
from django.contrib.auth.models import User
from core.domain.models import Review
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")
        extra_kwargs = {
            "email": {"required": True},
        }

    def validate_email(self, value):
        """Ensure email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value

    def validate(self, attrs):
        """Ensure passwords match"""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")  # remove extra field
        return User.objects.create_user(**validated_data)


class MeSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "email", "date_joined", "is_admin"]

    def get_is_admin(self, obj):
        return bool(obj.is_staff or obj.is_superuser)

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "title",
            "artist",
            "artist_id",
            "album",
            "album_id",
            "content",
            "rating",
            "created_at",
        ]

