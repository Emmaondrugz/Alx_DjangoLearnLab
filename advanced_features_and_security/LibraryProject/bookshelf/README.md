# Bookshelf App - Permissions and Groups Setup Guide

## Custom Permissions

This application uses custom permissions to control access to user management operations:

- **can_view**: Allows viewing user information
- **can_create**: Allows creating new users
- **can_edit**: Allows editing existing users
- **can_delete**: Allows deleting users

## Groups Configuration

### 1. Viewers Group
- **Permissions**: can_view
- **Purpose**: Users who can only view other users
- **Use Case**: Read-only access for auditors or observers

### 2. Editors Group
- **Permissions**: can_create, can_edit
- **Purpose**: Users who can create and modify user accounts
- **Use Case**: HR staff or user managers

### 3. Admins Group
- **Permissions**: can_view, can_create, can_edit, can_delete
- **Purpose**: Full access to all user management operations
- **Use Case**: System administrators

## Setting Up Groups (Django Shell)

Run: `python manage.py shell`
```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import CustomUser

# Get content type
content_type = ContentType.objects.get_for_model(CustomUser)

# Get permissions
can_view = Permission.objects.get(codename='can_view', content_type=content_type)
can_create = Permission.objects.get(codename='can_create', content_type=content_type)
can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)

# Create groups
editors = Group.objects.create(name='Editors')
editors.permissions.add(can_create, can_edit)

viewers = Group.objects.create(name='Viewers')
viewers.permissions.add(can_view)

admins = Group.objects.create(name='Admins')
admins.permissions.add(can_view, can_create, can_edit, can_delete)
```

## Assigning Users to Groups

### Via Django Admin:
1. Go to http://127.0.0.1:8000/admin/
2. Navigate to Users
3. Select a user
4. Scroll to "Groups" section
5. Select appropriate group(s)
6. Save

### Via Django Shell:
```python
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()
user = User.objects.get(username='testuser')
group = Group.objects.get(name='Editors')
user.groups.add(group)
```

## Protected Views

- **list_users** (`/users/`): Requires `can_view` permission
- **create_user** (`/users/create/`): Requires `can_create` permission
- **edit_user** (`/users/edit/<id>/`): Requires `can_edit` permission
- **delete_user** (`/users/delete/<id>/`): Requires `can_delete` permission

All views require user to be logged in (@login_required decorator).

## Testing Instructions

1. **Create test users:**
```python
   python manage.py createsuperuser  # Create admin first
```

2. **Create groups via Django shell** (see above)

3. **Create test users and assign to groups:**
   - viewer_user → Viewers group
   - editor_user → Editors group
   - admin_user → Admins group
   - no_perm_user → No group

4. **Test access:**
   - Login as each user
   - Try accessing each URL
   - Verify 403 Forbidden for unauthorized actions

## Expected Test Results

| User Type | can_view | can_create | can_edit | can_delete |
|-----------|----------|------------|----------|------------|
| Viewer    | ✓        | ✗          | ✗        | ✗          |
| Editor    | ✗        | ✓          | ✓        | ✗          |
| Admin     | ✓        | ✓          | ✓        | ✓          |
| No Perms  | ✗        | ✗          | ✗        | ✗          |