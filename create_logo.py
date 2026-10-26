from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Create a new image with transparent background
    width, height = 500, 150
    logo = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo)
    
    # Colors
    primary_color = (65, 105, 225)  # Royal Blue
    accent_color = (255, 69, 0)     # Red-Orange
    
    # Try to load a custom font, fall back to default if not available
    try:
        # Try to find a nice font on the system
        font_path = os.path.join('static', 'fonts', 'OpenSans-Bold.ttf')
        if os.path.exists(font_path):
            main_font = ImageFont.truetype(font_path, 72)
        else:
            main_font = ImageFont.truetype("arial.ttf", 72)
    except:
        main_font = ImageFont.load_default()
    
    # Draw the main text "Evently"
    text_width, text_height = draw.textsize("Evently", font=main_font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    
    # Draw text shadow
    shadow_offset = 3
    draw.text((position[0] + shadow_offset, position[1] + shadow_offset), 
              "Evently", fill=(0, 0, 0, 100), font=main_font)
    
    # Draw main text
    draw.text(position, "Evently", fill=primary_color, font=main_font)
    
    # Draw an event icon
    icon_size = 40
    icon_position = (position[0] - icon_size - 10, position[1] + text_height // 2 - icon_size // 2)
    
    # Draw a calendar icon
    draw.rectangle([icon_position, (icon_position[0] + icon_size, icon_position[1] + icon_size)], 
                   fill=accent_color, outline=None)
    
    # Draw calendar details
    inner_margin = 5
    draw.rectangle([
        (icon_position[0] + inner_margin, icon_position[1] + inner_margin),
        (icon_position[0] + icon_size - inner_margin, icon_position[1] + icon_size - inner_margin)
    ], fill=(255, 255, 255), outline=None)
    
    # Draw a tagline
    try:
        tagline_font = ImageFont.truetype(font_path, 20) if os.path.exists(font_path) else ImageFont.truetype("arial.ttf", 20)
    except:
        tagline_font = ImageFont.load_default()
    
    tagline = "Event Management Made Simple"
    tagline_width, tagline_height = draw.textsize(tagline, font=tagline_font)
    tagline_position = ((width - tagline_width) // 2, position[1] + text_height + 5)
    draw.text(tagline_position, tagline, fill=primary_color, font=tagline_font)
    
    # Save the logo
    static_dir = os.path.join('static', 'images')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    logo_path = os.path.join(static_dir, 'evently_logo.png')
    logo.save(logo_path)
    print(f"Logo saved to {logo_path}")
    
    # Create a smaller version for the navbar
    navbar_logo = logo.copy()
    navbar_logo = navbar_logo.resize((200, 60), Image.LANCZOS)
    navbar_logo_path = os.path.join(static_dir, 'evently_logo_small.png')
    navbar_logo.save(navbar_logo_path)
    print(f"Navbar logo saved to {navbar_logo_path}")
    
    return logo_path, navbar_logo_path

if __name__ == "__main__":
    create_logo()
