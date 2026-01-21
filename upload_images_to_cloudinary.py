"""
Script to upload recipe images to Cloudinary and update fixture files
"""
import json
import os
import requests
import cloudinary
import cloudinary.uploader
from pathlib import Path

# Import env.py to load Cloudinary credentials
import env  # This loads the CLOUDINARY_URL

# Parse Cloudinary URL manually
cloudinary_url = os.environ.get('CLOUDINARY_URL')
# cloudinary://272974694284733:j6lYm583o11AaAPckqjmPMgRoEQ@dz3tztxgb
if cloudinary_url:
    # Remove 'cloudinary://' prefix
    credentials = cloudinary_url.replace('cloudinary://', '')
    # Split into api_key:api_secret@cloud_name
    auth, cloud_name = credentials.split('@')
    api_key, api_secret = auth.split(':')

    # Configure Cloudinary
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True
    )
    print(f"✅ Cloudinary configured: {cloud_name}")
else:
    print("❌ CLOUDINARY_URL not found in environment!")
    exit(1)

# Fixture files to process
FIXTURE_FILES = [
    'fixtures/breakfast_recipes.json',
    'fixtures/lunch_recipes.json',
    'fixtures/dinner_recipes.json',
    'fixtures/snack_recipes.json',
    'fixtures/all_recipes.json',
]


def upload_image_to_cloudinary(image_url, recipe_id, recipe_title):
    """
    Upload an image from URL to Cloudinary
    Returns the Cloudinary URL or None if failed
    """
    try:
        # Create a unique public_id based on recipe
        public_id = f"recipes/{recipe_title.lower().replace(' ', '_')}_{recipe_id}"

        print(f"  Uploading: {recipe_title}...")

        # Upload to Cloudinary directly from URL
        result = cloudinary.uploader.upload(
            image_url,
            public_id=public_id,
            folder="recipes",
            overwrite=True,
            resource_type="image"
        )

        print(f"    ✅ Uploaded: {result['secure_url']}")
        return result['secure_url']

    except Exception as e:
        print(f"    ❌ Error uploading {recipe_title}: {e}")
        return None


def update_fixtures_with_cloudinary():
    """
    Process all fixture files and update image URLs with Cloudinary URLs
    """
    total_uploaded = 0
    total_failed = 0

    for fixture_file in FIXTURE_FILES:
        print(f"\n{'='*fixture_file.__len__()}")
        print(f"Processing: {fixture_file}")
        print(f"{'='*fixture_file.__len__()}")

        # Read fixture file
        with open(fixture_file, 'r', encoding='utf-8') as f:
            recipes = json.load(f)

        # Process each recipe
        for recipe in recipes:
            fields = recipe['fields']
            recipe_id = recipe['pk']
            title = fields['title']
            current_url = fields.get('image_url', '')

            # Skip if already a Cloudinary URL
            if 'cloudinary.com' in current_url:
                print(f"  Skipping {title} - already on Cloudinary")
                continue

            # Upload to Cloudinary
            cloudinary_url = upload_image_to_cloudinary(
                current_url, recipe_id, title)

            if cloudinary_url:
                # Update the image_url in the fixture
                fields['image_url'] = cloudinary_url
                total_uploaded += 1
            else:
                total_failed += 1

        # Save updated fixture file
        with open(fixture_file, 'w', encoding='utf-8') as f:
            json.dump(recipes, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Updated: {fixture_file}")

    # Print summary
    print(f"\n{'='*fixture_file.__len__()}")
    print(f"SUMMARY")
    print(f"{'='*fixture_file.__len__()}")
    print(f"✅ Successfully uploaded: {total_uploaded} images")
    if total_failed > 0:
        print(f"❌ Failed uploads: {total_failed} images")
    print(f"{'='*fixture_file.__len__()}")


if __name__ == '__main__':
    print("🚀 Starting Cloudinary Image Upload Process...")
    print(f"Cloudinary Cloud Name: {cloudinary.config().cloud_name}")

    # Confirm before proceeding
    response = input(
        "\nThis will upload ~65 images to Cloudinary. Continue? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        update_fixtures_with_cloudinary()
        print("\n✅ All done! Fixture files have been updated.")
        print("You can now reload fixtures with: python manage.py loaddata breakfast_recipes lunch_recipes dinner_recipes snack_recipes")
    else:
        print("❌ Cancelled.")
