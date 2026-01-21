from django.core.management.base import BaseCommand
from mealapp.models import Recipe
import cloudinary
import cloudinary.uploader
import os


class Command(BaseCommand):
    help = 'Upload all recipe images to Cloudinary using the recipe title as the public_id, and update the database.'

    def handle(self, *args, **options):
        updated = 0
        failed = 0
        for recipe in Recipe.objects.all():
            url = str(recipe.image_url)
            # Only upload if not already a Cloudinary URL
            if not url or 'cloudinary.com' in url or url == 'default.jpg':
                continue
            public_id = f"recipes/{recipe.title.lower().replace(' ', '_')}"
            try:
                result = cloudinary.uploader.upload(
                    url,
                    public_id=public_id,
                    folder="recipes",
                    overwrite=True,
                    resource_type="image"
                )
                recipe.image_url = result['secure_url']
                recipe.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(
                    f"Uploaded and updated: {recipe.title}"))
            except Exception as e:
                failed += 1
                self.stdout.write(self.style.ERROR(
                    f"Failed for {recipe.title}: {e}"))
        self.stdout.write(self.style.SUCCESS(f"Total updated: {updated}"))
        if failed:
            self.stdout.write(self.style.ERROR(f"Total failed: {failed}"))
        else:
            self.stdout.write(self.style.SUCCESS(
                "All images uploaded and recipes updated!"))
