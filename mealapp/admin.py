from django.contrib import admin
from .models import UserProfile, Admin


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'weight_kg',
                    'height_cm', 'bmi', 'daily_calorie_goal')
    list_filter = ('gender',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('bmi',)

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('age', 'gender', 'height_cm', 'weight_kg', 'bmi')
        }),
        ('Goals', {
            'fields': ('daily_calorie_goal',)
        }),
    )


@admin.register(Admin)
class AdminProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)
