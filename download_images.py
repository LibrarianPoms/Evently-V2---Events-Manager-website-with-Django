import os
import urllib.request
import ssl

# Disable SSL certificate verification (only for this script)
ssl._create_default_https_context = ssl._create_unverified_context

# Create directories if they don't exist
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, 'static', 'images')

# Ensure directories exist
directories = ['banners', 'events', 'gallery', 'profiles']
for dir_name in directories:
    ensure_dir(os.path.join(static_dir, dir_name))

# Image URLs (free stock images)
images = {
    'banners': [
        ('https://images.unsplash.com/photo-1492684223066-81342ee5ff30', 'banner1.jpg'),
        ('https://images.unsplash.com/photo-1501281668745-f7f57925c3b4', 'banner2.jpg'),
        ('https://images.unsplash.com/photo-1505236858219-8359eb29e329', 'banner3.jpg'),
    ],
    'events': [
        ('https://images.unsplash.com/photo-1511578314322-379afb476865', 'concert.jpg'),
        ('https://images.unsplash.com/photo-1540575467063-178a50c2df87', 'conference.jpg'),
        ('https://images.unsplash.com/photo-1464047736614-af63643285bf', 'wedding.jpg'),
        ('https://images.unsplash.com/photo-1519750783826-e2420f4d687f', 'party.jpg'),
        ('https://images.unsplash.com/photo-1524178232363-1fb2b075b655', 'workshop.jpg'),
        ('https://images.unsplash.com/photo-1560439514-4e9645039924', 'sports.jpg'),
    ],
    'gallery': [
        ('https://images.unsplash.com/photo-1472653431158-6364773b2a56', 'gallery1.jpg'),
        ('https://images.unsplash.com/photo-1501281668745-f7f57925c3b4', 'gallery2.jpg'),
        ('https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec', 'gallery3.jpg'),
        ('https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3', 'gallery4.jpg'),
        ('https://images.unsplash.com/photo-1501386761578-eac5c94b800a', 'gallery5.jpg'),
        ('https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3', 'gallery6.jpg'),
    ],
    'profiles': [
        ('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d', 'profile1.jpg'),
        ('https://images.unsplash.com/photo-1494790108377-be9c29b29330', 'profile2.jpg'),
        ('https://images.unsplash.com/photo-1500648767791-00dcc994a43e', 'profile3.jpg'),
        ('https://images.unsplash.com/photo-1534528741775-53994a69daeb', 'profile4.jpg'),
    ],
}

# Download images
for category, image_list in images.items():
    print(f"Downloading {category} images...")
    for i, (url, filename) in enumerate(image_list):
        output_path = os.path.join(static_dir, category, filename)
        if not os.path.exists(output_path):
            try:
                print(f"  Downloading {filename}...")
                # Add a query parameter to get a specific size
                full_url = f"{url}?q=80&w=1000&auto=format&fit=crop"
                urllib.request.urlretrieve(full_url, output_path)
                print(f"  Saved to {output_path}")
            except Exception as e:
                print(f"  Error downloading {filename}: {e}")
        else:
            print(f"  {filename} already exists, skipping")

print("All images downloaded successfully!")
