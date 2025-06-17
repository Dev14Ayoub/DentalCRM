## Roles and Permissions

1. **Administrator**
   - Full access to all data and system settings.
   - Can add, edit, delete doctors, patients, office assistants, leads, appointments, payments, prescriptions, notes, treatment plans.
   - Can manage users and assign roles.

2. **Doctor**
   - Can see patients assigned to them or in their clinic.
   - Can create and update patient notes, prescriptions, treatment plans.
   - Can schedule and update appointments.
   - Cannot delete patients or manage users/settings.

3. **Office Assistant**
   - Can see patients in their clinic.
   - Can manage appointments, payments, and basic patient info.
   - Can update appointments to another schedule.
   - Can delete appointments.
   - Cannot view or edit medical notes or prescriptions.
   - Cannot delete patients.

4. **Lead**
   - Can see leads and their contact info.
   - Can update lead status and notes.
   - Cannot access patient medical data or manage appointments/payments.

## User Interface ( UI ) Controls

- Buttons and actions in the UI will be shown or hidden based on user roles and permissions.
- Only allowed actions will be enabled for the user.
- Backend permission checks will enforce security regardless of UI controls.

## Implementation Suggestions

- Use Django Groups and Permissions framework.
- Assign users to groups representing roles.
- Use decorators and mixins to enforce permissions in views.
- Use Django template tags to conditionally render UI elements.
- Optionally, use custom permissions and object-level permissions for fine-grained control.

## Next Steps

- Implement group and permission setup.
- Update views and templates for permission enforcement.
- Test critical paths and edge cases.

Please confirm if you want me to proceed with the implementation or if you have any modifications or questions.
