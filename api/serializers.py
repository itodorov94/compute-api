from django.contrib.auth.models import User, Permission
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirmed = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirmed', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmed']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.is_staff = True
        can_view_request_perm = Permission.objects.get(name='Can view request')
        can_view_result_perm = Permission.objects.get(name='Can view result')
        user.user_permissions.add(can_view_request_perm)
        user.user_permissions.add(can_view_result_perm)
        user.save()

        return user
