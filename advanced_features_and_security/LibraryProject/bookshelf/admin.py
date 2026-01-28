from django.contrib import admin
from .models import Book
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)

admin.site.register(Book, BookAdmin)

# Register your models here.
class CustomUserAdmin(UserAdmin):
    """
    custom admin interface for the user model.
    """
    model = CustomUser

    # fileds to diplay in the user list view
    list_display = ['username', 'email', 'date_of_birth', 'profile_photo']

    # fields to filter by in the sidebar
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']

    # fileds to search
    search_fields = ['username', 'email', 'date_of_birth']

    # ordering
    ordering = ['username']

    # fieldset for the user detail/edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {
            'fields': ('date_of_birth', 'profile_photo')
        })
    )

    # Fieldsets for adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)