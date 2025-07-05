from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View

from users.forms import RegisterForm
from users.models import Profile


class UserRegisterView(View):
    template_name = 'users/pages/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('users:dashboard'))
        register_form_data = request.session.get('register_form_data')
        form = RegisterForm(register_form_data)
        context = {
            'form': form,
            'form_action': reverse('users:create'),
        }
        return render(
            request, self.template_name, context=context
        )


class UserCreateView(View):
    def get(self, request):
        raise Http404()

    def post(self, request):
        import threading
        POST = request.POST
        FILES = request.FILES
        request.session['register_form_data'] = POST
        form = RegisterForm(POST, FILES)
        print(f"DEBUG: form.is_valid() = {form.is_valid()}")
        if not form.is_valid():
            print(f"DEBUG: form.errors = {form.errors}")
        if form.is_valid():
            user = form.save(commit=False)
            # Removed redundant password setting to avoid double hashing
            # user.set_password(user.password)
            user.save()
            print(f"DEBUG: user.is_active={user.is_active}, user.password={user.password}")
            print(f"DEBUG: user.has_usable_password()={user.has_usable_password()}")
            # Update profile fields after signal creates profile
            profile = user.profile
            profile.phone_number = form.cleaned_data.get('phone_number', '')
            profile.photo = form.cleaned_data.get('photo')
            # Set clinic from logged-in administrator if available
            if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.clinic:
                profile.clinic = request.user.profile.clinic
            else:
                clinic_name = form.cleaned_data.get('clinic')
                if clinic_name:
                    from clinic.models import Clinic
                    clinic_obj, created = Clinic.objects.get_or_create(name=clinic_name)
                    profile.clinic = clinic_obj

            profile.save()
            # Set user's first_name and last_name from form data
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.username = form.cleaned_data.get('username', user.username)
            user.set_password(form.cleaned_data.get('password1', ''))
            user.save()

            # Assign administrator role and permissions synchronously to ensure immediate recognition
            from administrator.models import Role, UserRole, Permission, RolePermission
            admin_role = Role.objects.filter(name='administrator').first()
            if admin_role:
                UserRole.objects.get_or_create(user=user, role=admin_role)
                add_patient_permission = Permission.objects.filter(codename='add_patient').first()
                if add_patient_permission:
                    RolePermission.objects.get_or_create(role=admin_role, permission=add_patient_permission)
                # Audit log for user role assignment
                from administrator.models import AuditLog
                AuditLog.objects.create(
                    user=user,
                    action_type='assign_role',
                    object_type='UserRole',
                    description=f"Assigned administrator role to user {user.username}"
                )

            user_created = _(
                'User has been created, please log in'
            )
            messages.success(request, user_created)
            del request.session['register_form_data']
            return redirect(reverse('users:login'))
        return redirect('users:register')


class ClearSessionView(View):
    http_method_names = ['post']

    def get(self, request):
        raise Http404()

    def post(self, request):
        if 'register_form_data' in request.session:
            del request.session['register_form_data']
        return JsonResponse({'success': True})
