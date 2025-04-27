# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Define the model
    model = CustomUser

    # The fields to display in the user list view
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "date_joined",
    )

    # Add filtering options to the admin panel
    list_filter = ("is_active", "is_staff", "date_joined")

    # The fields to search by in the admin panel
    search_fields = ("email", "first_name", "last_name")

    # The form layout for the user detail view in the admin
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "address_line1",
                    "address_line2",
                    "city",
                    "country",
                    "postal_code",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    # The fields for creating a new user (the "add" form)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    # Override the ordering to not use the non-existent 'username' field
    ordering = ("email",)  # Change 'username' to 'email' since 'username' doesn't exist


# Register the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)
