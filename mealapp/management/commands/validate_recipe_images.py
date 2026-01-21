from django.core.management.base import BaseCommand
from mealapp.models import Recipe


class Command(BaseCommand):
    help = 'Validate all recipe image_url fields are Cloudinary URLs and print a summary.'

    def handle(self, *args, **options):
        total = Recipe.objects.count()
        cloudinary_count = 0
        missing = 0
        other = 0
        for recipe in Recipe.objects.all():
            url = str(recipe.image_url)
            if 'cloudinary.com' in url:
                cloudinary_count += 1
            elif url.strip() == '' or url == 'default.jpg':
                missing += 1
            else:
                other += 1
                self.stdout.write(self.style.WARNING(
                    f"Non-cloudinary image for {recipe.title}: {url}"))
        self.stdout.write(self.style.SUCCESS(f"Total recipes: {total}"))
        self.stdout.write(self.style.SUCCESS(
            f"Cloudinary images: {cloudinary_count}"))
        self.stdout.write(self.style.WARNING(
            f"Missing/default images: {missing}"))
        self.stdout.write(self.style.WARNING(f"Other images: {other}"))
        if cloudinary_count == total:
            self.stdout.write(self.style.SUCCESS(
                "All recipes have Cloudinary image URLs!"))
        else:
            self.stdout.write(self.style.ERROR(
                "Some recipes do not have Cloudinary image URLs."))
