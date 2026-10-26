import os
import shutil

# Define the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(base_dir, 'static', 'images')

# Define the image categories
categories = {
    'events': [
        'event1.jpg', 'event2.jpg', 'event3.jpg', 
        'concert.jpg', 'conference.jpg', 'workshop.jpg',
        'featured-event.jpg', 'social.jpg'
    ],
    'icons': [
        'icon-concert.png', 'icon-conference.png', 'icon-social.png', 
        'icon-workshop.png', 'calendar-icon.png', 'qr-code.png', 'success.png'
    ],
    'backgrounds': [
        'background.jpg', 'banner.jpg', 'login-bg.jpg', 'profile-bg.jpg',
        'register-bg.jpg', 'ticket-bg.jpg', 'pattern.svg', 'auth-side.jpg'
    ],
    'users': [
        'user1.jpg', 'user2.jpg', 'testimonial1.jpg', 'testimonial2.jpg',
        'avatar-default.png', 'speaker1.jpg', 'speaker2.jpg', 'speaker3.jpg'
    ],
    'venues': [
        'venue1.jpg', 'venue2.jpg', 'map.jpg'
    ],
    'ui': [
        'logo.png', 'favicon.ico', 'apple-touch-icon.png', 'error-404.jpg',
        'social-preview.jpg'
    ]
}

# Create a dictionary to track which files have been moved
moved_files = set()

# Move files to their respective folders
for category, files in categories.items():
    category_dir = os.path.join(images_dir, category)
    
    # Ensure the category directory exists
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)
    
    # Move each file to its category directory
    for file in files:
        src_path = os.path.join(images_dir, file)
        dst_path = os.path.join(category_dir, file)
        
        if os.path.exists(src_path):
            try:
                shutil.copy2(src_path, dst_path)
                print(f"Copied {file} to {category} folder")
                moved_files.add(file)
            except Exception as e:
                print(f"Error copying {file}: {e}")
        else:
            print(f"File not found: {file}")

# List files that weren't categorized
all_files = set(os.listdir(images_dir))
uncategorized = [f for f in all_files if f not in moved_files and os.path.isfile(os.path.join(images_dir, f))]

if uncategorized:
    print("\nUncategorized files:")
    for file in uncategorized:
        print(f"- {file}")
else:
    print("\nAll files have been categorized!")

print("\nImage organization complete!")
