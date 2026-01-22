from django.test import TestCase

# Create your tests here.
from mealapp.models import Recipe

# Update a single recipe
recipe = Recipe.objects.first()
recipe.image_url = 'https://res.cloudinary.com/YOUR_CLOUD_'
'NAME/image/upload/v1234567890/recipe.jpg'
recipe.save()

# Or update multiple recipes
Recipe.objects.filter(title='Oatmeal').update(
    image_url='https://res.cloudinary.com/YOUR_CLOUD_NAME/'
    'image/upload/v1234567890/oatmeal.jpg'
)

exit()
