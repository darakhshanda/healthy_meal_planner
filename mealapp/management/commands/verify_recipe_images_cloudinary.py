from django.core.management.base import BaseCommand
from mealapp.models import Recipe
import cloudinary
import cloudinary.api
import os


class Command(BaseCommand):
    help = 'Check each recipe image_url against Cloudinary uploads and report missing or mismatched images.'

    def handle(self, *args, **options):
        cloud_name = cloudinary.config().cloud_name
        checked = 0
        missing = 0
        valid = 0
        for recipe in Recipe.objects.all():
            url = str(recipe.image_url)
            if 'cloudinary.com' in url:
                # Extract public_id from URL
                try:
                    # Cloudinary URLs look like: https://res.cloudinary.com/<cloud_name>/image/upload/v1234567890/recipes/recipe_title_id.jpg
                    parts = url.split(f"/{cloud_name}/image/upload/")
                    if len(parts) == 2:
                        public_id = parts[1].split('.')[0]  # Remove extension
                        public_id = public_id.split(
                            '?')[0]  # Remove query params
                        # Check if resource exists
                        try:
                            cloudinary.api.resource(public_id)
                            valid += 1
                        except cloudinary.exceptions.NotFound:
                            self.stdout.write(self.style.ERROR(
                                f"Missing on Cloudinary: {recipe.title} ({public_id})"))
                            missing += 1
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"Could not parse public_id for {recipe.title}: {url}"))
                        missing += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"Error checking {recipe.title}: {e}"))
                    missing += 1
            else:
                self.stdout.write(self.style.WARNING(
                    f"Not a Cloudinary URL: {recipe.title} ({url})"))
                missing += 1
            checked += 1
        self.stdout.write(self.style.SUCCESS(f"Checked: {checked} recipes"))
        self.stdout.write(self.style.SUCCESS(
            f"Valid Cloudinary images: {valid}"))
        self.stdout.write(self.style.ERROR(
            f"Missing or invalid images: {missing}"))
