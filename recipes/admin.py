from django.contrib import admin
from .models import Recipe

# Register your models here.


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_by',
                    'servings', 'total_calories', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'image_url')
        }),
        ('Recipe Details', {
            'fields':  ('instructions', 'ingredients', 'servings')
        }),
        ('Time', {
            'fields': ('prep_time_minutes', 'cook_time_minutes')
        }),
        ('Nutrition', {
            'fields': ('total_calories', 'protein', 'carbs', 'fat')
        }),
        ('Ownership', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-assign created_by if not set"""
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
