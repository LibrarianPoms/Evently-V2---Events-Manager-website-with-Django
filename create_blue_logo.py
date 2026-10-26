from PIL import Image, ImageDraw, ImageFont
import os

def create_blue_logo():
    # Create a new image with white background
    width, height = 600, 200
    logo = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(logo)
    
    # Blue color palette
    primary_blue = (25, 118, 210)     # Darker blue
    secondary_blue = (66, 165, 245)   # Medium blue
    accent_blue = (144, 202, 249)     # Light blue
    dark_blue = (13, 71, 161)         # Very dark blue
    
    # Draw a background shape
    draw.rectangle([(0, 0), (width, height)], fill=(240, 247, 255))
    
    # Draw a decorative element - blue square with gradient effect
    draw.rectangle([(40, 50), (140, 150)], fill=primary_blue, outline=None)
    
    # Add some decorative lines to the square (calendar-like)
    line_spacing = 20
    for i in range(4):
        y = 70 + i * line_spacing
        draw.line([(50, y), (130, y)], fill=accent_blue, width=3)
    
    # Draw a highlight on the square
    draw.rectangle([(40, 50), (140, 60)], fill=secondary_blue, outline=None)
    
    # Draw the main text "Evently"
    try:
        # Try to use Arial font
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        # Fall back to default font
        font = ImageFont.load_default()
    
    # Draw text shadow
    draw.text((165, 73), "Evently", fill=(200, 220, 240), font=font)
    
    # Draw main text
    draw.text((160, 70), "Evently", fill=dark_blue, font=font)
    
    # Draw tagline
    try:
        tagline_font = ImageFont.truetype("arial.ttf", 20)
    except:
        tagline_font = ImageFont.load_default()
    
    draw.text((165, 150), "Event Management Made Simple", fill=primary_blue, font=tagline_font)
    
    # Save the logo
    static_dir = os.path.join('static', 'images')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    logo_path = os.path.join(static_dir, 'evently_logo.png')
    logo.save(logo_path)
    print(f"Blue logo saved to {logo_path}")
    
    # Create a smaller version for the navbar
    navbar_logo = logo.copy()
    navbar_logo = navbar_logo.resize((240, 80), Image.LANCZOS)
    navbar_logo_path = os.path.join(static_dir, 'evently_logo_small.png')
    navbar_logo.save(navbar_logo_path)
    print(f"Navbar logo saved to {navbar_logo_path}")
    
    # Create a favicon
    favicon_size = 32
    favicon = Image.new('RGB', (favicon_size, favicon_size), (255, 255, 255))
    favicon_draw = ImageDraw.Draw(favicon)
    
    # Draw a small "E" in blue
    favicon_draw.rectangle([2, 2, favicon_size-2, favicon_size-2], fill=primary_blue)
    
    # Add "E" shape
    favicon_draw.rectangle([8, 6, favicon_size-8, 10], fill=(255, 255, 255))
    favicon_draw.rectangle([8, 14, favicon_size-12, 18], fill=(255, 255, 255))
    favicon_draw.rectangle([8, 22, favicon_size-8, 26], fill=(255, 255, 255))
    favicon_draw.rectangle([8, 6, 12, 26], fill=(255, 255, 255))
    
    favicon_path = os.path.join(static_dir, 'favicon.ico')
    favicon.save(favicon_path)
    print(f"Favicon saved to {favicon_path}")
    
    return logo_path, navbar_logo_path

if __name__ == "__main__":
    create_blue_logo()
