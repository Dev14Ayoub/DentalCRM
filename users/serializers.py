from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.forms import RegisterForm, UpdateForm
from users.models import Profile


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        source='profile.phone_number', required=False)
    from clinic.models import Clinic

    clinic = serializers.PrimaryKeyRelatedField(
        source='profile.clinic',
        queryset=Clinic.objects.all(),
        required=True,
        allow_null=False,
        write_only=True,
    )
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_staff = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',
                  'phone_number', 'clinic', 'is_staff']

    def get_is_staff(self, user):
        return user.is_staff

    def get_form_data(self, validated_data):
        profile = validated_data.get('profile', {})
        phone_number = profile.get('phone_number', '')
        clinic = profile.get('clinic', '')
        return {
            'username': validated_data.get('username', ''),
            'password1': validated_data.get('password1', ''),
            'password2': validated_data.get('password2', ''),
            'email': validated_data.get('email', ''),
            'first_name': validated_data.get('first_name', ''),
            'last_name': validated_data.get('last_name', ''),
            'phone_number': phone_number,
            'clinic': clinic,
        }

    def get_updated_data(self, user, validated_data):
        profile = validated_data.get('profile', {})
        phone_number = profile.get('phone_number', user.profile.phone_number)
        return {
            'username': validated_data.get('username', user.username),
            'password1': validated_data.get('password1', user.password),
            'password2': validated_data.get('password2', user.password),
            'email': validated_data.get('email', user.email),
            'first_name': validated_data.get('first_name', user.first_name),
            'last_name': validated_data.get('last_name', user.last_name),
            'phone_number': phone_number,
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        clinic = profile_data.pop('clinic', None)
        phone_number = profile_data.get('phone_number', '')

        form_data = self.get_form_data(validated_data)
        form_data['phone_number'] = phone_number
        if clinic:
            # Convert clinic object or ID to clinic name string for RegisterForm
            if hasattr(clinic, 'name'):
                form_data['clinic'] = clinic.name
            else:
                from clinic.models import Clinic
                try:
                    clinic_obj = Clinic.objects.get(id=clinic)
                    form_data['clinic'] = clinic_obj.name
                except Clinic.DoesNotExist:
                    form_data['clinic'] = ''

        register_form = RegisterForm(form_data)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(validated_data['password1'])
            user.save()
            profile = user.profile
            profile.phone_number = phone_number
            if clinic:
                profile.clinic = clinic
            profile.save()
            return user
        else:
            raise serializers.ValidationError(register_form.errors)

    def update(self, user, validated_data):
        form_data = self.get_updated_data(user, validated_data)
        update_form = UpdateForm(data=form_data, instance=user)
        if update_form.is_valid():
            user.username = form_data.get(
                'username', user.username)
            user.first_name = form_data.get(
                'first_name', user.first_name)
            user.last_name = form_data.get(
                'last_name', user.last_name)
            user.email = form_data.get('email', user.email)
            user.profile.phone_number = form_data.get(
                'phone_number', user.profile.phone_number)
            user.save()
            return user
        else:
            raise serializers.ValidationError(update_form.errors)

    def validate(self, data):
        if self.context['request'].method != 'PATCH':
            profile = data.get('profile', {})
            clinic = data.get('clinic') or profile.get('clinic')
            if not clinic:
                raise serializers.ValidationError(
                    'Clinic field is required.')
            if data['password1'] != data['password2']:
                raise serializers.ValidationError('Passwords must match.')
        return data
