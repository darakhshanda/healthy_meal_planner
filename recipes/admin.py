from django.contrib import admin
from .models import Recipe

# Register your models here.


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'total_calories',
                    'protein', 'carbs', 'fat', 'created_by', 'created_at')
    list_filter = ('category', 'created_at', 'created_by')
    search_fields = ('title', 'description', 'instructions')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'image_url', 'serving_size')
        }),
        ('Instructions', {
            'fields': ('instructions',)
        }),
        ('Nutritional Information', {
            'fields': ('total_calories', 'protein', 'carbs', 'fat')
        }),
        ('Meta', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
