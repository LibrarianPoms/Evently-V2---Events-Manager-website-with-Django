import urllib.request
import os
import ssl

# Disable SSL certificate verification (only for this script)
ssl._create_default_https_context = ssl._create_unverified_context

def download_logo():
    # Create directories if they don't exist
    static_dir = os.path.join('static', 'images')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    # Logo URLs (free stock images)
    logo_urls = [
        ('https://img.freepik.com/free-vector/gradient-e-logo-template_23-2149883326.jpg', 'evently_logo.png'),
        ('https://img.freepik.com/free-vector/gradient-e-logo-template_23-2149883326.jpg', 'evently_logo_small.png')
    ]
    
    # Download logos
    for url, filename in logo_urls:
        output_path = os.path.join(static_dir, filename)
        try:
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, output_path)
            print(f"Saved to {output_path}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
    
    print("Logo download completed!")

if __name__ == "__main__":
    download_logo()
