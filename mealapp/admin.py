from .models import MealPlan, UserProfile, Recipe
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# INLINE PROFILE IN USER ADMIN


class UserProfileInline(admin.StackedInline):  # Fixed: Removed extra space
    """Display profile inline with user in admin"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

    # Only show these fields in admin
    fields = ('age', 'gender', 'height_cm',
              'weight_kg', 'bmi', 'daily_calorie_goal')
    readonly_fields = ('bmi', 'daily_calorie_goal')


# CUSTOM USER ADMIN


class CustomUserAdmin(BaseUserAdmin):
    """Extended User admin with profile"""
    inlines = (UserProfileInline,)

    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ()}),
    )


# Re-register UserAdmin with profile inline
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# USER PROFILE ADMIN


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'gender', 'height_cm',
                    'weight_kg', 'bmi', 'daily_calorie_goal']
    list_filter = ['gender', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = [
        'bmi', 'daily_calorie_goal', 'created_at', 'updated_at']

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('age', 'gender', 'height_cm', 'weight_kg')
        }),
        ('Calculated Fields', {
            'fields': ('bmi', 'daily_calorie_goal'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# RECIPE ADMIN


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category',
                    'total_calories', 'created_by', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'created_by']

    fieldsets = (
        ('Recipe Information',
         {'fields':
          ('title', 'description', 'category',
           'image_url', 'servings', 'total_calories')
          }),
        ('Cooking Details',
         {'fields':
          ('prep_time_minutes', 'cook_time_minutes',
           'ingredients', 'instructions')
          }),
        ('Nutrition Information', {
            'fields': ('protein', 'carbs', 'fat'),
            'classes': ('collapse',)
        }),
        ('Author', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-set created_by to current user"""
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
# MEAL PLAN ADMIN


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'day', 'breakfast_recipe',
                    'lunch_recipe', 'dinner_recipe', 'snack_recipe']
    list_filter = ['day', 'user']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User & Date', {
            'fields': ('user', 'day')
        }),
        ('Meal Assignments',
         {'fields':
          ('breakfast_recipe', 'lunch_recipe', 'dinner_recipe', 'snack_recipe')
          }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
