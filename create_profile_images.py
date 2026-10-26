from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random

def create_profile_picture():
    """Create a professional profile picture for admin"""
    # Create a square image
    size = 400
    img = Image.new('RGB', (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Colors - blue theme
    primary_blue = (25, 118, 210)     # Darker blue
    secondary_blue = (66, 165, 245)   # Medium blue
    
    # Draw a circular background
    draw.ellipse((0, 0, size, size), fill=primary_blue)
    
    # Draw a slightly smaller inner circle
    margin = 10
    draw.ellipse((margin, margin, size-margin, size-margin), fill=secondary_blue)
    
    # Add initials "A" for admin
    try:
        # Try to use Arial font
        font = ImageFont.truetype("arial.ttf", 200)
    except:
        # Fall back to default font
        font = ImageFont.load_default()
    
    # Draw text
    text = "A"
    # Approximate text position
    text_position = (size//2 - 60, size//2 - 100)
    draw.text(text_position, text, fill=(255, 255, 255), font=font)
    
    # Apply a slight blur for smoothing
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Save the profile picture
    static_dir = os.path.join('static', 'images', 'profiles')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    profile_path = os.path.join(static_dir, 'admin_profile.png')
    img.save(profile_path)
    print(f"Admin profile picture saved to {profile_path}")
    
    return profile_path

def create_profile_background():
    """Create a professional background for profile page"""
    # Create a wide image for background
    width, height = 1200, 300
    img = Image.new('RGB', (width, height), (240, 247, 255))
    draw = ImageDraw.Draw(img)
    
    # Colors - blue theme
    primary_blue = (25, 118, 210)     # Darker blue
    secondary_blue = (66, 165, 245)   # Medium blue
    accent_blue = (144, 202, 249)     # Light blue
    
    # Draw a pattern of shapes
    for i in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(10, 50)
        opacity = random.randint(20, 80)
        color = random.choice([primary_blue, secondary_blue, accent_blue])
        color_with_opacity = (*color, opacity)
        
        shape_type = random.choice(['circle', 'rectangle'])
        if shape_type == 'circle':
            draw.ellipse((x, y, x+size, y+size), fill=color_with_opacity)
        else:
            draw.rectangle((x, y, x+size, y+size), fill=color_with_opacity)
    
    # Apply a slight blur for a professional look
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    
    # Save the background image
    static_dir = os.path.join('static', 'images', 'backgrounds')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    bg_path = os.path.join(static_dir, 'profile_background.png')
    img.save(bg_path)
    print(f"Profile background saved to {bg_path}")
    
    return bg_path

if __name__ == "__main__":
    create_profile_picture()
    create_profile_background()
