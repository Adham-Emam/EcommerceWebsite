from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "country",
        ]
        read_only_fields = ["id"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "country",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
