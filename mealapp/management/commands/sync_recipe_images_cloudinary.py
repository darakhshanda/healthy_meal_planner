from django.core.management.base import BaseCommand
from mealapp.models import Recipe
import cloudinary
import cloudinary.uploader
import os

# Ensure env.py is loaded if needed for credentials


def upload_to_cloudinary_and_update(recipe):
    url = str(recipe.image_url)
    if not url or 'cloudinary.com' in url or url == 'default.jpg':
        return False
    try:
        public_id = f"recipes/{recipe.title.lower().replace(' ', '_')}_{recipe.id}"
        result = cloudinary.uploader.upload(
            url,
            public_id=public_id,
            folder="recipes",
            overwrite=True,
            resource_type="image"
        )
        recipe.image_url = result['secure_url']
        recipe.save()
        return True
    except Exception as e:
        print(f"Error uploading {recipe.title}: {e}")
        return False


class Command(BaseCommand):
    help = 'Upload non-Cloudinary recipe images to Cloudinary and update the database.'

    def handle(self, *args, **options):
        updated = 0
        failed = 0
        for recipe in Recipe.objects.all():
            url = str(recipe.image_url)
            if url and 'cloudinary.com' not in url and url != 'default.jpg':
                self.stdout.write(f"Uploading for {recipe.title}...")
                if upload_to_cloudinary_and_update(recipe):
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"Updated: {recipe.title}"))
                else:
                    failed += 1
                    self.stdout.write(self.style.ERROR(
                        f"Failed: {recipe.title}"))
        self.stdout.write(self.style.SUCCESS(f"Total updated: {updated}"))
        if failed:
            self.stdout.write(self.style.ERROR(f"Total failed: {failed}"))
        else:
            self.stdout.write(self.style.SUCCESS(
                "All non-Cloudinary images updated!"))
