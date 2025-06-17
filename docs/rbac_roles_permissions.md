# Role-Based Access Control (RBAC) for DentalCRM

## Roles and Permissions Overview

### 1. Administrator
- **Can see:**
  - All patients, doctors, office assistants, leads, appointments, payments, prescriptions, notes, treatment plans.
  - All dashboards and reports.
- **Can do:**
  - Create, update, delete any records.
  - Manage users and assign roles.
  - Access all system settings.
- **Restrictions:**
  - None (full access).

### 2. Doctor
- **Can see:**
  - Patients assigned to them or in their clinic.
  - Their own appointments, notes, prescriptions, treatment plans.
- **Can do:**
  - Create and update patient notes, prescriptions, treatment plans.
  - View patient medical history.
  - Schedule and update appointments.
- **Restrictions:**
  - Cannot delete patients.
  - Cannot manage users or system settings.

### 3. Office Assistant
- **Can see:**
  - Patients in their clinic.
  - Appointments, payments, and basic patient info.
- **Can do:**
  - Schedule appointments.
  - Manage patient contact info.
  - Record payments.
- **Restrictions:**
  - Cannot view or edit medical notes or prescriptions.
  - Cannot delete patients or appointments.

### 4. Lead
- **Can see:**
  - Leads and their contact info.
- **Can do:**
  - Update lead status and notes.
- **Restrictions:**
  - Cannot access patient medical data.
  - Cannot manage appointments or payments.

## Implementation Suggestions

- Use Django Groups to represent roles.
- Assign model-level and view-level permissions accordingly.
- Use decorators like `@permission_required` or mixins to enforce access.
- Customize templates to show/hide UI elements based on permissions.
- Consider object-level permissions for sensitive data if needed.

---

This document can be expanded with detailed permission lists and implementation steps.
