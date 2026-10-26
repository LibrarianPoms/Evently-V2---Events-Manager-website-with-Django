import urllib.request
import os
import ssl

# Disable SSL certificate verification (only for this script)
ssl._create_default_https_context = ssl._create_unverified_context

def download_profile_images():
    # Create directories if they don't exist
    profiles_dir = os.path.join('static', 'images', 'profiles')
    backgrounds_dir = os.path.join('static', 'images', 'backgrounds')
    
    if not os.path.exists(profiles_dir):
        os.makedirs(profiles_dir)
    if not os.path.exists(backgrounds_dir):
        os.makedirs(backgrounds_dir)
    
    # Image URLs (free stock images)
    images = {
        'admin_profile': 'https://images.unsplash.com/photo-1568602471122-7832951cc4c5?q=80&w=400&auto=format&fit=crop',
        'profile_background': 'https://images.unsplash.com/photo-1557682250-33bd709cbe85?q=80&w=1200&h=300&auto=format&fit=crop'
    }
    
    # Download images
    for name, url in images.items():
        if name == 'admin_profile':
            output_path = os.path.join(profiles_dir, f"{name}.jpg")
        else:
            output_path = os.path.join(backgrounds_dir, f"{name}.jpg")
            
        try:
            print(f"Downloading {name}...")
            urllib.request.urlretrieve(url, output_path)
            print(f"Saved to {output_path}")
        except Exception as e:
            print(f"Error downloading {name}: {e}")
    
    print("Profile images download completed!")

if __name__ == "__main__":
    download_profile_images()
